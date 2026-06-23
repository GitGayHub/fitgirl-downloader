import urllib.request
import json
import os

# Ignore proxies for local requests
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

url = "http://127.0.0.1:8000/api/status"

def format_time(seconds):
    if seconds < 60: return f"{seconds}s"
    mins = seconds // 60
    secs = seconds % 60
    if mins < 60: return f"{mins}m {secs}s"
    hrs = mins // 60
    rem_mins = mins % 60
    return f"{hrs}h {rem_mins}m"

try:
    with urllib.request.urlopen(url, timeout=5) as res:
        data = json.loads(res.read().decode())
        
        # Calculate total bytes left
        total_bytes_left = 0
        for f in data["files"]:
            if f["status"] != "finished":
                size = f["size"] if f["size"] > 0 else 2000000000
                total_bytes_left += max(0, size - f["downloaded"])
                
        active_idx = data.get("active_index", -1)
        speed = data.get("total_speed", 0)
        
        print("=== DOWNLOADING PROGRESS STATS ===")
        if active_idx != -1:
            active_file = data["files"][active_idx]
            print(f"Active File: {active_file['filename']}")
            print(f"File Status: {active_file['status']}")
            print(f"File Progress: {active_file['progress']}%")
        else:
            print("Active File: None")
            
        print(f"Current Speed: {speed / (1024*1024):.2f} MB/s")
        print(f"Remaining bytes: {total_bytes_left / (1024*1024*1024):.2f} GB")
        
        if speed > 0:
            total_seconds_left = int(total_bytes_left / speed)
            print(f"Time left for ENTIRE download: {format_time(total_seconds_left)}")
        else:
            print("Time left for ENTIRE download: --:--")
        print("==================================")
except Exception as e:
    print("Error:", e)
