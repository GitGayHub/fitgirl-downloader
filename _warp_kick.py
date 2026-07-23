import json
import time
import urllib.request

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


def main():
    try:
        print("clear", api("GET", "/api/clear_pixeldrain_limit"))
    except Exception as e:
        print("clear err", e)
    print("pause", api("POST", "/api/pause", {}))
    time.sleep(3)
    print("start", api("POST", "/api/start", {}))
    for i in range(6):
        time.sleep(5)
        st = api("GET", "/api/status")
        spd = (st.get("total_speed") or 0) / 1048576
        print(
            f"t+{(i+1)*5}s run={st.get('is_running')} prog={st.get('total_progress')} "
            f"spd={spd:.2f} MiB/s pd_limit={st.get('pixeldrain_limit_reached')}"
        )
        for f in st.get("files") or []:
            if f.get("status") in ("downloading", "connecting", "failed"):
                print(
                    " ",
                    f.get("status"),
                    f.get("progress"),
                    round((f.get("speed") or 0) / 1048576, 2),
                    "MiB/s",
                    (f.get("filename") or "")[:48],
                    (f.get("error") or "")[:70],
                )


if __name__ == "__main__":
    main()
