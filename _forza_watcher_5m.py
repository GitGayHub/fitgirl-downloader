"""Emit one status line every 5 minutes until Forza is finished+extracted."""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

INTERVAL = 5 * 60
URL = "http://127.0.0.1:8000/api/status"


def snap() -> dict:
    with urllib.request.urlopen(URL, timeout=30) as r:
        return json.load(r)


def disk_gb(path: str) -> float:
    if not path or not os.path.isdir(path):
        return 0.0
    total = 0
    for root, _, names in os.walk(path):
        for n in names:
            try:
                total += os.path.getsize(os.path.join(root, n))
            except OSError:
                pass
    return total / (1024**3)


def main() -> int:
    # First report immediately
    while True:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            s = snap()
            files = s.get("files") or []
            n = len(files)
            fin = sum(1 for f in files if f.get("status") == "finished")
            fail = sum(1 for f in files if f.get("status") == "failed")
            act = sum(
                1
                for f in files
                if f.get("status") in ("downloading", "connecting", "copying")
            )
            spd = (s.get("total_speed") or 0) / (1024 * 1024)
            disk = disk_gb(s.get("download_dir") or "")
            line = (
                f"[{ts}] Forza {s.get('total_progress')}% | {fin}/{n} done "
                f"fail={fail} act={act} | {spd:.2f} MiB/s | disk={disk:.2f}GB | "
                f"run={s.get('is_running')} extract={s.get('is_extracting')}/{s.get('is_extracted')}"
            )
            print(line, flush=True)
            if n > 0 and fin == n and s.get("is_extracted"):
                print(f"[{ts}] COMPLETE extracted=true", flush=True)
                return 0
            # If all finished but not extracted yet, keep polling faster
            if n > 0 and fin == n and not s.get("is_extracted"):
                time.sleep(30)
                continue
        except Exception as e:
            print(f"[{ts}] status error: {e}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    sys.exit(main())
