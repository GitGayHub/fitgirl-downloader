import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000"


def get(path):
    return json.load(urllib.request.urlopen(BASE + path, timeout=20))


def post(path, body=None):
    data = b"{}" if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    return json.load(urllib.request.urlopen(req, timeout=30))


print("warp", get("/api/warp/status"))
st = get("/api/status")
print(
    "status warp",
    st.get("warp_status"),
    "connected",
    st.get("warp_connected"),
    "prog",
    st.get("total_progress"),
)
print("start", post("/api/start"))
time.sleep(10)
st = get("/api/status")
spd = (st.get("total_speed") or 0) / 1048576
print("spd", round(spd, 2), "prog", st.get("total_progress"), "run", st.get("is_running"))
for f in st.get("files") or []:
    if f.get("status") == "downloading":
        print(
            "dl",
            f.get("progress"),
            round((f.get("speed") or 0) / 1048576, 2),
            (f.get("filename") or "")[:50],
        )
