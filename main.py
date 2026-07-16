import os
import sys
import re
import json
import threading
import time
import urllib.parse
import webbrowser
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer

# Monkey patch requests to globally disable SSL verification (bypasses VPN/proxy SSL conflicts)
import requests
original_request = requests.Session.request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 15
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

# DNS-over-HTTPS fallback to bypass ISP/censor blocking (e.g. Vodafone CUII in Germany, RKN in Russia)
import socket
import urllib.parse
from curl_cffi import CurlOpt

BLOCK_IPS = {
    "139.7.146.129",  # Vodafone Germany / CUII
}

# Hosts that frequently fail local DNS / get censored — always pin via DoH RESOLVE
FORCE_DOH_HOSTS = {
    "paste.fitgirl-repacks.site",
    "fitgirl-repacks.site",
    "www.fitgirl-repacks.site",
}

_doh_cache = {}
original_getaddrinfo = socket.getaddrinfo

def resolve_doh(host):
    if not host or host.replace(".", "").isdigit():
        return host
    if host in _doh_cache:
        return _doh_cache[host]
    
    # Query DoH endpoints directly via their IP addresses to bypass local DNS resolution for the DNS service
    doh_queries = [
        ("https://1.1.1.1/dns-query", {"name": host, "type": "A"}, {"accept": "application/dns-json"}),
        ("https://8.8.8.8/resolve", {"name": host, "type": "A"}, {}),
        ("https://9.9.9.9:5053/dns-query", {"name": host, "type": "A"}, {"accept": "application/dns-json"}),
    ]
    for url, params, headers in doh_queries:
        try:
            r = requests.get(url, params=params, headers=headers or None, verify=False, timeout=5)
            data = r.json()
            if "Answer" in data:
                for ans in data["Answer"]:
                    if ans.get("type") == 1:  # A record
                        ip = ans.get("data")
                        if ip and not ip.startswith("0."):
                            _doh_cache[host] = ip
                            return ip
        except Exception:
            pass
    return None

def _needs_doh(host):
    if not host:
        return False
    if host in FORCE_DOH_HOSTS:
        return True
    try:
        res = original_getaddrinfo(host, 443)
        if res:
            first_ip = res[0][4][0]
            if first_ip in BLOCK_IPS:
                return True
        return False
    except Exception:
        return True

def _set_session_resolve(session, host, doh_ip):
    """
    curl_cffi 0.15 accepts curl_options only on Session (self.curl_options),
    NOT as a Session.request() keyword argument.
    """
    if not session or not host or not doh_ip:
        return
    if not hasattr(session, "curl_options") or session.curl_options is None:
        session.curl_options = {}
    # copy so we don't mutate a shared frozen dict
    opts = dict(session.curl_options)
    opts[CurlOpt.RESOLVE] = [f"{host}:443:{doh_ip}", f"{host}:80:{doh_ip}"]
    session.curl_options = opts

def patched_getaddrinfo(host, port, *args, **kwargs):
    if host in ("1.1.1.1", "8.8.8.8", "9.9.9.9", "cloudflare-dns.com", "dns.google"):
        return original_getaddrinfo(host, port, *args, **kwargs)

    if host in FORCE_DOH_HOSTS:
        doh_ip = resolve_doh(host)
        if doh_ip:
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (doh_ip, port or 0))]
        
    try:
        res = original_getaddrinfo(host, port, *args, **kwargs)
        if res:
            first_ip = res[0][4][0]
            if first_ip in BLOCK_IPS:
                doh_ip = resolve_doh(host)
                if doh_ip:
                    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (doh_ip, port or 0))]
        return res
    except Exception:
        doh_ip = resolve_doh(host)
        if doh_ip:
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (doh_ip, port or 0))]
        raise

socket.getaddrinfo = patched_getaddrinfo

# Monkey patch curl_cffi Session.request — set RESOLVE on session, never as request kwarg
original_cf_request = cf_requests.Session.request

def patched_cf_request(self, method, url, *args, **kwargs):
    # Guard: older code / callers may still pass curl_options into request()
    kwargs.pop("curl_options", None)

    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    
    if host and _needs_doh(host):
        doh_ip = resolve_doh(host)
        if doh_ip:
            _set_session_resolve(self, host, doh_ip)
                
    try:
        return original_cf_request(self, method, url, *args, **kwargs)
    except Exception as e:
        err_text = str(e).lower()
        if host and ("could not resolve" in err_text or "resolve host" in err_text or "getaddrinfo" in err_text or "curl: (6)" in err_text):
            # Bust cache and force a fresh DoH resolve on DNS failures
            _doh_cache.pop(host, None)
            doh_ip = resolve_doh(host)
            if doh_ip:
                _set_session_resolve(self, host, doh_ip)
                return original_cf_request(self, method, url, *args, **kwargs)
            raise Exception(
                f"Cannot resolve host '{host}'. Local DNS failed and DoH fallback found no IP. "
                f"Try another mirror, enable VPN/WARP, or check your network. Original: {e}"
            ) from e
        if host:
            doh_ip = resolve_doh(host)
            if doh_ip:
                _set_session_resolve(self, host, doh_ip)
                try:
                    return original_cf_request(self, method, url, *args, **kwargs)
                except Exception:
                    pass
        raise e

cf_requests.Session.request = patched_cf_request


class SafeList(list):
    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except IndexError:
            class DummyDict(dict):
                def __setitem__(self, key, value):
                    pass
                def get(self, key, default=None):
                    return super().get(key, default)
            return DummyDict()

# Global State
state = {
    "game_title": "",
    "files": SafeList(),
    "download_dir": "",
    "base_download_dir": "",
    "default_download_dir": "C:\\Games",
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
    "active_mirror": "",
    "warp_status": "checking",
    "warp_error_message": "",
    "pixeldrain_limit_reached": False,
    "gofile_proxy": False,
    "gdrive_accounts": [],
    "active_gdrive_account": "",
    "gdrive_session_cookies": {},
    "gdrive_client_id": "",
    "gdrive_client_secret": "",
    "original_size": ""
}

state_lock = threading.RLock()
extraction_lock = threading.Lock()
gdrive_oauth_lock = threading.Lock()

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

session_state_path = os.path.join(os.path.dirname(__file__), "session_state.json")

def save_session_state():
    try:
        with state_lock:
            serializable_files = []
            for f in state["files"]:
                serializable_files.append({
                    "filename": f["filename"],
                    "url": f["url"],
                    "type": f["type"],
                    "status": f["status"],
                    "progress": f["progress"],
                    "downloaded": f["downloaded"],
                    "size": f["size"],
                    "speed": f["speed"],
                    "time_left": f["time_left"],
                    "error": f.get("error", "")
                })
            data = {
                "game_title": state["game_title"],
                "files": serializable_files,
                "download_dir": state["download_dir"],
                "base_download_dir": state.get("base_download_dir", state["default_download_dir"]),
                "default_download_dir": state["default_download_dir"],
                "is_configured": state["is_configured"],
                "total_progress": state["total_progress"],
                "active_mirror": state["active_mirror"],
                "average_download_speed": state.get("average_download_speed", 5000000.0)
            }
        with open(session_state_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        add_log(f"[WARNING] Failed to save session state: {str(e)}")

def load_session_state():
    try:
        if os.path.exists(session_state_path):
            with open(session_state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            with state_lock:
                state["game_title"] = data.get("game_title", "")
                files_list = data.get("files", [])
                state["files"].clear()
                for f in files_list:
                    if f["status"] in ["downloading", "connecting"]:
                        f["status"] = "waiting"
                        f["speed"] = 0
                    state["files"].append(f)
                
                state["download_dir"] = data.get("download_dir", "")
                state["base_download_dir"] = data.get("base_download_dir", "")
                state["default_download_dir"] = data.get("default_download_dir", "C:\\Games")
                state["is_configured"] = data.get("is_configured", False)
                state["is_running"] = False
                state["total_progress"] = data.get("total_progress", 0)
                state["active_mirror"] = data.get("active_mirror", "")
                state["average_download_speed"] = data.get("average_download_speed", 5000000.0)
                state["original_size"] = data.get("original_size", state.get("original_size", ""))

                # Ensure path = base / Game / Cloud (per-provider folders)
                try:
                    gt = safe_folder_name(state.get("game_title") or "")
                    base = state.get("base_download_dir") or state.get("default_download_dir") or ""
                    mirror = safe_folder_name(state.get("active_mirror") or "")
                    if gt and base:
                        game_root = os.path.abspath(os.path.join(base, gt))
                        expected = os.path.join(game_root, mirror) if mirror else game_root
                        cur = os.path.abspath(state.get("download_dir") or "")
                        # If session pointed at flat game root but we have an active mirror → use mirror subfolder
                        if mirror and (not cur or cur == game_root or os.path.basename(cur) != mirror):
                            # keep if already under a different known provider subfolder matching basename
                            if cur and os.path.dirname(cur) == game_root and os.path.basename(cur):
                                pass  # already Game/Something — trust it
                            else:
                                state["download_dir"] = expected
                        elif not cur:
                            state["download_dir"] = expected
                except Exception:
                    pass
                
            add_log("[SYSTEM] Previous session state restored successfully.")
            # Immediately rebuild real progress from disk so UI island is accurate on startup
            if state.get("is_configured") and state.get("download_dir") and state.get("files"):
                try:
                    initialize_queue_on_disk()
                    save_session_state()
                    add_log(f"[SYSTEM] Download folder: {state['download_dir']}")
                except Exception as scan_err:
                    print(f"Disk progress scan after session load failed: {scan_err}")
    except Exception as e:
        print(f"Error loading session state: {e}")

gdrive_accounts_path = os.path.join(os.path.dirname(__file__), "gdrive_accounts.json")
def load_gdrive_accounts():
    if os.path.exists(gdrive_accounts_path):
        try:
            with open(gdrive_accounts_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                state["gdrive_accounts"] = data.get("accounts", [])
                state["active_gdrive_account"] = data.get("active_account", "")
                state["gdrive_session_cookies"] = data.get("session_cookies", {})
                state["gdrive_client_id"] = data.get("custom_client_id", "")
                state["gdrive_client_secret"] = data.get("custom_client_secret", "")
        except Exception:
            pass
load_gdrive_accounts()

def save_gdrive_accounts():
    try:
        with open(gdrive_accounts_path, "w", encoding="utf-8") as f:
            json.dump({
                "accounts": state["gdrive_accounts"],
                "active_account": state["active_gdrive_account"],
                "session_cookies": state["gdrive_session_cookies"],
                "custom_client_id": state.get("gdrive_client_id", ""),
                "custom_client_secret": state.get("gdrive_client_secret", "")
            }, f, indent=4)
    except Exception:
        pass

def get_gdrive_credentials():
    with state_lock:
        cid = state.get("gdrive_client_id", "").strip()
        csec = state.get("gdrive_client_secret", "").strip()
    if cid and csec:
        return cid, csec
    return RCLONE_CLIENT_ID, RCLONE_CLIENT_SECRET

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

def is_warp_available():
    import shutil
    warp_cli = shutil.which("warp-cli")
    if not warp_cli:
        std_path = r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe"
        if os.path.exists(std_path):
            warp_cli = std_path
    return warp_cli is not None

def get_effective_max_workers():
    with state_lock:
        if state.get("active_mirror") and "pixeldrain" in state["active_mirror"].lower():
            return 1
        if any("pixeldrain.com" in f.get("url", "") for f in state.get("files", [])):
            return 1
        return state.get("max_workers", 4)

def rotate_warp_ip():
    add_log("Attempting to rotate IP using Cloudflare WARP...")
    import shutil
    warp_cli = shutil.which("warp-cli")
    if not warp_cli:
        std_path = r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe"
        if os.path.exists(std_path):
            warp_cli = std_path
            
    if not warp_cli:
        add_log("WARP CLI not found in PATH or standard Program Files location. Please install Cloudflare WARP to enable automatic IP rotation.")
        return False
        
    try:
        add_log("WARP: Disconnecting...")
        subprocess.run([warp_cli, "disconnect"], capture_output=True, text=True, check=True)
        time.sleep(2)
        
        add_log("WARP: Reconnecting...")
        subprocess.run([warp_cli, "connect"], capture_output=True, text=True, check=True)
        
        # Wait up to 10 seconds for connection to be active
        for _ in range(10):
            time.sleep(1)
            status_res = subprocess.run([warp_cli, "status"], capture_output=True, text=True)
            if "Connected" in status_res.stdout:
                add_log("WARP: Reconnected successfully with a new IP!")
                return True
        add_log("WARP: Reconnection timed out.")
        return False
    except Exception as e:
        add_log(f"WARP: Failed to rotate IP: {e}")
        return False

def check_and_install_warp():
    """Checks if Cloudflare WARP is installed, and if not, attempts to download and install it silently."""
    add_log("Checking Cloudflare WARP status...")
    import shutil
    warp_cli = shutil.which("warp-cli")
    if not warp_cli:
        std_path = r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe"
        if os.path.exists(std_path):
            warp_cli = std_path
            
    if warp_cli:
        with state_lock:
            state["warp_status"] = "installed"
        add_log("Cloudflare WARP is installed and ready.")
        return True

    # If missing, try downloading and running silent install
    add_log("Cloudflare WARP not detected. Initializing silent installation...")
    with state_lock:
        state["warp_status"] = "installing"
        
    try:
        msi_url = "https://1111-releases.cloudflareclient.com/windows/Cloudflare_WARP_Release-x64.msi"
        temp_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "fg_warp")
        os.makedirs(temp_dir, exist_ok=True)
        msi_path = os.path.join(temp_dir, "warp.msi")
        
        add_log(f"Downloading WARP installer from {msi_url}...")
        r = requests.get(msi_url, stream=True, timeout=60, verify=False)
        r.raise_for_status()
        with open(msi_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=256*1024):
                if chunk:
                    f.write(chunk)
        add_log("Download complete. Triggering silent installation with administrator UAC privileges...")
        
        try:
            import ctypes
            # runas verb triggers UAC prompt in interactive sessions
            res_execute = ctypes.windll.shell32.ShellExecuteW(None, "runas", "msiexec", f'/i "{msi_path}" /qn /norestart', None, 1)
            add_log(f"UAC elevation request returned code: {res_execute}")
        except Exception as shell_err:
            add_log(f"ShellExecuteW elevation request failed: {shell_err}")
            res_execute = 0
            
        if res_execute > 32:
            add_log("UAC dialog triggered. Please approve the prompt if visible to allow installation.")
            # Wait up to 30 seconds, checking for warp-cli existence periodically
            installed_ok = False
            for check_sec in range(30):
                time.sleep(1)
                warp_cli = shutil.which("warp-cli")
                if not warp_cli and os.path.exists(r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe"):
                    warp_cli = r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe"
                if warp_cli:
                    installed_ok = True
                    break
        else:
            add_log("UAC elevation request denied or canceled by user.")
            installed_ok = False
            
        if installed_ok:
            with state_lock:
                state["warp_status"] = "installed"
            add_log("Cloudflare WARP silently installed successfully.")
            return True
        else:
            if res_execute <= 32:
                err_msg = "Cloudflare WARP not installed. Silent installation requires Administrator privileges (UAC prompt was denied or cancelled). You can click 'Skip & Continue' to run the app without automatic IP rotation."
            else:
                err_msg = "Silent installation failed. Please verify that you have Administrator privileges, approve the UAC prompt, or manually install Cloudflare WARP from: https://1111-releases.cloudflareclient.com/windows/Cloudflare_WARP_Release-x64.msi"
                
            add_log("Silent installation failed: WARP could not be installed.")
            with state_lock:
                state["warp_status"] = "error"
                state["warp_error_message"] = err_msg
            return False
            
    except Exception as e:
        err_msg = f"Failed to download or silently install WARP: {str(e)}"
        add_log(err_msg)
        with state_lock:
            state["warp_status"] = "error"
            state["warp_error_message"] = err_msg
        return False

def clear_pixeldrain_cookies():
    """Clears python requests default cookies and browser sqlite cookie databases to bypass session tracking."""
    add_log("Clearing Pixeldrain cookies and browser profile session state...")
    try:
        requests.cookies.clear()
    except Exception as e:
        add_log(f"Error clearing requests cookies: {e}")
        
    try:
        cf_requests.cookies.clear()
    except Exception:
        pass
        
    try:
        profile_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "scratch", "chrome_profile"))
        if os.path.exists(profile_dir):
            cookies_cleared = False
            for root, dirs, files in os.walk(profile_dir):
                for file in files:
                    if file.lower() in ["cookies", "cookies-journal", "cookies.sqlite"]:
                        try:
                            os.remove(os.path.join(root, file))
                            cookies_cleared = True
                        except Exception:
                            pass
            if cookies_cleared:
                add_log("Playwright browser cookies database files deleted successfully.")
    except Exception as e:
        add_log(f"Error clearing browser cookie database: {e}")

RCLONE_CLIENT_ID = "202264815644.apps.googleusercontent.com"
RCLONE_CLIENT_SECRET = "X4Z3ca8xfWDb1Voo-F9a7ZxJ"

class OAuthRedirectHandler(BaseHTTPRequestHandler):
    timeout = 3.0  # Socket read timeout to prevent browser pre-connect hangs
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(url_parsed.query)
        code = query.get("code", [""])[0]
        error = query.get("error", [""])[0]
        error_desc = query.get("error_description", [""])[0]
        
        if error:
            error_msg = f"Google OAuth Error: {error}"
            if error_desc:
                error_msg += f" - {error_desc}"
            self.server.captured_code = ""
            self.server.captured_error = error_msg
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authorization Failed</title>
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                        background: #040409; 
                        color: #fff; 
                        text-align: center; 
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    .card {{
                        background: rgba(18, 18, 32, 0.45);
                        border: 1px solid rgba(255, 55, 55, 0.2);
                        padding: 30px;
                        border-radius: 16px;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                        backdrop-filter: blur(20px);
                    }}
                    h1 {{ color: #ff5555; margin-top: 0; font-size: 1.5rem; }}
                    p {{ color: #8c8ca0; font-size: 0.9rem; margin-bottom: 0; }}
                </style>
                <script>
                    window.onload = function() {{
                        setTimeout(function() {{
                            try {{
                                window.open('', '_self', '');
                                window.close();
                            }} catch(e) {{}}
                        }}, 2500);
                    }}
                </script>
            </head>
            <body>
                <div class="card">
                    <h1>Authorization Failed</h1>
                    <p>{error_msg}</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            return
            
        self.server.captured_code = code
        self.server.captured_error = ""
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authorized</title>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                    background: #040409; 
                    color: #fff; 
                    text-align: center; 
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .card {
                    background: rgba(18, 18, 32, 0.45);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    padding: 30px;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(20px);
                }
                h1 { color: #2ecc71; margin-top: 0; font-size: 1.5rem; }
                p { color: #8c8ca0; font-size: 0.9rem; margin-bottom: 0; }
            </style>
            <script>
                window.onload = function() {
                try {
                    window.open('', '_self', '');
                    window.close();
                } catch(e) {}
                // Fallback if window.close is blocked
                setTimeout(function() {
                    var statusEl = document.getElementById("status");
                    if (statusEl) {
                        statusEl.innerText = "Authorized. You can close this tab now.";
                    }
                }, 500);
            }
            </script>
        </head>
        <body>
            <div class="card">
                <h1 id="status">Authorized Successfully</h1>
                <p>This tab can be closed.</p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

def start_auth_code_listener(timeout=60):
    """Starts a temporary HTTP server on 127.0.0.1:53683 to capture the Google OAuth code."""
    server_address = ('127.0.0.1', 53683)
    httpd = HTTPServer(server_address, OAuthRedirectHandler)
    httpd.captured_code = ""
    
    # We want to serve only 1 request, then close
    def run_server():
        try:
            httpd.handle_request()
        except Exception:
            pass
            
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if httpd.captured_code:
            break
        time.sleep(0.5)
        
    captured = httpd.captured_code
    httpd.server_close()
    return captured

# Global auth state (NOT in state dict to avoid JSON serialization issues)
_gdrive_pending_auth_httpd = None
_gdrive_pending_auth_code = ""
_gdrive_pending_auth_error = ""
_gdrive_copy_auth_httpd = None

def get_gdrive_auth_code_playwright(auth_url, email=None, force_visible=False):
    """
    Captures Google authorization code.
    
    Two strategies:
    - force_visible=True (Add Account): Opens the user's DEFAULT browser (Firefox/Chrome).
      User is already logged in → just clicks "Allow" → code captured via localhost redirect.
      Google trusts the system browser, no "unsafe browser" warnings.
    - force_visible=False (downloads): Uses headless Playwright with persistent profile.
      If Google session exists, auto-redirects silently. Otherwise returns None.
    """

    
    if force_visible:
        # === ADD ACCOUNT: Open in user's default browser ===
        add_log("GDrive: Opening Google authorization in your default browser...")
        add_log(f"GDrive: IF THE BROWSER DID NOT OPEN, MANUALLY OPEN THIS LINK: {auth_url}")
        
        httpd = None
        for bind_attempt in range(3):
            try:
                httpd = HTTPServer(('127.0.0.1', 53683), OAuthRedirectHandler)
                break
            except OSError as e:
                add_log(f"GDrive: Port 53683 busy (attempt {bind_attempt+1}): {e}")
                time.sleep(1.5)
        
        if not httpd:
            add_log("GDrive: Cannot bind port 53683.")
            return None
        
        httpd.captured_code = ""
        httpd.timeout = 900  # 15 minutes for user to log in
        
        # Start listener in background
        listener_thread = threading.Thread(
            target=lambda h=httpd: _safe_handle_request(h), daemon=True
        )
        listener_thread.start()
        
        # Open URL in user's default browser (Firefox/Chrome — where they're already logged in)
        import webbrowser
        webbrowser.open(auth_url)
        add_log("GDrive: Browser tab opened. Please authorize access to Google Drive.")
        
        # Wait for redirect to our listener
        start_time = time.time()
        while time.time() - start_time < 180:
            if httpd.captured_code:
                break
            time.sleep(0.5)
        
        captured = httpd.captured_code
        try:
            httpd.server_close()
        except Exception:
            pass
        
        if captured:
            add_log("GDrive: Authorization successful! Account linked.")
            return captured
        else:
            add_log("GDrive: Authorization timed out. Please try again.")
            return None
    
    else:
        # === DOWNLOADS: Try headless first, then system browser auto-redirect ===
        httpd = None
        for bind_attempt in range(3):
            try:
                httpd = HTTPServer(('127.0.0.1', 53683), OAuthRedirectHandler)
                break
            except OSError as e:
                add_log(f"GDrive: Port 53683 busy (attempt {bind_attempt+1}): {e}")
                time.sleep(1.5)
        
        if not httpd:
            add_log("GDrive: Cannot bind port 53683.")
            return None
        
        global _gdrive_copy_auth_httpd
        _gdrive_copy_auth_httpd = httpd
        
        httpd.captured_code = ""
        httpd.timeout = 900
        
        listener_thread = threading.Thread(
            target=lambda h=httpd: _safe_handle_request(h), daemon=True
        )
        listener_thread.start()
        
        # Skip headless Playwright because Google blocks sign-in on headless browsers.
        # We go straight to system browser auto-redirect which will run silently and instantly
        # since the user already gave consent in settings.
        pass
        
        # Attempt 2: Open in system browser (auto-redirect since consent already given)
        # User already gave consent during Add Account, so Google will auto-redirect
        # to 127.0.0.1:53683 without any interaction needed. Tab opens briefly and closes.
        add_log("GDrive: Silent auth failed. Trying system browser auto-redirect...")
        try:
            import subprocess
            import os
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, auth_url])
                add_log("GDrive: Opened Chrome directly for auto-redirect.")
            else:
                import webbrowser
                webbrowser.open(auth_url)
                add_log("GDrive: Opened system default browser for auto-redirect.")
        except Exception as e2:
            add_log(f"GDrive: Cannot open system browser: {e2}")
        
        # Wait for auto-redirect (should be 300 seconds now)
        start_time = time.time()
        while time.time() - start_time < 300:
            if httpd.captured_code:
                break
            # Check if active account was deleted or changed to prevent intercepting new account logins
            with state_lock:
                active = state.get("active_gdrive_account")
                if not active or not any(a["email"] == active for a in state.get("gdrive_accounts", [])):
                    add_log("GDrive: Active account was removed during authorization. Cancelling copy flow listener.")
                    break
            time.sleep(0.3)
        
        captured = httpd.captured_code
        try:
            httpd.server_close()
        except:
            pass
        
        _gdrive_copy_auth_httpd = None
        
        if captured:
            add_log("GDrive: Authorization via system browser successful!")
            return captured
        
        add_log("GDrive: All auth attempts failed. Please re-add your Google account in Settings.")
        return None

def _safe_handle_request(httpd):
    """Helper to safely handle HTTP requests on the OAuth listener in a loop to bypass browser pre-connect hangs."""
    import time
    httpd.timeout = 2.0
    start_time = time.time()
    while time.time() - start_time < 900:
        if getattr(httpd, "captured_code", "") or getattr(httpd, "captured_error", ""):
            break
        try:
            httpd.handle_request()
        except Exception:
            pass

def get_gdrive_account_details(access_token, existing_limit=16106127360, existing_usage=0, existing_name="Unknown Name", existing_email="Unknown Account", existing_photo=""):
    """Fetches user details and storage quota from Google APIs with robust fallback."""
    email = existing_email
    name = existing_name
    photo = existing_photo
    limit = existing_limit
    usage = existing_usage
    
    userinfo_success = False
    quota_success = False
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 1. Try Userinfo API for name, email, photo (independent quota, high rate limits)
    try:
        r_user = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers, timeout=10, verify=False)
        if r_user.status_code == 200:
            data = r_user.json()
            email = data.get("email", email)
            name = data.get("name", name)
            photo = data.get("picture", photo)
            userinfo_success = True
        else:
            add_log(f"GDrive: Userinfo API returned status {r_user.status_code}")
    except Exception as e:
        add_log(f"GDrive: Userinfo API exception: {e}")
        
    # 2. Try Drive About API for storage limits (often 403 rate-limited on public Client ID)
    try:
        if userinfo_success:
            # We already have user info, just get quota to minimize scope/fields payload size
            url = "https://www.googleapis.com/drive/v3/about"
            params = {"fields": "storageQuota(limit,usage)"}
            r_about = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
        else:
            url = "https://www.googleapis.com/drive/v3/about"
            params = {"fields": "user(displayName,emailAddress,photoLink),storageQuota(limit,usage)"}
            r_about = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
            
        if r_about.status_code == 200:
            data = r_about.json()
            if not userinfo_success:
                user_info = data.get("user", {})
                email = user_info.get("emailAddress", email)
                name = user_info.get("displayName", name)
                photo = user_info.get("photoLink", photo)
                userinfo_success = True
            
            quota = data.get("storageQuota", {})
            limit = int(quota.get("limit", limit))
            usage = int(quota.get("usage", usage))
            quota_success = True
        else:
            add_log(f"GDrive: Drive About API returned status {r_about.status_code} (likely rate limit). Using fallback limits.")
    except Exception as e:
        add_log(f"GDrive: Drive About API exception: {e}. Using fallback limits.")
        
    return {
        "success": userinfo_success or quota_success,
        "email": email,
        "name": name,
        "photo": photo,
        "limit": limit,
        "usage": usage
    }

def exchange_gdrive_code(auth_code):
    """Exchanges authorization code for Google Drive refresh token using Rclone credentials."""
    url = "https://oauth2.googleapis.com/token"
    client_id, client_secret = get_gdrive_credentials()
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "redirect_uri": "http://127.0.0.1:53683/",
        "grant_type": "authorization_code"
    }
    try:
        r = requests.post(url, data=payload, timeout=15, verify=False)
        r.raise_for_status()
        data = r.json()
        refresh_token = data.get("refresh_token")
        access_token = data.get("access_token")
        
        details = {"email": "Unknown Account", "name": "Unknown Name", "photo": "", "limit": 0, "usage": 0}
        if access_token:
            det_res = get_gdrive_account_details(access_token)
            if det_res.get("success", False):
                details = det_res
                
        return {
            "success": True,
            "email": details["email"],
            "name": details["name"],
            "photo": details["photo"],
            "limit": details["limit"],
            "usage": details["usage"],
            "refresh_token": refresh_token
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_gdrive_access_token(refresh_token):
    """Refreshes and returns a temporary access token for Google Drive API."""
    url = "https://oauth2.googleapis.com/token"
    client_id, client_secret = get_gdrive_credentials()
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    try:
        r = requests.post(url, data=payload, timeout=15, verify=False)
        r.raise_for_status()
        return r.json().get("access_token")
    except Exception as e:
        add_log(f"GDrive: Failed to refresh access token: {e}")
        return None

def find_gdrive_file(filename, access_token):
    """Queries user's Google Drive for a file with the given name."""
    url = "https://www.googleapis.com/drive/v3/files"
    escaped_filename = filename.replace("'", "\\'")
    params = {
        "q": f"name = '{escaped_filename}' and trashed = false",
        "fields": "files(id, name, size)"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15, verify=False)
        r.raise_for_status()
        files = r.json().get("files", [])
        if files:
            return files[0]
        return None
    except Exception as e:
        add_log(f"GDrive: Failed to search file {filename}: {e}")
        return None

def delete_gdrive_file(file_id, access_token):
    """Deletes a file by ID from the user's Google Drive."""
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        r = requests.delete(url, headers=headers, timeout=15, verify=False)
        if r.status_code in [200, 204]:
            add_log(f"GDrive: Successfully deleted file {file_id} from Google Drive.")
            return True
        else:
            add_log(f"GDrive: Delete returned status code {r.status_code}")
            return False
    except Exception as e:
        add_log(f"GDrive: Failed to delete file {file_id}: {e}")
        return False

_cached_working_proxy = None

def get_working_gofile_proxy():
    """Scrapes sslproxies.org and returns the first tested SSL proxy that successfully talks to the Gofile API."""
    global _cached_working_proxy
    if _cached_working_proxy:
        # Quick check if it is still alive
        test_proxies = {
            "http": f"http://{_cached_working_proxy}",
            "https": f"http://{_cached_working_proxy}"
        }
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            test_r = requests.post("https://api.gofile.io/accounts", headers=headers, proxies=test_proxies, timeout=4, verify=False)
            if test_r.status_code == 200:
                return _cached_working_proxy
        except Exception:
            _cached_working_proxy = None

    add_log("Searching for a working free SSL proxy for Gofile...")
    try:
        from bs4 import BeautifulSoup
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get("https://www.sslproxies.org/", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        proxies = []
        table = soup.find('table', class_='table') or soup.find('table')
        if table:
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    if ip.count('.') == 3 and port.isdigit():
                        proxies.append(f"{ip}:{port}")
                        
        add_log(f"Found {len(proxies)} SSL proxies. Testing against Gofile API...")
        for proxy in proxies[:15]:
            test_proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            try:
                test_r = requests.post("https://api.gofile.io/accounts", headers=headers, proxies=test_proxies, timeout=4, verify=False)
                if test_r.status_code == 200:
                    add_log(f"Proxy {proxy} successfully bypassed Gofile block!")
                    _cached_working_proxy = proxy
                    return proxy
            except Exception:
                pass
        add_log("No working free SSL proxy found for Gofile.")
        return None
    except Exception as e:
        add_log(f"Failed to scrape/test free proxies: {e}")
        return None

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
    # Check if we should use a proxy
    proxy_server = None
    if state.get("gofile_proxy", False):
        proxy_server = get_working_gofile_proxy()
        
    with extraction_lock:
        from playwright.sync_api import sync_playwright
        import os
        if proxy_server:
            add_log(f"Extracting Gofile direct link for: {page_url} via proxy {proxy_server}")
        else:
            add_log(f"Extracting Gofile direct link for: {page_url}")
        try:
            with sync_playwright() as p:
                launch_args = {
                    "headless": True,
                    "args": [
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                }
                if proxy_server:
                    launch_args["proxy"] = {"server": f"http://{proxy_server}"}
                    
                browser = p.chromium.launch(**launch_args)
                context = browser.new_context()
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
                                    link = cinfo.get("directLink") or cinfo.get("link")
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
                
                gofile_token = None
                try:
                    for cookie in context.cookies():
                        if cookie.get("name") == "accountToken":
                            gofile_token = cookie.get("value")
                            break
                    if not gofile_token:
                        gofile_token = page.evaluate("localStorage.getItem('accountToken')")
                except Exception:
                    pass
                if gofile_token:
                    with state_lock:
                        state["gofile_account_token"] = gofile_token
                    add_log("Gofile: Captured session token.")
                
                browser.close()
                
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
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                context = browser.new_context()
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
                
                browser.close()
                
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
            elif "gofile" in url_lower:
                f["size"] = 5 * 1024 * 1024 * 1024  # 5 GB for Gofile parts
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


def _strip_bonus_soundtrack_section(text):
    """Remove Included Bonus Soundtracks / OST dump from Game Description."""
    if not text:
        return text
    # Cut from soundtrack header to end (or next major section if any)
    patterns = [
        r"(?is)\n?\s*included\s+bonus\s+soundtracks?\s*:?\s*\n.*$",
        r"(?is)\n?\s*bonus\s+soundtracks?\s*:?\s*\n.*$",
        r"(?is)\n?\s*included\s+bonus\s+osts?\s*:?\s*\n.*$",
        r"(?is)\n?\s*включ[её]нные\s+бонусные\s+саундтреки\s*:?\s*\n.*$",
    ]
    out = text
    for pat in patterns:
        out = re.sub(pat, "", out)
    # Also drop trailing lone soundtrack-ish bullet lines if header was mid-block
    lines = out.split("\n")
    cleaned = []
    skip_mode = False
    for ln in lines:
        low = ln.strip().lower().rstrip(":")
        if re.match(
            r"^(included\s+)?bonus\s+(soundtracks?|osts?)|включ[её]нные\s+бонусные\s+саундтреки$",
            low,
        ):
            skip_mode = True
            continue
        if skip_mode:
            # stop skipping if a real new section starts
            if low in ("game features", "особенности игры", "pc features", "features") or (
                ln.strip().endswith(":") and len(ln.strip()) < 48 and "soundtrack" not in low
            ):
                skip_mode = False
                cleaned.append(ln)
            # otherwise drop OST bullets / names
            continue
        cleaned.append(ln)
    out = "\n".join(cleaned).strip()
    # Collapse excessive blank lines
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def _merge_folder_files(src_dir, dst_dir):
    """Move archive files from src_dir (recursively) into dst_dir (keep larger copy)."""
    import shutil
    if not src_dir or not dst_dir or not os.path.isdir(src_dir):
        return
    if os.path.abspath(src_dir) == os.path.abspath(dst_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    for root, _dirs, files in os.walk(src_dir):
        for name in files:
            low = name.lower()
            if not low.endswith((".rar", ".bin", ".zip", ".7z", ".exe", ".iso")):
                continue
            src = os.path.join(root, name)
            dst = os.path.join(dst_dir, name)
            try:
                if os.path.exists(dst):
                    if os.path.getsize(src) > os.path.getsize(dst):
                        os.replace(src, dst)
                    else:
                        try:
                            os.remove(src)
                        except Exception:
                            pass
                else:
                    shutil.move(src, dst)
            except Exception:
                pass
    # prune empty dirs under src
    for root, dirs, files in os.walk(src_dir, topdown=False):
        for d in dirs:
            p = os.path.join(root, d)
            try:
                if not os.listdir(p):
                    os.rmdir(p)
            except Exception:
                pass


def _consolidate_provider_subfolders(game_dir):
    """Merge legacy per-mirror subfolders (Rootz/Gofile/FileDitch/…) into game_dir.

    Older builds saved as:  C:\\Games\\Game\\Rootz\\part01.rar
    New layout is flat:     C:\\Games\\Game\\part01.rar
    """
    if not game_dir:
        return
    game_dir = os.path.abspath(game_dir)
    os.makedirs(game_dir, exist_ok=True)

    # 1) Subfolders inside the game dir
    try:
        for name in list(os.listdir(game_dir)):
            sub = os.path.join(game_dir, name)
            if not os.path.isdir(sub):
                continue
            # Skip obvious non-provider dirs (extracted game content later)
            if name.lower() in ("_redist", "redist", "crack", "support"):
                continue
            # Only consolidate if it looks like a hoster dump (has .rar/.bin)
            try:
                entries = os.listdir(sub)
            except Exception:
                continue
            if not any(
                e.lower().endswith((".rar", ".bin", ".zip", ".7z", ".exe"))
                for e in entries
            ):
                continue
            _merge_folder_files(sub, game_dir)
            try:
                if not os.listdir(sub):
                    os.rmdir(sub)
            except Exception:
                pass
    except Exception:
        pass

    # 2) Sibling typos like "Forza Horizon 6 Gofile" next to "Forza Horizon 6"
    parent = os.path.dirname(game_dir)
    base = os.path.basename(game_dir)
    if parent and base and os.path.isdir(parent):
        try:
            for name in os.listdir(parent):
                if name == base:
                    continue
                # "Game Title Gofile" / "Game Title - Rootz"
                if not name.startswith(base):
                    continue
                suffix = name[len(base):].strip(" -_")
                if not suffix:
                    continue
                sibling = os.path.join(parent, name)
                if os.path.isdir(sibling):
                    _merge_folder_files(sibling, game_dir)
                    try:
                        if not os.listdir(sibling):
                            os.rmdir(sibling)
                    except Exception:
                        pass
        except Exception:
            pass


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def initialize_queue_on_disk():
    """Scan download folder and rebuild accurate progress for the floating bar / UI."""
    with state_lock:
        if not state["download_dir"]:
            return
        try:
            os.makedirs(state["download_dir"], exist_ok=True)
        except Exception:
            return
        for f in state["files"]:
            # Restore expected size from sizes_cache when session lost it
            if (not f.get("size") or f["size"] <= 0) and f.get("filename") in sizes_cache:
                try:
                    f["size"] = int(sizes_cache[f["filename"]])
                except Exception:
                    pass

            file_path = os.path.join(state["download_dir"], f["filename"])
            if os.path.exists(file_path):
                try:
                    size_on_disk = os.path.getsize(file_path)
                except Exception:
                    size_on_disk = 0
                expected_size = f["size"] if f.get("size", 0) > 0 else get_expected_size(f["filename"], f.get("type", "game_part"))
                if expected_size <= 0:
                    expected_size = size_on_disk
                f["downloaded"] = size_on_disk
                f["size"] = max(int(expected_size or 0), size_on_disk)
                if f["size"] > 0:
                    f["progress"] = min(100, int((size_on_disk / f["size"]) * 100))
                else:
                    f["progress"] = 0
                # Treat complete / nearly complete as finished
                if f["size"] > 0 and size_on_disk >= f["size"] * 0.995:
                    f["status"] = "finished"
                    f["progress"] = 100
                    f["speed"] = 0
                    save_size_to_cache(f["filename"], f["size"])
                elif f.get("status") == "finished" and size_on_disk < f["size"] * 0.995:
                    # File incomplete but was marked finished — resume-ready
                    f["status"] = "waiting"
                    f["speed"] = 0
            else:
                # No file on disk
                if f.get("status") == "finished":
                    f["status"] = "waiting"
                if f.get("status") in ("downloading", "connecting"):
                    f["status"] = "waiting"
                f["downloaded"] = 0
                f["progress"] = 0
                f["speed"] = 0
        recalculate_total_progress()
        add_log(
            f"[SYSTEM] Disk scan: {state['total_progress']}% "
            f"({sum(1 for x in state['files'] if x.get('status')=='finished')}/{len(state['files'])} files done)"
        )

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
                if state["should_stop"] or not state["is_running"] or state["active_workers_count"] > get_effective_max_workers():
                    break
                    
                target_idx = -1
                for idx, f in enumerate(state["files"]):
                    if f["status"] == "waiting":
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

def extract_gdrive_id(text):
    if not text:
        return None
    # Matches id=FILE_ID or d/FILE_ID or /d/FILE_ID
    match = re.search(r'(?:id=|/d/|d/)([A-Za-z0-9_-]{25,})', text)
    if match:
        return match.group(1)
    return None

def download_file(index, file_info):
    filename = file_info["filename"]
    page_url = file_info["url"]
    file_path = os.path.join(state["download_dir"], filename)
    
    file_id = None
    access_token = None
    account = None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    with state_lock:
        if index < len(state["files"]):
            state["files"][index]["status"] = "connecting"
            state["files"][index]["error"] = ""
        
    add_log(f"Starting download for {filename}...")
    
    # Step 1: Extract direct download link based on hoster
    if "fuckingfast.co" in page_url:
        direct_link = extract_direct_link(page_url)
        if not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Could not bypass Cloudflare for FuckingFast."
            return False
    elif "datanodes.to" in page_url:
        direct_link = extract_datanodes_link(page_url)
        if not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Could not extract direct link for DataNodes."
            return False
    elif "fileditchfiles.me" in page_url or "fileditch.com" in page_url:
        direct_link = extract_fileditch_link(page_url)
        if not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Could not extract direct link for FileDitch."
            return False
    elif "gofile.io" in page_url:
        direct_link = extract_gofile_link(page_url)
        if not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Could not extract direct link for Gofile."
            return False
        elif direct_link == "ERROR_NOT_PREMIUM":
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Gofile: Free accounts cannot download this folder. Premium account required."
            return False
        elif direct_link == "ERROR_NOT_FOUND":
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Gofile: File not found (404)."
            return False
        elif direct_link == "ERROR_BLOCKED":
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Gofile: Connection timed out. Gofile may be blocked on your network (e.g. university firewall). Try enabling a VPN."
            return False
    elif "rootz.so" in page_url or "rootz.cc" in page_url:
        direct_link = extract_rootz_link(page_url)
        if direct_link == "ERROR_NOT_FOUND" or not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Rootz: File not found (404)."
            return False
    elif "vikingfile.com" in page_url or "vik1ngfile.site" in page_url:
        direct_link = extract_viking_link(page_url)
        if direct_link == "ERROR_CAPTCHA_REQUIRED" or not direct_link:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "VikingFile: Captcha verification required."
            return False
    elif "drive.online-fix.me" in page_url and "/download/" in page_url:
        with state_lock:
            active_account = state.get("active_gdrive_account")
            accounts = state.get("gdrive_accounts", [])
            
        if not active_account:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "No Google Drive account configured in settings."
            return False
            
        account = next((a for a in accounts if a["email"] == active_account), None)
        if not account:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = f"Active Google account '{active_account}' not found."
            return False
            
        access_token = get_gdrive_access_token(account["refresh_token"])
        if not access_token:
            with state_lock:
                if index < len(state["files"]):
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Failed to refresh Google Drive access token."
            return False
            
        # Try to find file first, but ignore rate limits if it fails
        file_metadata = find_gdrive_file(filename, access_token)
        if file_metadata:
            file_id = file_metadata["id"]
            add_log(f"Found existing copy on Google Drive: {filename} (ID: {file_id})")
        else:
            post_headers = {
                "Referer": "https://online-fix.me/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            copied = False
            quota_error = False
            active_email = account["email"]
            
            # Step A: Attempt to copy using cached cookies for active account
            with state_lock:
                cookies_dict = state.get("gdrive_session_cookies", {})
                if not isinstance(cookies_dict, dict):
                    cookies_dict = {}
                session_cookies = dict(cookies_dict.get(active_email, {}))
                
            if session_cookies:
                add_log(f"Attempting to copy {filename} using cached session cookies for {active_email}...")
                try:
                    res = requests.post(page_url, headers=post_headers, cookies=session_cookies, data={"api_key": ""}, timeout=20, verify=False)
                    if res.status_code == 200:
                        res_data = res.json()
                        if res_data.get("success", False):
                            add_log(f"Online-Fix copy request successful using cached cookies: {res_data.get('message', '')}")
                            # Extract file ID directly from message / response keys to bypass Search API limits
                            file_id = res_data.get("id", "")
                            if not file_id:
                                file_id = extract_gdrive_id(res_data.get("message", ""))
                            if not file_id and res_data.get("url"):
                                file_id = extract_gdrive_id(res_data["url"])
                            
                            with state_lock:
                                if "gdrive_session_cookies" not in state or not isinstance(state["gdrive_session_cookies"], dict):
                                    state["gdrive_session_cookies"] = {}
                                if active_email not in state["gdrive_session_cookies"] or not isinstance(state["gdrive_session_cookies"][active_email], dict):
                                    state["gdrive_session_cookies"][active_email] = {}
                                state["gdrive_session_cookies"][active_email].update(res.cookies.get_dict())
                            save_gdrive_accounts()
                            copied = True
                        else:
                            msg = res_data.get("message", "")
                            if any(x in msg.lower() for x in ["unknown error", "quota", "limit", "google drive"]):
                                add_log(f"GDrive copy failed (non-auth error): {msg}")
                                with state_lock:
                                    if index < len(state["files"]):
                                        state["files"][index]["status"] = "failed"
                                        state["files"][index]["error"] = f"GDrive copy limit: {msg}"
                                quota_error = True
                except Exception as e:
                    add_log(f"Cache copy attempt failed for {filename}: {str(e)}")
                    
            if not copied and not quota_error:
                # Step B: Lock OAuth flow so only 1 thread opens browser
                with gdrive_oauth_lock:
                    # Double-check if cookies were populated while we were waiting for the lock
                    with state_lock:
                        cookies_dict = state.get("gdrive_session_cookies", {})
                        if not isinstance(cookies_dict, dict):
                            cookies_dict = {}
                        session_cookies = dict(cookies_dict.get(active_email, {}))
                        
                    if session_cookies:
                        add_log(f"Attempting copy for {filename} with cookies updated by another worker...")
                        try:
                            res = requests.post(page_url, headers=post_headers, cookies=session_cookies, data={"api_key": ""}, timeout=20, verify=False)
                            if res.status_code == 200:
                                res_data = res.json()
                                if res_data.get("success", False):
                                    add_log(f"Online-Fix copy request successful using newly cached cookies: {res_data.get('message', '')}")
                                    # Extract file ID directly from message / response keys
                                    file_id = res_data.get("id", "")
                                    if not file_id:
                                        file_id = extract_gdrive_id(res_data.get("message", ""))
                                    if not file_id and res_data.get("url"):
                                        file_id = extract_gdrive_id(res_data["url"])
                                    
                                    with state_lock:
                                        if "gdrive_session_cookies" not in state or not isinstance(state["gdrive_session_cookies"], dict):
                                            state["gdrive_session_cookies"] = {}
                                        if active_email not in state["gdrive_session_cookies"] or not isinstance(state["gdrive_session_cookies"][active_email], dict):
                                            state["gdrive_session_cookies"][active_email] = {}
                                        state["gdrive_session_cookies"][active_email].update(res.cookies.get_dict())
                                        save_gdrive_accounts()
                                    copied = True
                                else:
                                    msg = res_data.get("message", "")
                                    if any(x in msg.lower() for x in ["unknown error", "quota", "limit", "google drive"]):
                                        add_log(f"GDrive copy failed (non-auth error inside lock): {msg}")
                                        with state_lock:
                                            if index < len(state["files"]):
                                                state["files"][index]["status"] = "failed"
                                                state["files"][index]["error"] = f"GDrive copy limit: {msg}"
                                        quota_error = True
                        except Exception as e:
                            add_log(f"Copy with newly cached cookies failed: {str(e)}")
                            
                    if not copied and not quota_error:
                        add_log(f"Initiating copy flow to your Google Drive for {filename}...")
                        
                        client_id = RCLONE_CLIENT_ID
                        redirect_uri = "http://127.0.0.1:53683/"
                        # Only request the drive scope as required by Rclone and Online-Fix
                        scope = "https://www.googleapis.com/auth/drive"
                        auth_url = (
                            f"https://accounts.google.com/o/oauth2/v2/auth?"
                            f"client_id={client_id}&"
                            f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
                            f"response_type=code&"
                            f"scope={urllib.parse.quote(scope)}&"
                            f"access_type=offline&"
                            f"login_hint={urllib.parse.quote(account['email'])}"
                        )
                        
                        add_log("GDrive: Requesting Google authorization code...")
                        add_log(f"GDrive: IF THE BROWSER DID NOT OPEN, MANUALLY OPEN THIS LINK: {auth_url}")
                        auth_code = get_gdrive_auth_code_playwright(auth_url, account["email"])
                        if not auth_code:
                            with state_lock:
                                if index < len(state["files"]):
                                    state["files"][index]["status"] = "failed"
                                    state["files"][index]["error"] = "Google authorization timed out or cancelled by user."
                            return False
                            
                        add_log("Establishing session cookie on Online-Fix Drive server...")
                        try:
                            # A GET request to the public folder page establishes the online_fix_auth cookie
                            with state_lock:
                                game_title = state.get("game_title", "")
                            folder_name = urllib.parse.quote(game_title)
                            folder_url = f"https://drive.online-fix.me:2053/{folder_name}"
                            res_get = requests.get(folder_url, headers=post_headers, timeout=20, verify=False)
                            fresh_cookies = res_get.cookies.get_dict()
                            if fresh_cookies and "online_fix_auth" in fresh_cookies:
                                with state_lock:
                                    if "gdrive_session_cookies" not in state or not isinstance(state["gdrive_session_cookies"], dict):
                                        state["gdrive_session_cookies"] = {}
                                    state["gdrive_session_cookies"][active_email] = fresh_cookies
                                    save_gdrive_accounts()
                        except Exception as e:
                            add_log(f"Warning: Failed to establish fresh session cookie: {str(e)}")
                            fresh_cookies = {}
                            
                        add_log("Sending authorization key to Online-Fix Drive server...")
                        post_data = {
                            "api_key": auth_code
                        }
                        try:
                            res = requests.post(page_url, headers=post_headers, cookies=fresh_cookies, data=post_data, timeout=20, verify=False)
                            if res.status_code != 200:
                                with state_lock:
                                    if index < len(state["files"]):
                                        state["files"][index]["status"] = "failed"
                                        state["files"][index]["error"] = f"Online-Fix copy request failed with status code {res.status_code}."
                                return False
                                
                            res_data = res.json()
                            if not res_data.get("success", False):
                                msg = res_data.get("message", "Copy request rejected by Online-Fix.")
                                with state_lock:
                                    if index < len(state["files"]):
                                        state["files"][index]["status"] = "failed"
                                        state["files"][index]["error"] = f"Online-Fix error: {msg}"
                                return False
                                
                            add_log(f"Online-Fix copy request successful: {res_data.get('message', '')}")
                            
                            # Extract file ID directly from message / response keys
                            file_id = res_data.get("id", "")
                            if not file_id:
                                file_id = extract_gdrive_id(res_data.get("message", ""))
                            if not file_id and res_data.get("url"):
                                file_id = extract_gdrive_id(res_data["url"])
                            
                            # Cache the authorized cookies specifically for this active email account
                            with state_lock:
                                if "gdrive_session_cookies" not in state or not isinstance(state["gdrive_session_cookies"], dict):
                                    state["gdrive_session_cookies"] = {}
                                # Combine fresh_cookies and cookies returned in POST response
                                final_cookies = dict(fresh_cookies)
                                final_cookies.update(res.cookies.get_dict())
                                state["gdrive_session_cookies"][active_email] = final_cookies
                            save_gdrive_accounts()
                                
                        except Exception as e:
                            with state_lock:
                                if index < len(state["files"]):
                                    state["files"][index]["status"] = "failed"
                                    state["files"][index]["error"] = f"Failed to contact Online-Fix server: {str(e)}"
                            return False
                            
            if not file_id:
                add_log("Waiting for the file to appear in your Google Drive (polling)...")
                for attempt in range(15):
                    time.sleep(3)
                    file_metadata = find_gdrive_file(filename, access_token)
                    if file_metadata:
                        file_id = file_metadata["id"]
                        add_log(f"File discovered on Google Drive: {filename} (ID: {file_id})")
                        break
                    
            if not file_id:
                with state_lock:
                    if index < len(state["files"]):
                        state["files"][index]["status"] = "failed"
                        state["files"][index]["error"] = "File copy timed out or could not be found on Google Drive."
                return False
                
        direct_link = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        headers["Authorization"] = f"Bearer {access_token}"
    else:
        direct_link = page_url
        
    # Attach Gofile account token cookie if available
    if "gofile.io" in page_url or (direct_link and "gofile.io" in direct_link):
        gofile_token = state.get("gofile_account_token")
        if gofile_token:
            headers["Cookie"] = f"accountToken={gofile_token}"
        
    resume_byte = 0
    if os.path.exists(file_path):
        resume_byte = os.path.getsize(file_path)
        add_log(f"Local file found: {filename}. Size: {resume_byte} bytes.")
        
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
        save_session_state()
        return True
        
    downloaded = resume_byte
    low_speed_seconds = 0
    last_low_speed_warning_time = 0
    proxy_server = None
    
    # If using proxy for Gofile:
    if "gofile.io" in page_url and state.get("gofile_proxy", False):
        proxy_server = get_working_gofile_proxy()
        
    while True:
        # Prepare headers & mode
        if downloaded > 0:
            headers["Range"] = f"bytes={downloaded}-"
            mode = "ab"
            add_log(f"Attempting resume/reconnect from byte {downloaded} for {filename}...")
        else:
            if "Range" in headers:
                del headers["Range"]
            mode = "wb"
            add_log(f"Starting download from scratch for {filename}...")
            
        if "Authorization" in headers and "drive.online-fix.me" in page_url and account:
            access_token = get_gdrive_access_token(account["refresh_token"])
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"
            
        proxies = None
        if proxy_server:
            proxies = {
                "http": f"http://{proxy_server}",
                "https": f"http://{proxy_server}"
            }
            
        try:
            response = requests.get(direct_link, headers=headers, stream=True, timeout=30, proxies=proxies)
            
            # Check for Pixeldrain download limit reached (402/429 or 403 with limit error)
            is_limit = False
            is_concurrent_limit = False
            if "pixeldrain.com" in direct_link:
                if response.status_code in [402, 429]:
                    is_limit = True
                elif response.status_code == 403:
                    try:
                        body_snippet = response.content[:500].decode("utf-8", errors="replace")
                        body_snippet_lower = body_snippet.lower()
                        if "max_concurrent_downloads" in body_snippet_lower or "open download connections" in body_snippet_lower:
                            is_concurrent_limit = True
                        elif any(x in body_snippet_lower for x in ["limit", "exceeded", "quota", "too many", "payment"]):
                            is_limit = True
                    except:
                        pass
                        
            if is_concurrent_limit:
                add_log(f"[INFO] Pixeldrain: Connection limit reached for {filename}. Waiting 5 seconds before retry...")
                response.close()
                time.sleep(5)
                continue
                
            if is_limit:
                add_log("[WARNING] Pixeldrain Daily Bandwidth Limit Reached (6 GB exceeded)!")
                with state_lock:
                    state["pixeldrain_limit_reached"] = True
                add_log("Attempting automatic IP rotation via WARP...")
                response.close()
                clear_pixeldrain_cookies()
                if rotate_warp_ip():
                    add_log("WARP IP rotated successfully. Retrying connection...")
                    time.sleep(2)
                    continue
                else:
                    add_log("WARP IP rotation failed or unavailable.")
                    with state_lock:
                        if index < len(state["files"]):
                            state["files"][index]["status"] = "failed"
                            state["files"][index]["error"] = "Pixeldrain Daily Limit (6 GB) Reached. Please enable VPN / WARP or wait."
                    return False
                    
            if response.status_code not in [200, 206]:
                if response.status_code == 416:
                    add_log(f"File {filename} appears to be fully downloaded (HTTP 416).")
                    break
                response.close()
                add_log(f"Download request failed with HTTP code: {response.status_code}")
                with state_lock:
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = f"HTTP Error {response.status_code}"
                return False
                
            # Check if we accidentally downloaded an HTML page instead of binary data
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type:
                response.close()
                add_log(f"Error: Server returned HTML page instead of binary stream for {filename}.")
                with state_lock:
                    state["files"][index]["status"] = "failed"
                    state["files"][index]["error"] = "Bypass failed: server returned HTML page."
                return False
                
            if response.status_code == 200:
                if downloaded > 0:
                    add_log(f"Server did not support range resume for {filename}. Restarting from scratch.")
                    downloaded = 0
                    mode = "wb"
                    
            with state_lock:
                state["files"][index]["status"] = "downloading"
                if total_size <= 0:
                    try:
                        sz = int(response.headers.get('content-length', 0))
                        if sz > 0:
                            total_size = sz + downloaded
                            state["files"][index]["size"] = total_size
                            save_size_to_cache(filename, total_size)
                    except Exception:
                        pass
                else:
                    state["files"][index]["size"] = total_size
                    
            chunk_size = 256 * 1024
            last_time = time.time()
            bytes_in_sec = 0
            throttled_trigger = False
            
            with open(file_path, mode) as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    with state_lock:
                        if state["should_stop"]:
                            response.close()
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
                            progress = min(100, int((downloaded / total_size) * 100)) if total_size > 0 else 0
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
                            
                            # Speed drop monitoring for Pixeldrain
                            if "pixeldrain.com" in direct_link:
                                # We check if speed is under 1.15 MB/s (to catch the 1.05 MB/s throttle limit)
                                if speed < 1150 * 1024:
                                    low_speed_seconds += int(elapsed)
                                    if low_speed_seconds >= 15:
                                        curr_time = time.time()
                                        if curr_time - last_low_speed_warning_time > 300: # 5 minutes cooldown
                                            last_low_speed_warning_time = curr_time
                                            add_log(f"[WARNING] Pixeldrain: Low download speed detected ({speed/1024:.1f} KB/s). Daily limit may be reached (throttled to 1 MB/s).")
                                            
                                            with state_lock:
                                                state["pixeldrain_limit_reached"] = True
                                                    
                                        if is_warp_available():
                                            add_log("Triggering IP auto-rotation via Cloudflare WARP...")
                                            throttled_trigger = True
                                            break
                                else:
                                    low_speed_seconds = 0
                                    
                            bytes_in_sec = 0
                            last_time = curr_time
                            
            response.close()
            
            if throttled_trigger:
                clear_pixeldrain_cookies()
                if rotate_warp_ip():
                    add_log("WARP IP rotated. Reconnecting download...")
                    time.sleep(2)
                    low_speed_seconds = 0
                    continue
                else:
                    add_log("WARP IP rotation failed during active throttling. Continuing at throttled speed...")
                    low_speed_seconds = 0
                    
            break
            
        except Exception as e:
            add_log(f"Download connection error for {filename}: {e}. Retrying in 2 seconds...")
            time.sleep(2)
            
    if downloaded == 0:
        add_log(f"Error: Downloaded 0 bytes for {filename}.")
        with state_lock:
            state["files"][index]["status"] = "failed"
            state["files"][index]["error"] = "Downloaded 0 bytes. Connection failed or direct link expired."
        save_session_state()
        return False
        
    if file_id and "drive.online-fix.me" in page_url and access_token:
        add_log(f"GDrive: Automatically deleting temporary copy {filename} from Google Drive...")
        delete_gdrive_file(file_id, access_token)
        
    add_log(f"Successfully downloaded {filename}.")
    save_session_state()
    return True

def recalculate_total_progress():
    """Calculates overall progress across all selected files."""
    with state_lock:
        if not state["files"]:
            state["total_progress"] = 0
            state["active_index"] = -1
            return
        total_bytes = 0
        downloaded_bytes = 0
        for f in state["files"]:
            size = f["size"] if f["size"] > 0 else get_expected_size(f["filename"], f["type"])
            total_bytes += size
            # Finished parts always count as fully downloaded (disk may already have full file)
            if f.get("status") == "finished":
                downloaded_bytes += size
            else:
                downloaded_bytes += f.get("downloaded", 0) or 0
        state["total_progress"] = int((downloaded_bytes / total_bytes) * 100) if total_bytes > 0 else 0
        
        active_idx = -1
        for idx, f in enumerate(state["files"]):
            if f["status"] in ["connecting", "downloading", "copying"]:
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
    
    # Strip suffixes like "+ Windows 7 Fix", "+ 6 GB VRAM Bypass", "+ Unlocker", "+ Bypass", "+ Fix"
    title = re.sub(r'\+\s*(?:\d+\s*GB\s*)?(?:Windows\s*7\s*Fix|VRAM\s*Bypass|Bypass|Unlocker|Hotfix|Multiplayer|Fix|Patch|Crack|Offline|Update|Bonus\s*OST|OST|Soundtrack|Bonus|Content)\b.*', '', title, flags=re.IGNORECASE)
    
    # Strip edition suffixes like Deluxe Edition, Gold Edition, Ultimate, etc.
    title = re.sub(r'[\s:–—\-]+(?:digital\s+)?(?:deluxe|ultimate|premium|standard|limited|gold|complete|special)\s+edition\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[\s:–—\-]+(?:digital\s+)?(?:deluxe|ultimate|premium|standard|limited|gold|complete|special)\b', '', title, flags=re.IGNORECASE)
    # Strip DLC suffixes like + 3 DLCs/Bonuses, + All DLCs, OST, etc.
    title = re.sub(r'\+\s*(?:\d+\s*|All\s+)?(?:DLCs?|Bonuses?|OST|Soundtracks?|Music|Bonus|Extras?)(?:\s*(?:/|\+|and)\s*(?:\d+\s*|All\s+)?(?:DLCs?|Bonuses?|OST|Soundtracks?|Music|Bonus|Extras?))*\b', '', title, flags=re.IGNORECASE)
    # Clean empty parenthesis/brackets
    title = re.sub(r'\(\s*\)', '', title)
    title = re.sub(r'\[\s*\]', '', title)
    title = re.sub(r'^[\s,\+\-–—]+|[\s,\+\-–—]+$', '', title).strip()
    title = re.sub(r'\s+', ' ', title)
    return title, version

def fetch_steam_metadata(game_title):
    import urllib.request, urllib.parse, json, re
    # Clean the title slightly to improve search match
    search_query = game_title
    # Replace common unicode replacements and curly quotes
    search_query = search_query.replace('\ufffd', "'").replace('’', "'").replace('‘', "'")
    search_query = re.sub(r'[^a-zA-Z0-9\s\'\-\:]', '', search_query)
    # Strip year from search query (e.g. "Game 2024" -> "Game") to improve search success
    search_query = re.sub(r'\b\d{4}\b', '', search_query).strip()
    
    try:
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API Search Query: '{search_query}' (original: '{game_title}')\n")
        url = 'https://store.steampowered.com/api/storesearch/?term=' + urllib.parse.quote(search_query) + '&l=english&cc=US'
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API Search URL: {url}\n")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10).read()
        data = json.loads(res)
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API search results: {list(data.keys()) if data else 'Empty'}\n")
            if data and data.get('items'):
                f_dbg.write(f"Steam API items: {len(data['items'])} items found. First: {data['items'][0]['name']}\n")
        if data.get('items'):
            # Match the closest item by title or fallback to first
            appid = data['items'][0]['id']
            for item in data['items']:
                if item.get('name', '').lower() == game_title.lower():
                    appid = item['id']
                    break
            
            # Fetch appdetails
            details_url = 'https://store.steampowered.com/api/appdetails?appids=' + str(appid) + '&l=english'
            details_req = urllib.request.Request(details_url, headers={'User-Agent': 'Mozilla/5.0'})
            details_res = urllib.request.urlopen(details_req, timeout=10).read()
            details_data = json.loads(details_res)
            
            if details_data.get(str(appid)) and details_data[str(appid)].get('success'):
                g = details_data[str(appid)]['data']
                
                # Fetch reviews for score description and percentage
                rating_str = ''
                try:
                    reviews_url = 'https://store.steampowered.com/appreviews/' + str(appid) + '?json=1&purchase_type=all'
                    reviews_req = urllib.request.Request(reviews_url, headers={'User-Agent': 'Mozilla/5.0'})
                    reviews_res = urllib.request.urlopen(reviews_req, timeout=8).read()
                    reviews_data = json.loads(reviews_res)
                    if reviews_data.get('success') and reviews_data.get('query_summary'):
                        qs = reviews_data['query_summary']
                        tot = qs.get('total_reviews', 0)
                        pos = qs.get('total_positive', 0)
                        pct = round((pos / tot) * 100) if tot > 0 else 0
                        desc = qs.get('review_score_desc', 'Positive')
                        rating_str = f"{pct}% ({desc})"
                except Exception:
                    pass
                
                return {
                    'description': g.get('short_description', ''),
                    'developers': g.get('developers', []),
                    'publishers': g.get('publishers', []),
                    'release_date': g.get('release_date', {}).get('date', ''),
                    'genres': [genre.get('description') for genre in g.get('genres', []) if genre.get('description')],
                    'metacritic': g.get('metacritic', {}).get('score'),
                    'screenshots': [s.get('path_full') for s in g.get('screenshots', [])],
                    'header_image': g.get('header_image', ''),
                    'steam_rating': rating_str
                }
    except Exception as e:
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API error: {str(e)}\n")
        add_log(f"Steam API metadata fetch error: {str(e)}")
    return None

def parse_online_fix_page(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all(class_=['article', 'article-short'])
    results = []
    for art in articles:
        title_a = None
        
        # 1. Look for headers like h2 class="title" or news-title
        title_header = art.find(['h1', 'h2', 'h3', 'h4'], class_=['title', 'news-title', 'post-title'])
        if title_header:
            if title_header.parent and title_header.parent.name == 'a':
                title_a = title_header.parent
            else:
                title_a = title_header.find('a') or title_header
                
        # 2. Look for specific classes on link
        if not title_a:
            title_a = art.find('a', class_=['news-title', 'title', 'post-title'])
            
        # 3. Fallback to links with text and games/programs/guides in href
        if not title_a:
            for a in art.find_all('a'):
                href = a.get('href', '')
                if ('/games/' in href or '/programs/' in href or '/guides/' in href) and a.text.strip():
                    title_a = a
                    break
                    
        if not title_a:
            continue
            
        title_text = title_a.text.strip()
        title_text = title_text.split('\n')[0].strip()
        
        # Extract link
        href = ""
        if hasattr(title_a, 'get'):
            href = title_a.get('href', '')
            
        # If the element itself is a header (no link wrapped), check parents or children for link
        if not href and title_a.name in ['h1', 'h2', 'h3', 'h4']:
            parent_a = title_a.find_parent('a')
            if parent_a:
                href = parent_a.get('href', '')
            else:
                child_a = title_a.find('a')
                if child_a:
                    href = child_a.get('href', '')
                    
        if href:
            href = urllib.parse.urljoin(base_url, href)
            
        # Filter: check if URL contains games, programs, or guides
        if not any(token in href for token in ['/games/', '/programs/', '/guides/']):
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
            company_match = re.search(r'Companies:\s*([^\n]+)', text_all, re.IGNORECASE)
            
            item['cover_image'] = clean_cover_url(cover_image)
            item['original_size'] = clean_size(orig_match.group(1)) if orig_match else "Unknown"
            item['repack_size'] = clean_size(repack_match.group(1)) if repack_match else "Unknown"
            
            developer = ""
            if company_match:
                comp_str = company_match.group(1).strip()
                # Split by comma and take the first one (usually the developer)
                parts = comp_str.split(',')
                if parts:
                    developer = parts[0].strip()
            item['developer'] = developer
    except Exception as e:
        pass
        
    title, version = clean_and_parse_title(item.get('title', ''))
    item['title'] = title
    item['version'] = version
    return item

def prefetch_covers_background(results):
    if not results:
        return
    def download_worker():
        for item in results:
            img_url = item.get("cover_image")
            if not img_url:
                continue
            try:
                import hashlib
                url_hash = hashlib.md5(img_url.encode('utf-8')).hexdigest()
                ext = "jpg"
                if "." in img_url.split('/')[-1]:
                    parts = img_url.split('/')[-1].split('.')
                    if len(parts) > 1 and len(parts[-1]) <= 4 and parts[-1].isalnum():
                        ext = parts[-1]
                cache_dir = os.path.join(os.getcwd(), "cover_cache")
                cache_path = os.path.join(cache_dir, f"{url_hash}.{ext}")
                
                # If cached file exists, verify it is not an HTML redirect page
                if os.path.exists(cache_path):
                    with open(cache_path, "rb") as f:
                        header = f.read(15)
                    if header.startswith(b'<!DOCTYPE') or header.startswith(b'<html') or header.startswith(b'<'):
                        try:
                            os.remove(cache_path)
                        except Exception:
                            pass
                    else:
                        continue
                
                # Fetch and save cover using raw urllib
                req = urllib.request.Request(
                    img_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=12) as response:
                    if response.status == 200:
                        content = response.read()
                        if not (content.startswith(b'<!DOCTYPE') or content.startswith(b'<html') or content.startswith(b'<')):
                            os.makedirs(cache_dir, exist_ok=True)
                            with open(cache_path, "wb") as f:
                                f.write(content)
                import time
                time.sleep(0.15)
            except Exception:
                pass
    threading.Thread(target=download_worker, daemon=True).start()

# HTTP Web Server
class APIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
        
    def do_GET(self):
        global _gdrive_pending_auth_error, _gdrive_pending_auth_code, _gdrive_pending_auth_httpd, _gdrive_copy_auth_httpd
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
            
        elif path == "/api/clear_pixeldrain_limit":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with state_lock:
                state["pixeldrain_limit_reached"] = False
            self.wfile.write(json.dumps({"success": True}).encode())
            return
            
        elif path == "/api/gdrive/list_accounts":
            updated_accounts = []
            with state_lock:
                accounts = list(state.get("gdrive_accounts", []))
                active = state.get("active_gdrive_account", "")
                
            for acc in accounts:
                old_email = acc.get("email", "Unknown Account")
                token = get_gdrive_access_token(acc["refresh_token"])
                if token:
                    det = get_gdrive_account_details(
                        token,
                        existing_limit=acc.get("limit", 16106127360),
                        existing_usage=acc.get("usage", 0),
                        existing_name=acc.get("name", "Unknown Name"),
                        existing_email=acc.get("email", "Unknown Account"),
                        existing_photo=acc.get("photo", "")
                    )
                    if det.get("success", False):
                        acc["name"] = det["name"]
                        acc["photo"] = det["photo"]
                        acc["limit"] = det["limit"]
                        acc["usage"] = det["usage"]
                        acc["email"] = det["email"]
                        
                        # Sync active account email if it was matching old_email
                        if active == old_email and det["email"] != old_email:
                            active = det["email"]
                updated_accounts.append(acc)
                
            with state_lock:
                state["gdrive_accounts"] = updated_accounts
                state["active_gdrive_account"] = active
                save_gdrive_accounts()
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True, 
                "accounts": [{
                    "email": a["email"],
                    "name": a.get("name", "Unknown Name"),
                    "photo": a.get("photo", ""),
                    "limit": a.get("limit", 0),
                    "usage": a.get("usage", 0),
                    "fully_configured": (
                        isinstance(state.get("gdrive_session_cookies"), dict) and
                        isinstance(state["gdrive_session_cookies"].get(a["email"]), dict) and
                        "online_fix_auth" in state["gdrive_session_cookies"][a["email"]]
                    )
                } for a in updated_accounts], 
                "active_account": active,
                "custom_client_id": state.get("gdrive_client_id", ""),
                "custom_client_secret": state.get("gdrive_client_secret", "")
            }).encode())
            return
            
        elif path == "/api/skip_warp":
            with state_lock:
                state["warp_status"] = "skipped"
            try:
                with open("warp_skipped.txt", "w") as f:
                    f.write("1")
            except:
                pass
            add_log("User skipped Cloudflare WARP installer check.")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return
            
        elif path == "/api/retry_warp":
            with state_lock:
                state["warp_status"] = "checking"
                state["warp_error_message"] = ""
            add_log("Retrying Cloudflare WARP install process...")
            threading.Thread(target=check_and_install_warp, daemon=True).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return
            
        elif path == "/api/proxy_image":
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                img_url = query_params.get("url", [""])[0]
                if not img_url:
                    self.send_response(400)
                    self.end_headers()
                    return
                
                # Proxy original high-resolution cover directly (hotlinking is bypassed by backend request)
                lower_url = img_url.lower()
                
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
                    # Verify it's not a broken HTML file
                    with open(cache_path, "rb") as f:
                        header = f.read(15)
                    if header.startswith(b'<!DOCTYPE') or header.startswith(b'<html') or header.startswith(b'<'):
                        try:
                            os.remove(cache_path)
                        except Exception:
                            pass
                    else:
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

                # Download and cache using raw urllib.request
                add_log(f"Proxying image: {img_url}")
                req = urllib.request.Request(
                    img_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    content = response.read()
                    content_type = response.headers.get("Content-Type", "image/jpeg")
                    is_success = (response.status == 200) and not (content.startswith(b'<!DOCTYPE') or content.startswith(b'<html') or content.startswith(b'<'))
                    
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
                        self.send_response(404)
                        self.end_headers()
            except Exception as e:
                add_log(f"Proxy image exception: {str(e)}")
                self.send_response(500)
                self.end_headers()
            return
            
        elif path == "/api/proxy_page":
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                page_url = query_params.get("url", [""])[0]
                if not page_url:
                    self.send_response(400)
                    self.end_headers()
                    return
                
                add_log(f"Proxying page request: {page_url}")
                response = cf_requests.get(page_url, impersonate="chrome120", timeout=20, verify=False)
                
                if response.status_code == 200:
                    html = response.text
                    
                    def link_replacer(match):
                        matched_url = match.group(1)
                        if "fitgirl-repacks.site" in matched_url and not matched_url.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".torrent", ".zip", ".rar")):
                            return f'href="/api/proxy_page?url={urllib.parse.quote(matched_url)}"'
                        return match.group(0)
                        
                    html = re.sub(r'href="([^"]+)"', link_replacer, html)
                    html = re.sub(r"href='([^']+)'", link_replacer, html)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                else:
                    self.send_response(response.status_code)
                    self.end_headers()
            except Exception as e:
                add_log(f"Proxy page exception: {str(e)}")
                self.send_response(500)
                self.end_headers()
            return
            
        elif path == "/api/popular":
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                provider = query_params.get("provider", ["fitgirl"])[0]
                type_val = query_params.get("type", ["monthly"])[0]
                page = int(query_params.get("page", ["1"])[0])
                try:
                    page_size = int(query_params.get("page_size", ["27"])[0])
                except (TypeError, ValueError):
                    page_size = 27
                # Allow large page_size so UI can fetch full popular list and client-slice
                page_size = max(4, min(120, page_size))
                
                results = []
                has_next = False
                if provider == "onlinefix":
                    add_log("Fetching popular Online-Fix games (pages 1 & 2)...")
                    url = "https://online-fix.me/"
                    response = cf_requests.get(url, impersonate="chrome120", timeout=20, verify=False)
                    
                    popular_results = []
                    standard_results = []
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        slider = soup.find('div', class_='horizontal-slider')
                        if slider:
                            items = slider.find_all('a')
                            for a in items:
                                href = a.get('href', '')
                                title = a.get('title', '')
                                img = a.find('img')
                                if a and img and href and title:
                                    img_src = img.get('src', '')
                                    if img_src:
                                        img_src = urllib.parse.urljoin(url, img_src)
                                        img_src = clean_cover_url(img_src)
                                    href = urllib.parse.urljoin(url, href)
                                    clean_t, version = clean_and_parse_title(title)
                                    popular_results.append({
                                        "title": clean_t,
                                        "version": version,
                                        "url": href,
                                        "cover_image": img_src,
                                        "original_size": "Unknown",
                                        "repack_size": "Unknown",
                                        "summary": "Popular Online-Fix Game"
                                    })
                        
                        # Scrape standard page 1 games
                        standard_results.extend(parse_online_fix_page(response.text, url))
                        
                    # Also scrape pages 2, 3, and 4 standard games to fill the 54 list
                    for page_num in range(2, 5):
                        try:
                            url_next = f"https://online-fix.me/page/{page_num}/"
                            response_next = cf_requests.get(url_next, impersonate="chrome120", timeout=20, verify=False)
                            if response_next.status_code == 200:
                                standard_results.extend(parse_online_fix_page(response_next.text, url_next))
                        except Exception as e_next:
                            add_log(f"Warning: Failed to fetch Online-Fix page {page_num}: {e_next}")
                        
                    if standard_results or popular_results:
                        # Filter standard results to remove duplicates (including items that are in popular_results)
                        pop_urls = {item["url"] for item in popular_results}
                        unique_standard = []
                        seen_urls = set()
                        for item in standard_results:
                            if item["url"] not in pop_urls and item["url"] not in seen_urls:
                                seen_urls.add(item["url"])
                                unique_standard.append(item)
                        
                        # Limit total standard results to exactly 54
                        all_results = unique_standard[:54]
                        
                        PAGE_SIZE = page_size
                        start_idx = (page - 1) * PAGE_SIZE
                        end_idx = page * PAGE_SIZE
                        results = all_results[start_idx:end_idx]
                        has_next = end_idx < len(all_results)
                        
                        prefetch_covers_background(popular_results)
                        prefetch_covers_background(results)
                        
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True, 
                            "results": results, 
                            "popular": popular_results, 
                            "has_next": has_next
                        }).encode())
                        return
                    else:
                        raise Exception("Failed to scrape any Online-Fix games.")
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
                        
                        # Cap FitGirl popular list; UI may request full list via page_size
                        all_results = all_results[:60]
                        PAGE_SIZE = page_size
                        start_idx = (page - 1) * PAGE_SIZE
                        end_idx = page * PAGE_SIZE
                        results = all_results[start_idx:end_idx]
                        has_next = end_idx < len(all_results)
                    else:
                        raise Exception(f"HTTP status: {response.status_code}")
                
                prefetch_covers_background(all_results)
                
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
        elif path == "/details-fix.css":
            file_to_serve = os.path.join(os.path.dirname(__file__), "web", "details-fix.css")
            content_type = "text/css"
        elif path == "/app.js":
            file_to_serve = os.path.join(os.path.dirname(__file__), "web", "app.js")
            content_type = "application/javascript"
        else:
            self.send_error(404, "File Not Found")
            return
            
        try:
            if path == "/" or path == "/index.html":
                with open(file_to_serve, "r", encoding="utf-8") as f:
                    content_str = f.read()
                import time
                ts = str(int(time.time()))
                content_str = content_str.replace("style.css?v=2.1", f"style.css?v={ts}")
                content_str = content_str.replace("app.js?v=2.1", f"app.js?v={ts}")
                for ver in ("2.1", "3.9", "4.0"):
                    content_str = content_str.replace(f"style.css?v={ver}", f"style.css?v={ts}")
                    content_str = content_str.replace(f"app.js?v={ver}", f"app.js?v={ts}")
                    content_str = content_str.replace(f"details-fix.css?v={ver}", f"details-fix.css?v={ts}")
                content = content_str.encode("utf-8")
            else:
                with open(file_to_serve, "rb") as f:
                    content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")

    def do_POST(self):
        global _gdrive_pending_auth_httpd, _gdrive_pending_auth_code, _gdrive_pending_auth_error, _gdrive_copy_auth_httpd
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path
        
        if path == "/api/start":
            with state_lock:
                if not state["is_running"] and state["files"]:
                    state["is_running"] = True
                    state["should_stop"] = False
                    workers_to_start = get_effective_max_workers()
                    add_log(f"Download manager resumed/started with {workers_to_start} parallel workers.")
                    for _ in range(workers_to_start):
                        threading.Thread(target=download_worker, daemon=True).start()
            save_session_state()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            
        elif path == "/api/retry":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                idx = int(data.get("index", -1))
                with state_lock:
                    if 0 <= idx < len(state["files"]):
                        state["files"][idx]["status"] = "waiting"
                        state["files"][idx]["error"] = ""
                    if not state["is_running"]:
                        state["is_running"] = True
                        state["should_stop"] = False
                        workers_to_start = get_effective_max_workers()
                        for _ in range(workers_to_start):
                            threading.Thread(target=download_worker, daemon=True).start()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                return
            except Exception as e:
                self.send_error(500, f"Error retrying: {str(e)}")
                return

        elif path == "/api/gdrive/set_credentials":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                client_id = data.get("client_id", "").strip()
                client_secret = data.get("client_secret", "").strip()
                with state_lock:
                    state["gdrive_client_id"] = client_id
                    state["gdrive_client_secret"] = client_secret
                    save_gdrive_accounts()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
                return
            except Exception as e:
                self.send_error(500, f"Error saving credentials: {str(e)}")
                return
            
        elif path == "/api/gdrive/start_auth":
            # Step 1: Generate auth URL and start HTTP listener to capture redirect
            client_id, _ = get_gdrive_credentials()
            redirect_uri = "http://127.0.0.1:53683/"
            scope = "https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
            auth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"client_id={client_id}&"
                f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
                f"response_type=code&"
                f"scope={urllib.parse.quote(scope)}&"
                f"access_type=offline&"
                f"prompt=consent"
            )
            
            add_log("Settings: Starting Google Account authorization...")
            
            # Close any active copy flow listener first to release port 53683
            
            # Close any active copy flow listener first to release port 53683
            if _gdrive_copy_auth_httpd:
                add_log("Settings: Closing active GDrive copy flow auth listener to release port 53683...")
                try:
                    _gdrive_copy_auth_httpd.server_close()
                except Exception:
                    pass
                _gdrive_copy_auth_httpd = None

            # Close any existing settings pending listener
            if _gdrive_pending_auth_httpd:
                try:
                    _gdrive_pending_auth_httpd.server_close()
                except:
                    pass
            
            httpd = None
            for bind_attempt in range(3):
                try:
                    httpd = HTTPServer(('127.0.0.1', 53683), OAuthRedirectHandler)
                    break
                except OSError as e:
                    add_log(f"GDrive: Port 53683 busy (attempt {bind_attempt+1}): {e}")
                    time.sleep(1.5)
            
            if not httpd:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Cannot bind port 53683. Try again."}).encode())
                return
            
            httpd.captured_code = ""
            httpd.captured_error = ""
            httpd.timeout = 900  # 15 minutes
            
            # Store reference for polling
            _gdrive_pending_auth_httpd = httpd
            _gdrive_pending_auth_code = ""
            _gdrive_pending_auth_error = ""
            
            # Handle request in background thread
            def _auth_listener(h):
                global _gdrive_pending_auth_code, _gdrive_pending_auth_error
                import time
                h.timeout = 2.0
                start_time = time.time()
                while time.time() - start_time < 900:
                    if getattr(h, "captured_code", "") or getattr(h, "captured_error", ""):
                        break
                    try:
                        h.handle_request()
                    except Exception:
                        pass
                if getattr(h, "captured_code", ""):
                    _gdrive_pending_auth_code = h.captured_code
                if getattr(h, "captured_error", ""):
                    _gdrive_pending_auth_error = h.captured_error
            
            threading.Thread(target=_auth_listener, args=(httpd,), daemon=True).start()
            
            # Return the auth URL — frontend will open it via window.open()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "auth_url": auth_url}).encode())
            return
            
        elif path == "/api/gdrive/poll_auth":
            # Step 2: Check if auth code was captured, exchange for tokens
            error = _gdrive_pending_auth_error
            code = _gdrive_pending_auth_code
            
            if error:
                _gdrive_pending_auth_error = ""
                # Clean up listener
                try:
                    if _gdrive_pending_auth_httpd:
                        _gdrive_pending_auth_httpd.server_close()
                        _gdrive_pending_auth_httpd = None
                except:
                    pass
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": error}).encode())
                return
                
            if not code:
                # Still waiting
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "waiting"}).encode())
                return
            
            # Code captured! Exchange for tokens
            add_log("Settings: Authorization code received, exchanging for tokens...")
            _gdrive_pending_auth_code = ""  # Reset
            
            # Clean up listener
            try:
                if _gdrive_pending_auth_httpd:
                    _gdrive_pending_auth_httpd.server_close()
                    _gdrive_pending_auth_httpd = None
            except:
                pass
            
            res = exchange_gdrive_code(code)
            if not res.get("success", False):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": res.get("error", "Token exchange failed.")}).encode())
                return
                
            email = res["email"]
            refresh_token = res["refresh_token"]
            
            with state_lock:
                state["gdrive_accounts"] = [a for a in state["gdrive_accounts"] if a["email"] != email]
                state["gdrive_accounts"].append({
                    "email": email,
                    "refresh_token": refresh_token,
                    "name": res.get("name", "Unknown Name"),
                    "photo": res.get("photo", ""),
                    "limit": res.get("limit", 0),
                    "usage": res.get("usage", 0)
                })
                state["active_gdrive_account"] = email
                save_gdrive_accounts()
                
            add_log(f"Google Account linked successfully: {email}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "done", "success": True, "email": email}).encode())
            return
            
        elif path == "/api/gdrive/start_copy_auth":
            # Phase 2: Start Rclone redirect listener and return auth URL
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                email = data.get("email", "").strip()
            except:
                email = ""
                
            redirect_uri = "http://127.0.0.1:53683/"
            scope = "https://www.googleapis.com/auth/drive"
            auth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"client_id={RCLONE_CLIENT_ID}&"
                f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
                f"response_type=code&"
                f"scope={urllib.parse.quote(scope)}&"
                f"access_type=offline&"
                f"prompt=consent"
            )
            if email:
                auth_url += f"&login_hint={urllib.parse.quote(email)}"
                
            add_log("Settings: Starting GDrive copy flow (Rclone) authorization...")
            
            # Close any active listeners first
            try:
                if _gdrive_pending_auth_httpd:
                    _gdrive_pending_auth_httpd.server_close()
                    _gdrive_pending_auth_httpd = None
            except:
                pass
            try:
                if _gdrive_copy_auth_httpd:
                    _gdrive_copy_auth_httpd.server_close()
                    _gdrive_copy_auth_httpd = None
            except:
                pass
                
            # Start listener on port 53683
            httpd = None
            for bind_attempt in range(3):
                try:
                    httpd = HTTPServer(('127.0.0.1', 53683), OAuthRedirectHandler)
                    break
                except OSError as e:
                    add_log(f"GDrive: Port 53683 busy (attempt {bind_attempt+1}): {e}")
                    time.sleep(1.5)
                    
            if not httpd:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Cannot bind port 53683. Try again."}).encode())
                return
                
            httpd.captured_code = ""
            httpd.captured_error = ""
            httpd.timeout = 900
            
            _gdrive_pending_auth_httpd = httpd
            _gdrive_pending_auth_code = ""
            _gdrive_pending_auth_error = ""
            
            def _auth_listener(h):
                global _gdrive_pending_auth_code, _gdrive_pending_auth_error
                import time
                h.timeout = 2.0
                start_time = time.time()
                while time.time() - start_time < 900:
                    if getattr(h, "captured_code", "") or getattr(h, "captured_error", ""):
                        break
                    try:
                        h.handle_request()
                    except Exception:
                        pass
                if getattr(h, "captured_code", ""):
                    _gdrive_pending_auth_code = h.captured_code
                if getattr(h, "captured_error", ""):
                    _gdrive_pending_auth_error = h.captured_error
                    
            threading.Thread(target=_auth_listener, args=(httpd,), daemon=True).start()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "auth_url": auth_url}).encode())
            return
            
        elif path == "/api/gdrive/poll_copy_auth":
            # Phase 2: Poll for Rclone auth code and exchange for Online-Fix cookies
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                email = data.get("email", "").strip()
            except:
                email = ""
                
            if not email:
                with state_lock:
                    email = state.get("active_gdrive_account", "")
                    
            error = _gdrive_pending_auth_error
            code = _gdrive_pending_auth_code
            
            if error:
                _gdrive_pending_auth_error = ""
                try:
                    if _gdrive_pending_auth_httpd:
                        _gdrive_pending_auth_httpd.server_close()
                        _gdrive_pending_auth_httpd = None
                except:
                    pass
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": error}).encode())
                return
                
            if not code:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "waiting"}).encode())
                return
                
            # Code captured! Exchange for Online-Fix cookies
            add_log("Settings: GDrive copy flow authorization code received. Establishing cookies on Online-Fix...")
            _gdrive_pending_auth_code = ""
            
            try:
                if _gdrive_pending_auth_httpd:
                    _gdrive_pending_auth_httpd.server_close()
                    _gdrive_pending_auth_httpd = None
            except:
                pass
                
            # Establish cookies using curl_cffi Session and a fresh download URL
            success = False
            err_msg = ""
            try:
                with state_lock:
                    game_title = state.get("game_title") or "Among Us VR"
                folder_name = urllib.parse.quote(game_title)
                folder_url = f"https://drive.online-fix.me:2053/{folder_name}"
                
                add_log(f"Establishing session on Online-Fix folder page: {folder_url}")
                
                # Use cf_requests Session to automatically handle cookies
                session = cf_requests.Session()
                
                h = {
                    "Referer": "https://online-fix.me/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                
                # 1. GET folder page to set guest session cookies
                r = session.get(folder_url, headers=h, impersonate="chrome120", timeout=20, verify=False)
                if r.status_code != 200:
                    raise Exception(f"Failed to access folder page. Status code: {r.status_code}")
                
                # Parse folder page for fresh download URLs
                soup = BeautifulSoup(r.text, 'html.parser')
                links = []
                for a in soup.find_all('a', onclick=True):
                    onclick = a.get('onclick', '')
                    match = re.search(r"openDownloadModal\s*\(\s*event\s*,\s*'([^']+)'\s*\)", onclick)
                    if match:
                        links.append(match.group(1))
                
                if not links:
                    raise Exception("No download links found in folder page HTML.")
                    
                page_url = links[0]
                add_log(f"Scraped fresh download URL: {page_url[:80]}...")
                
                # 2. GET download URL (with folder referer)
                h["Referer"] = folder_url
                r_get = session.get(page_url, headers=h, impersonate="chrome120", timeout=20, verify=False)
                # GET download URL will return 405 Method Not Allowed, which is fine since it sets more cookies
                
                # 3. POST authorization key to download URL
                add_log("Sending copy flow authorization key to Online-Fix...")
                res = session.post(page_url, headers=h, data={"api_key": code}, impersonate="chrome120", timeout=20, verify=False)
                
                if res.status_code == 200:
                    try:
                        res_data = res.json()
                    except Exception:
                        err_msg = f"Online-Fix returned non-JSON response (status {res.status_code})."
                        res_data = {}
                        
                    if res_data.get("success", False):
                        # Save cookies
                        final_cookies = session.cookies.get_dict()
                        with state_lock:
                            if "gdrive_session_cookies" not in state or not isinstance(state["gdrive_session_cookies"], dict):
                                state["gdrive_session_cookies"] = {}
                            state["gdrive_session_cookies"][email] = final_cookies
                            save_gdrive_accounts()
                        success = True
                    elif not err_msg:
                        err_msg = res_data.get("message", "Copy request rejected by Online-Fix.")
                else:
                    err_msg = f"Online-Fix server returned status code {res.status_code}."
            except Exception as e:
                err_msg = str(e)
                
            if success:
                add_log(f"GDrive copy flow configured successfully for {email}")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "done", "success": True}).encode())
            else:
                add_log(f"Settings GDrive copy flow setup failed: {err_msg}")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": f"Failed to configure copy flow: {err_msg}"}).encode())
            return
            
        elif path == "/api/gdrive/remove_account":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                email_to_remove = data.get("email")
                if email_to_remove:
                    with state_lock:
                        state["gdrive_accounts"] = [a for a in state["gdrive_accounts"] if a["email"] != email_to_remove]
                        if state["active_gdrive_account"] == email_to_remove:
                            if state["gdrive_accounts"]:
                                state["active_gdrive_account"] = state["gdrive_accounts"][0]["email"]
                            else:
                                state["active_gdrive_account"] = ""
                        save_gdrive_accounts()
                    add_log(f"Linked Google account removed: {email_to_remove}")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode())
                    return
            except Exception as e:
                pass
            self.send_error(400, "Bad Request")
            
        elif path == "/api/gdrive/select_account":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                email = data.get("email")
                if email:
                    with state_lock:
                        if any(a["email"] == email for a in state["gdrive_accounts"]):
                            state["active_gdrive_account"] = email
                            save_gdrive_accounts()
                            add_log(f"Active Google account changed to: {email}")
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True}).encode())
                            return
            except Exception as e:
                pass
            self.send_error(400, "Bad Request")
            
        elif path == "/api/gdrive/cleanup":
            with state_lock:
                active_account = state.get("active_gdrive_account")
                accounts = state.get("gdrive_accounts", [])
                files = list(state.get("files", []))
                
            if not active_account:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "No active Google Drive account."}).encode())
                return
                
            account = next((a for a in accounts if a["email"] == active_account), None)
            if not account:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": f"Account '{active_account}' not found."}).encode())
                return
                
            access_token = get_gdrive_access_token(account["refresh_token"])
            if not access_token:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Failed to refresh access token."}).encode())
                return
                
            def run_cleanup():
                deleted_count = 0
                add_log("GDrive: Starting manual cleanup of temporary repack files...")
                for f in files:
                    filename = f["filename"]
                    meta = find_gdrive_file(filename, access_token)
                    if meta:
                        file_id = meta["id"]
                        add_log(f"GDrive: Deleting {filename} (ID: {file_id}) from Drive...")
                        if delete_gdrive_file(file_id, access_token):
                            deleted_count += 1
                add_log(f"GDrive: Manual cleanup finished. Deleted {deleted_count} files.")
                
            threading.Thread(target=run_cleanup, daemon=True).start()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return
            
        elif path == "/api/pause":
            with state_lock:
                if state["is_running"]:
                    state["is_running"] = False
                    state["total_speed"] = 0
                    state["should_stop"] = True
                    add_log("Pausing downloads... Workers will exit shortly.")
            save_session_state()
            
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
                            needed = get_effective_max_workers() - state["active_workers_count"]
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
                
                prefetch_covers_background(results)
                
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
                    # Retries + longer timeout — FitGirl often slow / flaky behind CF
                    response = None
                    scrape_err = None
                    fg_host = urllib.parse.urlparse(url).hostname or "fitgirl-repacks.site"
                    for attempt in range(3):
                        try:
                            _doh_cache.pop(fg_host, None)
                            fg_ip = resolve_doh(fg_host)
                            session_kwargs = {}
                            if fg_ip:
                                session_kwargs["curl_options"] = {
                                    CurlOpt.RESOLVE: [f"{fg_host}:443:{fg_ip}", f"{fg_host}:80:{fg_ip}"]
                                }
                                add_log(f"FitGirl page DNS via DoH: {fg_host} -> {fg_ip}")
                            with cf_requests.Session(**session_kwargs) as fg_sess:
                                response = fg_sess.get(
                                    url,
                                    impersonate="chrome120",
                                    timeout=45,
                                    verify=False,
                                )
                            if response is not None and response.status_code == 200:
                                break
                            scrape_err = f"HTTP {getattr(response, 'status_code', '?')}"
                            add_log(f"FitGirl scrape attempt {attempt + 1}/3: {scrape_err}")
                        except Exception as se:
                            scrape_err = se
                            add_log(f"FitGirl scrape attempt {attempt + 1}/3 failed: {se}")
                            time.sleep(0.8 * (attempt + 1))
                    if response is not None and response.status_code == 200:
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
                                        
                        # Extract description / features / screenshots (FitGirl page structure)
                        description = ""
                        screenshots = []
                        videos = []
                        genres_tags = ""
                        company = ""
                        languages = ""
                        repack_features_list = []

                        # Broken FitGirl HTML often closes .entry-content (and even <article>)
                        # early, so Screenshots / Repack Features / Game Description become
                        # siblings under #primary — prefer that wider root first.
                        parse_root = (
                            soup.find(id="primary")
                            or soup.find("article")
                            or content_el
                            or soup
                        )

                        # Junk image hosts / torrent stats banners (green text stats)
                        _SHOT_BLOCKLIST = (
                            "torrent-stats.info", "torrentstats", "kitty-kode", "statspics",
                            "tracker-stats", "opentrackr", "favicon", "gravatar", "emoji",
                            "smiley", "avatar", "wp-includes", "wp-content/plugins", "spinner",
                            "loading.gif", "badge", "pixel.gif", "1x1",
                        )

                        def _normalize_shot_url(candidate):
                            if not candidate:
                                return ""
                            candidate = candidate.strip()
                            if candidate.startswith("//"):
                                candidate = "https:" + candidate
                            if candidate.startswith("/"):
                                candidate = urllib.parse.urljoin(url, candidate)
                            elif not candidate.startswith("http"):
                                candidate = urllib.parse.urljoin(url, candidate)
                            # RiotPixels thumbs: xxx.jpg.240p.jpg → full xxx.jpg (not xxx.jpg.jpg)
                            candidate = re.sub(
                                r'\.(jpg|jpeg|png|webp)\.(?:240p|400p|720p)\.(?:jpg|jpeg|png|webp)$',
                                r'.\1',
                                candidate,
                                flags=re.IGNORECASE,
                            )
                            # Fallback: bare .240p.jpg suffix without prior ext
                            candidate = re.sub(
                                r'\.(?:240p|400p|720p)\.(jpg|jpeg|png|webp)$',
                                r'.\1',
                                candidate,
                                flags=re.IGNORECASE,
                            )
                            return clean_cover_url(candidate)

                        def _is_junk_shot(u):
                            if not u:
                                return True
                            lu = u.lower()
                            if any(b in lu for b in _SHOT_BLOCKLIST):
                                return True
                            if re.search(r'-\d{2,3}x\d{2,3}\.(jpg|jpeg|png|webp)$', lu):
                                return True
                            if not (
                                lu.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
                                or 'riotpixels.net/data/' in lu
                                or 'steamstatic' in lu
                                or 'imageban' in lu
                                or 'imgur' in lu
                            ):
                                return True
                            return False

                        def _prefer_video_url(src):
                            """Keep playable Steam microtrailer.webm as-is.

                            movie_max.mp4 siblings often 404 on FitGirl embeds — do NOT
                            rewrite microtrailer → movie_max (that broke autoplay).
                            """
                            if not src:
                                return ""
                            src = src.strip()
                            if src.startswith("//"):
                                src = "https:" + src
                            return src

                        def _extract_features_from(root):
                            found = []
                            if not root:
                                return found
                            for el in root.find_all(["h3", "h4"]):
                                if "repack features" not in el.get_text(strip=True).lower():
                                    continue
                                # Prefer the next UL (may skip text nodes / <br>)
                                ul = el.find_next_sibling("ul")
                                if not ul:
                                    curr = el
                                    for _ in range(16):
                                        curr = curr.next_sibling
                                        if not curr:
                                            break
                                        if isinstance(curr, str):
                                            continue
                                        if getattr(curr, "name", None) == "ul":
                                            ul = curr
                                            break
                                        if getattr(curr, "name", None) in ("h3", "h4"):
                                            break
                                if ul:
                                    # FitGirl often omits </li>; BS nests subsequent <li> inside
                                    # the first one. Take only direct text of each <li>.
                                    for li in ul.find_all("li"):
                                        parts = []
                                        for c in li.contents:
                                            if getattr(c, "name", None) in ("ul", "ol", "li"):
                                                continue
                                            parts.append(
                                                c.get_text(" ", strip=True)
                                                if hasattr(c, "get_text")
                                                else str(c).strip()
                                            )
                                        item = re.sub(r"\s+", " ", " ".join(p for p in parts if p)).strip()
                                        if item and item not in found:
                                            found.append(item)
                                break
                            return found

                        def _extract_description_from(root):
                            if not root:
                                return ""
                            game_desc_paragraphs = []

                            def _chunks_from_body(body):
                                """Extract readable Game Description from FitGirl spoiler body.

                                FitGirl often mixes:
                                  - bare text nodes (first paragraph)
                                  - <p> paragraphs
                                  - <b>Game Features</b> + <ul><li>…</li>
                                Never discard a longer full-text extraction for a
                                short p-only fallback (that was the CoD MW2 bug).
                                """
                                if not body:
                                    return []

                                def _is_junk_desc(t):
                                    tl = (t or "").lower()
                                    return any(
                                        x in tl
                                        for x in (
                                            "paste.fitgirl",
                                            "click to show direct",
                                            "filehoster:",
                                            "download mirrors",
                                        )
                                    )

                                def _norm(t):
                                    return re.sub(r"\s+", " ", (t or "")).strip()

                                def _li_text(li):
                                    parts = []
                                    for c in li.contents:
                                        if getattr(c, "name", None) in ("ul", "ol", "li"):
                                            continue
                                        parts.append(
                                            c.get_text(" ", strip=True)
                                            if hasattr(c, "get_text")
                                            else str(c).strip()
                                        )
                                    item = _norm(" ".join(p for p in parts if p))
                                    if not item:
                                        item = _norm(li.get_text(" ", strip=True))
                                    return item

                                structured = []

                                def _emit(t, bullet=False):
                                    t = _norm(t)
                                    if not t or _is_junk_desc(t):
                                        return
                                    if bullet and not t.startswith("•"):
                                        t = "• " + t
                                    structured.append(t)

                                # Walk direct children first (preserves order)
                                for child in list(body.children):
                                    if isinstance(child, str):
                                        t = _norm(child)
                                        if len(t) >= 12:
                                            _emit(t)
                                        continue
                                    name = getattr(child, "name", None)
                                    if name in (None, "script", "style", "br"):
                                        continue
                                    if name in ("ul", "ol"):
                                        for li in child.find_all("li"):
                                            item = _li_text(li)
                                            if item and len(item) >= 3:
                                                _emit(item, bullet=True)
                                        continue
                                    if name in ("p", "div", "blockquote", "section"):
                                        # Leading non-list content (headers / paragraphs)
                                        lead = []
                                        for c in child.contents:
                                            if getattr(c, "name", None) in ("ul", "ol"):
                                                break
                                            if isinstance(c, str):
                                                lead.append(c)
                                            elif getattr(c, "name", None) not in ("script", "style"):
                                                lead.append(
                                                    c.get_text(" ", strip=True)
                                                    if hasattr(c, "get_text")
                                                    else ""
                                                )
                                        lead_t = _norm(" ".join(lead))
                                        if lead_t:
                                            _emit(lead_t)
                                        for ul in child.find_all(["ul", "ol"], recursive=False):
                                            for li in ul.find_all("li"):
                                                item = _li_text(li)
                                                if item and len(item) >= 3:
                                                    _emit(item, bullet=True)
                                        # nested lists deeper
                                        if not child.find(["ul", "ol"], recursive=False) and not lead_t:
                                            t = _norm(child.get_text(" ", strip=True))
                                            if t:
                                                _emit(t)
                                        continue
                                    if name in ("h3", "h4", "h5", "h6", "strong", "b"):
                                        t = _norm(child.get_text(" ", strip=True))
                                        if t:
                                            _emit(t)
                                        continue
                                    # generic block
                                    t = _norm(child.get_text(" ", strip=True))
                                    if t and len(t) >= 20:
                                        _emit(t)

                                # Dedup
                                chunks = []
                                seen = set()
                                for t in structured:
                                    key = t[:96].lower()
                                    if key in seen:
                                        continue
                                    seen.add(key)
                                    chunks.append(t)

                                # Full plain-text baseline
                                frag_html = re.sub(
                                    r"<br\s*/?>",
                                    "\n",
                                    body.decode_contents() if hasattr(body, "decode_contents") else str(body),
                                    flags=re.I,
                                )
                                frag = BeautifulSoup(frag_html, "html.parser")
                                raw = frag.get_text("\n", strip=True)
                                raw_clean = _norm(raw.replace("\n", " "))
                                chunks_len = sum(len(c) for c in chunks)

                                # If structured walk lost content (classic p-only miss of
                                # leading text node), rebuild from full text lines.
                                if raw and (not chunks or len(raw_clean) > chunks_len + 60):
                                    lines = [_norm(ln) for ln in raw.split("\n") if _norm(ln)]
                                    rebuilt = []
                                    for ln in lines:
                                        if _is_junk_desc(ln):
                                            continue
                                        low = ln.rstrip(":").lower()
                                        if low in (
                                            "game features",
                                            "included bonus soundtracks",
                                            "features",
                                            "pc features",
                                            "about this game",
                                        ) or (ln.endswith(":") and len(ln) < 60):
                                            rebuilt.append(ln)
                                        elif len(ln) > 24 and " – " in ln[:80]:
                                            rebuilt.append("• " + ln if not ln.startswith("•") else ln)
                                        else:
                                            rebuilt.append(ln)
                                    if sum(len(x) for x in rebuilt) >= chunks_len:
                                        chunks = rebuilt

                                if not chunks and raw_clean:
                                    chunks = [raw_clean]
                                return chunks

                            for spoiler in root.select("div.su-spoiler"):
                                title_el = spoiler.select_one(".su-spoiler-title")
                                title_txt = title_el.get_text(" ", strip=True).lower() if title_el else ""
                                if "game description" not in title_txt:
                                    continue
                                body = spoiler.select_one(".su-spoiler-content") or spoiler
                                game_desc_paragraphs = _chunks_from_body(body)
                                break

                            if not game_desc_paragraphs:
                                for el in root.find_all(["h3", "h4", "strong", "b", "span", "div"]):
                                    label = el.get_text(" ", strip=True).lower()
                                    if label != "game description" and not (
                                        el.get("class") and "su-spoiler-title" in (el.get("class") or [])
                                        and "game description" in label
                                    ):
                                        continue
                                    parent = el.find_parent("div", class_=re.compile(r"su-spoiler"))
                                    if parent:
                                        body = parent.select_one(".su-spoiler-content") or parent
                                        game_desc_paragraphs = _chunks_from_body(body)
                                    break

                            return "\n\n".join(game_desc_paragraphs).strip()

                        if parse_root:
                            # 1. Metadata lines (entry-content preferred — top of post)
                            meta_root = content_el or parse_root
                            for p in meta_root.find_all("p", recursive=True):
                                text = p.get_text()
                                if "genres/tags:" in text.lower() or "genre/tag:" in text.lower():
                                    match = re.search(r"(?:genres/tags|genre/tag|genres):\s*(.*)", text, re.IGNORECASE)
                                    if match:
                                        genres_tags = match.group(1).strip()
                                if "compan" in text.lower():
                                    match = re.search(r"(?:companies|company):\s*(.*)", text, re.IGNORECASE)
                                    if match:
                                        company = match.group(1).strip()
                                if "languages:" in text.lower() or "language:" in text.lower():
                                    match = re.search(r"(?:languages|language):\s*(.*)", text, re.IGNORECASE)
                                    if match:
                                        languages = match.group(1).strip()

                            # 2. Repack Features
                            repack_features_list = _extract_features_from(parse_root)
                            if not repack_features_list and content_el is not parse_root:
                                repack_features_list = _extract_features_from(content_el)

                            # 3. Game Description
                            description = _extract_description_from(parse_root)
                            if not description and content_el is not parse_root:
                                description = _extract_description_from(content_el)
                            # Drop "Included Bonus Soundtracks" and similar repack-extra lists
                            # (they belong in features / selective download, not story text)
                            if description:
                                description = _strip_bonus_soundtrack_section(description)

                            # 4. Screenshots — ONLY under h3 "Screenshots...", never torrent-stats / mirror images
                            def _add_shot(candidate):
                                cleaned = _normalize_shot_url(candidate)
                                if _is_junk_shot(cleaned):
                                    return
                                if cleaned == cover_image or cleaned in screenshots:
                                    return
                                screenshots.append(cleaned)

                            shot_header = None
                            for el in parse_root.find_all(["h3", "h4"]):
                                if "screenshot" in el.get_text(strip=True).lower():
                                    shot_header = el
                                    break
                            if shot_header:
                                curr = shot_header
                                for _ in range(40):
                                    curr = curr.next_sibling
                                    if not curr:
                                        break
                                    if isinstance(curr, str):
                                        continue
                                    name = getattr(curr, "name", None)
                                    if name in ("h3", "h4"):
                                        break
                                    if not name:
                                        continue
                                    # Trailers often sit inside the screenshots <p> as <video>
                                    for video in curr.find_all("video") if hasattr(curr, "find_all") else []:
                                        source = video.find("source")
                                        video_src = source.get("src", "") if source else video.get("src", "")
                                        video_src = _prefer_video_url(video_src)
                                        if video_src and video_src not in videos:
                                            videos.append(video_src)
                                    for a in curr.find_all("a") if hasattr(curr, "find_all") else []:
                                        href = a.get("href", "")
                                        # Don't treat riotpixels gallery page links as shots
                                        if href and not re.search(r"/screenshots/?(\?|$)", href, re.I):
                                            _add_shot(href)
                                        img = a.find("img")
                                        if img:
                                            _add_shot(img.get("data-src") or img.get("src") or "")
                                    for img in curr.find_all("img") if hasattr(curr, "find_all") else []:
                                        _add_shot(
                                            img.get("data-src")
                                            or img.get("data-lazy-src")
                                            or img.get("src")
                                            or ""
                                        )
                                    if name == "a":
                                        _add_shot(curr.get("href", ""))
                                    if name == "img":
                                        _add_shot(curr.get("src") or curr.get("data-src") or "")
                                    if name == "video":
                                        source = curr.find("source")
                                        video_src = source.get("src", "") if source else curr.get("src", "")
                                        video_src = _prefer_video_url(video_src)
                                        if video_src and video_src not in videos:
                                            videos.append(video_src)
                            else:
                                # fallback: only riotpixels embeds
                                for img in parse_root.find_all("img"):
                                    src = img.get("data-src") or img.get("src") or ""
                                    if "riotpixels" in src.lower():
                                        _add_shot(src)

                            screenshots = screenshots[:12]

                            # 5. Videos / trailers (direct <video> + YouTube only near content, not sidebar widgets)
                            for video in parse_root.find_all("video"):
                                source = video.find("source")
                                video_src = source.get("src", "") if source else video.get("src", "")
                                video_src = _prefer_video_url(video_src)
                                if video_src and video_src not in videos:
                                    videos.append(video_src)

                            # YouTube embeds inside article only (skip sidebar OST widgets)
                            for iframe in parse_root.find_all("iframe"):
                                # Skip widgets outside article content
                                if iframe.find_parent(class_=re.compile(r"widget|sidebar|footer", re.I)):
                                    continue
                                src = iframe.get("src") or iframe.get("data-src") or ""
                                if "youtube" in src or "youtu.be" in src:
                                    if src.startswith("//"):
                                        src = "https:" + src
                                    # enable autoplay-friendly embed params later on FE
                                    if src not in videos:
                                        videos.append(src)

                            # Trailer-first order: direct steam/mp4 first, then youtube
                            def _video_rank(v):
                                vl = (v or "").lower()
                                if "microtrailer" in vl:
                                    return 2
                                if any(x in vl for x in (".mp4", ".webm", "steamstatic", "store_trailers")):
                                    return 0
                                if "youtube" in vl or "youtu.be" in vl:
                                    return 1
                                return 3
                            videos = sorted(list(dict.fromkeys(videos)), key=_video_rank)

                        
                        developer_val = ""
                        publisher_val = ""
                        release_date_val = ""
                        genres_val = []
                        metacritic_val = None
                        steam_rating_val = ""
                        header_image_val = ""

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
                            "screenshots": screenshots,
                            "developer": developer_val,
                            "publisher": publisher_val,
                            "release_date": release_date_val,
                            "genres": genres_val,
                            "metacritic": metacritic_val,
                            "steam_rating": steam_rating_val,
                            "header_image": header_image_val,
                            "genres_tags": genres_tags,
                            "company": company,
                            "languages": languages,
                            "repack_features": repack_features_list
                        }).encode())
                        return
                    else:
                        status = getattr(response, "status_code", None) if response is not None else None
                        err = f"Failed to fetch FitGirl page after retries. HTTP Status: {status}. Last error: {scrape_err}"
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": err}).encode())
                        return

                # drive.online-fix.me direct folder URL
                elif "drive.online-fix.me" in url and "/download/" not in url:
                    add_log(f"Scraping drive.online-fix.me folder: {url}")
                    h_headers = {
                        "Referer": "https://online-fix.me/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    response = requests.get(url, headers=h_headers, timeout=20, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_el = soup.find('title') or soup.find(class_='card-header')
                        raw_title = title_el.text.strip() if title_el else "Online-Fix Drive Game"
                        title = raw_title.replace("Online-Fix Drive |", "").strip()
                        title, version = clean_and_parse_title(title)
                        
                        files = []
                        for a in soup.find_all('a', onclick=True):
                            onclick = a.get('onclick', '')
                            match = re.search(r"openDownloadModal\s*\(\s*event\s*,\s*'([^']+)'\s*\)", onclick)
                            if match:
                                download_url = match.group(1)
                                filename = a.text.strip()
                                
                                file_type = "game_part"
                                filename_lower = filename.lower()
                                if "setup" in filename_lower or filename_lower.endswith(".exe"):
                                    file_type = "installer"
                                elif "optional" in filename_lower or "selective" in filename_lower or "language" in filename_lower or "lang" in filename_lower or any(lang in filename_lower for lang in ["russian", "english", "french", "german", "spanish", "chinese", "brazilian", "japanese", "korean", "polish", "mexican", "italian", "greek", "portuguese"]):
                                    file_type = "lang_part"
                                    
                                cached_size = sizes_cache.get(filename, 0)
                                files.append({
                                    "filename": filename,
                                    "url": download_url,
                                    "type": file_type,
                                    "status": "waiting",
                                    "progress": 0,
                                    "downloaded": 0,
                                    "size": cached_size,
                                    "speed": 0,
                                    "time_left": -1,
                                    "error": ""
                                })
                        
                        files.sort(key=lambda x: natural_sort_key(x["filename"]))
                        prefill_part_sizes(files)
                        
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
                    else:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": False, "error": f"Failed to fetch drive page. HTTP Status: {response.status_code}"}).encode())
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
                            
                        # Find hoster URL and direct Google Drive URL
                        hoster_url = None
                        gdrive_url = None
                        for a in soup.find_all('a', href=True):
                            href = a['href']
                            if "hosters.online-fix.me" in href:
                                hoster_url = href
                            elif "drive.online-fix.me" in href:
                                gdrive_url = href
                                
                        if not hoster_url and not gdrive_url:
                            self.send_response(400)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "No download links (hosters or drive) found on this page."}).encode())
                            return
                            
                        mirrors = []
                        if gdrive_url:
                            mirrors.append({
                                "name": "Use Own Google Disk",
                                "url": gdrive_url,
                                "num_files": 1
                            })
                            
                        if hoster_url:
                            # Fetch hoster page to parse mirrors
                            add_log(f"Fetching hosters page: {hoster_url}")
                            h_headers = {
                                "Referer": url
                            }
                            h_response = cf_requests.get(hoster_url, headers=h_headers, impersonate="chrome120", timeout=20, verify=False)
                            if h_response.status_code == 200:
                                h_soup = BeautifulSoup(h_response.text, 'html.parser')
                                options_container = h_soup.find(id='optionsContainer') or h_soup.find(class_='options-container')
                                if options_container:
                                    options = options_container.find_all(class_='option')
                                    for opt in options:
                                        name = opt.text.strip()
                                        encoded_url = f"online-fix-hoster:{hoster_url}?mirror={urllib.parse.quote(name)}&referer={urllib.parse.quote(url)}"
                                        data_links_str = opt.get('data-links', '[]')
                                        try:
                                            num_files = len(json.loads(data_links_str))
                                        except Exception:
                                            num_files = 0
                                        mirrors.append({
                                            "name": name,
                                            "url": encoded_url,
                                            "num_files": num_files
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
                        size_val = "Unknown"
                        
                        story = soup.find(class_='full-story-content')
                        if story:
                            text = story.get_text()
                            match = re.search(r'(?:Информация о игре:|Информация об игре:)\s*(.*?)(?=(?:Файлы для игры:|Как запускать:|Скачать с|1\.|$))', text, re.DOTALL | re.IGNORECASE)
                            if match:
                                description = match.group(1).strip()
                                
                            # Search for size inside story text
                            size_match = re.search(r'(?:Размер|Size|Размер раздачи):\s*([0-9.,]+\s*(?:GB|MB|ГБ|МБ|Gb|Mb|гб|мб))', text, re.IGNORECASE)
                            if size_match:
                                size_val = size_match.group(1).strip()
                                
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
                            
                        # If size not found in story, search entire soup text as fallback
                        if size_val == "Unknown":
                            size_match = re.search(r'(?:Размер|Size|Размер раздачи):\s*([0-9.,]+\s*(?:GB|MB|ГБ|МБ|Gb|Mb|гб|мб))', soup.get_text(), re.IGNORECASE)
                            if size_match:
                                size_val = size_match.group(1).strip()

                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True,
                            "type": "fitgirl_page",
                            "title": title,
                            "version": version,
                            "original_size": size_val,
                            "repack_size": size_val,
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
                    add_log(f"Loading paste via curl_cffi: {url}")
                    headers = {
                        'X-Requested-With': 'JSONHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                    # Prefer DoH-resolved IP for paste host (common DNS blocks)
                    # curl_cffi 0.15: curl_options belongs on Session, not request()/get() kwargs
                    paste_host = urllib.parse.urlparse(url).hostname or "paste.fitgirl-repacks.site"
                    _doh_cache.pop(paste_host, None)
                    paste_ip = resolve_doh(paste_host)
                    if paste_ip:
                        add_log(f"PrivateBin DNS via DoH: {paste_host} -> {paste_ip}")

                    last_err = None
                    resp = None
                    for attempt in range(3):
                        try:
                            session_kwargs = {}
                            if paste_ip:
                                session_kwargs["curl_options"] = {
                                    CurlOpt.RESOLVE: [f"{paste_host}:443:{paste_ip}", f"{paste_host}:80:{paste_ip}"]
                                }
                            with cf_requests.Session(**session_kwargs) as paste_sess:
                                resp = paste_sess.get(
                                    url,
                                    headers=headers,
                                    impersonate="chrome120",
                                    timeout=45,
                                )
                            break
                        except Exception as pe:
                            last_err = pe
                            add_log(f"PrivateBin fetch attempt {attempt + 1}/3 failed: {pe}")
                            _doh_cache.pop(paste_host, None)
                            paste_ip = resolve_doh(paste_host)
                            time.sleep(0.6 * (attempt + 1))
                    if resp is None:
                        raise Exception(
                            f"Cannot reach PrivateBin mirror ({paste_host}). "
                            f"DNS/network blocked. Try another hoster mirror or enable WARP/VPN. "
                            f"Details: {last_err}"
                        )
                    if resp.status_code != 200:
                        raise Exception(f"PrivateBin server returned status code {resp.status_code}")
                    
                    from privatebinapi.download import decrypt_paste, extract_passphrase
                    data = resp.json()
                    res_paste = decrypt_paste(data, extract_passphrase(url))
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
                if files:
                    files.sort(key=lambda x: natural_sort_key(x["filename"]))
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
                
                # Path: base / Game Title / CloudProvider
                # Parts from different clouds stay in separate folders.
                provider_sub = safe_folder_name(active_mirror)
                if provider_sub:
                    computed_dir = os.path.join(
                        base_download_dir, safe_folder_name(game_title), provider_sub
                    )
                else:
                    computed_dir = os.path.join(base_download_dir, safe_folder_name(game_title))
                
                with state_lock:
                    state["game_title"] = game_title
                    state["base_download_dir"] = os.path.abspath(base_download_dir)
                    state["download_dir"] = os.path.abspath(computed_dir)
                    state["files"] = SafeList(files)
                    state["active_mirror"] = active_mirror
                    state["original_size"] = data.get("original_size", "").strip()
                    state["is_configured"] = True
                    state["is_running"] = False
                    state["should_stop"] = False
                    state["active_index"] = -1
                    state["total_speed"] = 0
                    state["is_extracted"] = False
                    state["is_extracting"] = False
                    state["extraction_progress"] = 0
                    state["gofile_proxy"] = data.get("gofile_proxy", False)
                    
                initialize_queue_on_disk()
                save_session_state()
                
                add_log(f"Configured download for: {game_title}")
                add_log(f"Save directory: {state['download_dir']}  (Game / {provider_sub or 'default'})")
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
                state["files"] = SafeList()
                state["download_dir"] = ""
                state["base_download_dir"] = ""
                state["original_size"] = ""
                state["is_configured"] = False
                state["is_running"] = False
                state["should_stop"] = False
                state["active_index"] = -1
                state["total_speed"] = 0
                state["total_progress"] = 0
                state["is_extracted"] = False
                state["is_extracting"] = False
                state["extraction_progress"] = 0
            
            # Clean up the session state file
            try:
                if os.path.exists(session_state_path):
                    os.remove(session_state_path)
            except Exception:
                pass
                
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
                    # Separate folder per cloud: base/Game/Provider
                    provider_sub = safe_folder_name(new_mirror)
                    new_download_dir = os.path.abspath(
                        os.path.join(
                            base_download_dir,
                            safe_folder_name(game_title),
                            provider_sub if provider_sub else "",
                        )
                    )
                    state["download_dir"] = new_download_dir
                    
                    # Optionally delete ONLY the previous provider's folder (never the whole game)
                    if (
                        delete_old
                        and old_download_dir
                        and os.path.exists(old_download_dir)
                        and old_download_dir != new_download_dir
                    ):
                        import shutil
                        try:
                            # Safety: only delete if it looks like a provider subfolder under the game
                            game_root = os.path.abspath(
                                os.path.join(base_download_dir, safe_folder_name(game_title))
                            )
                            if os.path.dirname(old_download_dir) == game_root:
                                shutil.rmtree(old_download_dir)
                                add_log(f"Deleted previous provider folder: {old_download_dir}")
                        except Exception as delete_err:
                            add_log(f"Warning: Failed to delete old provider folder: {delete_err}")
                            
                    new_files_map = {f["filename"]: f for f in files}
                    updated_files = []
                    for f in state["files"]:
                        fn = f["filename"]
                        if fn in new_files_map:
                            new_info = new_files_map[fn]
                            f["url"] = new_info["url"]
                            # Fresh progress for this cloud folder; disk scan restores local partials
                            f["status"] = "waiting"
                            f["downloaded"] = 0
                            f["progress"] = 0
                            f["error"] = ""
                            if new_info.get("size", 0) > 0:
                                f["size"] = new_info["size"]
                        updated_files.append(f)
                    state["files"] = SafeList(updated_files)
                    
                    os.makedirs(new_download_dir, exist_ok=True)
                    state["should_stop"] = False
                
                initialize_queue_on_disk()
                
                if was_running:
                    with state_lock:
                        state["is_running"] = True
                        workers_to_start = get_effective_max_workers()
                        add_log(f"Resuming download with new provider: {new_mirror}")
                        for _ in range(workers_to_start):
                            threading.Thread(target=download_worker, daemon=True).start()
                            
                add_log(f"Switched provider → {new_mirror}. Folder: {state['download_dir']}")
                
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
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    server_address = ('127.0.0.1', port)
    httpd = ThreadingHTTPServer(server_address, APIRequestHandler)
    print(f"Web server running at http://localhost:{port}")
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
    load_session_state()
    if os.path.exists("warp_skipped.txt"):
        state["warp_status"] = "skipped"
    else:
        threading.Thread(target=check_and_install_warp, daemon=True).start()
    start_server()
