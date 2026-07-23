"""Re-queue falsely-finished incomplete RARs, re-register mirrors, resume."""
import json
import os
import time
import urllib.request

BASE = "http://127.0.0.1:8000"


def api(method, path, body=None, timeout=120):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else {}


def main():
    for _ in range(20):
        try:
            st = api("GET", "/api/status")
            break
        except Exception:
            time.sleep(1)
    else:
        raise SystemExit("server down")

    ddir = st.get("download_dir") or ""
    files = st.get("files") or []
    fixed = 0
    for i, f in enumerate(files):
        fn = f.get("filename") or ""
        path = os.path.join(ddir, fn) if ddir else ""
        disk = os.path.getsize(path) if path and os.path.isfile(path) else 0
        size = int(f.get("size") or 0)
        # Expected multi-GB parts shouldn't be "finished" at 10MB
        if f.get("status") == "finished":
            if size > 50 * 1024 * 1024 and disk < size * 0.95:
                print(f"REOPEN incomplete finished: {fn} disk={disk} size={size}")
                api("POST", "/api/retry", {"index": i})
                fixed += 1
            elif size <= 0 and disk < 100 * 1024 * 1024 and fn.lower().endswith(".rar") and "part" in fn.lower():
                print(f"REOPEN tiny part: {fn} disk={disk}")
                api("POST", "/api/retry", {"index": i})
                fixed += 1
    print(f"fixed={fixed}")

    # Re-register catalog from last retest result if present
    if os.path.isfile("_proper_speed_retest_result.json"):
        # Rebuild catalog via analyze is heavy; just set rank demoting PD
        st = api("GET", "/api/status")
        cat = st.get("mirror_catalog") or {}
        if cat:
            speeds = st.get("mirror_speeds") or {}
            # demote pixeldrain if limit
            rank = sorted(speeds.keys(), key=lambda k: speeds.get(k) or 0, reverse=True)
            api(
                "POST",
                "/api/register_mirrors",
                {
                    "catalog": cat,
                    "speeds": speeds,
                    "rank": rank,
                    "high_speed_mode": True,
                    "min_acceptable_speed": int(0.3 * 1024 * 1024),  # 0.3 MiB/s — avoid thrash on slow Rootz
                },
            )
            print("catalog re-registered, rank", rank)

    api("POST", "/api/start", {})
    time.sleep(3)
    st = api("GET", "/api/status")
    print(
        "run",
        st.get("is_running"),
        "prog",
        st.get("total_progress"),
        "spd",
        round((st.get("total_speed") or 0) / 1048576, 2),
        "pd_limit",
        st.get("pixeldrain_limit_reached"),
    )
    from collections import Counter

    print(Counter(f.get("status") for f in st.get("files") or []))


if __name__ == "__main__":
    main()
