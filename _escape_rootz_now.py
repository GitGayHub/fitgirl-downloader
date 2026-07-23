import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000"


def post(path, body=None):
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(
        BASE + path, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    return urllib.request.urlopen(req, timeout=60).read().decode()


def get(path):
    return json.load(urllib.request.urlopen(BASE + path, timeout=20))


print("escape", post("/api/escape_pixeldrain", {"mirror": "Rootz"}))
time.sleep(10)
for i in range(10):
    time.sleep(5)
    st = get("/api/status")
    spd = (st.get("total_speed") or 0) / 1048576
    act = [f for f in (st.get("files") or []) if f.get("status") in ("downloading", "connecting")]
    hosts = {}
    for f in act:
        u = f.get("url") or ""
        if "rootz" in u:
            h = "rootz"
        elif "pixeldrain" in u:
            h = "pd"
        else:
            h = "other"
        hosts[h] = hosts.get(h, 0) + 1
    print(
        f"t+{(i+1)*5}s spd={spd:.2f} prog={st.get('total_progress')} "
        f"mirror={st.get('active_mirror')} act={len(act)} hosts={hosts} "
        f"workers={st.get('active_workers_count')}"
    )
    for f in act[:5]:
        print(
            " ",
            (f.get("filename") or "")[:42],
            f.get("status"),
            round((f.get("speed") or 0) / 1048576, 2),
            (f.get("url") or "")[:55],
        )
