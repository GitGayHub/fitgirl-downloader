import urllib.request
import json

url = "http://127.0.0.1:8000/api/status"
try:
    with urllib.request.urlopen(url, timeout=5) as res:
        data = json.loads(res.read().decode())
        active_idx = data.get("active_index", -1)
        if active_idx != -1:
            active_file = data["files"][active_idx]
            print(f"Active File: {active_file['filename']}")
            print(f"Status: {active_file['status']}")
            print(f"Progress: {active_file['progress']}%")
            print(f"Downloaded: {active_file['downloaded'] / (1024*1024):.2f} MB / {active_file['size'] / (1024*1024):.2f} MB")
            print(f"Speed: {data['total_speed'] / (1024*1024):.2f} MB/s")
        else:
            print("No active file.")
except Exception as e:
    print("Error:", e)
