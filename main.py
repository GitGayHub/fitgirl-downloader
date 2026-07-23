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
    "warp_status": "checking",  # checking|installing|installed|error|skipped
    "warp_error_message": "",
    "warp_connected": False,
    "warp_last_rotate_ts": 0,
    "warp_rotating": False,
    # Bumped after auto IP rotate — download workers reconnect streams
    "reconnect_gen": 0,
    "pixeldrain_limit_reached": False,
    "gofile_proxy": False,
    "gdrive_accounts": [],
    "active_gdrive_account": "",
    "gdrive_session_cookies": {},
    "gdrive_client_id": "",
    "gdrive_client_secret": "",
    "original_size": "",
    # High-speed multi-mirror keep-alive:
    # catalog[mirror][filename] = page/direct url from Online-Fix hosters
    "mirror_catalog": {},
    # ranked preferred mirrors by measured MiB/s (best first)
    "mirror_rank": [],
    "mirror_speeds": {},  # mirror -> bytes/sec sample
    "high_speed_mode": True,
    # sustained below this → treat as throttled / bad host
    "min_acceptable_speed": 2 * 1024 * 1024,  # 2 MiB/s
    # track which mirrors already failed for a given filename this session
    "file_mirror_blacklist": {},  # filename -> [mirror names]
    # Optional Turnstile solver key (CapSolver CAP-... or 2Captcha)
    "captcha_api_key": "",
    "captcha_provider": "",  # capsolver | 2captcha | auto
    # Post-download smart pipeline
    "post_download_running": False,
    "post_download_status": "",  # checking|extracting|ready|needs_install|incomplete|...
    "post_download_message": "",
    "post_download_report": {},
}

state_lock = threading.RLock()
extraction_lock = threading.Lock()
gdrive_oauth_lock = threading.Lock()
warp_rotate_lock = threading.Lock()
_speed_watchdog_started = False

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
                "average_download_speed": state.get("average_download_speed", 5000000.0),
                "original_size": state.get("original_size", ""),
                "is_extracted": state.get("is_extracted", False),
                "mirror_catalog": state.get("mirror_catalog") or {},
                "mirror_rank": state.get("mirror_rank") or [],
                "mirror_speeds": state.get("mirror_speeds") or {},
                "high_speed_mode": bool(state.get("high_speed_mode", True)),
                "min_acceptable_speed": int(state.get("min_acceptable_speed", 2 * 1024 * 1024)),
                "pixeldrain_limit_reached": bool(state.get("pixeldrain_limit_reached", False)),
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
                state["is_extracted"] = bool(data.get("is_extracted", False))
                state["mirror_catalog"] = data.get("mirror_catalog") or {}
                state["mirror_rank"] = data.get("mirror_rank") or []
                state["mirror_speeds"] = data.get("mirror_speeds") or {}
                state["high_speed_mode"] = bool(data.get("high_speed_mode", True))
                state["min_acceptable_speed"] = int(
                    data.get("min_acceptable_speed", 2 * 1024 * 1024)
                )
                state["pixeldrain_limit_reached"] = bool(
                    data.get("pixeldrain_limit_reached", False)
                )
                state["file_mirror_blacklist"] = {}

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

def get_warp_cli():
    """Locate warp-cli.exe (PATH or standard Cloudflare install dirs)."""
    import shutil
    candidates = [
        shutil.which("warp-cli"),
        r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe",
        r"C:\Program Files (x86)\Cloudflare\Cloudflare WARP\warp-cli.exe",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    # Last resort: shallow search under Cloudflare Program Files
    for root in (
        r"C:\Program Files\Cloudflare",
        r"C:\Program Files (x86)\Cloudflare",
    ):
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            if "warp-cli.exe" in files:
                return os.path.join(dirpath, "warp-cli.exe")
    return None


def is_warp_available():
    return get_warp_cli() is not None


def _warp_run(cli, args, timeout=30):
    try:
        return subprocess.run(
            [cli] + list(args),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as e:
        class _R:
            returncode = 1
            stdout = ""
            stderr = str(e)
        return _R()


def get_warp_connection_info():
    """Return {installed, connected, status_text, cli}."""
    cli = get_warp_cli()
    if not cli:
        return {
            "installed": False,
            "connected": False,
            "status_text": "Not installed",
            "cli": None,
        }
    res = _warp_run(cli, ["status"], timeout=15)
    out = (res.stdout or "") + "\n" + (res.stderr or "")
    connected = "Status update: Connected" in out or (
        "Connected" in out and "Disconnected" not in out.split("Status update:")[-1][:80]
    )
    if "Registration Missing" in out or "Unable" in out:
        connected = False
    return {
        "installed": True,
        "connected": connected,
        "status_text": "Connected" if connected else "Installed (not connected)",
        "cli": cli,
        "raw": out[:500],
    }


def ensure_warp_connected(cli=None):
    """Register (if needed) + connect WARP. Returns True if Connected."""
    cli = cli or get_warp_cli()
    if not cli:
        return False
    info = get_warp_connection_info()
    if info.get("connected"):
        return True
    add_log("WARP: Ensuring registration and connection...")
    # registration new is idempotent-ish; ignore failures if already registered
    _warp_run(cli, ["registration", "new"], timeout=60)
    _warp_run(cli, ["mode", "warp"], timeout=15)
    _warp_run(cli, ["connect"], timeout=30)
    for _ in range(15):
        time.sleep(1)
        info = get_warp_connection_info()
        if info.get("connected"):
            add_log("WARP: Connected.")
            with state_lock:
                state["warp_status"] = "installed"
                state["warp_connected"] = True
            return True
    add_log("WARP: Failed to reach Connected state.")
    with state_lock:
        state["warp_connected"] = False
    return False


def get_effective_max_workers():
    """Pixeldrain free tier: max concurrent downloads per IP is low — stay at 1
    only while the *active* queue still uses pixeldrain URLs.
    After failover to Viking/Gofile/etc, allow full parallelism.
    """
    with state_lock:
        active_urls = [
            (f.get("url") or "")
            for f in state.get("files", [])
            if f.get("status") in ("waiting", "connecting", "downloading", "copying")
        ]
        if any("pixeldrain.com" in u for u in active_urls):
            return 1
        if state.get("active_mirror") and "pixeldrain" in state["active_mirror"].lower():
            # mirror label still Pixeldrain but URLs may have failed over
            if any("pixeldrain.com" in u for u in active_urls) or not active_urls:
                # if all remaining non-finished still on PD → 1 worker
                unfinished = [
                    f for f in state.get("files", [])
                    if f.get("status") not in ("finished",)
                ]
                if unfinished and all("pixeldrain.com" in (f.get("url") or "") for f in unfinished):
                    return 1
        return state.get("max_workers", 4)


def _hoster_name_from_url(url: str) -> str:
    u = (url or "").lower()
    if "pixeldrain.com" in u:
        return "Pixeldrain"
    if "gofile.io" in u:
        return "Gofile"
    if "vikingfile.com" in u or "vik1ngfile.site" in u or "cloudflarestorage" in u:
        return "VikingFile"
    if "rootz.so" in u or "rootz.cc" in u:
        return "Rootz"
    if "fileditch" in u:
        return "FileDitch"
    if "datanodes" in u:
        return "DataNodes"
    if "fuckingfast" in u:
        return "FuckingFast"
    if "drive.online-fix.me" in u or "drive.google.com" in u:
        return "GoogleDrive"
    return "Unknown"


def resolve_direct_link_for_probe(page_url: str):
    """Resolve hoster page → real CDN URL (used by speed probe)."""
    if not page_url:
        return None
    # Already a direct/binary endpoint
    if "pixeldrain.com/api/file/" in page_url:
        return page_url
    if "pixeldrain.com/u/" in page_url:
        return page_url.replace("pixeldrain.com/u/", "pixeldrain.com/api/file/")
    try:
        if "fuckingfast.co" in page_url:
            return extract_direct_link(page_url)
        if "datanodes.to" in page_url:
            return extract_datanodes_link(page_url)
        if "fileditchfiles.me" in page_url or "fileditch.com" in page_url:
            return extract_fileditch_link(page_url)
        if "gofile.io" in page_url:
            link = extract_gofile_link(page_url)
            if link and not str(link).startswith("ERROR_"):
                return link
            return None
        if "rootz.so" in page_url or "rootz.cc" in page_url:
            link = extract_rootz_link(page_url)
            if link and not str(link).startswith("ERROR_"):
                return link
            return None
        if "vikingfile.com" in page_url or "vik1ngfile.site" in page_url:
            link = extract_viking_link(page_url)
            if link and not str(link).startswith("ERROR_"):
                return link
            return None
        # Assume already direct (CDN, S3, etc.)
        if page_url.startswith("http"):
            return page_url
    except Exception as e:
        add_log(f"resolve_direct_link_for_probe error: {e}")
    return None


def probe_url_speed(page_or_direct_url: str, seconds: float = 12.0, max_bytes: int = 20 * 1024 * 1024):
    """Download a sample after resolving the real CDN link. Returns dict with bps/mib."""
    direct = resolve_direct_link_for_probe(page_or_direct_url)
    if not direct:
        return {"success": False, "error": "Could not resolve direct link", "bps": 0.0, "mib": 0.0, "direct": ""}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Range": f"bytes=0-{max_bytes - 1}",
    }
    # Gofile token cookie if we have one
    if "gofile.io" in direct:
        tok = state.get("gofile_account_token")
        if tok:
            headers["Cookie"] = f"accountToken={tok}"
    t0 = time.time()
    total = 0
    status = 0
    try:
        resp = requests.get(direct, headers=headers, stream=True, timeout=25)
        status = resp.status_code
        if status not in (200, 206):
            body = ""
            try:
                body = resp.content[:300].decode("utf-8", "replace")
            except Exception:
                pass
            resp.close()
            return {
                "success": False,
                "error": f"HTTP {status}: {body[:120]}",
                "bps": 0.0,
                "mib": 0.0,
                "direct": direct,
                "http_status": status,
            }
        ctype = (resp.headers.get("content-type") or "").lower()
        if "text/html" in ctype:
            resp.close()
            return {
                "success": False,
                "error": "Got HTML instead of binary (extractor missed CDN URL)",
                "bps": 0.0,
                "mib": 0.0,
                "direct": direct,
            }
        for chunk in resp.iter_content(256 * 1024):
            if not chunk:
                break
            total += len(chunk)
            if time.time() - t0 >= seconds or total >= max_bytes:
                break
        resp.close()
    except Exception as e:
        return {"success": False, "error": str(e), "bps": 0.0, "mib": 0.0, "direct": direct or ""}
    elapsed = max(0.001, time.time() - t0)
    bps = total / elapsed
    return {
        "success": total > 64 * 1024,  # at least 64KB to count as real
        "error": "" if total > 64 * 1024 else f"Only got {total} bytes",
        "bps": bps,
        "mib": bps / (1024 * 1024),
        "bytes": total,
        "seconds": elapsed,
        "direct": direct,
        "http_status": status,
        "hoster": _hoster_name_from_url(direct),
    }


def register_mirror_catalog(catalog: dict, speeds: dict | None = None, rank: list | None = None):
    """catalog: {MirrorName: {filename: url}} or {MirrorName: [filedicts]}"""
    normalized = {}
    for name, payload in (catalog or {}).items():
        fmap = {}
        if isinstance(payload, dict):
            # either filename->url or already nested
            for k, v in payload.items():
                if isinstance(v, str):
                    fmap[k] = v
                elif isinstance(v, dict) and v.get("url"):
                    fmap[v.get("filename") or k] = v["url"]
        elif isinstance(payload, list):
            for item in payload:
                if not isinstance(item, dict):
                    continue
                fn = item.get("filename")
                url = item.get("url")
                if fn and url:
                    fmap[fn] = url
        if fmap:
            normalized[name] = fmap
    with state_lock:
        state["mirror_catalog"] = normalized
        if speeds is not None:
            state["mirror_speeds"] = {k: float(v) for k, v in speeds.items()}
        if rank is not None:
            state["mirror_rank"] = list(rank)
        elif speeds:
            state["mirror_rank"] = sorted(
                speeds.keys(), key=lambda m: float(speeds.get(m) or 0), reverse=True
            )
    save_session_state()
    add_log(
        f"[SPEED] Registered mirror catalog: {list(normalized.keys())} "
        f"rank={state.get('mirror_rank')}"
    )


def pick_failover_url(filename: str, current_url: str):
    """Pick next-best mirror URL for the same filename (same download folder, just swap URL)."""
    if not state.get("high_speed_mode", True):
        return None, None
    catalog = state.get("mirror_catalog") or {}
    if not catalog:
        return None, None
    rank = list(state.get("mirror_rank") or [])
    speeds = state.get("mirror_speeds") or {}
    # append any mirrors not in rank
    for m in catalog.keys():
        if m not in rank:
            rank.append(m)
    # When Pixeldrain free limit is active, demote it hard
    if state.get("pixeldrain_limit_reached"):
        rank = [m for m in rank if "pixeldrain" not in m.lower()] + [
            m for m in rank if "pixeldrain" in m.lower()
        ]
    blacklist = set((state.get("file_mirror_blacklist") or {}).get(filename) or [])
    cur_host = _hoster_name_from_url(current_url)
    blacklist.add(cur_host)
    cur_bps = float(speeds.get(cur_host) or speeds.get(state.get("active_mirror") or "") or 0)
    # Prefer measured rank; skip dead/broken free hosts for auto
    candidates = []
    for mirror in rank:
        if mirror in blacklist:
            continue
        ml = mirror.lower()
        if "google" in ml or "own" in ml:
            continue
        # Gofile Online-Fix folders need premium (API error-notPremium)
        if "gofile" in ml:
            continue
        # FileDitch on OF often only has fix packs / HTML gate — not full multi-part
        if "fileditch" in ml:
            continue
        # Viking: captcha can be solved (Playwright token/POST or CapSolver/2Captcha key)
        # Keep it available — zero sample speed no longer means unusable
        bps = float(speeds.get(mirror) or 0)
        fmap = catalog.get(mirror) or {}
        url = fmap.get(filename)
        if not url or url == current_url:
            continue
        candidates.append((mirror, url, bps))

    # Only switch if alternate is meaningfully faster than current sample,
    # OR current host is hard-blocked (0 bps / PD limit with near-zero speed).
    for mirror, url, bps in candidates:
        if bps <= 0:
            continue
        if cur_bps > 0 and bps < cur_bps * 1.15:
            # not faster — skip (don't trade 1.0 MiB/s PD for 0.13 Rootz)
            continue
        return mirror, url

    # Hard block path: no useful current speed → take best positive alternate even if slow
    if cur_bps < 80_000:  # < ~80 KB/s
        best = None
        for mirror, url, bps in candidates:
            if bps <= 0:
                continue
            if best is None or bps > best[2]:
                best = (mirror, url, bps)
        if best:
            return best[0], best[1]
    return None, None


def apply_file_failover(index: int, reason: str) -> bool:
    """Swap file URL to next mirror in-place (keeps path for resume). Returns True if swapped."""
    with state_lock:
        if index < 0 or index >= len(state["files"]):
            return False
        f = state["files"][index]
        filename = f.get("filename") or ""
        current = f.get("url") or ""
        cur_host = _hoster_name_from_url(current)
        bl = state.setdefault("file_mirror_blacklist", {})
        bl.setdefault(filename, [])
        if cur_host not in bl[filename]:
            bl[filename].append(cur_host)
    mirror, url = pick_failover_url(filename, current)
    if not mirror or not url:
        add_log(f"[SPEED] No failover mirror left for {filename} ({reason})")
        return False
    with state_lock:
        if index < len(state["files"]):
            state["files"][index]["url"] = url
            state["files"][index]["error"] = ""
            # stay waiting/connecting so worker retries
            if state["files"][index].get("status") not in ("finished",):
                state["files"][index]["status"] = "waiting"
            # active_mirror label: keep original for UI, but log host switch
    save_session_state()
    add_log(
        f"[SPEED] Failover {filename}: {cur_host} → {mirror} ({reason}). "
        f"Resume from disk at same path."
    )
    # Spawn extra workers if we left Pixeldrain constraint
    try:
        with state_lock:
            if state.get("is_running"):
                needed = get_effective_max_workers() - state.get("active_workers_count", 0)
                if needed > 0:
                    for _ in range(needed):
                        threading.Thread(target=download_worker, daemon=True).start()
    except Exception:
        pass
    return True

def rotate_warp_ip():
    """Disconnect/reconnect WARP to obtain a new egress IP (resets Pixeldrain free quota)."""
    add_log("Attempting to rotate IP using Cloudflare WARP...")
    warp_cli = get_warp_cli()
    if not warp_cli:
        add_log(
            "WARP CLI not found. Install Cloudflare WARP from Settings "
            "(or allow the startup installer)."
        )
        return False

    try:
        # Ensure registered/connected once, then cycle disconnect→connect for new IP
        ensure_warp_connected(warp_cli)

        add_log("WARP: Disconnecting for IP rotation (hold 6s for new egress)...")
        _warp_run(warp_cli, ["disconnect"], timeout=30)
        time.sleep(6)

        add_log("WARP: Reconnecting...")
        _warp_run(warp_cli, ["connect"], timeout=30)

        for _ in range(20):
            time.sleep(1)
            info = get_warp_connection_info()
            if info.get("connected"):
                add_log("WARP: Reconnected successfully with a new IP!")
                with state_lock:
                    state["pixeldrain_limit_reached"] = False
                    state["warp_connected"] = True
                    state["warp_status"] = "installed"
                    state["warp_last_rotate_ts"] = time.time()
                    state["reconnect_gen"] = int(state.get("reconnect_gen") or 0) + 1
                clear_pixeldrain_cookies()
                return True

        # One more hard reset attempt
        add_log("WARP: First reconnect timed out — trying registration + connect...")
        _warp_run(warp_cli, ["registration", "new"], timeout=60)
        _warp_run(warp_cli, ["connect"], timeout=30)
        for _ in range(15):
            time.sleep(1)
            if get_warp_connection_info().get("connected"):
                add_log("WARP: Connected after re-registration.")
                with state_lock:
                    state["pixeldrain_limit_reached"] = False
                    state["warp_connected"] = True
                    state["warp_status"] = "installed"
                    state["warp_last_rotate_ts"] = time.time()
                    state["reconnect_gen"] = int(state.get("reconnect_gen") or 0) + 1
                clear_pixeldrain_cookies()
                return True

        add_log("WARP: Reconnection timed out.")
        return False
    except Exception as e:
        add_log(f"WARP: Failed to rotate IP: {e}")
        return False


def try_auto_warp_rotate(
    reason: str, min_interval_sec: float = 25.0, force: bool = False
) -> bool:
    """Single-flight auto rotate when Pixeldrain free-tier caps speed (~1 MiB/s).

    Called from download workers AND background speed watchdog — only one rotate
    runs at a time. On success bumps reconnect_gen so open streams reconnect.

    force=True: ignore cooldown (manual UI / Settings button).
    """
    if not is_warp_available():
        add_log(f"[AUTO-WARP] Skip rotate ({reason}): WARP not installed.")
        return False

    # Non-blocking: if another rotate is in progress, skip (caller should wait on gen)
    if not warp_rotate_lock.acquire(blocking=False):
        add_log(f"[AUTO-WARP] Rotate already in progress ({reason}) — wait for reconnect_gen.")
        return False

    try:
        with state_lock:
            last = float(state.get("warp_last_rotate_ts") or 0)
            remaining = min_interval_sec - (time.time() - last)
            if not force and remaining > 0:
                add_log(
                    f"[AUTO-WARP] Cooldown {remaining:.0f}s left ({reason}) — "
                    f"will retry after cooldown (not 'no WARP')."
                )
                return False
            if state.get("warp_rotating"):
                return False
            state["warp_rotating"] = True
            state["pixeldrain_limit_reached"] = True

        add_log(f"[AUTO-WARP] Rotating IP now. Reason: {reason} force={force}")
        ok = rotate_warp_ip()
        if ok:
            add_log(
                "[AUTO-WARP] IP rotated OK. Download workers will reconnect streams "
                f"(reconnect_gen={state.get('reconnect_gen')})."
            )
        else:
            add_log("[AUTO-WARP] IP rotate FAILED — will keep trying on next throttle window.")
        return ok
    finally:
        with state_lock:
            state["warp_rotating"] = False
        try:
            warp_rotate_lock.release()
        except Exception:
            pass


def wait_for_warp_rotate_or_do(
    reason: str, min_interval_sec: float = 25.0, wait_sec: int = 55
) -> bool:
    """Ensure a WARP rotate happens: do it, or wait for in-flight/cooldown rotate.

    Always preferred over the misleading 'No WARP' reconnect path.
    """
    if not is_warp_available():
        return False

    with state_lock:
        gen0 = int(state.get("reconnect_gen") or 0)

    if try_auto_warp_rotate(reason, min_interval_sec=min_interval_sec):
        return True

    # Wait for another thread's rotate, or cooldown to expire then force
    deadline = time.time() + wait_sec
    while time.time() < deadline:
        with state_lock:
            gen = int(state.get("reconnect_gen") or 0)
            rotating = bool(state.get("warp_rotating"))
            last = float(state.get("warp_last_rotate_ts") or 0)
        if gen != gen0:
            add_log(f"[AUTO-WARP] Saw reconnect_gen {gen0}→{gen} while waiting ({reason}).")
            return True
        if not rotating and (time.time() - last) >= min_interval_sec:
            if try_auto_warp_rotate(f"{reason} (after wait)", min_interval_sec=min_interval_sec):
                return True
        time.sleep(1)

    # Last resort: force through cooldown
    add_log(f"[AUTO-WARP] Force-rotate after wait timeout ({reason}).")
    return try_auto_warp_rotate(f"{reason} (force)", min_interval_sec=0, force=True)


def is_pixeldrain_throttle_speed(speed_bps: float) -> bool:
    """True if speed looks like Pixeldrain free-tier throttle / dead link.

    Free PD typically sits ~1.0–1.15 MiB/s when quota is exhausted, but can also
    drop near-zero during connect storms / soft blocks. Treat everything from
    a few KB/s up to ~1.25 MiB/s as "need IP rotate" while actively downloading.
    """
    if speed_bps is None:
        return False
    s = float(speed_bps)
    # ~8 KB/s .. 1.25 MiB/s  (was 200KB+ only — missed 0.04 MiB/s dead crawl)
    return (8 * 1024) <= s <= (1.25 * 1024 * 1024)


def bulk_failover_unfinished_to_mirror(mirror_name: str = "Rootz") -> int:
    """Rewrite unfinished file URLs to another hoster from mirror_catalog.

    Keeps the same download_dir so partials resume. Used when Pixeldrain free-cap
    survives multiple WARP rotates (WARP IP pool also throttled).
    """
    catalog = (state.get("mirror_catalog") or {}).get(mirror_name) or {}
    if not catalog:
        add_log(f"[ESCAPE] No catalog entries for mirror {mirror_name}.")
        return 0

    switched = 0
    with state_lock:
        # Stop current workers so they re-pick with new URLs
        state["should_stop"] = True
        state["is_running"] = False
        for f in state.get("files") or []:
            if f.get("status") == "finished":
                continue
            fn = f.get("filename") or ""
            url = catalog.get(fn)
            if not url:
                continue
            old = f.get("url") or ""
            if url == old:
                continue
            f["url"] = url
            if f.get("status") in ("downloading", "connecting", "failed", "copying"):
                f["status"] = "waiting"
                f["speed"] = 0
                f["error"] = ""
            switched += 1
        if switched:
            state["active_mirror"] = f"{mirror_name} (auto-escape PD)"
            state["max_workers"] = max(int(state.get("max_workers") or 4), 4)
            state["pixeldrain_limit_reached"] = False
            # clear PD blacklists so Rootz is clean
            state["file_mirror_blacklist"] = {}

    if switched:
        add_log(
            f"[ESCAPE] Switched {switched} unfinished file(s) → {mirror_name}. "
            f"Same folder for resume. Workers={state.get('max_workers')}."
        )
        save_session_state()
        time.sleep(1.5)
        with state_lock:
            state["should_stop"] = False
            state["is_running"] = True
            n = get_effective_max_workers()
            for _ in range(n):
                threading.Thread(target=download_worker, daemon=True).start()
        add_log(f"[ESCAPE] Resumed with {get_effective_max_workers()} parallel workers.")
    return switched


def speed_watchdog_loop():
    """Background: WARP-rotate on PD free-cap; after repeated fails → escape to Rootz."""
    add_log("[AUTO-WARP] Speed watchdog started (auto-rotate + multi-host escape).")
    throttle_streak = 0
    samples = []  # last N total_speed samples while PD active
    pd_escape_strikes = 0  # free-cap windows that survived a WARP rotate
    last_escape_ts = 0.0
    while True:
        try:
            time.sleep(2)
            with state_lock:
                running = bool(state.get("is_running"))
                files = list(state.get("files") or [])
                total_spd = float(state.get("total_speed") or 0)
                rotating = bool(state.get("warp_rotating"))

            if not running or rotating:
                throttle_streak = 0
                samples = []
                continue

            pd_active = any(
                f.get("status") == "downloading"
                and "pixeldrain.com" in (f.get("url") or "").lower()
                for f in files
            )
            if not pd_active:
                # Not on PD anymore — reset escape counter slowly
                throttle_streak = 0
                samples = []
                if total_spd > 2 * 1024 * 1024:
                    pd_escape_strikes = 0
                continue

            samples.append(total_spd)
            if len(samples) > 20:
                samples = samples[-20:]

            if is_pixeldrain_throttle_speed(total_spd):
                throttle_streak += 1
            else:
                if total_spd > 1.5 * 1024 * 1024:
                    throttle_streak = 0
                    pd_escape_strikes = 0
                else:
                    throttle_streak = max(0, throttle_streak - 1)

            # ~16s sustained free-cap
            if throttle_streak >= 8 and len(samples) >= 6:
                recent = samples[-8:]
                avg = sum(recent) / max(1, len(recent))
                if is_pixeldrain_throttle_speed(avg):
                    gen_before = int(state.get("reconnect_gen") or 0)
                    wait_for_warp_rotate_or_do(
                        f"watchdog: avg {avg/1024/1024:.2f} MiB/s for ~{throttle_streak*2}s",
                        min_interval_sec=20,
                        wait_sec=45,
                    )
                    # Observe speed 25s after rotate
                    time.sleep(25)
                    with state_lock:
                        spd2 = float(state.get("total_speed") or 0)
                        gen_after = int(state.get("reconnect_gen") or 0)
                    if is_pixeldrain_throttle_speed(spd2) or spd2 < 1.3 * 1024 * 1024:
                        pd_escape_strikes += 1
                        add_log(
                            f"[ESCAPE] Still throttled after WARP "
                            f"(spd={spd2/1024/1024:.2f} MiB/s, strikes={pd_escape_strikes}, "
                            f"gen {gen_before}→{gen_after})."
                        )
                    else:
                        pd_escape_strikes = 0
                        add_log(
                            f"[AUTO-WARP] Recovered after rotate: {spd2/1024/1024:.2f} MiB/s"
                        )

                    # After 2 failed recoveries → Rootz multi-worker escape
                    if pd_escape_strikes >= 2 and (time.time() - last_escape_ts) > 120:
                        n = bulk_failover_unfinished_to_mirror("Rootz")
                        if n > 0:
                            last_escape_ts = time.time()
                            pd_escape_strikes = 0
                        else:
                            # try Viking if Rootz catalog empty
                            bulk_failover_unfinished_to_mirror("VikingFile")
                            last_escape_ts = time.time()
                            pd_escape_strikes = 0

                    throttle_streak = 0
                    samples = []
        except Exception as e:
            try:
                add_log(f"[AUTO-WARP] Watchdog error: {e}")
            except Exception:
                pass
            time.sleep(5)


def ensure_speed_watchdog():
    global _speed_watchdog_started
    if _speed_watchdog_started:
        return
    _speed_watchdog_started = True
    threading.Thread(target=speed_watchdog_loop, daemon=True, name="speed-watchdog").start()


def check_and_install_warp(force=False):
    """Detect / install / connect Cloudflare WARP for Pixeldrain free-limit bypass.

    force=True: ignore warp_skipped.txt (Settings → Install button).
    """
    add_log("Checking Cloudflare WARP status...")
    with state_lock:
        state["warp_status"] = "checking"
        state["warp_error_message"] = ""

    warp_cli = get_warp_cli()
    if warp_cli:
        with state_lock:
            state["warp_status"] = "installed"
        add_log("Cloudflare WARP is installed — connecting if needed...")
        ok = ensure_warp_connected(warp_cli)
        with state_lock:
            state["warp_connected"] = bool(ok)
            state["warp_status"] = "installed"
        return True

    # Respect skip only for *auto* install at startup
    if not force and os.path.exists("warp_skipped.txt"):
        with state_lock:
            state["warp_status"] = "skipped"
        add_log("WARP auto-install skipped (user chose Skip earlier). Install from Settings anytime.")
        return False

    add_log("Cloudflare WARP not detected. Initializing silent installation...")
    with state_lock:
        state["warp_status"] = "installing"

    try:
        msi_url = "https://1111-releases.cloudflareclient.com/windows/Cloudflare_WARP_Release-x64.msi"
        temp_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "fg_warp")
        os.makedirs(temp_dir, exist_ok=True)
        msi_path = os.path.join(temp_dir, "warp.msi")

        add_log(f"Downloading WARP installer from {msi_url}...")
        r = requests.get(msi_url, stream=True, timeout=120, verify=False)
        r.raise_for_status()
        with open(msi_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=256 * 1024):
                if chunk:
                    f.write(chunk)
        add_log("Download complete. Triggering silent installation (may show UAC)...")

        installed_ok = False
        res_execute = 0
        try:
            import ctypes
            res_execute = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", "msiexec", f'/i "{msi_path}" /qn /norestart', None, 1
            )
            add_log(f"UAC elevation request returned code: {res_execute}")
        except Exception as shell_err:
            add_log(f"ShellExecuteW elevation request failed: {shell_err}")
            res_execute = 0

        # Also try winget non-interactive (works if already elevated / allowed)
        if res_execute <= 32:
            try:
                add_log("Trying winget install Cloudflare.Warp ...")
                wg = subprocess.run(
                    [
                        "winget",
                        "install",
                        "--id",
                        "Cloudflare.Warp",
                        "-e",
                        "--accept-package-agreements",
                        "--accept-source-agreements",
                        "--disable-interactivity",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                add_log(f"winget exit={wg.returncode}")
            except Exception as wg_err:
                add_log(f"winget install failed: {wg_err}")

        # Wait for warp-cli to appear (install can take a while)
        for check_sec in range(90):
            time.sleep(1)
            warp_cli = get_warp_cli()
            if warp_cli:
                installed_ok = True
                break

        if installed_ok:
            # Clear skip flag after successful install
            try:
                if os.path.exists("warp_skipped.txt"):
                    os.remove("warp_skipped.txt")
            except Exception:
                pass
            with state_lock:
                state["warp_status"] = "installed"
            add_log("Cloudflare WARP installed successfully — connecting...")
            ensure_warp_connected(warp_cli)
            return True

        if res_execute <= 32:
            err_msg = (
                "Cloudflare WARP not installed. Silent install needs Administrator (UAC). "
                "Approve the UAC prompt, or install from Settings → Download WARP, "
                "or: winget install Cloudflare.Warp"
            )
        else:
            err_msg = (
                "Silent installation did not finish in time. Approve UAC if shown, "
                "or install manually: https://1111-releases.cloudflareclient.com/windows/Cloudflare_WARP_Release-x64.msi"
            )
        add_log("Silent installation failed: WARP could not be installed.")
        with state_lock:
            state["warp_status"] = "error"
            state["warp_error_message"] = err_msg
        return False

    except Exception as e:
        err_msg = f"Failed to download or install WARP: {str(e)}"
        add_log(err_msg)
        with state_lock:
            state["warp_status"] = "error"
            state["warp_error_message"] = err_msg
        return False

def clear_pixeldrain_cookies():
    """Clears local cookie jars / chrome profile cookies used for Pixeldrain tracking."""
    add_log("Clearing Pixeldrain cookies and browser profile session state...")
    try:
        s = requests.Session()
        s.cookies.clear()
        s.close()
    except Exception as e:
        add_log(f"Error clearing requests cookies: {e}")
        
    try:
        if hasattr(cf_requests, "cookies") and hasattr(cf_requests.cookies, "clear"):
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
    """FileDitch / fileditchfiles — often already a direct CDN URL from Online-Fix hosters.

    Strategies:
      1) URL already looks like direct file host → use as-is
      2) curl_cffi page scrape for Download button / CDN hrefs
      3) Playwright fallback for JS-rendered pages
    """
    try:
        add_log(f"Extracting direct link for FileDitch: {page_url}")
        u = (page_url or "").strip()
        low = u.lower()
        # Already a direct file URL from OF data-links
        if any(
            x in low
            for x in (
                "fileditchfiles.me/",
                "fileditchfiles.st/",
                "fileditch.com/",
            )
        ) and not low.rstrip("/").endswith(
            (".html", "/download", "/d")
        ):
            # path with hash-like segment + filename
            if re.search(r"/[a-f0-9]{8,}/[^/]+\.(rar|zip|7z|bin|exe|iso)", low):
                add_log("FileDitch: URL already looks direct — using as-is.")
                return u

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
            "Referer": "https://online-fix.me/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = cf_requests.get(
            u, headers=headers, impersonate="chrome120", timeout=25, verify=False
        )
        if response.status_code != 200:
            add_log(f"Error: FileDitch responded with status code {response.status_code}")
            # still try playwright
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            candidates = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = (a.get_text() or "").strip().lower()
                href_l = href.lower()
                if any(x in text for x in ("download", "скачать", "⬇")):
                    candidates.append(href)
                if any(
                    x in href_l
                    for x in (
                        "fileditchfiles",
                        ".rar",
                        ".zip",
                        ".7z",
                        "download",
                        "getfile",
                    )
                ):
                    candidates.append(href)
            # absolute-ize
            for href in candidates:
                full = urllib.parse.urljoin(u, href)
                if full.startswith("http") and "javascript:" not in full.lower():
                    add_log("Successfully extracted FileDitch direct link!")
                    return full
            match = re.search(
                r'href=["\'](https?://[^"\']*fileditch[^"\']+)["\']',
                response.text,
                re.I,
            )
            if match:
                add_log("FileDitch: regex CDN hit.")
                return match.group(1)
            match = re.search(
                r'href=["\']([^"\']+\.(?:rar|zip|7z|bin|exe))["\']',
                response.text,
                re.I,
            )
            if match:
                return urllib.parse.urljoin(u, match.group(1))

        # Playwright fallback for JS pages
        with extraction_lock:
            from playwright.sync_api import sync_playwright

            add_log("FileDitch: Playwright fallback...")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
                )
                page = browser.new_page()
                try:
                    page.goto(u, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(3000)
                    for sel in (
                        "a:has-text('Download')",
                        "a:has-text('download')",
                        "a[href*='fileditch']",
                        "a[href*='.rar']",
                    ):
                        loc = page.locator(sel)
                        if loc.count() > 0:
                            href = loc.first.get_attribute("href")
                            if href:
                                browser.close()
                                add_log("FileDitch: Playwright link OK.")
                                return urllib.parse.urljoin(u, href)
                except Exception as e:
                    add_log(f"FileDitch Playwright error: {e}")
                browser.close()

        add_log("Error: Direct link button not found in FileDitch HTML.")
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

# VikingFile Cloudflare Turnstile sitekey (from their page JS)
VIKING_TURNSTILE_SITEKEY = "0x4AAAAAAAgbsMNBuk2d3Qp6"
# file_id -> (cdn_url, expiry_unix)
_viking_link_cache = {}


def _viking_file_id(url: str):
    m = re.search(r"/f/([A-Za-z0-9_-]+)", url or "")
    return m.group(1) if m else None


def _viking_normalize_page_url(page_url: str) -> str:
    """vikingfile.com redirects to vik1ngfile.site — normalize to host that accepts POST."""
    u = (page_url or "").strip()
    fid = _viking_file_id(u)
    if fid:
        return f"https://vik1ngfile.site/f/{fid}"
    if "vikingfile.com" in u:
        return u.replace("vikingfile.com", "vik1ngfile.site")
    return u


def _viking_post_turnstile_token(page_url: str, token: str, cookie_header: str = ""):
    """After Turnstile solve: POST cf-turnstile-response to file page → JSON.link CDN URL.

    Site JS (custom-*.js):
      xhr.open("POST", window.location.href)
      xhr.send("cf-turnstile-response=" + token)
      // response.link  (NOT direct-link — old code was wrong)
    """
    url = _viking_normalize_page_url(page_url)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://vik1ngfile.site",
        "Referer": url,
        "Accept": "application/json, text/plain, */*",
    }
    if cookie_header:
        headers["Cookie"] = cookie_header
    try:
        # Prefer curl_cffi chrome impersonation (better TLS fingerprint)
        try:
            r = cf_requests.post(
                url,
                data={"cf-turnstile-response": token},
                headers=headers,
                impersonate="chrome120",
                timeout=30,
                verify=False,
            )
        except Exception:
            r = requests.post(
                url,
                data={"cf-turnstile-response": token},
                headers=headers,
                timeout=30,
                verify=False,
            )
        if r.status_code != 200:
            add_log(f"VikingFile: token POST HTTP {r.status_code}: {r.text[:160]}")
            return None
        data = r.json()
        link = data.get("link") or data.get("direct-link") or data.get("url")
        if link:
            return link
        err = data.get("error") or data.get("message") or r.text[:120]
        add_log(f"VikingFile: token POST no link: {err}")
        return None
    except Exception as e:
        add_log(f"VikingFile: token POST exception: {e}")
        return None


def _solve_turnstile_external(sitekey: str, page_url: str):
    """Optional paid/free solvers via API key (CapSolver or 2Captcha).

    Keys (first found wins):
      state['captcha_api_key'] / env CAPSOLVER_API_KEY / env TWOCAPTCHA_API_KEY
    """
    api_key = (
        (state.get("captcha_api_key") or "").strip()
        or os.environ.get("CAPSOLVER_API_KEY", "").strip()
        or os.environ.get("TWOCAPTCHA_API_KEY", "").strip()
        or os.environ.get("CAPTCHA_API_KEY", "").strip()
    )
    if not api_key:
        return None

    page_url = _viking_normalize_page_url(page_url)

    # CapSolver
    if api_key.startswith("CAP-") or os.environ.get("CAPSOLVER_API_KEY") or state.get("captcha_provider") == "capsolver":
        try:
            add_log("VikingFile: Solving Turnstile via CapSolver...")
            create = requests.post(
                "https://api.capsolver.com/createTask",
                json={
                    "clientKey": api_key if not api_key.startswith("CAP-") else api_key,
                    "task": {
                        "type": "AntiTurnstileTaskProxyLess",
                        "websiteURL": page_url,
                        "websiteKey": sitekey,
                    },
                },
                timeout=30,
            ).json()
            task_id = create.get("taskId")
            if not task_id:
                # try with CAP- key as-is
                create = requests.post(
                    "https://api.capsolver.com/createTask",
                    json={
                        "clientKey": api_key,
                        "task": {
                            "type": "AntiTurnstileTaskProxyLess",
                            "websiteURL": page_url,
                            "websiteKey": sitekey,
                        },
                    },
                    timeout=30,
                ).json()
                task_id = create.get("taskId")
            if not task_id:
                add_log(f"VikingFile: CapSolver createTask failed: {create}")
            else:
                for _ in range(40):
                    time.sleep(3)
                    res = requests.post(
                        "https://api.capsolver.com/getTaskResult",
                        json={"clientKey": api_key, "taskId": task_id},
                        timeout=30,
                    ).json()
                    if res.get("status") == "ready":
                        tok = (res.get("solution") or {}).get("token")
                        if tok:
                            add_log("VikingFile: CapSolver token OK.")
                            return tok
                    if res.get("status") == "failed" or res.get("errorId"):
                        add_log(f"VikingFile: CapSolver failed: {res}")
                        break
        except Exception as e:
            add_log(f"VikingFile: CapSolver exception: {e}")

    # 2Captcha Turnstile
    try:
        add_log("VikingFile: Solving Turnstile via 2Captcha...")
        in_url = (
            "http://2captcha.com/in.php"
            f"?key={api_key}&method=turnstile&sitekey={sitekey}"
            f"&pageurl={urllib.parse.quote(page_url)}&json=1"
        )
        created = requests.get(in_url, timeout=30).json()
        if created.get("status") != 1:
            add_log(f"VikingFile: 2Captcha in.php failed: {created}")
            return None
        req_id = created.get("request")
        for _ in range(40):
            time.sleep(5)
            polled = requests.get(
                f"http://2captcha.com/res.php?key={api_key}&action=get&id={req_id}&json=1",
                timeout=30,
            ).json()
            if polled.get("status") == 1:
                tok = polled.get("request")
                if tok:
                    add_log("VikingFile: 2Captcha token OK.")
                    return tok
            if polled.get("request") not in ("CAPCHA_NOT_READY", "CAPTCHA_NOT_READY"):
                if polled.get("status") == 0 and "NOT_READY" not in str(polled.get("request")):
                    add_log(f"VikingFile: 2Captcha error: {polled}")
                    break
    except Exception as e:
        add_log(f"VikingFile: 2Captcha exception: {e}")
    return None


def extract_viking_link(page_url):
    """Resolve VikingFile page → CDN link.

    Flow reverse-engineered from their frontend:
      1) Cloudflare Turnstile (sitekey 0x4AAAAAAAgbsMNBuk2d3Qp6)
      2) POST same URL with cf-turnstile-response=<token>
      3) JSON { "link": "https://...cdn..." }

    Strategies:
      A) Cache hit
      B) External solver (CapSolver / 2Captcha) if API key set
      C) Playwright stealth: wait for token in DOM → POST ourselves
      D) Playwright: capture POST JSON.response.link (field name was wrong before!)
    """
    with extraction_lock:
        add_log(f"Extracting VikingFile direct link for: {page_url}")
        page_url = _viking_normalize_page_url(page_url)
        fid = _viking_file_id(page_url)

        # A) Cache
        if fid and fid in _viking_link_cache:
            link, exp = _viking_link_cache[fid]
            if time.time() < exp and link:
                add_log("VikingFile: Using cached CDN link.")
                return link

        def _cache(link):
            if fid and link:
                _viking_link_cache[fid] = (link, time.time() + 6 * 3600)
            return link

        # B) External Turnstile solver
        try:
            token = _solve_turnstile_external(VIKING_TURNSTILE_SITEKEY, page_url)
            if token:
                link = _viking_post_turnstile_token(page_url, token)
                if link:
                    add_log("Successfully extracted VikingFile link via captcha solver!")
                    return _cache(link)
        except Exception as e:
            add_log(f"VikingFile: external solver path error: {e}")

        # C+D) Playwright multi-attempt
        from playwright.sync_api import sync_playwright

        launch_attempts = [
            {"headless": True, "channel": None},
            {"headless": True, "channel": "chrome"},
            {"headless": False, "channel": "chrome"},
        ]

        try:
            with sync_playwright() as p:
                for attempt in launch_attempts:
                    found_link = [None]
                    found_token = [None]
                    try:
                        launch_kwargs = {
                            "headless": attempt["headless"],
                            "args": [
                                "--disable-blink-features=AutomationControlled",
                                "--no-sandbox",
                                "--disable-dev-shm-usage",
                                "--disable-infobars",
                            ],
                        }
                        if attempt.get("channel"):
                            launch_kwargs["channel"] = attempt["channel"]
                        try:
                            browser = p.chromium.launch(**launch_kwargs)
                        except Exception as launch_err:
                            add_log(f"VikingFile: launch skip {attempt}: {launch_err}")
                            continue

                        context = browser.new_context(
                            user_agent=(
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                            ),
                            locale="en-US",
                            viewport={"width": 1400, "height": 900},
                        )
                        page = context.new_page()
                        page.add_init_script(
                            """
                            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                            window.chrome = { runtime: {} };
                            Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
                            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                            """
                        )

                        def on_response(response):
                            try:
                                if response.request.method != "POST":
                                    return
                                u = response.url or ""
                                if "vik1ngfile.site" not in u and "vikingfile.com" not in u:
                                    return
                                data = response.json()
                                # CRITICAL: real field is "link", old code looked for "direct-link"
                                dl = (
                                    data.get("link")
                                    or data.get("direct-link")
                                    or data.get("url")
                                )
                                if dl:
                                    found_link[0] = dl
                            except Exception:
                                pass

                        page.on("response", on_response)

                        try:
                            page.goto(page_url, wait_until="domcontentloaded", timeout=45000)
                        except Exception as e:
                            add_log(f"VikingFile navigation warning: {e}")

                        # Wait up to 50s: auto-turnstile token OR network JSON link
                        for sec in range(50):
                            if found_link[0]:
                                break
                            try:
                                tok = page.evaluate(
                                    """() => {
                                        const el = document.querySelector('[name="cf-turnstile-response"]');
                                        if (el && el.value && el.value.length > 20) return el.value;
                                        const el2 = document.querySelector('#cf-chl-widget-response, textarea[name="cf-turnstile-response"]');
                                        if (el2 && el2.value && el2.value.length > 20) return el2.value;
                                        return '';
                                    }"""
                                )
                                if tok and len(tok) > 20:
                                    found_token[0] = tok
                                    break
                            except Exception:
                                pass
                            # poke turnstile iframe
                            try:
                                for frame in page.frames:
                                    fu = frame.url or ""
                                    if "challenges.cloudflare.com" in fu:
                                        try:
                                            frame.locator("body").click(timeout=300)
                                        except Exception:
                                            pass
                            except Exception:
                                pass
                            page.wait_for_timeout(1000)

                        # If we got a token but no network link yet — POST ourselves
                        if not found_link[0] and found_token[0]:
                            cookies = context.cookies()
                            cookie_header = "; ".join(
                                f"{c['name']}={c['value']}" for c in cookies
                            )
                            add_log("VikingFile: Turnstile token captured — POSTing for CDN link...")
                            found_link[0] = _viking_post_turnstile_token(
                                page.url or page_url, found_token[0], cookie_header
                            )

                        # DOM fallback
                        if not found_link[0]:
                            try:
                                dl = page.locator("#download-link")
                                if dl.count() > 0:
                                    href = dl.get_attribute("href")
                                    if href and href.startswith("http"):
                                        found_link[0] = href
                            except Exception:
                                pass

                        browser.close()

                        if found_link[0]:
                            add_log(
                                f"Successfully extracted VikingFile link "
                                f"(attempt={attempt})!"
                            )
                            return _cache(found_link[0])
                    except Exception as e:
                        add_log(f"VikingFile attempt {attempt} error: {e}")
                        try:
                            browser.close()
                        except Exception:
                            pass

                add_log(
                    "VikingFile: Captcha not solved. Set CAPSOLVER_API_KEY or "
                    "TWOCAPTCHA_API_KEY (or Settings captcha key) for reliable bypass."
                )
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


def _is_bonus_content_header(line):
    """True for FitGirl 'Included Bonus Content / Soundtracks' section titles."""
    low = re.sub(r"\s+", " ", (line or "").strip().lower())
    low = low.lstrip("•·*-–— ").rstrip(":").strip()
    if not low:
        return False
    # e.g. Included Bonus Content (non-audio) / Included Bonus Content (Soundtracks)
    if re.match(
        r"^(included\s+)?bonus\s+(content|soundtracks?|osts?|materials?|extras?)(\s*\([^)]*\))?$",
        low,
    ):
        return True
    if re.match(
        r"^включ[её]нн\w*\s+бонусн\w*(\s+(контент|саундтрек\w*|материалы|дополнения))?(\s*\([^)]*\))?$",
        low,
    ):
        return True
    if "included bonus" in low and any(
        x in low for x in ("content", "soundtrack", "ost", "non-audio", "audio")
    ):
        return True
    return False


def _is_game_desc_resume_header(line):
    """Sections that end a bonus dump and resume real description (rare)."""
    low = re.sub(r"\s+", " ", (line or "").strip().lower()).rstrip(":")
    low = low.lstrip("•·*-–— ").strip()
    return low in (
        "game features",
        "features",
        "pc features",
        "about this game",
        "about the game",
        "story",
        "plot",
        "описание",
        "особенности игры",
        "системные требования",
        "system requirements",
    )


def _strip_bonus_soundtrack_section(text):
    """Remove Included Bonus Content / Soundtracks / OST dumps from Game Description.

    FitGirl often appends long bonus lists (PDFs, wallpapers, radio OST albums)
    after the actual story blurb — keep only the game description itself.
    """
    if not text:
        return text
    # Hard-cut from first bonus header to end (most pages put them last)
    patterns = [
        r"(?is)\n?\s*(?:•\s*)?included\s+bonus\s+content(?:\s*\([^)]*\))?\s*:?\s*\n.*$",
        r"(?is)\n?\s*(?:•\s*)?included\s+bonus\s+soundtracks?\s*:?\s*\n.*$",
        r"(?is)\n?\s*(?:•\s*)?bonus\s+soundtracks?\s*:?\s*\n.*$",
        r"(?is)\n?\s*(?:•\s*)?included\s+bonus\s+osts?\s*:?\s*\n.*$",
        r"(?is)\n?\s*(?:•\s*)?bonus\s+content(?:\s*\([^)]*\))?\s*:?\s*\n.*$",
        r"(?is)\n?\s*(?:•\s*)?включ[её]нн\w*\s+бонусн\w*.*$",
    ]
    out = text
    for pat in patterns:
        out = re.sub(pat, "", out)
    # Line-wise skip for headers mid-block (or if regex missed)
    lines = out.split("\n")
    cleaned = []
    skip_mode = False
    for ln in lines:
        stripped = ln.strip()
        if _is_bonus_content_header(stripped):
            skip_mode = True
            continue
        if skip_mode:
            if _is_game_desc_resume_header(stripped):
                skip_mode = False
                cleaned.append(ln)
            # drop bonus bullets / album names / file counts
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
                        all_ok = all(f.get("status") == "finished" for f in state["files"]) if state["files"] else False
                        if all_ok:
                            add_log("🎉 ALL DOWNLOADS COMPLETED SUCCESSFULLY!")
                        else:
                            add_log("Download queue idle (some files may have failed).")
                    break
                    
                file_info = state["files"][target_idx]
                
            success = download_file(target_idx, file_info)
            
            with state_lock:
                if not success:
                    if state["should_stop"]:
                        break
                    time.sleep(5)
            # After each successful file, check if entire queue is done → auto extract
            if success:
                maybe_auto_extract_if_complete()
    finally:
        with state_lock:
            state["active_workers_count"] -= 1
            if state["active_workers_count"] <= 0:
                state["is_running"] = False
                state["total_speed"] = 0
                state["should_stop"] = False
        # Last worker out: try auto-extract once more
        maybe_auto_extract_if_complete()

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
    speed_window = []  # last N 1s samples for throttle detection
    proxy_server = None
    
    # If using proxy for Gofile:
    if "gofile.io" in page_url and state.get("gofile_proxy", False):
        proxy_server = get_working_gofile_proxy()
        
    while True:
        with state_lock:
            stream_gen = int(state.get("reconnect_gen") or 0)

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
                # Official PD API: transfer_limit_exceeded / download_limit_exceeded /
                # ip_download_limited_captcha_required / file_rate_limited_captcha_required
                add_log(
                    "[WARNING] Pixeldrain free-tier HARD limit (HTTP) — auto WARP rotate..."
                )
                response.close()
                clear_pixeldrain_cookies()
                # 1) Auto WARP IP rotation (script-driven, no human watcher)
                if try_auto_warp_rotate("pixeldrain HTTP limit response", min_interval_sec=30):
                    time.sleep(2)
                    continue
                # 2) Failover this file to next-fastest hoster (keep local partial)
                if apply_file_failover(index, "pixeldrain hard limit"):
                    return False  # worker will pick file again with new URL
                with state_lock:
                    if index < len(state["files"]):
                        state["files"][index]["status"] = "failed"
                        state["files"][index]["error"] = (
                            "Pixeldrain free limit reached and no alternate mirror "
                            "available. Enable WARP/VPN, wait 24h, or premium."
                        )
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
            reconnect_requested = False
            
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
                        # Watchdog / other worker rotated WARP → drop stream and reopen
                        if int(state.get("reconnect_gen") or 0) != stream_gen:
                            reconnect_requested = True
                            
                    if reconnect_requested:
                        response.close()
                        add_log(
                            f"[AUTO-WARP] Reconnect gen changed — reopening stream for {filename} "
                            f"from byte {downloaded}."
                        )
                        break
                            
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
                            
                            # --- Pixeldrain free-cap auto-detect (in worker) ---
                            # Classic free throttle sits ~1.00–1.15 MiB/s constantly.
                            is_pd = "pixeldrain.com" in (direct_link or "")
                            if is_pd:
                                speed_window.append(speed)
                                if len(speed_window) > 25:
                                    speed_window = speed_window[-25:]
                                if is_pixeldrain_throttle_speed(speed):
                                    low_speed_seconds += int(elapsed)
                                elif speed > 1.5 * 1024 * 1024:
                                    low_speed_seconds = 0
                                    speed_window = []
                                # Sustained ~1 MiB/s for 12s with window avg also in band
                                if low_speed_seconds >= 12 and len(speed_window) >= 10:
                                    avg = sum(speed_window[-12:]) / min(12, len(speed_window))
                                    if is_pixeldrain_throttle_speed(avg):
                                        if curr_time - last_low_speed_warning_time > 30:
                                            last_low_speed_warning_time = curr_time
                                            add_log(
                                                f"[AUTO-WARP] Worker saw sustained PD free-cap: "
                                                f"now {speed/1024/1024:.2f} MiB/s, "
                                                f"avg {avg/1024/1024:.2f} MiB/s over {low_speed_seconds}s"
                                            )
                                        throttled_trigger = True
                                        break
                            else:
                                dead_floor = 80 * 1024
                                if speed < dead_floor:
                                    low_speed_seconds += int(elapsed)
                                    if low_speed_seconds >= 30:
                                        throttled_trigger = True
                                        break
                                else:
                                    low_speed_seconds = 0
                                    
                            bytes_in_sec = 0
                            last_time = curr_time
                            
            try:
                response.close()
            except Exception:
                pass
            
            if reconnect_requested:
                # New IP already applied by rotate; just reopen stream
                low_speed_seconds = 0
                speed_window = []
                time.sleep(1)
                continue

            if throttled_trigger:
                clear_pixeldrain_cookies()
                # Script MUST auto-rotate WARP on free-cap — never leave user clicking forever
                if "pixeldrain.com" in (direct_link or "") and is_warp_available():
                    rotated = wait_for_warp_rotate_or_do(
                        f"worker free-cap on {filename}",
                        min_interval_sec=20,
                        wait_sec=50,
                    )
                    add_log(
                        f"[AUTO-WARP] Reconnecting stream after rotate attempt "
                        f"(ok={rotated}, gen={state.get('reconnect_gen')})..."
                    )
                    time.sleep(2)
                    low_speed_seconds = 0
                    speed_window = []
                    continue
                # No WARP installed → try other hosters only then
                if apply_file_failover(index, f"sustained low speed on {_hoster_name_from_url(direct_link)}"):
                    with state_lock:
                        if index < len(state["files"]):
                            state["files"][index]["status"] = "waiting"
                            state["files"][index]["speed"] = 0
                    return False
                # IMPORTANT: do NOT break the download loop — that falsely marks the file finished.
                add_log(
                    "[AUTO-WARP] WARP missing and no alternate mirror — "
                    "reconnecting (install WARP in Settings for auto IP rotate)."
                )
                low_speed_seconds = 0
                speed_window = []
                time.sleep(2)
                continue
                    
            # Normal completion of this HTTP stream (server closed / EOF)
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

    # Incomplete stream (throttle reconnect path, server hang, etc.) — resume later
    if total_size > 0 and downloaded < total_size * 0.995:
        add_log(
            f"Incomplete download for {filename}: {downloaded}/{total_size} bytes "
            f"({100.0 * downloaded / total_size:.1f}%). Will retry/resume."
        )
        with state_lock:
            if index < len(state["files"]):
                state["files"][index]["status"] = "waiting"
                state["files"][index]["downloaded"] = downloaded
                state["files"][index]["progress"] = min(99, int((downloaded / total_size) * 100))
                state["files"][index]["speed"] = 0
                state["files"][index]["error"] = "Incomplete — resuming"
        save_session_state()
        return False
        
    if file_id and "drive.online-fix.me" in page_url and access_token:
        add_log(f"GDrive: Automatically deleting temporary copy {filename} from Google Drive...")
        delete_gdrive_file(file_id, access_token)
        
    # Mark complete only when fully on disk
    with state_lock:
        if index < len(state["files"]):
            state["files"][index]["status"] = "finished"
            state["files"][index]["progress"] = 100
            state["files"][index]["downloaded"] = downloaded if downloaded > 0 else state["files"][index].get("downloaded", 0)
            if total_size > 0:
                state["files"][index]["size"] = total_size
            state["files"][index]["speed"] = 0
            state["files"][index]["error"] = ""
    recalculate_total_progress()
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

def _looks_like_extracted_game(download_dir):
    """Detect FitGirl .bin setup OR Online-Fix ready-to-play folder layout."""
    if not download_dir or not os.path.isdir(download_dir):
        return False
    try:
        entries = os.listdir(download_dir)
    except Exception:
        return False
    if any(e.lower().endswith(".bin") for e in entries):
        return True
    # Online-Fix FAQ: after unpack you get the game tree (not selective .bin parts)
    for e in entries:
        low = e.lower()
        if low.endswith(".rar") or re.search(r"\.part\d+\.rar$", low):
            continue
        path = os.path.join(download_dir, e)
        if os.path.isdir(path):
            try:
                sub = [x.lower() for x in os.listdir(path)]
            except Exception:
                continue
            if any(x.endswith(".exe") for x in sub) or "steam_api64.dll" in sub or "steam_api.dll" in sub:
                return True
            # nested game folder one level deeper
            for s in sub[:30]:
                sp = os.path.join(path, s)
                if os.path.isdir(sp):
                    try:
                        sub2 = [x.lower() for x in os.listdir(sp)]
                    except Exception:
                        continue
                    if any(x.endswith(".exe") for x in sub2) or "steam_api64.dll" in sub2:
                        return True
        if low.endswith(".exe") and "setup" not in low and "unins" not in low:
            return True
    return False


def _find_setup_exe(download_dir):
    if not download_dir or not os.path.isdir(download_dir):
        return None
    try:
        for f in os.listdir(download_dir):
            if f.lower().endswith(".exe") and "setup" in f.lower():
                return os.path.join(download_dir, f)
        for f in os.listdir(download_dir):
            if f.lower().endswith(".exe") and "unins" not in f.lower():
                # prefer setup-like names only for install step
                continue
    except Exception:
        return None
    return None


def analyze_post_download(download_dir=None, files=None):
    """Smart check: need extract? already unpacked? FitGirl vs Online-Fix? missing parts?

    Returns a dict used by auto pipeline + /api/post_download_check.
    """
    download_dir = download_dir or state.get("download_dir") or ""
    files = files if files is not None else list(state.get("files") or [])
    result = {
        "download_dir": download_dir,
        "all_downloads_finished": bool(files) and all(f.get("status") == "finished" for f in files),
        "file_count": len(files),
        "finished_count": sum(1 for f in files if f.get("status") == "finished"),
        "has_rar": False,
        "has_part01": False,
        "multipart": False,
        "missing_on_disk": [],
        "tiny_on_disk": [],
        "already_extracted": False,
        "needs_extract": False,
        "needs_install": False,
        "has_setup_exe": False,
        "setup_exe": None,
        "content_type": "unknown",  # online_fix | fitgirl | mixed | unknown
        "archives_to_extract": [],
        "message": "",
        "ready_to_play": False,
    }
    if not download_dir:
        result["message"] = "No download directory."
        return result

    names = [(f.get("filename") or "") for f in files]
    names_l = [n.lower() for n in names]
    of_hint = any("ofme" in n or "online-fix" in n or "onlinefix" in n for n in names_l)
    of_hint = of_hint or "online" in (state.get("active_mirror") or "").lower() or "rootz" in (
        state.get("active_mirror") or ""
    ).lower() or "pixeldrain" in (state.get("active_mirror") or "").lower()
    fg_hint = any(n.endswith(".bin") for n in names_l) or any("fitgirl" in n for n in names_l)

    rar_names = [n for n in names if n.lower().endswith(".rar")]
    result["has_rar"] = bool(rar_names)
    part_nums = []
    for n in rar_names:
        m = re.search(r"\.part(\d+)\.rar$", n, re.I)
        if m:
            part_nums.append(int(m.group(1)))
            if int(m.group(1)) == 1:
                result["has_part01"] = True
                result["archives_to_extract"].append(n)
        else:
            # single-volume rar (updates, fix packs)
            result["archives_to_extract"].append(n)
    result["multipart"] = bool(part_nums)
    if part_nums and 1 not in part_nums:
        result["message"] = "Multi-part RAR set without part01 — cannot start unpack."
        result["needs_extract"] = False

    # Disk presence / size sanity
    for f in files:
        fn = f.get("filename") or ""
        if not fn:
            continue
        path = os.path.join(download_dir, fn)
        if not os.path.isfile(path):
            result["missing_on_disk"].append(fn)
            continue
        try:
            sz = os.path.getsize(path)
        except OSError:
            result["missing_on_disk"].append(fn)
            continue
        expected = int(f.get("size") or 0)
        # tiny incomplete masquerading as finished
        if expected > 50 * 1024 * 1024 and sz < expected * 0.95:
            result["tiny_on_disk"].append({"filename": fn, "disk": sz, "expected": expected})
        elif expected <= 0 and fn.lower().endswith(".rar") and sz < 1024 * 1024:
            result["tiny_on_disk"].append({"filename": fn, "disk": sz, "expected": expected})

    already = _looks_like_extracted_game(download_dir)
    result["already_extracted"] = already
    setup = _find_setup_exe(download_dir)
    # also search after-extract dirs for setup
    if not setup and os.path.isdir(download_dir):
        try:
            for e in os.listdir(download_dir):
                p = os.path.join(download_dir, e)
                if os.path.isdir(p):
                    for f in os.listdir(p):
                        if f.lower().endswith(".exe") and "setup" in f.lower():
                            setup = os.path.join(p, f)
                            break
                if setup:
                    break
        except Exception:
            pass
    result["setup_exe"] = setup
    result["has_setup_exe"] = bool(setup)

    if of_hint and not fg_hint:
        result["content_type"] = "online_fix"
    elif fg_hint and not of_hint:
        result["content_type"] = "fitgirl"
    elif of_hint and fg_hint:
        result["content_type"] = "mixed"
    elif result["has_rar"]:
        # default: try OF password path first in worker anyway
        result["content_type"] = "online_fix" if result["multipart"] else "unknown"

    # Decision tree
    if not result["all_downloads_finished"]:
        result["message"] = (
            f"Downloads incomplete ({result['finished_count']}/{result['file_count']})."
        )
        result["needs_extract"] = False
    elif result["missing_on_disk"]:
        result["message"] = f"Missing on disk: {len(result['missing_on_disk'])} file(s)."
        result["needs_extract"] = False
    elif result["tiny_on_disk"]:
        result["message"] = (
            f"Incomplete files on disk (size mismatch): {len(result['tiny_on_disk'])}."
        )
        result["needs_extract"] = False
    elif already:
        result["needs_extract"] = False
        if result["content_type"] == "fitgirl" and result["has_setup_exe"]:
            result["needs_install"] = True
            result["message"] = "Already extracted — FitGirl setup.exe found (can install)."
            result["ready_to_play"] = False
        else:
            result["ready_to_play"] = True
            result["message"] = (
                "Already extracted — looks playable "
                f"({result['content_type']}). No unpack needed."
            )
    elif result["has_rar"] and result["archives_to_extract"]:
        result["needs_extract"] = True
        result["message"] = (
            f"Need unpack: {len(result['archives_to_extract'])} archive head(s) "
            f"(multipart={result['multipart']}, type={result['content_type']})."
        )
    elif result["has_setup_exe"]:
        result["needs_install"] = True
        result["message"] = "No RAR left to unpack; setup.exe present."
    else:
        result["message"] = "Complete download, but no clear extract/install target found."

    return result


def maybe_auto_extract_if_complete():
    """If queue is fully finished, run smart post-download pipeline (check → extract)."""
    with state_lock:
        if not state.get("files"):
            return
        if state.get("is_extracting"):
            return
        if state.get("post_download_running"):
            return
        statuses = [f.get("status") for f in state["files"]]
        if not statuses or any(s != "finished" for s in statuses):
            return
        state["post_download_running"] = True
    threading.Thread(target=post_download_smart_pipeline, daemon=True, name="post-dl").start()


def post_download_smart_pipeline():
    """Auto: analyze → extract if needed → re-check → report install/play ready."""
    try:
        with state_lock:
            state["post_download_status"] = "checking"
            state["post_download_message"] = "Analyzing finished download..."
        report = analyze_post_download()
        add_log(f"[AUTO-CHECK] {report.get('message')}")
        add_log(
            f"[AUTO-CHECK] finished={report['finished_count']}/{report['file_count']} "
            f"type={report['content_type']} needs_extract={report['needs_extract']} "
            f"already={report['already_extracted']} missing={len(report['missing_on_disk'])} "
            f"tiny={len(report['tiny_on_disk'])}"
        )
        with state_lock:
            state["post_download_report"] = report
            state["post_download_message"] = report.get("message") or ""

        if report.get("missing_on_disk") or report.get("tiny_on_disk"):
            with state_lock:
                state["post_download_status"] = "incomplete"
                state["is_extracted"] = False
            add_log("[AUTO-CHECK] Not starting extract — fix incomplete/missing files first.")
            return

        if report.get("already_extracted"):
            with state_lock:
                state["is_extracted"] = True
                state["post_download_status"] = (
                    "needs_install" if report.get("needs_install") else "ready"
                )
            if report.get("needs_install"):
                add_log(
                    f"[AUTO-CHECK] Extracted FitGirl pack — setup: {report.get('setup_exe')}"
                )
            else:
                add_log("[AUTO-CHECK] Game looks ready to play (Online-Fix style).")
            return

        if not report.get("needs_extract"):
            with state_lock:
                state["post_download_status"] = "noop"
            add_log("[AUTO-CHECK] No extraction required.")
            return

        add_log(
            "[AUTO] Starting extraction — "
            f"heads={report.get('archives_to_extract')} "
            f"(OF password online-fix.me tried first)..."
        )
        with state_lock:
            state["post_download_status"] = "extracting"
        extraction_worker()

        # Re-analyze after unpack
        report2 = analyze_post_download()
        with state_lock:
            state["post_download_report"] = report2
            state["post_download_message"] = report2.get("message") or ""
            state["is_extracted"] = bool(report2.get("already_extracted"))
            if report2.get("already_extracted"):
                if report2.get("needs_install"):
                    state["post_download_status"] = "needs_install"
                    add_log(
                        "[AUTO] Unpack done — FitGirl setup detected. "
                        "Use Install button (not auto-launched)."
                    )
                else:
                    state["post_download_status"] = "ready"
                    add_log(
                        "[AUTO] Unpack done — Online-Fix/game content ready to play "
                        "(password was online-fix.me if protected)."
                    )
            else:
                state["post_download_status"] = "extract_uncertain"
                add_log(
                    "[AUTO] Unpack finished but game markers not clearly found — check folder manually."
                )
    except Exception as e:
        add_log(f"[AUTO-CHECK] Pipeline error: {e}")
        with state_lock:
            state["post_download_status"] = "error"
            state["post_download_message"] = str(e)
    finally:
        with state_lock:
            state["post_download_running"] = False
        try:
            save_session_state()
        except Exception:
            pass


def extraction_worker():
    """Background thread worker to extract split RAR volumes using unrar.exe.

    Online-Fix FAQ: the only archive password is online-fix.me
    Multi-part: unpack only part01 / first volume; other parts follow automatically.
    """
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
    
    # Prefer smart list from analyzer (part01 + single-volume only)
    report = analyze_post_download(download_dir, list(state.get("files") or []))
    archives_to_extract = []
    for filename in report.get("archives_to_extract") or []:
        if re.search(r"\.part(\d+)\.rar$", filename, re.I):
            archives_to_extract.append((filename, f"Archive Part 1: {filename}"))
        else:
            archives_to_extract.append((filename, f"Single Archive: {filename}"))

    if not archives_to_extract:
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
        
    # Online-Fix FAQ password; also works on unprotected FitGirl RARs with modern unrar
    of_password = "online-fix.me"
    # Prefer OF password when content looks like Online-Fix; still try both
    prefer_of = report.get("content_type") in ("online_fix", "mixed", "unknown")

    for filename, label in archives_to_extract:
        archive_path = os.path.join(download_dir, filename)
        if not os.path.exists(archive_path):
            add_log(f"Skip missing archive head: {filename}")
            continue
            
        add_log(f"Unpacking {label}... This may take a while...")
        
        try:
            cmds = [
                [unrar_path, "x", "-y", f"-p{of_password}", archive_path],
                [unrar_path, "x", "-y", archive_path],
            ]
            if not prefer_of:
                cmds = list(reversed(cmds))
            ok = False
            for cmd in cmds:
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
                    ok = True
                    break
                else:
                    add_log(f"Unpacker exit {process.returncode} for {label} (cmd={' '.join(cmd[1:4])}…); trying next strategy if any.")
            if not ok:
                add_log(f"Failed to unpack {label} with all strategies.")
        except Exception as e:
            add_log(f"Exception during extraction of {label}: {str(e)}")
            
    with state_lock:
        state["is_extracting"] = False
        state["extraction_progress"] = 100
        state["is_extracted"] = _looks_like_extracted_game(download_dir)
        
    add_log("Extraction workflow complete!")
    if state.get("is_extracted"):
        add_log("[AUTO] Game content detected after unpack. Ready to launch installer / play (Online-Fix is usually already playable).")

def clean_size(size_str):
    if not size_str:
        return "Unknown"
    s = re.sub(r'^from\s+', '', size_str, flags=re.IGNORECASE)
    s = re.sub(r'\s*\[Selective\s+Download[^\]]*\]', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\(\s*Selective\s+Download[^\)]*\)', '', s, flags=re.IGNORECASE)
    # FitGirl get_text often glues next section: "55/55.1 GB Download Mirrors..."
    s = re.sub(
        r'\s+(?:Download\s+Mirrors?|Filehoster|Genres?/Tags?|Companies?|Languages?|Repack\s+Size|Original\s+Size).*$',
        '',
        s,
        flags=re.IGNORECASE,
    )
    s = s.strip(" \t,;|")
    # Selective dual size "55/55.1 GB" → "55–55.1 GB" (not progress-looking)
    m = re.match(
        r'^([\d]+(?:[.,][\d]+)?)\s*/\s*([\d]+(?:[.,][\d]+)?)\s*([A-Za-z]+)?\s*$',
        s,
    )
    if m:
        unit = (m.group(3) or "GB").strip()
        s = f"{m.group(1)}–{m.group(2)} {unit}"
    return s.strip() or "Unknown"

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

def _steam_movie_play_urls(movie):
    """Build browser-playable trailer URLs from a Steam appdetails movie entry.

    Modern appdetails often only returns DASH/HLS — classic CDN mp4/webm still
    works via movie id: /steam/apps/{movie_id}/movie_max.mp4 etc.
    Prefer short microtrailer for autoplay cycle, then 480p, then max.
    """
    if not isinstance(movie, dict):
        return []
    urls = []
    # Prefer explicit mp4/webm maps when present (legacy payload)
    for container in ("mp4", "webm"):
        block = movie.get(container) or {}
        if isinstance(block, dict):
            for key in ("480", "max"):
                u = (block.get(key) or "").strip()
                if u:
                    if u.startswith("//"):
                        u = "https:" + u
                    urls.append(u)
    mid = movie.get("id")
    if mid:
        base = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{mid}/"
        # microtrailer first (short loop-friendly cycle), then progressive mp4
        for name in ("microtrailer.webm", "movie480.mp4", "movie_max.mp4"):
            urls.append(base + name)
    # de-dupe preserve order
    seen = set()
    out = []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def fetch_steam_metadata(game_title):
    import urllib.request, urllib.parse, json, re, unicodedata
    # Clean the title slightly to improve search match
    search_query = game_title or ""
    # Replace common unicode replacements and curly quotes
    search_query = search_query.replace('\ufffd', "'").replace('’', "'").replace('‘', "'")
    # Fold accents: Ragnarök → Ragnarok (NOT Ragnark — keep base letters)
    search_query = unicodedata.normalize("NFKD", search_query)
    search_query = "".join(ch for ch in search_query if not unicodedata.combining(ch))
    # Keep letters/digits/spaces/simple punctuation (unicode letters via \w after ascii fold)
    search_query = re.sub(r"[^\w\s'\-:]", " ", search_query, flags=re.UNICODE)
    search_query = re.sub(r"\s+", " ", search_query).strip()
    # Strip year from search query (e.g. "Game 2024" -> "Game") to improve search success
    search_query = re.sub(r'\b\d{4}\b', '', search_query).strip()
    # Drop common FitGirl noise for better Steam match
    search_query = re.sub(
        r'\b(repack|fitgirl|v\d+(\.\d+)*|update|dlc|bonus)\b',
        '',
        search_query,
        flags=re.I,
    ).strip()
    # Secondary query without subtitle after colon if primary fails
    alt_query = search_query.split(":")[0].strip() if ":" in search_query else ""

    def _search(term):
        if not term:
            return None
        url = 'https://store.steampowered.com/api/storesearch/?term=' + urllib.parse.quote(term) + '&l=english&cc=US'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10).read()
        return json.loads(res)
    
    try:
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API Search Query: '{search_query}' (original: '{game_title}')\n")
        data = _search(search_query)
        if (not data or not data.get("items")) and alt_query and alt_query != search_query:
            with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
                f_dbg.write(f"Steam API retry alt query: '{alt_query}'\n")
            data = _search(alt_query)
        with open("steam_debug.log", "a", encoding="utf-8") as f_dbg:
            f_dbg.write(f"Steam API search results: {list(data.keys()) if data else 'Empty'}\n")
            if data and data.get('items'):
                f_dbg.write(f"Steam API items: {len(data['items'])} items found. First: {data['items'][0]['name']}\n")
        if data.get('items'):
            # Match the closest item by title or fallback to first
            appid = data['items'][0]['id']
            def _norm(s):
                s = unicodedata.normalize("NFKD", s or "")
                s = "".join(ch for ch in s if not unicodedata.combining(ch))
                return re.sub(r'[^a-z0-9]+', '', s.lower())
            title_l = _norm(game_title)
            for item in data['items']:
                name_l = _norm(item.get('name'))
                if name_l == title_l or (title_l and title_l in name_l) or (name_l and name_l in title_l):
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

                # Trailer URLs — highlight movie first
                videos = []
                movies = list(g.get('movies') or [])
                movies.sort(key=lambda m: (0 if m.get('highlight') else 1, m.get('id') or 0))
                for movie in movies[:3]:
                    play_urls = _steam_movie_play_urls(movie)
                    # One playable URL per movie (prefer first = microtrailer/short)
                    if play_urls:
                        videos.append(play_urls[0])
                
                return {
                    'description': g.get('short_description', ''),
                    'developers': g.get('developers', []),
                    'publishers': g.get('publishers', []),
                    'release_date': g.get('release_date', {}).get('date', ''),
                    'genres': [genre.get('description') for genre in g.get('genres', []) if genre.get('description')],
                    'metacritic': g.get('metacritic', {}).get('score'),
                    'screenshots': [s.get('path_full') for s in g.get('screenshots', [])],
                    'header_image': g.get('header_image', ''),
                    'steam_rating': rating_str,
                    'videos': videos,
                    'appid': appid,
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
            
            text_all = soup.get_text("\n")
            size_val_re = r'([0-9][\d.,/\s–—-]*?(?:GB|MB|TB|GiB|MiB|gb|mb|tb)\b)'
            orig_match = re.search(r'Original\s+Size:\s*' + size_val_re, text_all, re.IGNORECASE)
            repack_match = re.search(r'Repack\s+Size:\s*' + size_val_re, text_all, re.IGNORECASE)
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

# ---------------------------------------------------------------------------
# Local FitGirl site proxy (bypasses German CUII / ISP DNS block via DoH)
# Browser cannot reach fitgirl-repacks.site; Python can → reverse-proxy HTML+assets.
# ---------------------------------------------------------------------------
PROXY_ALLOWED_HOST_SUFFIXES = (
    "fitgirl-repacks.site",
    "imageban.ru",
    "fastpic.org",
    "fastpic.ru",
    "imgur.com",
    "i.imgur.com",
    "wp.com",
    "gravatar.com",
    "w.org",
    "wordpress.com",
    "cloudflare.com",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "jsdelivr.net",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "riotpixels.com",
    "riotpixels.net",
    "steamstatic.com",
    "akamaihd.net",
    "pinimg.com",
    "ibb.co",
    "i.ibb.co",
    "imgbb.com",
    "duckduckgo.com",
)

_IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".svg", ".ico", ".bmp")
_FONT_EXTS = (".woff", ".woff2", ".ttf", ".otf", ".eot")

def _proxy_host_allowed(host):
    if not host:
        return False
    host = host.lower().rstrip(".")
    for suf in PROXY_ALLOWED_HOST_SUFFIXES:
        if host == suf or host.endswith("." + suf):
            return True
    return False

def _proxy_guess_kind(url):
    """Return 'image' | 'css' | 'js' | 'font' | 'html' | 'other' from URL path."""
    try:
        path = urllib.parse.urlparse(url).path.lower()
    except Exception:
        path = (url or "").lower()
    # strip wp.com resize query noise from path check
    if any(path.endswith(ext) for ext in _IMAGE_EXTS):
        return "image"
    if ".jpg" in path or ".jpeg" in path or ".png" in path or ".webp" in path or "/out/" in path:
        # imageban /out/HASH.jpg style
        if any(x in path for x in (".jpg", ".jpeg", ".png", ".webp", ".gif", "/out/")):
            return "image"
    if path.endswith(".css") or ".css?" in (url or "").lower():
        return "css"
    if path.endswith(".js") or ".js?" in (url or "").lower():
        return "js"
    if any(path.endswith(ext) for ext in _FONT_EXTS):
        return "font"
    return "other"

def _proxy_abs_url(raw, base_url):
    if not raw or raw.startswith(("#", "data:", "javascript:", "mailto:", "blob:")):
        return None
    raw = raw.strip().strip("'\"")
    if not raw:
        return None
    return urllib.parse.urljoin(base_url, raw)

def _unwrap_cdn_image_url(url):
    """
    WordPress.com Photon wraps hotlink hosts:
      https://i0.wp.com/i2.imageban.ru/out/...jpg?resize=150%2C200&ssl=1
    → https://i2.imageban.ru/out/...jpg  (direct imageban works; photon often  fails via proxy)
    Also upgrade http→https for known CDNs.
    """
    if not url:
        return url
    try:
        u = url.strip()
        # Photon: iN.wp.com/<host>/<path>
        m = re.match(r"^https?://i\d+\.wp\.com/([^/?#]+)/(.+?)(?:\?|#|$)", u, flags=re.I)
        if m:
            host = m.group(1)
            path = m.group(2)
            # drop photon resize query — full original is more reliable
            return f"https://{host}/{path}"
        # force https on imageban / riotpixels
        p = urllib.parse.urlparse(u)
        host = (p.hostname or "").lower()
        if host.endswith("imageban.ru") or host.endswith("riotpixels.net") or host.endswith("riotpixels.com"):
            if p.scheme == "http":
                u = "https://" + u[len("http://"):]
        return u
    except Exception:
        return url

def _proxy_local_url(abs_url):
    """Map remote URL → local proxy endpoint (same origin, unblocked)."""
    if not abs_url:
        return abs_url
    try:
        abs_url = _unwrap_cdn_image_url(abs_url)
        p = urllib.parse.urlparse(abs_url)
        if p.scheme not in ("http", "https"):
            return abs_url
        if not _proxy_host_allowed(p.hostname):
            return abs_url
        kind = _proxy_guess_kind(abs_url)
        # Images use dedicated endpoint (proper Accept + cache, works for imageban)
        if kind == "image":
            return "/api/proxy_image?url=" + urllib.parse.quote(abs_url, safe="")
        return "/api/proxy_page?url=" + urllib.parse.quote(abs_url, safe="")
    except Exception:
        return abs_url

def _proxy_rewrite_css(css_text, base_url):
    def repl_url(m):
        inner = m.group(1).strip().strip("'\"")
        abs_u = _proxy_abs_url(inner, base_url)
        if not abs_u:
            return m.group(0)
        local = _proxy_local_url(abs_u)
        return f"url({local})"
    return re.sub(r"url\(\s*([^)]+?)\s*\)", repl_url, css_text, flags=re.IGNORECASE)

def _proxy_rewrite_srcset(srcset, base_url):
    parts = []
    for chunk in srcset.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        bits = chunk.split()
        u = bits[0]
        rest = " ".join(bits[1:])
        abs_u = _proxy_abs_url(u, base_url)
        if abs_u:
            u = _proxy_local_url(abs_u)
        parts.append((u + (" " + rest if rest else "")).strip())
    return ", ".join(parts)

def _proxy_rewrite_html(html_text, page_url):
    """Rewrite FitGirl HTML so every asset/link loads through local proxy (DoH unblocked)."""
    try:
        soup = BeautifulSoup(html_text, "html.parser")
    except Exception:
        return html_text

    # Attrs that hold a single URL
    ATTR_MAP = {
        "a": ["href"],
        "link": ["href"],
        "script": ["src"],
        "img": [
            "src", "data-src", "data-lazy-src", "data-original", "data-lazy",
            "data-large_image", "data-srcset", "data-full-url", "data-url",
        ],
        "source": ["src", "srcset"],
        "video": ["src", "poster"],
        "audio": ["src"],
        "iframe": ["src"],
        "form": ["action"],
        "embed": ["src"],
        "object": ["data"],
        "use": ["href", "xlink:href"],
        "image": ["href", "xlink:href", "src"],
    }

    for tag_name, attrs in ATTR_MAP.items():
        for el in soup.find_all(tag_name):
            for attr in attrs:
                val = el.get(attr)
                if not val:
                    continue
                if attr == "srcset" or attr.endswith("srcset"):
                    el[attr] = _proxy_rewrite_srcset(val, page_url)
                    continue
                abs_u = _proxy_abs_url(val, page_url)
                if abs_u:
                    el[attr] = _proxy_local_url(abs_u)
            # srcset separate common attr
            if el.get("srcset"):
                el["srcset"] = _proxy_rewrite_srcset(el.get("srcset"), page_url)

    # Inline style url(...)
    for el in soup.find_all(style=True):
        try:
            el["style"] = _proxy_rewrite_css(el.get("style") or "", page_url)
        except Exception:
            pass

    # <style> blocks
    for st in soup.find_all("style"):
        if st.string:
            try:
                st.string = _proxy_rewrite_css(str(st.string), page_url)
            except Exception:
                pass

    # Remove base tags that would break relative paths outside proxy
    for b in soup.find_all("base"):
        b.decompose()

    # Inject chrome so user knows it's the real site via local unblock
    # Client-side fixer: catch Photon/wp.com, riotpixels, imageban that bypassed HTML rewrite
    # (lazy-load JS, srcset, dynamic attrs) and route them through /api/proxy_image.
    fix_script = r"""
<script>
(function(){
  function unwrapPhoton(u){
    try{
      var m=String(u).match(/^https?:\/\/i\d+\.wp\.com\/([^\/?#]+)\/(.+?)(?:\?|#|$)/i);
      if(m) return 'https://'+m[1]+'/'+m[2];
    }catch(e){}
    return u;
  }
  function shouldProxy(u){
    if(!u||u.indexOf('/api/proxy_')===0||u.indexOf('data:')===0) return false;
    return /fitgirl-repacks\.site|imageban\.ru|riotpixels\.(net|com)|i\d+\.wp\.com|imgur\.com|ibb\.co/i.test(u);
  }
  function toProxy(u){
    u=unwrapPhoton(u);
    if(/^http:\/\//i.test(u) && /imageban\.ru|riotpixels\./i.test(u)) u=u.replace(/^http:/i,'https:');
    if(/\.(jpg|jpeg|png|webp|gif|avif|ico)(\?|$)/i.test(u) || /\/out\/[a-f0-9]+\.jpg/i.test(u) || /riotpixels\./i.test(u))
      return '/api/proxy_image?url='+encodeURIComponent(u);
    return '/api/proxy_page?url='+encodeURIComponent(u);
  }
  function fixEl(el){
    if(!el||!el.getAttribute) return;
    ['src','data-src','data-lazy-src','data-original','data-large_image','href'].forEach(function(a){
      var v=el.getAttribute(a); if(!v||!shouldProxy(v)) return;
      el.setAttribute(a, toProxy(v));
    });
    var ss=el.getAttribute('srcset');
    if(ss && /imageban|riotpixels|wp\.com|fitgirl/i.test(ss)){
      el.setAttribute('srcset', ss.split(',').map(function(part){
        var p=part.trim().split(/\s+/); if(!p[0]) return part;
        if(shouldProxy(p[0])) p[0]=toProxy(p[0]);
        return p.join(' ');
      }).join(', '));
    }
  }
  function scan(root){
    (root||document).querySelectorAll('img,source,a,link,video').forEach(fixEl);
  }
  function retryBroken(){
    document.querySelectorAll('img').forEach(function(img){
      if(img.complete && img.naturalWidth>1) return;
      var s=img.getAttribute('src')||img.src||'';
      if(!s) return;
      var bare=s;
      if(s.indexOf('/api/proxy_image?url=')>=0){
        try{
          var q=s.split('/api/proxy_image?url=')[1]||'';
          q=q.split('&')[0]; // drop any extra query junk
          bare=decodeURIComponent(q);
        }catch(e){}
      }
      bare=unwrapPhoton(bare);
      // imageban paths are stable without query; strip cache-busters that break fetch
      if(/imageban\.ru\/out\//i.test(bare)) bare=bare.split('?')[0];
      if(shouldProxy(bare) || /imageban\.ru|riotpixels\./i.test(bare)){
        img.src='/api/proxy_image?url='+encodeURIComponent(bare);
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', function(){ scan(); setTimeout(retryBroken, 800); setTimeout(retryBroken, 2500); });
  else { scan(); setTimeout(retryBroken, 800); setTimeout(retryBroken, 2500); }
  try{
    new MutationObserver(function(muts){
      muts.forEach(function(m){ m.addedNodes && m.addedNodes.forEach(function(n){ if(n.nodeType===1){ fixEl(n); if(n.querySelectorAll) scan(n); } }); });
    }).observe(document.documentElement,{childList:true,subtree:true});
  }catch(e){}
})();
</script>
"""
    banner_html = (
        '<div id="fg-local-proxy-banner" style="position:fixed;top:0;left:0;right:0;'
        'z-index:2147483647;background:#1a1028;color:#f3e8ff;font:600 12px/1.4 system-ui,sans-serif;'
        'padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.12);display:flex;gap:12px;'
        'align-items:center;justify-content:space-between;">'
        "<span>FitGirl via local proxy (ISP block bypass) — real site content</span>"
        '<a href="http://127.0.0.1:8000/" style="color:#c4b5fd;text-decoration:underline;">Back to app</a>'
        "</div>"
        "<style>body{padding-top:42px !important;}#fg-local-proxy-banner a:hover{color:#fff;}</style>"
        + fix_script
    )

    # meta charset
    if soup.head and not soup.head.find("meta", attrs={"charset": True}):
        mc = soup.new_tag("meta", charset="utf-8")
        soup.head.insert(0, mc)

    out = str(soup)
    # Inject banner right after <body ...> (handles multi-line tags)
    low = out.lower()
    bidx = low.find("<body")
    if bidx >= 0:
        end = out.find(">", bidx)
        if end >= 0:
            out = out[: end + 1] + banner_html + out[end + 1 :]
        else:
            out = banner_html + out
    else:
        out = banner_html + out
    return out

def proxy_fetch_remote(page_url, kind=None):
    """GET remote URL with chrome impersonation + DoH (works when browser DNS is blocked)."""
    kind = kind or _proxy_guess_kind(page_url)
    if kind == "image":
        accept = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
    elif kind == "css":
        accept = "text/css,*/*;q=0.1"
    elif kind == "js":
        accept = "*/*"
    elif kind == "font":
        accept = "font/woff2,font/woff,application/font-woff,*/*;q=0.1"
    else:
        accept = (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://fitgirl-repacks.site/",
        "Sec-Fetch-Dest": "image" if kind == "image" else "document",
        "Sec-Fetch-Mode": "no-cors" if kind == "image" else "navigate",
        "Sec-Fetch-Site": "cross-site" if kind == "image" else "none",
    }
    r = cf_requests.get(
        page_url,
        impersonate="chrome120",
        timeout=35,
        verify=False,
        headers=headers,
        allow_redirects=True,
    )
    # imageban sometimes returns HTML interstitial if Accept wrong — retry as pure image
    if kind == "image" and r is not None:
        body = r.content or b""
        ctype = (r.headers.get("Content-Type") or "").lower()
        if "text/html" in ctype or body.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
            headers["Accept"] = "image/*,*/*;q=0.8"
            headers["Referer"] = "https://imageban.ru/"
            r = cf_requests.get(
                page_url,
                impersonate="chrome120",
                timeout=35,
                verify=False,
                headers=headers,
                allow_redirects=True,
            )
    return r

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
            except Exception:
                pass
            add_log("User skipped Cloudflare WARP installer check (can install later from Settings).")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return
            
        elif path == "/api/warp/status":
            info = get_warp_connection_info()
            with state_lock:
                if info.get("installed"):
                    state["warp_status"] = "installed"
                    state["warp_connected"] = bool(info.get("connected"))
                elif state.get("warp_status") not in ("installing", "checking", "error"):
                    state["warp_status"] = "skipped" if os.path.exists("warp_skipped.txt") else "error"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "installed": info.get("installed"),
                "connected": info.get("connected"),
                "status_text": info.get("status_text"),
                "warp_status": state.get("warp_status"),
                "warp_error_message": state.get("warp_error_message", ""),
                "last_rotate_ts": state.get("warp_last_rotate_ts", 0),
            }).encode())
            return

        # Also accept GET for escape (legacy) — preferred is POST
        elif path == "/api/escape_pixeldrain":
            mirror = "Rootz"
            qs = urllib.parse.parse_qs(url_parsed.query)
            if qs.get("mirror"):
                mirror = (qs.get("mirror")[0] or "Rootz").strip() or "Rootz"

            def _do_escape_get():
                n = bulk_failover_unfinished_to_mirror(mirror)
                add_log(f"[ESCAPE] API escape done: {n} file(s) → {mirror}")

            threading.Thread(target=_do_escape_get, daemon=True).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "started": True, "mirror": mirror}).encode())
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

                # Unwrap Photon CDN → direct imageban/etc (more reliable)
                img_url = _unwrap_cdn_image_url(img_url)
                # re-hash after unwrap for cache key consistency on first miss path
                url_hash = hashlib.md5(img_url.encode("utf-8")).hexdigest()
                cache_path = os.path.join(cache_dir, f"{url_hash}.{ext}")
                if os.path.exists(cache_path):
                    with open(cache_path, "rb") as f:
                        header = f.read(15)
                        rest = f.read()
                    if not (header.startswith(b"<!DOCTYPE") or header.startswith(b"<html") or header.startswith(b"<")):
                        content_type = "image/jpeg"
                        if ext.lower() == "png":
                            content_type = "image/png"
                        elif ext.lower() == "gif":
                            content_type = "image/gif"
                        elif ext.lower() == "webp":
                            content_type = "image/webp"
                        self.send_response(200)
                        self.send_header("Content-Type", content_type)
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.send_header("Cache-Control", "public, max-age=31536000")
                        self.end_headers()
                        self.wfile.write(header + rest)
                        return

                # Download via curl_cffi + DoH (urllib fails under DE DNS block / hotlink HTML)
                add_log(f"Proxying image: {img_url}")
                try:
                    response = proxy_fetch_remote(img_url, kind="image")
                    content = response.content or b""
                    content_type = response.headers.get("Content-Type", "image/jpeg")
                    is_success = (
                        response.status_code == 200
                        and content
                        and not content.lstrip()[:15].lower().startswith((b"<!doctype", b"<html", b"<"))
                    )
                    if is_success:
                        # normalize content-type if server lied
                        if "image" not in (content_type or "").lower():
                            if content[:3] == b"\xff\xd8\xff":
                                content_type = "image/jpeg"
                            elif content[:8] == b"\x89PNG\r\n\x1a\n":
                                content_type = "image/png"
                            elif content[:4] == b"RIFF" and content[8:12] == b"WEBP":
                                content_type = "image/webp"
                            else:
                                content_type = "image/jpeg"
                        try:
                            with open(cache_path, "wb") as f:
                                f.write(content)
                        except Exception:
                            pass
                        self.send_response(200)
                        self.send_header("Content-Type", content_type.split(";")[0].strip())
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.send_header("Cache-Control", "public, max-age=31536000")
                        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
                        self.end_headers()
                        self.wfile.write(content)
                        return
                except Exception as img_e:
                    add_log(f"proxy_image cf fetch failed: {img_e}")
                # fallback urllib
                try:
                    req = urllib.request.Request(
                        img_url,
                        headers={
                            "User-Agent": "Mozilla/5.0",
                            "Accept": "image/*,*/*;q=0.8",
                            "Referer": "https://fitgirl-repacks.site/",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=15) as response:
                        content = response.read()
                        content_type = response.headers.get("Content-Type", "image/jpeg")
                        is_success = (response.status == 200) and not (
                            content.startswith(b"<!DOCTYPE")
                            or content.startswith(b"<html")
                            or content.startswith(b"<")
                        )
                        if is_success:
                            with open(cache_path, "wb") as f:
                                f.write(content)
                            self.send_response(200)
                            self.send_header("Content-Type", content_type)
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("Cache-Control", "public, max-age=31536000")
                            self.end_headers()
                            self.wfile.write(content)
                            return
                except Exception:
                    pass
                self.send_response(404)
                self.end_headers()
            except Exception as e:
                add_log(f"Proxy image exception: {str(e)}")
                self.send_response(500)
                self.end_headers()
            return

        elif path == "/api/proxy_media":
            # Same-origin stream for video poster capture (CORS-safe mid-frame thumbs).
            # Prefer microtrailers / short clips; large movie_max is still allowed but slower.
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                media_url = query_params.get("url", [""])[0]
                if not media_url:
                    self.send_response(400)
                    self.end_headers()
                    return
                if media_url.startswith("//"):
                    media_url = "https:" + media_url
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "*/*",
                }
                # Forward Range so the browser can seek for mid-frame capture
                range_hdr = self.headers.get("Range")
                if range_hdr:
                    headers["Range"] = range_hdr
                req = urllib.request.Request(media_url, headers=headers)
                with urllib.request.urlopen(req, timeout=45) as response:
                    status = getattr(response, "status", 200) or 200
                    content_type = response.headers.get("Content-Type", "video/webm")
                    content_len = response.headers.get("Content-Length")
                    accept_ranges = response.headers.get("Accept-Ranges", "bytes")
                    content_range = response.headers.get("Content-Range")
                    body = response.read()
                self.send_response(status if status in (200, 206) else 200)
                self.send_header("Content-Type", content_type)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Expose-Headers", "Content-Length, Content-Range, Accept-Ranges")
                self.send_header("Accept-Ranges", accept_ranges or "bytes")
                self.send_header("Cache-Control", "public, max-age=86400")
                if content_range:
                    self.send_header("Content-Range", content_range)
                if content_len:
                    self.send_header("Content-Length", content_len)
                else:
                    self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                add_log(f"Proxy media exception: {str(e)}")
                try:
                    self.send_response(502)
                    self.end_headers()
                except Exception:
                    pass
            return
            
        elif path == "/api/proxy_page":
            # Full reverse proxy for FitGirl (+ hotlinked assets). Browser uses localhost
            # while Python fetches via DoH — bypasses German ISP / CUII DNS blocks.
            try:
                query_params = urllib.parse.parse_qs(url_parsed.query)
                page_url = (query_params.get("url", [""])[0] or "").strip()
                if not page_url:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"Missing url= parameter")
                    return

                # Allow already-decoded or double-encoded
                if page_url.startswith("//"):
                    page_url = "https:" + page_url
                parsed_target = urllib.parse.urlparse(page_url)
                if parsed_target.scheme not in ("http", "https") or not parsed_target.hostname:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid url")
                    return
                if not _proxy_host_allowed(parsed_target.hostname):
                    self.send_response(403)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(f"Host not allowed for proxy: {parsed_target.hostname}".encode())
                    return

                add_log(f"Proxying page request: {page_url}")
                response = None
                last_err = None
                fetch_kind = _proxy_guess_kind(page_url)
                for attempt in range(3):
                    try:
                        response = proxy_fetch_remote(page_url, kind=fetch_kind)
                        if response is not None and response.status_code < 500:
                            break
                    except Exception as se:
                        last_err = se
                        add_log(f"Proxy fetch attempt {attempt + 1}/3 failed: {se}")
                        time.sleep(0.5 * (attempt + 1))

                if response is None:
                    self.send_response(502)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(
                        f"<h1>Proxy fetch failed</h1><p>{last_err}</p>"
                        f"<p><a href='{urllib.parse.quote(page_url, safe=':/?=&')}'>Retry</a></p>".encode("utf-8")
                    )
                    return

                ctype = (response.headers.get("Content-Type") or "").lower()
                status = int(response.status_code or 200)
                body = response.content or b""

                # HTML → rewrite all links/assets through this proxy
                if "text/html" in ctype or body.lstrip()[:32].lower().startswith((b"<!doctype", b"<html", b"<head", b"<body")):
                    try:
                        text = body.decode(response.encoding or "utf-8", errors="replace")
                    except Exception:
                        text = body.decode("utf-8", errors="replace")
                    text = _proxy_rewrite_html(text, page_url)
                    out = text.encode("utf-8")
                    self.send_response(status if status < 400 else 200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(out)))
                    self.end_headers()
                    self.wfile.write(out)
                    return

                # CSS → rewrite url(...)
                if "text/css" in ctype or page_url.lower().split("?")[0].endswith(".css"):
                    try:
                        text = body.decode(response.encoding or "utf-8", errors="replace")
                    except Exception:
                        text = body.decode("utf-8", errors="replace")
                    text = _proxy_rewrite_css(text, page_url)
                    out = text.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/css; charset=utf-8")
                    self.send_header("Cache-Control", "public, max-age=3600")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(out)))
                    self.end_headers()
                    self.wfile.write(out)
                    return

                # Binary / JS / fonts / images — pass through with original type
                out_type = ctype.split(";")[0].strip() if ctype else "application/octet-stream"
                if not out_type or out_type == "application/octet-stream":
                    low = page_url.lower().split("?")[0]
                    if low.endswith(".js"):
                        out_type = "application/javascript"
                    elif low.endswith(".woff2"):
                        out_type = "font/woff2"
                    elif low.endswith(".woff"):
                        out_type = "font/woff"
                    elif low.endswith(".png"):
                        out_type = "image/png"
                    elif low.endswith((".jpg", ".jpeg")):
                        out_type = "image/jpeg"
                    elif low.endswith(".webp"):
                        out_type = "image/webp"
                    elif low.endswith(".svg"):
                        out_type = "image/svg+xml"
                    elif low.endswith(".gif"):
                        out_type = "image/gif"

                self.send_response(status if 200 <= status < 400 else 200)
                self.send_header("Content-Type", out_type)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(body)))
                # Avoid browser blocking mixed content / CORP
                self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                add_log(f"Proxy page exception: {str(e)}")
                try:
                    self.send_response(500)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(
                        f"<h1>Proxy error</h1><pre>{urllib.parse.quote(str(e), safe='')}</pre>".encode("utf-8")
                    )
                except Exception:
                    pass
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
            
        # Serve static web files (whitelist under /web)
        web_dir = os.path.join(os.path.dirname(__file__), "web")
        static_map = {
            "/": ("index.html", "text/html"),
            "/index.html": ("index.html", "text/html"),
            "/style.css": ("style.css", "text/css"),
            "/details-fix.css": ("details-fix.css", "text/css"),
            "/liquid-glass.css": ("liquid-glass.css", "text/css"),
            "/app.js": ("app.js", "application/javascript"),
            "/liquid-glass.js": ("liquid-glass.js", "application/javascript"),
        }
        if path not in static_map:
            self.send_error(404, "File Not Found")
            return
        fname, content_type = static_map[path]
        file_to_serve = os.path.join(web_dir, fname)

        try:
            if path == "/" or path == "/index.html":
                with open(file_to_serve, "r", encoding="utf-8") as f:
                    content_str = f.read()
                import time
                ts = str(int(time.time()))
                # Bust all local asset query strings so UI always loads latest glass/nav
                for name in (
                    "style.css",
                    "app.js",
                    "details-fix.css",
                    "liquid-glass.css",
                    "liquid-glass.js",
                ):
                    content_str = re.sub(
                        rf'{re.escape(name)}\?v=[^"\']+',
                        f"{name}?v={ts}",
                        content_str,
                    )
                    content_str = content_str.replace(
                        f'href="{name}"', f'href="{name}?v={ts}"'
                    ).replace(
                        f'src="{name}"', f'src="{name}?v={ts}"'
                    )
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
            # Always ensure background auto-WARP watchdog is running
            ensure_speed_watchdog()
            save_session_state()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())

        elif path == "/api/retry_warp" or path == "/api/warp/install":
            try:
                if os.path.exists("warp_skipped.txt"):
                    os.remove("warp_skipped.txt")
            except Exception:
                pass
            with state_lock:
                state["warp_status"] = "checking"
                state["warp_error_message"] = ""
            add_log("Installing / connecting Cloudflare WARP (force)...")
            threading.Thread(
                target=lambda: check_and_install_warp(force=True), daemon=True
            ).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return

        elif path == "/api/warp/rotate":
            def _do_rotate():
                add_log("[SPEED] Manual/UI WARP rotate requested (force)...")
                ok = try_auto_warp_rotate("manual/UI button", min_interval_sec=0, force=True)
                if not ok:
                    ok = wait_for_warp_rotate_or_do("manual/UI wait", min_interval_sec=0, wait_sec=40)
                if ok:
                    add_log("[SPEED] Manual WARP IP rotate finished OK — nudging download reconnect.")
                    with state_lock:
                        was = bool(state.get("is_running"))
                        state["should_stop"] = True
                        state["is_running"] = False
                    time.sleep(2)
                    with state_lock:
                        state["should_stop"] = False
                        if was or state.get("files"):
                            state["is_running"] = True
                            n = get_effective_max_workers()
                            for _ in range(n):
                                threading.Thread(target=download_worker, daemon=True).start()
                            add_log(f"[SPEED] Resumed {n} worker(s) after WARP rotate.")
                else:
                    add_log("[SPEED] Manual WARP IP rotate failed.")
            threading.Thread(target=_do_rotate, daemon=True).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "started": True}).encode())
            return

        elif path == "/api/escape_pixeldrain":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode() if content_length else "{}"
            try:
                data = json.loads(post_data) if post_data else {}
            except Exception:
                data = {}
            mirror = (data.get("mirror") or "Rootz").strip() or "Rootz"

            def _do_escape():
                n = bulk_failover_unfinished_to_mirror(mirror)
                add_log(f"[ESCAPE] API escape done: {n} file(s) → {mirror}")

            threading.Thread(target=_do_escape, daemon=True).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "started": True, "mirror": mirror}).encode())
            return

        elif path == "/api/set_captcha_key":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode() if content_length else "{}"
            try:
                data = json.loads(post_data) if post_data else {}
                key = (data.get("api_key") or data.get("captcha_api_key") or "").strip()
                provider = (data.get("provider") or "").strip().lower()
                with state_lock:
                    state["captcha_api_key"] = key
                    if provider in ("capsolver", "2captcha", "twocaptcha", "auto", ""):
                        state["captcha_provider"] = (
                            "2captcha" if provider in ("2captcha", "twocaptcha") else provider
                        )
                # Persist lightly next to session
                try:
                    path_key = os.path.join(os.path.dirname(__file__), "captcha_key.json")
                    with open(path_key, "w", encoding="utf-8") as f:
                        json.dump(
                            {
                                "captcha_api_key": key,
                                "captcha_provider": state.get("captcha_provider") or "",
                            },
                            f,
                        )
                except Exception:
                    pass
                add_log(
                    "Captcha solver key "
                    + ("saved." if key else "cleared.")
                    + " (VikingFile Turnstile)"
                )
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
                        # Prefer best catalog mirror URL on retry (recover from bad failover)
                        fn = state["files"][idx].get("filename") or ""
                        cat = state.get("mirror_catalog") or {}
                        rank = list(state.get("mirror_rank") or [])
                        speeds = state.get("mirror_speeds") or {}
                        for m in rank + list(cat.keys()):
                            if "gofile" in m.lower() or "fileditch" in m.lower():
                                continue
                            url = (cat.get(m) or {}).get(fn)
                            if url:
                                # prefer highest measured speed among valid
                                best_m, best_u, best_b = m, url, float(speeds.get(m) or 0)
                                for m2 in rank + list(cat.keys()):
                                    if "gofile" in m2.lower() or "fileditch" in m2.lower():
                                        continue
                                    u2 = (cat.get(m2) or {}).get(fn)
                                    b2 = float(speeds.get(m2) or 0)
                                    if u2 and b2 >= best_b:
                                        best_m, best_u, best_b = m2, u2, b2
                                if best_u and best_u != state["files"][idx].get("url"):
                                    add_log(f"[SPEED] Retry {fn}: reset URL → {best_m}")
                                    state["files"][idx]["url"] = best_u
                                # clear blacklist for this file so PD can be tried again after WARP/IP change
                                if fn in (state.get("file_mirror_blacklist") or {}):
                                    state["file_mirror_blacklist"][fn] = []
                                break
                    if not state["is_running"]:
                        state["is_running"] = True
                        state["should_stop"] = False
                        workers_to_start = get_effective_max_workers()
                        for _ in range(workers_to_start):
                            threading.Thread(target=download_worker, daemon=True).start()
                save_session_state()
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

        elif path == "/api/post_download_check":
            # Manual re-run or dry status of smart post-download analysis
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode() if content_length else "{}"
            try:
                data = json.loads(post_data) if post_data else {}
            except Exception:
                data = {}
            run_pipeline = bool(data.get("run") or data.get("auto"))
            report = analyze_post_download()
            with state_lock:
                state["post_download_report"] = report
                state["post_download_message"] = report.get("message") or ""
                if report.get("already_extracted"):
                    state["is_extracted"] = True
            if run_pipeline and report.get("all_downloads_finished"):
                with state_lock:
                    if not state.get("post_download_running") and not state.get("is_extracting"):
                        state["post_download_running"] = True
                        threading.Thread(
                            target=post_download_smart_pipeline, daemon=True
                        ).start()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "success": True,
                        "report": report,
                        "pipeline_started": run_pipeline
                        and report.get("all_downloads_finished"),
                        "post_download_status": state.get("post_download_status"),
                    }
                ).encode()
            )
            return
            
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
                        
                        # Scrape sizes (tight capture so next labels don't stick to the value)
                        text_all = soup.get_text("\n")
                        size_val_re = (
                            r'([0-9][\d.,/\s–—-]*?(?:GB|MB|TB|GiB|MiB|gb|mb|tb)\b)'
                        )
                        orig_match = re.search(
                            r'Original\s+Size:\s*' + size_val_re, text_all, re.IGNORECASE
                        )
                        repack_match = re.search(
                            r'Repack\s+Size:\s*' + size_val_re, text_all, re.IGNORECASE
                        )
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
                                skip_bonus = False

                                def _emit(t, bullet=False):
                                    nonlocal skip_bonus
                                    t = _norm(t)
                                    if not t or _is_junk_desc(t):
                                        return
                                    # Bonus Content / Soundtracks lists ≠ game description
                                    if _is_bonus_content_header(t):
                                        skip_bonus = True
                                        return
                                    if skip_bonus:
                                        if _is_game_desc_resume_header(t):
                                            skip_bonus = False
                                        else:
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
                                        if skip_bonus:
                                            continue
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
                                        if not skip_bonus:
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
                                        if _is_bonus_content_header(ln):
                                            # Drop this header and everything after in rebuild path
                                            break
                                        if low in (
                                            "game features",
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

                            # 4. Screenshots — under h3 "Screenshots..." (also find_all_next for nested HTML)
                            def _add_shot(candidate):
                                cleaned = _normalize_shot_url(candidate)
                                if _is_junk_shot(cleaned):
                                    return
                                if cover_image and cleaned == cover_image:
                                    return
                                # Dedup by normalized stem (thumb vs full)
                                stem = re.sub(r'\.(jpg|jpeg|png|webp)$', '', cleaned.lower())
                                stem = re.sub(r'[-_.]?(240p|400p|720p|150x200|300x\d+)$', '', stem)
                                for existing in screenshots:
                                    est = re.sub(r'\.(jpg|jpeg|png|webp)$', '', existing.lower())
                                    if stem == est or stem in est or est in stem:
                                        # Prefer longer / non-thumb URL
                                        if len(cleaned) > len(existing) and existing in screenshots:
                                            screenshots[screenshots.index(existing)] = cleaned
                                        return
                                screenshots.append(cleaned)

                            shot_header = None
                            for el in parse_root.find_all(["h3", "h4", "strong", "b"]):
                                txt = el.get_text(strip=True).lower()
                                if "screenshot" in txt or "скриншот" in txt:
                                    shot_header = el
                                    break

                            def _harvest_shot_node(node):
                                if not node or not getattr(node, "find_all", None):
                                    return
                                for video in node.find_all("video"):
                                    source = video.find("source")
                                    video_src = source.get("src", "") if source else video.get("src", "")
                                    video_src = _prefer_video_url(video_src)
                                    if video_src and video_src not in videos:
                                        videos.append(video_src)
                                for a in node.find_all("a"):
                                    href = a.get("href", "") or ""
                                    # Skip pure gallery index pages without image ext
                                    if href and not re.search(r"/screenshots/?(\?|$)", href, re.I):
                                        if re.search(r'\.(jpg|jpeg|png|webp)(\?|$)', href, re.I) or "riotpixels" in href.lower():
                                            _add_shot(href)
                                    img = a.find("img")
                                    if img:
                                        _add_shot(
                                            img.get("data-full-url")
                                            or img.get("data-large_image")
                                            or img.get("data-src")
                                            or img.get("src")
                                            or ""
                                        )
                                for img in node.find_all("img"):
                                    _add_shot(
                                        img.get("data-full-url")
                                        or img.get("data-large_image")
                                        or img.get("data-src")
                                        or img.get("data-lazy-src")
                                        or img.get("src")
                                        or ""
                                    )

                            if shot_header:
                                # A) next siblings
                                curr = shot_header
                                for _ in range(50):
                                    curr = curr.next_sibling
                                    if not curr:
                                        break
                                    if isinstance(curr, str):
                                        continue
                                    name = getattr(curr, "name", None)
                                    if name in ("h3", "h4") and "screenshot" not in (curr.get_text(strip=True) or "").lower():
                                        break
                                    if name in ("h2",) and "feature" in (curr.get_text(strip=True) or "").lower():
                                        break
                                    if name in ("h3", "h4") and any(
                                        x in (curr.get_text(strip=True) or "").lower()
                                        for x in ("repack feature", "game description", "description")
                                    ):
                                        break
                                    _harvest_shot_node(curr)
                                    if name == "a":
                                        href = curr.get("href", "")
                                        if href and not re.search(r"/screenshots/?(\?|$)", href, re.I):
                                            _add_shot(href)
                                    if name == "img":
                                        _add_shot(curr.get("src") or curr.get("data-src") or "")
                                    if name == "video":
                                        source = curr.find("source")
                                        video_src = source.get("src", "") if source else curr.get("src", "")
                                        video_src = _prefer_video_url(video_src)
                                        if video_src and video_src not in videos:
                                            videos.append(video_src)
                                # B) find_all_next until next section (catches nested broken HTML)
                                if len(screenshots) < 4:
                                    for nxt in shot_header.find_all_next(["img", "a", "video", "h3", "h4"], limit=80):
                                        nm = getattr(nxt, "name", None)
                                        if nm in ("h3", "h4"):
                                            t = (nxt.get_text(strip=True) or "").lower()
                                            if "screenshot" in t:
                                                continue
                                            if any(x in t for x in ("repack feature", "game description", "feature", "description", "download mirror")):
                                                break
                                            if nxt is not shot_header:
                                                break
                                        if nm == "img":
                                            _add_shot(
                                                nxt.get("data-full-url")
                                                or nxt.get("data-src")
                                                or nxt.get("src")
                                                or ""
                                            )
                                        elif nm == "a":
                                            href = nxt.get("href", "") or ""
                                            if re.search(r'\.(jpg|jpeg|png|webp)(\?|$)', href, re.I) or "riotpixels" in href.lower():
                                                if not re.search(r"/screenshots/?(\?|$)", href, re.I):
                                                    _add_shot(href)
                                        elif nm == "video":
                                            source = nxt.find("source")
                                            video_src = source.get("src", "") if source else nxt.get("src", "")
                                            video_src = _prefer_video_url(video_src)
                                            if video_src and video_src not in videos:
                                                videos.append(video_src)
                            else:
                                # fallback: riotpixels + steam CDN embeds anywhere in article
                                for img in parse_root.find_all("img"):
                                    src = img.get("data-src") or img.get("src") or ""
                                    if "riotpixels" in src.lower() or "steamstatic" in src.lower():
                                        _add_shot(src)

                            screenshots = screenshots[:24]

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
                            # microtrailer preferred for autoplay cycle (short, ends → slideshow)
                            def _video_rank(v):
                                vl = (v or "").lower()
                                if "microtrailer" in vl:
                                    return 0
                                if any(x in vl for x in (".mp4", ".webm", "steamstatic", "store_trailers")):
                                    return 1
                                if "youtube" in vl or "youtu.be" in vl:
                                    return 2
                                return 3
                            videos = sorted(list(dict.fromkeys(videos)), key=_video_rank)

                        # Steam enrichment: trailers + meta when FitGirl page has none
                        developer_val = ""
                        publisher_val = ""
                        release_date_val = ""
                        genres_val = []
                        metacritic_val = None
                        steam_rating_val = ""
                        header_image_val = ""
                        try:
                            steam_meta = fetch_steam_metadata(title or "")
                        except Exception as _steam_ex:
                            steam_meta = None
                            add_log(f"Steam metadata skipped: {_steam_ex}")
                        if steam_meta:
                            if not developer_val and steam_meta.get("developers"):
                                developer_val = ", ".join(steam_meta["developers"][:3])
                            if not publisher_val and steam_meta.get("publishers"):
                                publisher_val = ", ".join(steam_meta["publishers"][:3])
                            if not release_date_val:
                                release_date_val = steam_meta.get("release_date") or ""
                            if not genres_val:
                                genres_val = steam_meta.get("genres") or []
                            if metacritic_val is None:
                                metacritic_val = steam_meta.get("metacritic")
                            if not steam_rating_val:
                                steam_rating_val = steam_meta.get("steam_rating") or ""
                            if not header_image_val:
                                header_image_val = steam_meta.get("header_image") or ""
                            # Trailers: ONLY FitGirl page count/order.
                            # Steam movies ONLY as fallback when page has zero videos
                            # (never invent Trailer 2/3/4 that aren't on the repack page).
                            steam_videos = steam_meta.get("videos") or []
                            if steam_videos and not videos:
                                videos = list(dict.fromkeys([v for v in steam_videos if v]))
                            # Backfill screenshots only if page had almost none
                            if len(screenshots) < 3:
                                for s in (steam_meta.get("screenshots") or []):
                                    if s and s not in screenshots:
                                        screenshots.append(s)
                                screenshots = screenshots[:24]
                            if not description and steam_meta.get("description"):
                                description = steam_meta.get("description") or description

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

        elif path == "/api/register_mirrors":
            # Body: { catalog: {Mirror: [{filename,url}]| {fn:url}}, speeds?: {Mirror:bps}, rank?: [..] }
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data) if post_data else {}
                register_mirror_catalog(
                    data.get("catalog") or {},
                    speeds=data.get("speeds"),
                    rank=data.get("rank"),
                )
                if "high_speed_mode" in data:
                    with state_lock:
                        state["high_speed_mode"] = bool(data["high_speed_mode"])
                if "min_acceptable_speed" in data:
                    with state_lock:
                        state["min_acceptable_speed"] = int(data["min_acceptable_speed"])
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "mirrors": list((state.get("mirror_catalog") or {}).keys()),
                    "rank": state.get("mirror_rank") or [],
                    "speeds": state.get("mirror_speeds") or {},
                }).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                return

        elif path == "/api/speed_probe":
            # Body: { url, seconds?, max_bytes? } — resolves real CDN then samples throughput
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data) if post_data else {}
                url = (data.get("url") or "").strip()
                if not url:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "url required"}).encode())
                    return
                seconds = float(data.get("seconds") or 12)
                max_bytes = int(data.get("max_bytes") or (20 * 1024 * 1024))
                result = probe_url_speed(url, seconds=seconds, max_bytes=max_bytes)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
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
    # Optional captcha solver key for VikingFile Turnstile
    try:
        _ck = os.path.join(os.path.dirname(__file__), "captcha_key.json")
        if os.path.exists(_ck):
            with open(_ck, "r", encoding="utf-8") as f:
                _cd = json.load(f)
            state["captcha_api_key"] = (_cd.get("captcha_api_key") or "").strip()
            state["captcha_provider"] = (_cd.get("captcha_provider") or "").strip()
            if state["captcha_api_key"]:
                add_log("Captcha solver key loaded (VikingFile Turnstile).")
    except Exception:
        pass
    # Always detect WARP if already installed (even after Skip); auto-install unless skipped
    if is_warp_available():
        state["warp_status"] = "installed"
        threading.Thread(
            target=lambda: ensure_warp_connected(get_warp_cli()), daemon=True
        ).start()
    elif os.path.exists("warp_skipped.txt"):
        state["warp_status"] = "skipped"
        add_log("WARP not installed and auto-install was skipped earlier (Settings → Install).")
    else:
        threading.Thread(target=check_and_install_warp, daemon=True).start()
    # Always start auto free-cap detector (harmless when idle)
    ensure_speed_watchdog()
    start_server()
