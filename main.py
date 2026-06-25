import os
import sys
import re
import json
import threading
import time
import urllib.parse
import webbrowser
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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
    "base_download_dir": "",
    "default_download_dir": "D:\\Downloads",
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
    "extraction_progress": 0,
    "average_download_speed": 5000000.0,
    "active_mirror": ""
}

state_lock = threading.RLock()
extraction_lock = threading.Lock()

# Cache mechanism for file sizes
cache_path = os.path.join(os.path.dirname(__file__), "sizes_cache.json")
sizes_cache = {}
if os.path.exists(cache_path):
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            sizes_cache = json.load(f)
    except Exception:
        pass

state["average_download_speed"] = float(sizes_cache.get("__average_download_speed__", 5000000.0))

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

def extract_datanodes_link(page_url):
    """Uses Playwright to extract the direct download link from DataNodes."""
    with extraction_lock:
        from playwright.sync_api import sync_playwright
        add_log(f"Extracting DataNodes direct link for: {page_url}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                # Bypass webdriver detection
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                
                # Click 1: Continue to Download
                btn1 = page.locator("#method_free").first
                if btn1.count() > 0:
                    btn1.click()
                    page.wait_for_timeout(8000)
                    
                    # Wait 6 seconds on Page 2 for Cloudflare silent challenge and Google reCAPTCHA
                    page.wait_for_timeout(6000)
                    
                    # Click 2: Continue to Download (page 2) with retry loop
                    btn2 = page.locator("#method_free").first
                    page3_reached = False
                    for attempt in range(3):
                        add_log(f"Page 2: Clicking second button (attempt {attempt+1})...")
                        if btn2.count() > 0:
                            try:
                                btn2.click()
                            except Exception as click_err:
                                add_log(f"Page 2 click exception: {click_err}")
                        page.wait_for_timeout(6000)
                        
                        # Check if Page 3 loaded by looking for Free Download button
                        free_btn = page.locator("button:has-text('Free Download')")
                        if free_btn.count() == 0:
                            free_btn = page.locator("text=Free Download")
                        if free_btn.count() > 0:
                            page3_reached = True
                            break
                            
                    if page3_reached:
                        
                        # Click 3 (First): Free Download (page 3) to trigger ad popup
                        free_btn = page.locator("button:has-text('Free Download')")
                        if free_btn.count() == 0:
                            free_btn = page.locator("text=Free Download")
                            
                        if free_btn.count() > 0:
                            try:
                                with context.expect_page(timeout=8000) as popup_info:
                                    free_btn.first.click()
                                popup = popup_info.value
                                popup.close()
                            except Exception:
                                try:
                                    free_btn.first.click()
                                except Exception:
                                    pass
                                    
                            page.wait_for_timeout(4000)
                            
                            # Click 3 (Second): Free Download again to start countdown if still present
                            try:
                                if free_btn.count() > 0 and free_btn.first.is_visible() and "Free Download" in free_btn.first.inner_text():
                                    with context.expect_page(timeout=5000) as popup_info2:
                                        free_btn.first.click()
                                    popup2 = popup_info2.value
                                    popup2.close()
                            except Exception:
                                pass
                                
                            # Monitor and wait for "Start Download" countdown (up to 24 seconds)
                            start_btn = page.locator("text=Start Download")
                            start_visible = False
                            for _ in range(8):
                                page.wait_for_timeout(3000)
                                if start_btn.count() > 0 and start_btn.is_visible():
                                    start_visible = True
                                    break
                                
                            if start_visible:
                                try:
                                    # Click 4: Start Download and expect download
                                    with page.expect_download(timeout=30000) as download_info:
                                        start_btn.click()
                                    download = download_info.value
                                    dl_url = download.url
                                    download.cancel()
                                    
                                    add_log(f"Successfully extracted DataNodes direct link!")
                                    browser.close()
                                    return dl_url
                                except Exception as e:
                                    add_log(f"Error clicking Start Download or starting download: {str(e)}")
                            else:
                                add_log("Start Download button never became visible on Page 4.")
                        else:
                            add_log("Free Download button not found on Page 3.")
                    else:
                        add_log("Second #method_free button not found on Page 2.")
                else:
                    add_log("First #method_free button not found on Page 1.")
                
                browser.close()
                return None
        except Exception as e:
            add_log(f"DataNodes extraction exception: {str(e)}")
            return None

def extract_fileditch_link(page_url):
    try:
        add_log(f"Extracting direct link for FileDitch: {page_url}")
        response = cf_requests.get(page_url, impersonate="chrome120", timeout=20, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if "Download" in a.text:
                    direct_link = a['href']
                    add_log(f"Successfully extracted FileDitch direct link!")
                    return direct_link
            # Fallback to regex search if no download text
            match = re.search(r'href="([^"]+)"[^>]*>\s*⬇ Download', response.text)
            if match:
                return match.group(1)
            add_log("Error: Direct link button not found in FileDitch HTML.")
            return None
        else:
            add_log(f"Error: FileDitch responded with status code {response.status_code}")
            return None
    except Exception as e:
        add_log(f"FileDitch extraction exception: {str(e)}")
        return None

def extract_gofile_link(page_url):
    with extraction_lock:
        from playwright.sync_api import sync_playwright
        import os
        add_log(f"Extracting Gofile direct link for: {page_url}")
        try:
            profile_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "scratch", "chrome_profile"))
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=profile_dir,
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                page = context.new_page()
                
                gofile_links = []
                api_status = [None]
                
                def on_response(response):
                    if "api.gofile.io" in response.url:
                        try:
                            data = response.json()
                            status = data.get("status")
                            if status:
                                api_status[0] = status
                            if status == "ok":
                                children = data.get("data", {}).get("children", {})
                                for cid, cinfo in children.items():
                                    link = cinfo.get("link")
                                    if link:
                                        gofile_links.append(link)
                        except Exception:
                            pass
                page.on("response", on_response)
                
                navigation_failed = False
                try:
                    page.goto(page_url, wait_until="domcontentloaded", timeout=25000)
                except Exception as e:
                    add_log(f"Gofile navigation warning (gofile.io may be blocked by your network firewall): {e}")
                    navigation_failed = True
                    
                # Wait up to 15 seconds
                for _ in range(15):
                    if gofile_links or api_status[0]:
                        break
                    page.wait_for_timeout(1000)
                
                context.close()
                
                if gofile_links:
                    add_log("Successfully extracted Gofile direct link!")
                    return gofile_links[0]
                elif api_status[0] == "error-notPremium":
                    add_log("Gofile: Free accounts cannot download this folder. Premium account required.")
                    return "ERROR_NOT_PREMIUM"
                elif api_status[0] == "error-notFound":
                    add_log("Gofile: Folder/file not found (404).")
                    return "ERROR_NOT_FOUND"
                elif navigation_failed or not api_status[0]:
                    add_log("Gofile: Connection timed out. Gofile may be blocked on your network/VPN.")
                    return "ERROR_BLOCKED"
                else:
                    return None
        except Exception as e:
            add_log(f"Gofile extraction exception: {str(e)}")
            return None

def extract_rootz_link(page_url):
    with extraction_lock:
        from playwright.sync_api import sync_playwright
        add_log(f"Extracting Rootz direct link for: {page_url}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                try:
                    page.goto(page_url, wait_until="load", timeout=20000)
                except Exception as e:
                    add_log(f"Rootz: Navigation failed: {e}")
                    browser.close()
                    return None
                
                # Wait 4 seconds for client-side React rendering
                page.wait_for_timeout(4000)
                
                # Check for 404
                body_text = page.locator("body").inner_text()
                if "This page could not be found" in body_text or "404" in body_text:
                    add_log("Rootz: File not found (404).")
                    browser.close()
                    return "ERROR_NOT_FOUND"
                    
                download_btn = page.locator("button:has-text('Download')")
                if download_btn.count() == 0:
                    download_btn = page.locator("text=Download")
                    
                if download_btn.count() > 0:
                    try:
                        with page.expect_download(timeout=15000) as download_info:
                            download_btn.first.click()
                        download = download_info.value
                        dl_url = download.url
                        download.cancel()
                        add_log("Successfully extracted Rootz direct link!")
                        browser.close()
                        return dl_url
                    except Exception as click_err:
                        add_log(f"Rootz click/download exception: {click_err}")
                else:
                    add_log("Rootz: Download button not found.")
                
                browser.close()
                return "ERROR_NOT_FOUND"
        except Exception as e:
            add_log(f"Rootz extraction exception: {str(e)}")
            return None

def extract_viking_link(page_url):
    with extraction_lock:
        from playwright.sync_api import sync_playwright
        import os
        add_log(f"Extracting VikingFile direct link for: {page_url}")
        try:
            profile_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "scratch", "chrome_profile"))
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=profile_dir,
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                page = context.new_page()
                
                direct_link = [None]
                
                def on_response(response):
                    if "vik1ngfile.site" in response.url and response.request.method == "POST":
                        try:
                            data = response.json()
                            dl = data.get("direct-link")
                            if dl:
                                direct_link[0] = dl
                        except Exception:
                            pass
                page.on("response", on_response)
                
                try:
                    page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
                except Exception as e:
                    add_log(f"VikingFile navigation error/timeout: {e}")
                    
                # Wait up to 20 seconds for the Turnstile response with direct-link
                for _ in range(20):
                    if direct_link[0]:
                        break
                    page.wait_for_timeout(1000)
                
                # Fallback: check DOM #download-link
                if not direct_link[0]:
                    dl_link = page.locator("#download-link")
                    if dl_link.count() > 0:
                        href = dl_link.get_attribute("href")
                        if href and ("vikingfile" in href or "cloudflarestorage" in href):
                            direct_link[0] = href
                
                context.close()
                
                if direct_link[0]:
                    add_log("Successfully extracted VikingFile direct link!")
                    return direct_link[0]
                else:
                    add_log("VikingFile: Failed to extract direct link (possibly captcha unsolved).")
                    return "ERROR_CAPTCHA_REQUIRED"
        except Exception as e:
            add_log(f"VikingFile extraction exception: {str(e)}")
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
            elif "optional" in filename_lower or "selective" in filename_lower or "language" in filename_lower or "lang" in filename_lower or any(lang in filename_lower for lang in ["russian", "english", "french", "german", "spanish", "chinese", "brazilian", "japanese", "korean", "polish", "mexican", "italian", "greek", "portuguese"]):
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
    prefill_part_sizes(parsed_files)
    return parsed_files

def prefill_part_sizes(files):
    # Find all files with part numbers
    part_files = []
    max_part = 0
    
    for f in files:
        if f["type"] == "game_part" or f["filename"].endswith(".rar"):
            # Check for part number in filename
            match = re.search(r'\.part(\d+)\.rar$', f["filename"], re.IGNORECASE)
            if match:
                part_num = int(match.group(1))
                part_files.append((f, part_num))
                if part_num > max_part:
                    max_part = part_num
                    
    # Now prefill size for all parts except the last one (max_part)
    for f, part_num in part_files:
        if part_num < max_part:
            url_lower = f["url"].lower()
            if "fuckingfast" in url_lower or "datanodes" in url_lower:
                f["size"] = 2 * 1024 * 1024 * 1024  # 2 GB
            elif "multiupload" in url_lower or "multiup" in url_lower:
                f["size"] = int(1.95 * 1024 * 1024 * 1024)  # 1.95 GB
            else:
                f["size"] = 2 * 1024 * 1024 * 1024  # Default to 2 GB

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

def safe_folder_name(name):
    if not name:
        return ""
    return re.sub(r'[:\/\\\*\?"<>\|]', '', name).strip()

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
    
    # Step 1: Extract direct download link based on hoster
    if "fuckingfast.co" in page_url:
        direct_link = extract_direct_link(page_url)
        if not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Could not bypass Cloudflare for FuckingFast."
            return False
    elif "datanodes.to" in page_url:
        direct_link = extract_datanodes_link(page_url)
        if not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Could not extract direct link for DataNodes."
            return False
    elif "fileditchfiles.me" in page_url or "fileditch.com" in page_url:
        direct_link = extract_fileditch_link(page_url)
        if not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Could not extract direct link for FileDitch."
            return False
    elif "gofile.io" in page_url:
        direct_link = extract_gofile_link(page_url)
        if not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Could not extract direct link for Gofile."
            return False
        elif direct_link == "ERROR_NOT_PREMIUM":
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Gofile: Free accounts cannot download this folder. Premium account required."
            return False
        elif direct_link == "ERROR_NOT_FOUND":
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Gofile: File not found (404)."
            return False
        elif direct_link == "ERROR_BLOCKED":
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Gofile: Connection timed out. Gofile may be blocked on your network (e.g. university firewall). Try enabling a VPN."
            return False
    elif "rootz.so" in page_url or "rootz.cc" in page_url:
        direct_link = extract_rootz_link(page_url)
        if direct_link == "ERROR_NOT_FOUND" or not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Rootz: File not found (404)."
            return False
    elif "vikingfile.com" in page_url or "vik1ngfile.site" in page_url:
        direct_link = extract_viking_link(page_url)
        if direct_link == "ERROR_CAPTCHA_REQUIRED" or not direct_link:
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "VikingFile: Captcha verification required."
            return False
    elif "pixeldrain.com/u/" in page_url:
        direct_link = page_url.replace("pixeldrain.com/u/", "pixeldrain.com/api/file/")
    elif "multiup.io" in page_url:
        with state_lock:
            state["files"][index]["status"] = "failed"
            state["files"][index]["error"] = "Cloudflare Turnstile challenge blocked headless scraper. Please use DataNodes or FuckingFast mirrors."
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
        
        # Check if we accidentally downloaded an HTML page instead of binary data
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' in content_type:
            add_log(f"Error: Server returned HTML page instead of binary stream for {filename}.")
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Bypass failed: server returned HTML page instead of file data."
            return False
            
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
                            if speed > 100000:
                                state["average_download_speed"] = state["average_download_speed"] * 0.95 + speed * 0.05
                                save_size_to_cache("__average_download_speed__", state["average_download_speed"])
                            
                        recalculate_total_progress()
                        bytes_in_sec = 0
                        last_time = curr_time
                        
        if downloaded == 0:
            add_log(f"Error: Downloaded 0 bytes for {filename}.")
            with state_lock:
                state["files"][index]["status"] = "failed"
                state["files"][index]["error"] = "Downloaded 0 bytes. Direct link might have expired."
            return False
            
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

def clean_size(size_str):
    if not size_str:
        return "Unknown"
    s = re.sub(r'^from\s+', '', size_str, flags=re.IGNORECASE)
    s = re.sub(r'\s*\[Selective\s+Download[^\]]*\]', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\(\s*Selective\s+Download[^\)]*\)', '', s, flags=re.IGNORECASE)
    return s.strip()

def clean_cover_url(url):
    if not url:
        return ""
    url = url.split('?')[0]
    # Strip WordPress Jetpack CDN prefixes (e.g. i0.wp.com/)
    url = re.sub(r'^https?://i\d+\.wp\.com/', 'https://', url)
    # Strip WordPress size suffixes (e.g. -150x150, -300x225)
    url = re.sub(r'-\d+x\d+\.(jpg|jpeg|png|gif|webp)$', r'.\1', url, flags=re.IGNORECASE)
    return url

def clean_and_parse_title(raw_title):
    import html
    # Decode HTML entities
    title = html.unescape(raw_title)
    # Remove #number prefix
    title = re.sub(r'^#\d+\s*', '', title).strip()
    title = re.sub(r'\s+по\s+сети.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+скачать.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title)
    
    # We want to find where the version info starts.
    pattern = r'[\s,–—\-(\[]+(v[\s.]*\d|build[\s.]*\d|b[\s.]*\d)'
    match = re.search(pattern, title, re.IGNORECASE)
    
    version = ""
    if match:
        idx = match.start()
        # The main title is everything before the match
        main_title = title[:idx].strip()
        # The version/details start at the matched version string
        version_part = title[idx:].strip(' ,–—-()[]')
        
        # Now let's extract the version number itself
        v_match = re.search(r'\b(v[\s.]*\d[\w\.]*|Build[\s.]*\d[\w\.]*|b[\s.]*\d[\w\.]*)\b', version_part, re.IGNORECASE)
        if v_match:
            version = v_match.group(1).strip()
        else:
            version = version_part
            
        title = main_title
    else:
        # If no version pattern is found, check if there's a simple version suffix
        v_match = re.search(r'\b(v[\s.]*\d[\w\.]*|Build[\s.]*\d[\w\.]*)\b', title, re.IGNORECASE)
        if v_match:
            version = v_match.group(1).strip()
            title = title.replace(v_match.group(0), "").strip()
            
    # Clean up trailing/leading dashes/commas from title
    title = re.sub(r'^[\s,–—\-]+|[\s,–—\-]+$', '', title).strip()
    # Strip edition suffixes like Deluxe Edition, Gold Edition, Ultimate, etc.
    title = re.sub(r'[\s:–—\-]+(?:digital\s+)?(?:deluxe|ultimate|premium|standard|limited|gold|complete|special)\s+edition\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[\s:–—\-]+(?:digital\s+)?(?:deluxe|ultimate|premium|standard|limited|gold|complete|special)\b', '', title, flags=re.IGNORECASE)
    # Strip DLC suffixes like + 3 DLCs/Bonuses, + All DLCs, OST, etc.
    title = re.sub(r'\+\s*(?:\d+\s*|All\s+)?(?:DLCs?|Bonuses?|OST|Soundtracks?|Music|Bonus|Extras?)(?:\s*(?:/|\+|and)\s*(?:\d+\s*|All\s+)?(?:DLCs?|Bonuses?|OST|Soundtracks?|Music|Bonus|Extras?))*\b', '', title, flags=re.IGNORECASE)
    # Clean empty parenthesis/brackets
    title = re.sub(r'\(\s*\)', '', title)
    title = re.sub(r'\[\s*\]', '', title)
    title = re.sub(r'^[\s,–—\-]+|[\s,–—\-]+$', '', title).strip()
    title = re.sub(r'\s+', ' ', title)
    return title, version

def parse_online_fix_page(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all(class_=['article', 'article-short'])
    results = []
    for art in articles:
        title_a = art.find('a', class_=['news-title', 'title', 'post-title'])
        if not title_a:
            for h in art.find_all(['h1', 'h2', 'h3']):
                a = h.find('a')
                if a:
                    title_a = a
                    break
        if not title_a:
            for a in art.find_all('a'):
                if '/games/' in a.get('href', ''):
                    title_a = a
                    break
        if not title_a:
            continue
            
        title_text = title_a.text.strip()
        title_text = title_text.split('\n')[0].strip()
        href = title_a.get('href', '')
        if '/games/' not in href:
            continue
            
        img = art.find('img')
        img_src = ""
        if img:
            img_src = img.get('data-src') or img.get('src', '')
        if img_src:
            img_src = urllib.parse.urljoin(base_url, img_src)
            img_src = clean_cover_url(img_src)
            
        summary_el = art.find(class_='preview-text') or art.find(class_='entry-content')
        summary = summary_el.text.strip() if summary_el else ""
        summary = summary[:150] + "..." if len(summary) > 150 else summary
        
        clean_t, version = clean_and_parse_title(title_text)
        
        results.append({
            "title": clean_t,
            "version": version,
            "url": href,
            "cover_image": img_src,
            "original_size": "Unknown",
            "repack_size": "Unknown",
            "summary": summary
        })
    return results

def fetch_repack_details_helper(item):
    url = item['url']
    try:
        res = cf_requests.get(url, impersonate="chrome120", timeout=15, verify=False)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            cover_image = ""
            content_el = soup.find('div', class_='entry-content')
            if content_el:
                img_el = content_el.find('img', class_='alignleft')
                if img_el:
                    cover_image = img_el.get('src', '')
                else:
                    img_el = content_el.find('img')
                    if img_el:
                        cover_image = img_el.get('src', '')
            if cover_image:
                cover_image = urllib.parse.urljoin(url, cover_image)
            
            text_all = soup.get_text()
            orig_match = re.search(r'Original Size:\s*([^\n]+)', text_all, re.IGNORECASE)
            repack_match = re.search(r'Repack Size:\s*([^\n]+)', text_all, re.IGNORECASE)
            
            item['cover_image'] = clean_cover_url(cover_image)
            item['original_size'] = clean_size(orig_match.group(1)) if orig_match else "Unknown"
            item['repack_size'] = clean_size(repack_match.group(1)) if repack_match else "Unknown"
    except Exception as e:
        pass
        
    title, version = clean_and_parse_title(item.get('title', ''))
    item['title'] = title
    item['version'] = version
    return item

# HTTP Web Server
class APIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
        
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        if path == "/api/browse_folder":
            import subprocess
            ps_script = (
                "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; "
                "$dialog = New-Object System.Windows.Forms.FolderBrowserDialog; "
                "$dialog.Description = 'Select Download Save Folder'; "
                "$dialog.ShowNewFolderButton = $true; "
                "$win = New-Object System.Windows.Forms.Form; "
                "$win.TopMost = $true; "
                "if ($dialog.ShowDialog($win) -eq 'OK') { $dialog.SelectedPath }"
            )
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                    capture_output=True,
                    text=True,
                    timeout=180
                )
                selected_path = result.stdout.strip()
                if selected_path:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "path": selected_path}).encode())
                    return
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "No folder selected."}).encode())
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                return
                
        elif path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with state_lock:
                if state["download_dir"] and os.path.exists(state["download_dir"]):
                    # Look for standard setup .bin files or output to check if extracted
                    state["is_extracted"] = any(f.endswith(".bin") for f in os.listdir(state["download_dir"]))
                self.wfile.write(json.dumps(state).encode())
            return
            
        elif path == "/api/proxy_image":
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                img_url = query_params.get("url", [""])[0]
                if not img_url:
                    self.send_response(400)
                    self.end_headers()
                    return
                
                # Check for fastpic and imageban and convert to thumbnails to bypass hotlinking protection
                lower_url = img_url.lower()
                if "fastpic.ru" in lower_url or "fastpic.org" in lower_url:
                    thumb = img_url.replace("/big/", "/thumb/")
                    thumb = thumb.split('?')[0]
                    if thumb.endswith(".jpg"):
                        thumb = thumb[:-4] + ".jpeg"
                    elif thumb.endswith(".png"):
                        thumb = thumb[:-4] + ".jpeg"
                    thumb = thumb.replace(".ru/", ".org/")
                    img_url = thumb
                elif "imageban.ru" in lower_url or "imageban.net" in lower_url:
                    img_url = img_url.replace("/out/", "/thumbs/")
                
                # Check cache first
                import hashlib
                url_hash = hashlib.md5(img_url.encode('utf-8')).hexdigest()
                ext = "jpg"
                if "." in img_url.split('/')[-1]:
                    parts = img_url.split('/')[-1].split('.')
                    if len(parts) > 1 and len(parts[-1]) <= 4 and parts[-1].isalnum():
                        ext = parts[-1]
                
                cache_dir = os.path.join(os.getcwd(), "cover_cache")
                os.makedirs(cache_dir, exist_ok=True)
                cache_path = os.path.join(cache_dir, f"{url_hash}.{ext}")
                
                if os.path.exists(cache_path):
                    self.send_response(200)
                    content_type = "image/jpeg"
                    if ext.lower() == "png":
                        content_type = "image/png"
                    elif ext.lower() == "gif":
                        content_type = "image/gif"
                    elif ext.lower() == "webp":
                        content_type = "image/webp"
                    
                    self.send_header("Content-Type", content_type)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "public, max-age=31536000")
                    self.end_headers()
                    with open(cache_path, "rb") as f:
                        self.wfile.write(f.read())
                    return

                # Download and cache
                add_log(f"Proxying image: {img_url}")
                session = cf_requests.Session()
                response = session.get(img_url, impersonate="chrome120", timeout=15, verify=False)
                
                content_type = response.headers.get("Content-Type", "image/jpeg")
                content = response.content
                is_success = (response.status_code == 200)
                
                if is_success:
                    with open(cache_path, "wb") as f:
                        f.write(content)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "public, max-age=31536000")
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(response.status_code)
                    self.end_headers()
            except Exception as e:
                add_log(f"Proxy image exception: {str(e)}")
                self.send_response(500)
                self.end_headers()
            return
        elif path == "/api/popular":
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                provider = query_params.get("provider", ["fitgirl"])[0]
                type_val = query_params.get("type", ["monthly"])[0]
                page = int(query_params.get("page", ["1"])[0])
                
                results = []
                has_next = False
                if provider == "onlinefix":
                    add_log(f"Fetching Online-Fix page {page}...")
                    if page == 1:
                        url = "https://online-fix.me/"
                    else:
                        url = f"https://online-fix.me/page/{page}/"
                        
                    response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        results = parse_online_fix_page(response.text, url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        next_page_str = f"/page/{page+1}/"
                        has_next = any(next_page_str in (a.get('href') or '') for a in soup.find_all('a'))
                    else:
                        raise Exception(f"HTTP status: {response.status_code}")
                else: # fitgirl
                    add_log(f"Fetching popular FitGirl repacks ({type_val}, page {page})...")
                    if type_val == "yearly":
                        url = "https://fitgirl-repacks.site/popular-repacks-of-the-year/"
                    else: # monthly
                        url = "https://fitgirl-repacks.site/pop-repacks/"
                            
                    response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        content_el = soup.find('div', class_='entry-content')
                        all_results = []
                        if content_el:
                            items = content_el.find_all('div', class_='widget-grid-view-image')
                            for item in items:
                                a = item.find('a')
                                img = item.find('img')
                                if a and img:
                                    title = a.get('title', '')
                                    repack_url = a.get('href', '')
                                    
                                    repack_url_lower = repack_url.lower()
                                    if "digest" in repack_url_lower or "uncategorized" in repack_url_lower or "announcement" in repack_url_lower:
                                        continue
                                        
                                    clean_t, version = clean_and_parse_title(title)
                                    cover_image = clean_cover_url(img.get('src', ''))
                                    all_results.append({
                                        "title": clean_t,
                                        "version": version,
                                        "url": repack_url,
                                        "cover_image": cover_image,
                                        "original_size": "Unknown",
                                        "repack_size": "Unknown",
                                        "summary": "Popular Repack"
                                    })
                        
                        PAGE_SIZE = 24
                        start_idx = (page - 1) * PAGE_SIZE
                        end_idx = page * PAGE_SIZE
                        results = all_results[start_idx:end_idx]
                        has_next = end_idx < len(all_results)
                    else:
                        raise Exception(f"HTTP status: {response.status_code}")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "results": results, "has_next": has_next}).encode())
            except Exception as e:
                add_log(f"Popular fetch exception: {str(e)}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
            return
            
        elif path == "/api/latest":
            try:
                add_log("Fetching latest FitGirl repacks...")
                url = "https://fitgirl-repacks.site/"
                response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    articles = soup.find_all('article')
                    results = []
                    for art in articles[:10]:
                        title_el = art.find('h1', class_=['entry-title', 'post-title']) or art.find('h2', class_=['entry-title', 'post-title'])
                        link_el = title_el.find('a') if title_el else None
                        if not link_el:
                            continue
                        title = link_el.text.strip()
                        repack_url = link_el.get('href')
                        
                        summary_el = art.find(class_='entry-summary') or art.find(class_='entry-content')
                        summary = summary_el.text.strip() if summary_el else ""
                        summary = re.sub(r'\s*Continue reading\s*→.*$', '', summary, flags=re.IGNORECASE)
                        summary = summary[:150] + "..." if len(summary) > 150 else summary
                        
                        results.append({
                            "title": title,
                            "url": repack_url,
                            "summary": summary,
                            "cover_image": "",
                            "original_size": "Unknown",
                            "repack_size": "Unknown"
                        })
                    
                    from concurrent.futures import ThreadPoolExecutor
                    with ThreadPoolExecutor(max_workers=8) as executor:
                        final_results = list(executor.map(fetch_repack_details_helper, results))
                        
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "results": final_results}).encode())
                else:
                    self.send_response(500)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": f"HTTP status: {response.status_code}"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
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
            
        elif path == "/api/search":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                query = data.get("query", "").strip()
                provider = data.get("provider", "fitgirl")
                page = int(data.get("page", 1))
                
                if not query:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Query cannot be empty."}).encode())
                    return
                
                results = []
                has_next = False
                if provider == "onlinefix":
                    add_log(f"Searching Online-Fix for: {query} (page {page})...")
                    search_url = "https://online-fix.me/index.php?do=search"
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Referer": "https://online-fix.me/"
                    }
                    post_body = {
                        "do": "search",
                        "subaction": "search",
                        "search_start": str(page),
                        "story": query
                    }
                    response = cf_requests.post(search_url, headers=headers, data=post_body, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        results = parse_online_fix_page(response.text, search_url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        next_page_num = str(page + 1)
                        for a in soup.find_all('a'):
                            href = a.get('href') or ''
                            onclick = a.get('onclick') or ''
                            if f'search_start={next_page_num}' in href or f'list_submit({next_page_num})' in onclick or f'search_start:{next_page_num}' in onclick:
                                has_next = True
                                break
                        if not has_next and len(results) >= 10:
                            has_next = True
                    else:
                        raise Exception(f"HTTP status: {response.status_code}")
                else: # fitgirl
                    add_log(f"Searching FitGirl for: {query} (page {page})...")
                    if page == 1:
                        search_url = f"https://fitgirl-repacks.site/?s={urllib.parse.quote(query)}"
                    else:
                        search_url = f"https://fitgirl-repacks.site/?s={urllib.parse.quote(query)}&paged={page}"
                        
                    response = cf_requests.get(search_url, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        articles = soup.find_all('article')
                        raw_results = []
                        
                        for art in articles:
                            title_el = art.find('h1', class_=['entry-title', 'post-title']) or art.find('h2', class_=['entry-title', 'post-title'])
                            link_el = title_el.find('a') if title_el else None
                            if not link_el:
                                continue
                            title = link_el.text.strip()
                            repack_url = link_el.get('href')
                            
                            repack_url_lower = repack_url.lower()
                            if "digest" in repack_url_lower or "uncategorized" in repack_url_lower or "announcement" in repack_url_lower:
                                continue
                                
                            summary_el = art.find(class_='entry-summary') or art.find(class_='entry-content')
                            summary = summary_el.text.strip() if summary_el else ""
                            summary = re.sub(r'\s*Continue reading\s*→.*$', '', summary, flags=re.IGNORECASE)
                            summary = summary[:150] + "..." if len(summary) > 150 else summary
                            
                            raw_results.append({
                                "title": title,
                                "url": repack_url,
                                "summary": summary,
                                "cover_image": "",
                                "original_size": "Unknown",
                                "repack_size": "Unknown"
                            })
                        
                        from concurrent.futures import ThreadPoolExecutor
                        with ThreadPoolExecutor(max_workers=8) as executor:
                            results = list(executor.map(fetch_repack_details_helper, raw_results))
                            
                        # Filter out non-repacks
                        results = [r for r in results if not (r.get("repack_size") == "Unknown" and r.get("original_size") == "Unknown")]
                        has_next = (soup.find('a', class_='next') is not None) or (soup.find('a', class_='next page-numbers') is not None)
                    else:
                        raise Exception(f"HTTP status: {response.status_code}")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "results": results, "has_next": has_next}).encode())
            except Exception as e:
                add_log(f"Search exception: {str(e)}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
            return
            
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
                        raw_title = title_el.get_text(strip=True) if title_el else "Unknown Game"
                        title, version = clean_and_parse_title(raw_title)
                        
                        # Scrape sizes
                        text_all = soup.get_text()
                        orig_match = re.search(r'Original Size:\s*([^\n]+)', text_all, re.IGNORECASE)
                        repack_match = re.search(r'Repack Size:\s*([^\n]+)', text_all, re.IGNORECASE)
                        original_size = clean_size(orig_match.group(1)) if orig_match else "Unknown"
                        repack_size = clean_size(repack_match.group(1)) if repack_match else "Unknown"
                        
                        # Scrape cover image
                        cover_image = ""
                        content_el = soup.find('div', class_='entry-content')
                        if content_el:
                            img_el = content_el.find('img', class_='alignleft')
                            if img_el:
                                cover_image = img_el.get('src', '')
                            else:
                                img_el = content_el.find('img')
                                if img_el:
                                    cover_image = img_el.get('src', '')
                                    
                        if cover_image:
                            cover_image = clean_cover_url(urllib.parse.urljoin(url, cover_image))
                        
                        mirrors = []
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
                                        
                        if len(mirrors) > 3:
                            filtered = []
                            for m in mirrors:
                                m_name_lower = m["name"].lower()
                                m_url_lower = m["url"].lower()
                                if "datanodes" in m_name_lower or "datanodes" in m_url_lower or \
                                   "fuckingfast" in m_name_lower or "fuckingfast" in m_url_lower or \
                                   "multiupload" in m_name_lower or "multiup" in m_url_lower:
                                    filtered.append(m)
                            mirrors = filtered
                                        
                        # Scrape gameplay videos/trailers
                        videos = []
                        if content_el:
                            for iframe in content_el.find_all('iframe'):
                                src = iframe.get('src', '')
                                if "youtube" in src or "youtu.be" in src:
                                    if src.startswith('//'):
                                        src = 'https:' + src
                                    if src not in videos:
                                        videos.append(src)

                        # Extract description and screenshots
                        description = ""
                        screenshots = []
                        if content_el:
                            paragraphs = []
                            for p in content_el.find_all('p', recursive=True):
                                p_copy = BeautifulSoup(str(p), 'html.parser')
                                for br in p_copy.find_all('br'):
                                    br.replace_with('\n')
                                text = p_copy.get_text()
                                
                                cleaned_lines = []
                                for line in text.split('\n'):
                                    line = line.strip()
                                    if not line:
                                        continue
                                    line_lower = line.lower()
                                    if line_lower.endswith('.rar') or line_lower.endswith('.bin') or line_lower.endswith('.exe') or 'fitgirl-repacks' in line_lower:
                                        continue
                                    if any(token in line_lower for token in [
                                        "genres/tags:", "companies:", "languages:", "original size:", "repack size:", 
                                        "screenshots:", "discussion and", "download mirrors", "filehoster:", "repack features",
                                        "backwards compatibility", "game description", "if you experience", "repack notes",
                                        "show direct links", "magnet", "1337x", "rutor", "tapochek.net", "compatibl",
                                        "requires windows", "game updates", "unpack to", "run patch.bat", "patch", "update",
                                        "elamigos", "rune", "flt", "tenoke", "soundtrack"
                                    ]):
                                        continue
                                    cleaned_lines.append(line)
                                    
                                if cleaned_lines:
                                    p_text = " ".join(cleaned_lines)
                                    if len(p_text) > 40:
                                        paragraphs.append(p_text)
                                        if len(paragraphs) == 3:
                                            break
                            description = "\n\n".join(paragraphs)
                            
                            for a in content_el.find_all('a'):
                                href = a.get('href', '')
                                img = a.find('img')
                                img_src = img.get('src', '') if img else ''
                                for candidate in [href, img_src]:
                                    if not candidate:
                                        continue
                                    cand_lower = candidate.lower()
                                    if 'riotpixels.net/data/' in cand_lower:
                                        candidate = re.sub(r'\.(?:240p|400p)\.(?:jpg|jpeg|png)$', '', candidate, flags=re.IGNORECASE)
                                        cand_lower = candidate.lower()
                                    if cand_lower.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) or ('riotpixels.net/data/' in cand_lower and '.jpg' in cand_lower):
                                        if candidate not in screenshots and candidate != cover_image:
                                            screenshots.append(candidate)
                            screenshots = screenshots[:10]

                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True,
                            "type": "fitgirl_page",
                            "title": title,
                            "version": version,
                            "original_size": original_size,
                            "repack_size": repack_size,
                            "cover_image": cover_image,
                            "mirrors": mirrors,
                            "videos": videos,
                            "description": description,
                            "screenshots": screenshots
                        }).encode())
                        return
                    else:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch FitGirl page. HTTP Status: {response.status_code}"}).encode())
                        return

                # online-fix.me page URL (not the hoster URL)
                elif "online-fix.me" in url and "hosters.online-fix.me" not in url:
                    add_log(f"Scraping online-fix.me game page: {url}")
                    response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Parse title
                        title_el = soup.find('h1', id='news-title') or soup.find('h1')
                        raw_title = title_el.text.strip() if title_el else "Unknown Game"
                        title, version = clean_and_parse_title(raw_title)
                        
                        # Parse cover image
                        cover_image = ""
                        img_el = None
                        for img in soup.find_all('img'):
                            src = img.get('src', '')
                            alt = img.get('alt', '')
                            if "uploads/posts" in src and title.lower() in alt.lower():
                                img_el = img
                                break
                        if not img_el:
                            for img in soup.find_all('img'):
                                src = img.get('src', '')
                                if "uploads/posts" in src and "poster" in src:
                                    img_el = img
                                    break
                        if img_el:
                            cover_image = clean_cover_url(urllib.parse.urljoin(url, img_el.get('src', '')))
                            
                        # Find hoster URL
                        hoster_url = None
                        for a in soup.find_all('a', href=True):
                            href = a['href']
                            if "hosters.online-fix.me" in href:
                                hoster_url = href
                                break
                                
                        if not hoster_url:
                            self.send_response(400)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "Hoster link (hosters.online-fix.me) not found on the page."}).encode())
                            return
                            
                        # Fetch hoster page to parse mirrors
                        add_log(f"Fetching hosters page: {hoster_url}")
                        h_headers = {
                            "Referer": url
                        }
                        h_response = cf_requests.get(hoster_url, headers=h_headers, impersonate="chrome120", timeout=20, verify=False)
                        if h_response.status_code != 200:
                            self.send_response(500)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch hoster page. Status: {h_response.status_code}"}).encode())
                            return
                            
                        h_soup = BeautifulSoup(h_response.text, 'html.parser')
                        options_container = h_soup.find(id='optionsContainer') or h_soup.find(class_='options-container')
                        if not options_container:
                            self.send_response(500)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "No mirrors options container found on hosters page."}).encode())
                            return
                            
                        mirrors = []
                        options = options_container.find_all(class_='option')
                        for opt in options:
                            name = opt.text.strip()
                            encoded_url = f"online-fix-hoster:{hoster_url}?mirror={urllib.parse.quote(name)}&referer={urllib.parse.quote(url)}"
                            mirrors.append({
                                "name": name,
                                "url": encoded_url
                            })
                            
                        # Scrape gameplay videos/trailers
                        videos = []
                        for iframe in soup.find_all('iframe'):
                            src = iframe.get('src', '')
                            if "youtube" in src or "youtu.be" in src:
                                if src.startswith('//'):
                                    src = 'https:' + src
                                if src not in videos:
                                    videos.append(src)

                        # Extract description and screenshots
                        description = ""
                        screenshots = []
                        story = soup.find(class_='full-story-content')
                        if story:
                            text = story.get_text()
                            match = re.search(r'(?:Информация о игре:|Информация об игре:)\s*(.*?)(?=(?:Файлы для игры:|Как запускать:|Скачать с|1\.|$))', text, re.DOTALL | re.IGNORECASE)
                            if match:
                                description = match.group(1).strip()
                            # Online-Fix doesn't typically list screenshots in full-story-content,
                            # but we can check if there are any direct images inside the article content.
                            for img in story.find_all('img'):
                                img_src = img.get('src', '')
                                if img_src:
                                    img_url = urllib.parse.urljoin(url, img_src)
                                    img_url_lower = img_url.lower()
                                    if img_url_lower.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) and "poster" not in img_url_lower:
                                        if img_url not in screenshots and img_url != cover_image:
                                            screenshots.append(img_url)
                            screenshots = screenshots[:10]

                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True,
                            "type": "fitgirl_page",
                            "title": title,
                            "version": version,
                            "original_size": "Unknown",
                            "repack_size": "Unknown",
                            "cover_image": cover_image,
                            "mirrors": mirrors,
                            "videos": videos,
                            "description": description,
                            "screenshots": screenshots
                        }).encode())
                        return
                    else:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch online-fix page. Status: {response.status_code}"}).encode())
                        return

                # online-fix-hoster mirror files list resolution
                elif url.startswith("online-fix-hoster:"):
                    raw_path = url[len("online-fix-hoster:"):]
                    parsed = urllib.parse.urlparse(raw_path)
                    query = urllib.parse.parse_qs(parsed.query)
                    mirror_name = query.get("mirror", [""])[0]
                    referer = query.get("referer", [""])[0]
                    actual_hoster_url = parsed._replace(query="").geturl()
                    
                    add_log(f"Resolving online-fix mirror files: {mirror_name} from {actual_hoster_url}")
                    h_headers = {}
                    if referer:
                        h_headers["Referer"] = referer
                    response = cf_requests.get(actual_hoster_url, headers=h_headers, impersonate="chrome120", timeout=20, verify=False)
                    if response.status_code != 200:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch hoster page. Status: {response.status_code}"}).encode())
                        return
                        
                    soup = BeautifulSoup(response.text, 'html.parser')
                    options_container = soup.find(id='optionsContainer') or soup.find(class_='options-container')
                    if not options_container:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": "No options container found on hoster page."}).encode())
                        return
                        
                    matching_option = None
                    for opt in options_container.find_all(class_='option'):
                        if opt.text.strip().lower() == mirror_name.lower():
                            matching_option = opt
                            break
                            
                    if not matching_option:
                        self.send_response(400)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Mirror '{mirror_name}' not found on hosters page."}).encode())
                        return
                        
                    data_links_str = matching_option.get('data-links', '[]')
                    try:
                        links = json.loads(data_links_str)
                    except Exception as json_err:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to parse links JSON: {str(json_err)}"}).encode())
                        return
                        
                    files = []
                    for item in links:
                        filename = item.get("file_name", "")
                        direct_link = item.get("direct_link", "")
                        
                        if "pixeldrain.com/u/" in direct_link:
                            direct_link = direct_link.replace("pixeldrain.com/u/", "pixeldrain.com/api/file/")
                            
                        file_type = "game_part"
                        filename_lower = filename.lower()
                        if "setup" in filename_lower or filename_lower.endswith(".exe"):
                            file_type = "installer"
                        elif "optional" in filename_lower or "selective" in filename_lower or "language" in filename_lower or "lang" in filename_lower or any(lang in filename_lower for lang in ["russian", "english", "french", "german", "spanish", "chinese", "brazilian", "japanese", "korean", "polish", "mexican", "italian", "greek", "portuguese"]):
                            file_type = "lang_part"
                            
                        cached_size = sizes_cache.get(filename, 0)
                        files.append({
                            "filename": filename,
                            "url": direct_link,
                            "type": file_type,
                            "status": "waiting",
                            "progress": 0,
                            "downloaded": 0,
                            "size": cached_size,
                            "speed": 0,
                            "time_left": -1,
                            "error": ""
                        })
                        
                    prefill_part_sizes(files)
                    
                    title_el = soup.find(class_='game-name') or soup.find('title') or soup.find('h1')
                    title = title_el.text.strip() if title_el else "Online-Fix Game"
                    title = re.sub(r'^Online-Fix Hosters\s*\|\s*', '', title, flags=re.IGNORECASE)
                    title = re.sub(r'^Online-Fix Drive\s*\|\s*', '', title, flags=re.IGNORECASE)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "type": "files",
                        "title": title,
                        "files": files
                    }).encode())
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
                base_download_dir = data.get("base_download_dir", data.get("download_dir", "")).strip()
                files = data.get("files", [])
                active_mirror = data.get("active_mirror", "").strip()
                
                if not base_download_dir:
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
                
                provider_sub = safe_folder_name(active_mirror)
                if provider_sub:
                    computed_dir = os.path.join(base_download_dir, safe_folder_name(game_title), provider_sub)
                else:
                    computed_dir = os.path.join(base_download_dir, safe_folder_name(game_title))
                
                with state_lock:
                    state["game_title"] = game_title
                    state["base_download_dir"] = os.path.abspath(base_download_dir)
                    state["download_dir"] = os.path.abspath(computed_dir)
                    state["files"] = files
                    state["active_mirror"] = active_mirror
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
                state["base_download_dir"] = ""
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

        elif path == "/api/switch_provider":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                new_mirror = data.get("new_mirror", "").strip()
                files = data.get("files", [])
                delete_old = data.get("delete_old", False)
                
                if not new_mirror or not files:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "New mirror name and files are required."}).encode())
                    return
                
                was_running = False
                with state_lock:
                    if state["is_running"]:
                        was_running = True
                        state["should_stop"] = True
                        state["is_running"] = False
                
                import time
                for _ in range(50):
                    with state_lock:
                        if state["active_workers_count"] == 0:
                            break
                    time.sleep(0.1)
                
                with state_lock:
                    old_download_dir = state["download_dir"]
                    game_title = state["game_title"]
                    base_download_dir = state.get("base_download_dir", state["default_download_dir"])
                    if not base_download_dir:
                        base_download_dir = state["default_download_dir"]
                    
                    state["active_mirror"] = new_mirror
                    new_download_dir = os.path.abspath(os.path.join(base_download_dir, safe_folder_name(game_title), safe_folder_name(new_mirror)))
                    state["download_dir"] = new_download_dir
                    
                    if delete_old and old_download_dir and os.path.exists(old_download_dir) and old_download_dir != new_download_dir:
                        import shutil
                        try:
                            shutil.rmtree(old_download_dir)
                            add_log(f"Deleted old provider directory: {old_download_dir}")
                        except Exception as delete_err:
                            add_log(f"Warning: Failed to delete old directory: {str(delete_err)}")
                            
                    new_files_map = {f["filename"]: f for f in files}
                    updated_files = []
                    for f in state["files"]:
                        fn = f["filename"]
                        if fn in new_files_map:
                            new_info = new_files_map[fn]
                            f["url"] = new_info["url"]
                            f["status"] = "waiting"
                            f["downloaded"] = 0
                            f["progress"] = 0
                            if new_info.get("size", 0) > 0:
                                f["size"] = new_info["size"]
                        updated_files.append(f)
                    state["files"] = updated_files
                    
                    os.makedirs(new_download_dir, exist_ok=True)
                    state["should_stop"] = False
                    
                initialize_queue_on_disk()
                
                if was_running:
                    with state_lock:
                        state["is_running"] = True
                        workers_to_start = state["max_workers"]
                        add_log(f"Resuming download with new provider: {new_mirror}")
                        for _ in range(workers_to_start):
                            threading.Thread(target=download_worker, daemon=True).start()
                            
                add_log(f"Successfully switched provider to: {new_mirror}")
                
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

def start_server():
    server_address = ('127.0.0.1', 8000)
    httpd = ThreadingHTTPServer(server_address, APIRequestHandler)
    print("Web server running at http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    add_log("[SYSTEM] Server initialized in idle setup mode.")
    try:
        import os
        os.makedirs(os.path.join(os.getcwd(), "cover_cache"), exist_ok=True)
    except Exception:
        pass
    start_server()
