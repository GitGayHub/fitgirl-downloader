import json
import time
import urllib.request
from collections import Counter

BASE = "http://127.0.0.1:8000"


def api(method, path, body=None):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else {}


st = api("GET", "/api/status")
for i, f in enumerate(st.get("files") or []):
    if f.get("status") == "failed":
        print("retry", i, f.get("filename"), f.get("error"))
        # reset URL to Pixeldrain from catalog if present
        cat = st.get("mirror_catalog") or {}
        pd = (cat.get("Pixeldrain") or {}).get(f.get("filename"))
        if pd:
            # can't set URL via API easily — retry keeps URL; re-register won't help
            pass
        api("POST", "/api/retry", {"index": i})

api("POST", "/api/start", {})
time.sleep(6)
st = api("GET", "/api/status")
print(
    "run",
    st.get("is_running"),
    "spd",
    round((st.get("total_speed") or 0) / 1048576, 2),
    "prog",
    st.get("total_progress"),
)
print(Counter(f.get("status") for f in st.get("files") or []))
for f in st.get("files") or []:
    if f.get("status") in ("downloading", "failed", "finished", "connecting"):
        print(
            f.get("status"),
            f.get("progress"),
            round((f.get("downloaded") or 0) / 1048576, 1),
            (f.get("filename") or "")[:55],
            (f.get("error") or "")[:70],
            (f.get("url") or "")[:60],
        )
