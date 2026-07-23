import json
import time
import urllib.request
from collections import Counter

def get():
    return json.load(urllib.request.urlopen("http://127.0.0.1:8000/api/status", timeout=15))

d = get()
print("before", d.get("max_workers"), d.get("active_workers_count"), round((d.get("total_speed") or 0) / 1048576, 2))
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/set_workers",
    data=json.dumps({"max_workers": 4}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
print(urllib.request.urlopen(req, timeout=15).read().decode())
time.sleep(4)
d = get()
print("after", d.get("max_workers"), d.get("active_workers_count"), round((d.get("total_speed") or 0) / 1048576, 2))
print(Counter(f.get("status") for f in d.get("files") or []))
