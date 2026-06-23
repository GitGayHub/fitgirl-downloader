import urllib.request
import json

url = "http://127.0.0.1:8000/api/status"
try:
    with urllib.request.urlopen(url, timeout=5) as res:
        data = json.loads(res.read().decode())
        print("Success! Keys in response:", data.keys())
        print("Files count:", len(data.get("files", [])))
        print("Is running:", data.get("is_running"))
        print("Active index:", data.get("active_index"))
        if data.get("files"):
            print("First file status:", data["files"][0]["status"])
except Exception as e:
    print("Error:", e)
