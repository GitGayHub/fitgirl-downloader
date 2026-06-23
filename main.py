import os
import sys
import re
import json
import threading
import time
import urllib.parse
import webbrowser
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

# Monkey patch requests to globally disable SSL verification (bypasses VPN/proxy SSL conflicts)
import requests
original_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, *args, **kwargs)
requests.Session.request = patched_request

# Disable urllib3 insecure request warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Force python requests to bypass any local proxies/VPNs that cause SSL errors
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

# Try importing required packages
try:
    import privatebinapi
except ImportError:
    print("Error: privatebinapi is not installed. Run 'pip install privatebinapi'")
    sys.exit(1)

try:
    from curl_cffi import requests as cf_requests
except ImportError:
    print("Error: curl_cffi is not installed. Run 'pip install curl_cffi'")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is not installed. Run 'pip install beautifulsoup4'")
    sys.exit(1)

import requests  # Standard requests for downloading

# Global State
state = {
    "game_title": "",
    "files": [],
    "download_dir": "",
    "default_download_dir": os.path.join(os.path.expanduser("~"), "Downloads"),
    "is_configured": False,
    "is_running": False,
    "active_index": -1,
    "total_speed": 0,
    "total_progress": 0,
    "log_messages": [],
    "should_stop": False,
    "max_workers": 4,
    "active_workers_count": 0,
    "is_extracted": False,
    "is_extracting": False,
    "extraction_progress": 0
}

state_lock = threading.RLock()

# Cache mechanism for file sizes
cache_path = os.path.join(os.path.dirname(__file__), "sizes_cache.json")
sizes_cache = {}
if os.path.exists(cache_path):
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            sizes_cache = json.load(f)
    except Exception:
        pass

def save_size_to_cache(filename, size):
    sizes_cache[filename] = size
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(sizes_cache, f)
    except Exception:
        pass

def add_log(message):
    timestamp = time.strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    with state_lock:
        state["log_messages"].append(formatted)
        if len(state["log_messages"]) > 150:
            state["log_messages"].pop(0)
    try:
        print(formatted)
    except UnicodeEncodeError:
        try:
            enc = sys.stdout.encoding or 'ascii'
            print(formatted.encode(enc, errors='replace').decode(enc))
        except Exception:
            print(f"[{timestamp}] [Log encoding error] " + "".join(c if ord(c) < 128 else '?' for c in message))

def extract_direct_link(page_url):
    """Bypasses Cloudflare using curl_cffi to get the direct dl.fuckingfast.co link."""
    try:
        add_log(f"Extracting direct link for: {page_url}")
        response = cf_requests.get(page_url, impersonate="chrome120", timeout=20, verify=False)
        if response.status_code == 200:
            html = response.text
            match = re.search(r'window\.open\("(https://dl\.fuckingfast\.co/dl/[^"]+)"\)', html)
            if match:
                direct_link = match.group(1)
                add_log(f"Successfully extracted direct link!")
                return direct_link
            else:
                add_log("Error: Direct link pattern not found in HTML page.")
                return None
        else:
            add_log(f"Error: Server responded with status code {response.status_code}")
            return None
    except Exception as e:
        add_log(f"Extraction exception: {str(e)}")
        return None

def get_expected_size(filename, file_type):
    if filename in sizes_cache:
        return sizes_cache[filename]
    if file_type == "installer":
        return 7468619
    else:
        return 524288000  # Default 500MB if unknown

def parse_links_from_text(text):
    """Parses a text block line by line, extracting urls and filenames from hash fragments or paths."""
    lines = text.split('\n')
    parsed_files = []
    
    url_pattern = r'(https?://[^\s]+)'
    
    for line in lines:
        match = re.search(url_pattern, line)
        if match:
            url_full = match.group(1)
            parsed_url = urllib.parse.urlparse(url_full)
            base_url = parsed_url._replace(fragment='').geturl()
            
            filename = ""
            if parsed_url.fragment:
                filename = urllib.parse.unquote(parsed_url.fragment)
            else:
                path_parts = [p for p in parsed_url.path.split('/') if p]
                if path_parts:
                    filename = urllib.parse.unquote(path_parts[-1])
            
            if not filename or filename.startswith('?') or '.' not in filename:
                continue
                
            filename = filename.strip(' "\'')
            
            file_type = "game_part"
            filename_lower = filename.lower()
            if "setup" in filename_lower or filename_lower.endswith(".exe"):
                file_type = "installer"
            elif "optional" in filename_lower or "language" in filename_lower or "lang" in filename_lower or any(lang in filename_lower for lang in ["russian", "english", "french", "german", "spanish", "chinese", "brazilian", "japanese", "korean", "polish", "mexican", "italian"]):
                file_type = "lang_part"
                
            if not any(f["filename"] == filename for f in parsed_files):
                cached_size = sizes_cache.get(filename, 0)
                parsed_files.append({
                    "filename": filename,
                    "url": base_url,
                    "type": file_type,
                    "status": "waiting",
                    "progress": 0,
                    "downloaded": 0,
                    "size": cached_size,
                    "speed": 0,
                    "time_left": -1,
                    "error": ""
                })
    return parsed_files

def guess_game_title(files):
    if not files:
        return "Custom Repack"
    game_files = [f["filename"] for f in files if f["type"] == "game_part"]
    if not game_files:
        game_files = [f["filename"] for f in files]
        
    sample = game_files[0]
    cleaned = re.sub(r'[-_]+fitgirl-repacks\.site[-_]+', '', sample, flags=re.IGNORECASE)
    cleaned = re.sub(r'[-_]+fitgirl-repacks[-_]+', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\.part\d+\.rar$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\.rar$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\.bin$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\.exe$', '', cleaned, flags=re.IGNORECASE)
    
    cleaned = cleaned.replace('_', ' ').replace('.', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if cleaned else "Custom Game"

def initialize_queue_on_disk():
    with state_lock:
        if not state["download_dir"]:
            return
        os.makedirs(state["download_dir"], exist_ok=True)
        for f in state["files"]:
            file_path = os.path.join(state["download_dir"], f["filename"])
            if os.path.exists(file_path):
                size_on_disk = os.path.getsize(file_path)
                expected_size = f["size"] if f["size"] > 0 else get_expected_size(f["filename"], f["type"])
                f["downloaded"] = size_on_disk
                f["progress"] = int((size_on_disk / expected_size) * 100) if expected_size > 0 else 0
                if size_on_disk >= expected_size:
                    f["status"] = "finished"
                    f["size"] = size_on_disk
                    save_size_to_cache(f["filename"], size_on_disk)
        recalculate_total_progress()

def download_worker():
    """Background thread worker to download files concurrently."""
    with state_lock:
        if not state["download_dir"]:
            return
        os.makedirs(state["download_dir"], exist_ok=True)
        state["active_workers_count"] += 1
        
    try:
        while True:
            with state_lock:
                if state["should_stop"] or not state["is_running"] or state["active_workers_count"] > state["max_workers"]:
                    break
                    
                target_idx = -1
                for idx, f in enumerate(state["files"]):
                    if f["status"] in ["waiting", "failed"]:
                        target_idx = idx
                        f["status"] = "connecting"
                        break
                
                if target_idx == -1:
                    active_workers = any(f["status"] in ["connecting", "downloading"] for f in state["files"])
                    if not active_workers:
                        state["is_running"] = False
                        state["total_speed"] = 0
                        add_log("🎉 ALL DOWNLOADS COMPLETED SUCCESSFULLY!")
                    break
                    
                file_info = state["files"][target_idx]
                
            success = download_file(target_idx, file_info)
            
            with state_lock:
                if not success:
                    if state["should_stop"]:
                        break
                    time.sleep(5)
    finally:
        with state_lock:
            state["active_workers_count"] -= 1
            if state["active_workers_count"] <= 0:
                state["is_running"] = False
                state["total_speed"] = 0
                state["should_stop"] = False

def download_file(index, file_info):
    filename = file_info["filename"]
    page_url = file_info["url"]
    file_path = os.path.join(state["download_dir"], filename)
    
    with state_lock:
        state["files"][index]["status"] = "connecting"
        state["files"][index]["error"] = ""
        
    add_log(f"Starting download for {filename}...")
    
    # Step 1: Extract direct download link if FuckingFast
    if "fuckingfast.co" in page_url:
        direct_link = extract_direct_link(page_url)
        if not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Could not bypass Cloudflare for FuckingFast."
            return False
    else:
        direct_link = page_url
        
    resume_byte = 0
    if os.path.exists(file_path):
        resume_byte = os.path.getsize(file_path)
        add_log(f"Local file found: {filename}. Size: {resume_byte} bytes.")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    total_size = 0
    try:
        r_head = requests.get(direct_link, headers=headers, stream=True, timeout=15)
        total_size = int(r_head.headers.get('content-length', 0))
        r_head.close()
        if total_size > 0:
            save_size_to_cache(filename, total_size)
    except Exception as e:
        add_log(f"Warning: Could not query file size for {filename}: {str(e)}")
        
    if total_size > 0 and resume_byte >= total_size:
        add_log(f"File {filename} is already fully downloaded ({resume_byte}/{total_size} bytes).")
        with state_lock:
            state["files"][index]["status"] = "finished"
            state["files"][index]["progress"] = 100
            state["files"][index]["downloaded"] = total_size
            state["files"][index]["size"] = total_size
        return True
        
    if resume_byte > 0:
        headers["Range"] = f"bytes={resume_byte}-"
        add_log(f"Attempting resume from byte {resume_byte} for {filename}...")
        
    try:
        response = requests.get(direct_link, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 206:
            mode = "ab"
            downloaded = resume_byte
            total_size = int(response.headers.get('content-length', 0)) + resume_byte
            add_log(f"Resuming download from byte {resume_byte} for {filename}...")
            if total_size > 0:
                save_size_to_cache(filename, total_size)
        elif response.status_code == 200:
            mode = "wb"
            downloaded = 0
            total_size = int(response.headers.get('content-length', 0))
            if resume_byte > 0:
                add_log(f"Server did not support resume for {filename}. Starting from scratch.")
            if total_size > 0:
                save_size_to_cache(filename, total_size)
        elif response.status_code == 416:
            add_log(f"File {filename} appears to be fully downloaded already.")
            with state_lock:
                state["files"][index]["status"] = "finished"
                state["files"][index]["progress"] = 100
                state["files"][index]["downloaded"] = resume_byte
                state["files"][index]["size"] = resume_byte
            return True
        else:
            add_log(f"Download request failed with HTTP status code: {response.status_code}")
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = f"HTTP Error {response.status_code}"
            return False
            
        with state_lock:
            state["files"][index]["status"] = "downloading"
            state["files"][index]["size"] = total_size
            
        chunk_size = 256 * 1024
        last_time = time.time()
        bytes_in_sec = 0
        
        with open(file_path, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                with state_lock:
                    if state["should_stop"]:
                        add_log(f"Download of {filename} paused by user.")
                        state["files"][index]["status"] = "waiting"
                        state["files"][index]["speed"] = 0
                        state["total_speed"] = sum(x["speed"] for x in state["files"] if x["status"] == "downloading")
                        return False
                        
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    bytes_in_sec += len(chunk)
                    
                    curr_time = time.time()
                    elapsed = curr_time - last_time
                    if elapsed >= 1.0:
                        speed = bytes_in_sec / elapsed
                        progress = int((downloaded / total_size) * 100) if total_size > 0 else 0
                        time_left = int((total_size - downloaded) / speed) if speed > 0 else -1
                        
                        with state_lock:
                            state["files"][index]["downloaded"] = downloaded
                            state["files"][index]["progress"] = progress
                            state["files"][index]["speed"] = speed
                            state["files"][index]["time_left"] = time_left
                            state["total_speed"] = sum(x["speed"] for x in state["files"] if x["status"] == "downloading")
                            
                        recalculate_total_progress()
                        bytes_in_sec = 0
                        last_time = curr_time
                        
        with state_lock:
            state["files"][index]["status"] = "finished"
            state["files"][index]["progress"] = 100
            state["files"][index]["downloaded"] = total_size
            state["files"][index]["speed"] = 0
            state["files"][index]["time_left"] = 0
            state["total_speed"] = sum(x["speed"] for x in state["files"] if x["status"] == "downloading")
        recalculate_total_progress()
        add_log(f"Successfully downloaded {filename}.")
        return True
        
    except Exception as e:
        add_log(f"Exception during download of {filename}: {str(e)}")
        with state_lock:
            state["files"][index]["status"] = "failed"
            state["files"][index]["error"] = str(e)
            state["files"][index]["speed"] = 0
            state["total_speed"] = sum(x["speed"] for x in state["files"] if x["status"] == "downloading")
        return False

def recalculate_total_progress():
    """Calculates overall progress across all selected files."""
    with state_lock:
        if not state["files"]:
            state["total_progress"] = 0
            state["active_index"] = -1
            return
        total_bytes = sum(f["size"] if f["size"] > 0 else get_expected_size(f["filename"], f["type"]) for f in state["files"])
        downloaded_bytes = sum(f["downloaded"] for f in state["files"])
        state["total_progress"] = int((downloaded_bytes / total_bytes) * 100) if total_bytes > 0 else 0
        
        active_idx = -1
        for idx, f in enumerate(state["files"]):
            if f["status"] in ["connecting", "downloading"]:
                active_idx = idx
                break
        state["active_index"] = active_idx

def extraction_worker():
    """Background thread worker to extract split RAR volumes using unrar.exe."""
    with state_lock:
        if state.get("is_extracting"):
            add_log("Extraction already in progress. Skipping thread launch.")
            return
        state["is_extracting"] = True
        state["extraction_progress"] = 0
        
    unrar_path = r"C:\Program Files\WinRAR\unrar.exe"
    if not os.path.exists(unrar_path):
        add_log("Error: WinRAR/unrar.exe not found at: " + unrar_path)
        with state_lock:
            state["is_extracting"] = False
        return
        
    download_dir = state["download_dir"]
    finished_files = [f["filename"] for f in state["files"] if f["status"] == "finished"]
    
    archives_to_extract = []
    for filename in finished_files:
        if filename.endswith(".rar"):
            part_match = re.search(r'\.part(\d+)\.rar$', filename, re.IGNORECASE)
            if part_match:
                part_num = int(part_match.group(1))
                if part_num == 1:
                    archives_to_extract.append((filename, f"Archive Part 1: {filename}"))
            else:
                archives_to_extract.append((filename, f"Single Archive: {filename}"))
                
    if not archives_to_extract:
        add_log("No RAR archives found to extract among completed downloads.")
        with state_lock:
            state["is_extracting"] = False
        return
        
    for filename, label in archives_to_extract:
        archive_path = os.path.join(download_dir, filename)
        if not os.path.exists(archive_path):
            continue
            
        add_log(f"Unpacking {label}... This may take a while...")
        
        try:
            cmd = [unrar_path, "x", "-y", archive_path]
            process = subprocess.Popen(
                cmd,
                cwd=download_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                encoding='cp866',
                errors='replace'
            )
            
            last_progress = -1
            buffer = ""
            while True:
                char = process.stdout.read(1)
                if not char:
                    break
                buffer += char
                if char in ['\r', '\n']:
                    matches = re.findall(r'(\d+)%', buffer)
                    if matches:
                        pct = int(matches[-1])
                        if pct != last_progress:
                            last_progress = pct
                            with state_lock:
                                state["extraction_progress"] = pct
                            if pct % 5 == 0:
                                add_log(f"Extraction progress ({label}): {pct}%")
                    buffer = ""
                    
            process.wait()
            if process.returncode == 0:
                add_log(f"Successfully unpacked {label}.")
            else:
                add_log(f"Unpacker finished with exit code {process.returncode} for {label}.")
        except Exception as e:
            add_log(f"Exception during extraction of {label}: {str(e)}")
            
    with state_lock:
        state["is_extracting"] = False
        state["extraction_progress"] = 100
        state["is_extracted"] = any(f.endswith(".bin") for f in os.listdir(download_dir)) if os.path.exists(download_dir) else False
        
    add_log("Extraction workflow complete!")

# HTTP Web Server
class APIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
        
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with state_lock:
                if state["download_dir"] and os.path.exists(state["download_dir"]):
                    # Look for standard setup .bin files or output to check if extracted
                    state["is_extracted"] = any(f.endswith(".bin") for f in os.listdir(state["download_dir"]))
                self.wfile.write(json.dumps(state).encode())
            return
            
        # Serve static web files
        if path == "/" or path == "/index.html":
            file_to_serve = os.path.join(os.path.dirname(__file__), "web", "index.html")
            content_type = "text/html"
        elif path == "/style.css":
            file_to_serve = os.path.join(os.path.dirname(__file__), "web", "style.css")
            content_type = "text/css"
        elif path == "/app.js":
            file_to_serve = os.path.join(os.path.dirname(__file__), "web", "app.js")
            content_type = "application/javascript"
        else:
            self.send_error(404, "File Not Found")
            return
            
        try:
            with open(file_to_serve, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        if path == "/api/start":
            with state_lock:
                if not state["is_running"] and state["files"]:
                    state["is_running"] = True
                    state["should_stop"] = False
                    workers_to_start = state["max_workers"]
                    add_log(f"Download manager resumed/started with {workers_to_start} parallel workers.")
                    for _ in range(workers_to_start):
                        threading.Thread(target=download_worker, daemon=True).start()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            
        elif path == "/api/pause":
            with state_lock:
                if state["is_running"]:
                    state["should_stop"] = True
                    add_log("Pausing downloads... please wait for current chunk to finish.")
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            
        elif path == "/api/set_dir":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                new_dir = data.get("download_dir")
                if new_dir:
                    new_dir = os.path.abspath(new_dir)
                    with state_lock:
                        state["download_dir"] = new_dir
                    add_log(f"Download directory changed to: {new_dir}")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode())
                    return
            except Exception as e:
                pass
            self.send_error(400, "Bad Request")
            
        elif path == "/api/set_workers":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                workers = int(data.get("max_workers", 4))
                if 1 <= workers <= 10:
                    with state_lock:
                        state["max_workers"] = workers
                        add_log(f"Max workers changed to: {workers}")
                        if state["is_running"]:
                            needed = state["max_workers"] - state["active_workers_count"]
                            if needed > 0:
                                add_log(f"Spawning {needed} additional worker threads.")
                                for _ in range(needed):
                                    threading.Thread(target=download_worker, daemon=True).start()
                                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode())
                    return
            except Exception as e:
                pass
            self.send_error(400, "Bad Request")
            
        elif path == "/api/install":
            download_dir = state["download_dir"]
            installer_path = None
            if os.path.exists(download_dir):
                for f in os.listdir(download_dir):
                    if f.endswith(".exe") and "setup" in f.lower():
                        installer_path = os.path.join(download_dir, f)
                        break
                if not installer_path:
                    for f in os.listdir(download_dir):
                        if f.endswith(".exe"):
                            installer_path = os.path.join(download_dir, f)
                            break
                            
            if installer_path and os.path.exists(installer_path):
                try:
                    add_log(f"Launching installer setup at: {installer_path}...")
                    if sys.platform == "win32":
                        os.startfile(installer_path)
                    else:
                        subprocess.Popen([installer_path])
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode())
                except Exception as e:
                    add_log(f"Failed to launch installer: {str(e)}")
                    self.send_error(500, f"Failed to launch: {str(e)}")
            else:
                add_log(f"Error: Installer setup .exe not found in {download_dir}")
                self.send_error(404, "Installer file not found on disk.")
                
        elif path == "/api/extract":
            with state_lock:
                if state.get("is_extracting"):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Extraction already in progress."}).encode())
                    return
                threading.Thread(target=extraction_worker, daemon=True).start()
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            
        elif path == "/api/analyze":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                url = data.get("url", "").strip()
                if not url:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "URL cannot be empty."}).encode())
                    return
                
                # FitGirl repack page URL
                if "fitgirl-repacks.site" in url and "paste.fitgirl-repacks.site" not in url:
                    add_log(f"Scraping repack page: {url}")
                    response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_el = soup.find('h1', class_='entry-title')
                        title = title_el.get_text(strip=True) if title_el else "Unknown Game"
                        title = re.sub(r'\s+Repack\s*$', '', title, flags=re.IGNORECASE)
                        title = re.sub(r'\s+Updated\s*$', '', title, flags=re.IGNORECASE)
                        
                        mirrors = []
                        content_el = soup.find('div', class_='entry-content')
                        if content_el:
                            links = content_el.find_all('a')
                            for a in links:
                                href = a.get('href', '')
                                if 'paste.fitgirl-repacks.site' in href:
                                    text = a.get_text(strip=True)
                                    name = text.replace("Filehoster:", "").replace("Mirror:", "").strip()
                                    if "torrent" in name.lower() or "torrent" in href.lower():
                                        continue
                                    if not name:
                                        name = "PrivateBin Mirror"
                                    if not any(m["url"] == href or m["name"] == name for m in mirrors):
                                        mirrors.append({"name": name, "url": href})
                                        
                        if not mirrors and content_el:
                            links = content_el.find_all('a')
                            for a in links:
                                href = a.get('href', '')
                                if any(host in href for host in ['fuckingfast.co', 'qiwi.gg', 'datanodes.to', 'krakenfiles.com', 'gofile.io', 'pixeldrain.com']):
                                    text = a.get_text(strip=True)
                                    name = text if text else href.split('/')[2]
                                    if "torrent" in name.lower() or "torrent" in href.lower():
                                        continue
                                    if not any(m["url"] == href or m["name"] == name for m in mirrors):
                                        mirrors.append({"name": name, "url": href})
                                        
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True,
                            "type": "fitgirl_page",
                            "title": title,
                            "mirrors": mirrors
                        }).encode())
                        return
                    else:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch FitGirl page. HTTP Status: {response.status_code}"}).encode())
                        return

                # PrivateBin URL directly
                elif "paste.fitgirl-repacks.site" in url:
                    add_log(f"Loading paste: {url}")
                    res_paste = privatebinapi.get(url)
                    text = res_paste.get('text', '')
                    if not text:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": "PrivateBin content is empty or decryption failed."}).encode())
                        return
                        
                    files = parse_links_from_text(text)
                    guessed_title = guess_game_title(files)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "type": "files",
                        "title": guessed_title,
                        "files": files
                    }).encode())
                    return

                # Raw links list
                else:
                    files = parse_links_from_text(url)
                    if not files:
                        self.send_response(400)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": "No valid direct download links found in pasted text."}).encode())
                        return
                        
                    guessed_title = guess_game_title(files)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "type": "files",
                        "title": guessed_title,
                        "files": files
                    }).encode())
                    return
                    
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                return
                
        elif path == "/api/confirm_config":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                game_title = data.get("game_title", "Custom Game").strip()
                download_dir = data.get("download_dir", "").strip()
                files = data.get("files", [])
                
                if not download_dir:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Save directory is required."}).encode())
                    return
                
                if not files:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "At least one file must be selected."}).encode())
                    return
                
                with state_lock:
                    state["game_title"] = game_title
                    state["download_dir"] = os.path.abspath(download_dir)
                    state["files"] = files
                    state["is_configured"] = True
                    state["is_running"] = False
                    state["should_stop"] = False
                    state["active_index"] = -1
                    state["total_speed"] = 0
                    state["is_extracted"] = False
                    state["is_extracting"] = False
                    state["extraction_progress"] = 0
                    
                initialize_queue_on_disk()
                
                add_log(f"Configured download for: {game_title}")
                add_log(f"Save directory: {state['download_dir']}")
                add_log(f"Selected {len(files)} files.")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                return

        elif path == "/api/reset":
            with state_lock:
                state["game_title"] = ""
                state["files"] = []
                state["download_dir"] = ""
                state["is_configured"] = False
                state["is_running"] = False
                state["should_stop"] = False
                state["active_index"] = -1
                state["total_speed"] = 0
                state["total_progress"] = 0
                state["is_extracted"] = False
                state["is_extracting"] = False
                state["extraction_progress"] = 0
            add_log("[SYSTEM] Downloader session reset. Ready for new configuration.")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return

def start_server():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, APIRequestHandler)
    print("Web server running at http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    add_log("[SYSTEM] Server initialized in idle setup mode.")
    start_server()
