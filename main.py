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

import requests  # Standard requests for downloading

# Global State
state = {
    "paste_url": "http://paste.fitgirl-repacks.site/?d34f9ff6586b30a0#9FFvsRfZUe5DbuRtfzYwHZ2EpJtuT4qyGFUzkBgcXzBe",
    "files": [],
    "download_dir": os.path.join(os.path.expanduser("~"), "Downloads", "Call of Duty - Modern Warfare (2019)"),
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
MAX_WORKERS = 3

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
        # Keep last 100 log messages
        if len(state["log_messages"]) > 100:
            state["log_messages"].pop(0)
    try:
        print(formatted)
    except UnicodeEncodeError:
        try:
            # Fallback to replacing characters
            enc = sys.stdout.encoding or 'ascii'
            print(formatted.encode(enc, errors='replace').decode(enc))
        except Exception:
            # Absolute fallback
            print(f"[{timestamp}] [Log encoding error - fallback] " + "".join(c if ord(c) < 128 else '?' for c in message))

def extract_direct_link(page_url):
    """Bypasses Cloudflare using curl_cffi to get the direct dl.fuckingfast.co link."""
    try:
        add_log(f"Extracting direct link for: {page_url}")
        # FuckingFast might require desktop chrome emulation
        response = cf_requests.get(page_url, impersonate="chrome120", timeout=20, verify=False)
        if response.status_code == 200:
            html = response.text
            match = re.search(r'window\.open\("(https://dl\.fuckingfast\.co/dl/[^"]+)"\)', html)
            if match:
                direct_link = match.group(1)
                add_log(f"Successfully extracted link!")
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
    if file_type == "installer":
        return 7468619
    elif filename == "Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part145.rar":
        return 209228843
    elif filename == "fg-optional-russian.part5.rar":
        return 3592179
    else:
        return 524288000

def fetch_and_filter_paste():
    """Fetches the PrivateBin paste (falling back to local file if blocked) and filters links."""
    add_log(f"Loading paste data...")
    try:
        text = ""
        local_path = os.path.join(os.path.dirname(__file__), "paste_text.txt")
        if os.path.exists(local_path):
            add_log(f"Found local decrypted paste_text.txt. Loading...")
            with open(local_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            add_log(f"Local file not found. Decrypting paste URL: {state['paste_url']}")
            response = privatebinapi.get(state["paste_url"])
            text = response.get('text', '')
            
        if not text:
            add_log("Error: Paste content is empty.")
            return False

        lines = text.split('\n')
        parsed_files = []
        
        # Regex to match fuckingfast URLs and hash filenames
        # Example: - https://fuckingfast.co/szei3l5ldjl0#Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part001.rar
        pattern = r'-\s*(https://fuckingfast\.co/[^\s#]+)#([^\s]+)'
        
        for line in lines:
            match = re.search(pattern, line)
            if match:
                url = match.group(1)
                filename = match.group(2)
                
                # Check filters
                is_target = False
                file_type = ""
                
                # Filter 1: Main game 145 parts
                if re.search(r'\.part[0-9]{3}\.rar$', filename):
                    # Call of Duty MW 2019 parts 001 to 145
                    is_target = True
                    file_type = "game_part"
                # Filter 2: Russian language 5 parts
                elif re.search(r'fg-optional-russian\.part[1-5]\.rar$', filename):
                    is_target = True
                    file_type = "lang_part"
                # Filter 3: Setup installer
                elif filename == "setup-non-campaign-files-only.exe":
                    is_target = True
                    file_type = "installer"
                
                if is_target:
                    cached_size = sizes_cache.get(filename, 0)
                    parsed_files.append({
                        "filename": filename,
                        "url": url,
                        "type": file_type,
                        "status": "waiting",
                        "progress": 0,
                        "downloaded": 0,
                        "size": cached_size,
                        "speed": 0,
                        "time_left": -1,
                        "error": ""
                    })
                    
        # Sort files: installer first, then game parts, then language parts
        def sort_key(f):
            if f["type"] == "installer":
                return (0, f["filename"])
            elif f["type"] == "game_part":
                return (1, f["filename"])
            else:
                return (2, f["filename"])
                
        parsed_files.sort(key=sort_key)
        
        # Scan disk to check for already downloaded parts at startup
        os.makedirs(state["download_dir"], exist_ok=True)
        for f in parsed_files:
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
        
        with state_lock:
            state["files"] = parsed_files
            
        # Initial recalculation of total progress
        recalculate_total_progress()
            
        add_log(f"Successfully loaded {len(parsed_files)} target files (145 main parts, 5 Russian parts, 1 installer).")
        return True
    except Exception as e:
        add_log(f"Error loading paste: {str(e)}")
        return False

def download_worker():
    """Background thread worker to download files concurrently."""
    os.makedirs(state["download_dir"], exist_ok=True)
    
    with state_lock:
        state["active_workers_count"] += 1
        
    try:
        while True:
            with state_lock:
                # If we should stop, or queue is not running, or we have too many workers active
                if state["should_stop"] or not state["is_running"] or state["active_workers_count"] > state["max_workers"]:
                    break
                    
                # Find first waiting or failed file
                target_idx = -1
                for idx, f in enumerate(state["files"]):
                    if f["status"] in ["waiting", "failed"]:
                        target_idx = idx
                        f["status"] = "connecting"
                        break
                
                if target_idx == -1:
                    # No files waiting or failed. Are other workers still downloading?
                    active_workers = any(f["status"] in ["connecting", "downloading"] for f in state["files"])
                    if not active_workers:
                        state["is_running"] = False
                        state["total_speed"] = 0
                        add_log("🎉 ALL DOWNLOADS COMPLETED SUCCESSFULLY!")
                    break
                    
                file_info = state["files"][target_idx]
                
            # Perform download for the file
            success = download_file(target_idx, file_info)
            
            with state_lock:
                if not success:
                    if state["should_stop"]:
                        break
                    # Short sleep before trying another file
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
    
    # Step 1: Extract direct download link
    direct_link = extract_direct_link(page_url)
    if not direct_link:
        with state_lock:
            state["files"][index]["status"] = "failed"
            state["files"][index]["error"] = "Could not bypass Cloudflare. Retrying later."
        return False
        
    # Step 2: Check local file for partial download resume
    resume_byte = 0
    if os.path.exists(file_path):
        resume_byte = os.path.getsize(file_path)
        add_log(f"Local file found. Size: {resume_byte} bytes.")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Step 3: Query total file size first (streamed request) to check if fully downloaded
    total_size = 0
    try:
        r_head = requests.get(direct_link, headers=headers, stream=True, timeout=15)
        total_size = int(r_head.headers.get('content-length', 0))
        r_head.close()
        if total_size > 0:
            save_size_to_cache(filename, total_size)
    except Exception as e:
        add_log(f"Warning: Could not query file size: {str(e)}")
        
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
        add_log(f"Attempting resume from byte {resume_byte}...")
        
    try:
        response = requests.get(direct_link, headers=headers, stream=True, timeout=30)
        
        # Handle response codes
        if response.status_code == 206:
            # Server accepted range request, append to file
            mode = "ab"
            downloaded = resume_byte
            total_size = int(response.headers.get('content-length', 0)) + resume_byte
            add_log(f"Resuming download from byte {resume_byte}...")
            if total_size > 0:
                save_size_to_cache(filename, total_size)
        elif response.status_code == 200:
            # Server ignored range or downloading from scratch
            mode = "wb"
            downloaded = 0
            total_size = int(response.headers.get('content-length', 0))
            if resume_byte > 0:
                add_log("Server did not support resume. Starting from scratch.")
            if total_size > 0:
                save_size_to_cache(filename, total_size)
        elif response.status_code == 416:
            # Range not satisfiable (usually means file is already fully downloaded)
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
            
        # Step 4: Stream content to file
        chunk_size = 256 * 1024  # 256 KB
        last_time = time.time()
        bytes_in_sec = 0
        
        with open(file_path, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                # Check for stop signal
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
                    
                    # Update progress and speeds every 0.5 - 1.0s
                    curr_time = time.time()
                    elapsed = curr_time - last_time
                    if elapsed >= 1.0:
                        speed = bytes_in_sec / elapsed  # Bytes/sec
                        progress = int((downloaded / total_size) * 100) if total_size > 0 else 0
                        time_left = int((total_size - downloaded) / speed) if speed > 0 else -1
                        
                        with state_lock:
                            state["files"][index]["downloaded"] = downloaded
                            state["files"][index]["progress"] = progress
                            state["files"][index]["speed"] = speed
                            state["files"][index]["time_left"] = time_left
                            state["total_speed"] = sum(x["speed"] for x in state["files"] if x["status"] == "downloading")
                            
                        # Update overall progress
                        recalculate_total_progress()
                        
                        bytes_in_sec = 0
                        last_time = curr_time
                        
        # Finished writing file successfully
        with state_lock:
            state["files"][index]["status"] = "finished"
            state["files"][index]["progress"] = 100
            state["files"][index]["downloaded"] = total_size
            state["files"][index]["speed"] = 0
            state["files"][index]["time_left"] = 0
            state["total_speed"] = 0
        recalculate_total_progress()
        add_log(f"Successfully downloaded {filename}.")
        return True
        
    except Exception as e:
        add_log(f"Exception during download of {filename}: {str(e)}")
        with state_lock:
            state["files"][index]["status"] = "failed"
            state["files"][index]["error"] = str(e)
            state["files"][index]["speed"] = 0
            state["total_speed"] = 0
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
        
        # Track the first active download index in the state
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

    # We need to extract:
    # 1. Main game split parts: Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part001.rar
    # 2. Russian language parts: fg-optional-russian.part1.rar (if exists)
    
    archives = [
        ("Call_of_Duty_MW_2019_--_fitgirl-repacks.site_--_.part001.rar", "Main game parts"),
        ("fg-optional-russian.part1.rar", "Russian language parts")
    ]
    
    for filename, label in archives:
        archive_path = os.path.join(state["download_dir"], filename)
        if not os.path.exists(archive_path):
            add_log(f"Archive not found: {archive_path}. Skipping.")
            continue
            
        add_log(f"Unpacking {label} ({filename}). This may take a while...")
        
        try:
            cmd = [unrar_path, "x", "-y", archive_path]
            process = subprocess.Popen(
                cmd,
                cwd=state["download_dir"],
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
        state["is_extracted"] = os.path.exists(os.path.join(state["download_dir"], "fg-01.bin"))
        
    add_log("Extraction workflow complete!")

# HTTP Web Server
class APIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging every static asset request to console
        pass
        
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        # JSON API: Get Status
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with state_lock:
                state["is_extracted"] = os.path.exists(os.path.join(state["download_dir"], "fg-01.bin"))
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
                if not state["is_running"]:
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
                        
                        # If the downloader is running, dynamically spawn threads to match the new limit
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
            # Run the installer setup exe
            installer_path = os.path.join(state["download_dir"], "setup-non-campaign-files-only.exe")
            if os.path.exists(installer_path):
                try:
                    add_log(f"Launching installer setup at: {installer_path}...")
                    # Run setup in the background as a detached process
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
                add_log(f"Error: Installer setup not found at {installer_path}")
                self.send_error(404, "Installer file not found on disk.")
                
        elif path == "/api/extract":
            with state_lock:
                if state.get("is_extracting"):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Extraction already in progress."}).encode())
                    return
                # Spawn background thread for extraction
                threading.Thread(target=extraction_worker, daemon=True).start()
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())

def start_server():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, APIRequestHandler)
    print("Web server running at http://localhost:8000")
    
    # webbrowser.open is disabled to prevent blocking in automated runs
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    # 1. Fetch paste content
    success = fetch_and_filter_paste()
    if not success:
        print("Failed to initialize paste contents. Check internet connection.")
        
    # 2. Start local web GUI server
    start_server()
