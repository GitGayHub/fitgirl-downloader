import json
import os
import urllib.request
from collections import Counter

d = json.load(urllib.request.urlopen("http://127.0.0.1:8000/api/status", timeout=20))
files = d.get("files") or []
c = Counter(f.get("status") for f in files)
total = sum(int(f.get("size") or 0) for f in files)
done = sum(int(f.get("size") or f.get("downloaded") or 0) for f in files if f.get("status") == "finished")
partial = sum(int(f.get("downloaded") or 0) for f in files if f.get("status") != "finished")
spd = (d.get("total_speed") or 0) / 1048576
print(
    f"title={d.get('game_title')} mirror={d.get('active_mirror')} "
    f"prog={d.get('total_progress')}% run={d.get('is_running')} spd={spd:.2f} MiB/s"
)
print(f"counts={dict(c)} expected_total_GB={total/1e9:.2f} doneish_GB={(done+partial)/1e9:.2f}")
print(f"dir={d.get('download_dir')}")
dd = d.get("download_dir") or ""
if dd and os.path.isdir(dd):
    disk = 0
    for root, _, names in os.walk(dd):
        for n in names:
            try:
                disk += os.path.getsize(os.path.join(root, n))
            except OSError:
                pass
    print(f"disk_GB={disk/1e9:.3f}")
for f in files:
    st = f.get("status")
    if st in ("downloading", "connecting", "finished", "failed"):
        print(
            f"  {st:12} {f.get('progress'):3}% "
            f"{(f.get('downloaded') or 0)/1048576:8.1f}MB "
            f"{(f.get('speed') or 0)/1048576:5.2f}MiB/s "
            f"{f.get('filename')} {(f.get('error') or '')[:100]}"
        )
for line in (d.get("logs") or [])[-8:]:
    print(line)
