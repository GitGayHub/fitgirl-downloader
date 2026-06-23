import urllib.request
import json
import time
import os

# Ignore proxies for local requests
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

status_url = "http://127.0.0.1:8000/api/status"
start_url = "http://127.0.0.1:8000/api/start"

def get_status():
    try:
        with urllib.request.urlopen(status_url, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Error getting status:", e)
        return None

def start_download():
    try:
        req = urllib.request.Request(start_url, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Error starting download:", e)
        return None

print("Checking server status...")
status = get_status()
if status:
    print(f"Server is running. Loaded {len(status['files'])} files.")
    print("Sending start download command...")
    res = start_download()
    print("Start command result:", res)
    
    # Wait and monitor progress for 15 seconds
    for i in range(15):
        time.sleep(1)
        status = get_status()
        if status:
            active_idx = status.get("active_index", -1)
            is_running = status.get("is_running", False)
            total_speed = status.get("total_speed", 0)
            
            if active_idx != -1:
                active_file = status["files"][active_idx]
                print(f"Time {i+1}s: {active_file['filename']} - Status: {active_file['status']}, Speed: {total_speed / (1024*1024):.2f} MB/s, Progress: {active_file['progress']}%")
            else:
                print(f"Time {i+1}s: Queue is running={is_running}, no active file yet.")
else:
    print("Could not connect to server.")
