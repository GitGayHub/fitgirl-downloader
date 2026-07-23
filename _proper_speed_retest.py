#!/usr/bin/env python3
"""Proper Online-Fix hoster speed retest for Forza Horizon 6.

Unlike the first pass (raw urllib on page URLs), this:
  1) resolves each hoster's REAL CDN link via /api/speed_probe (Playwright extractors)
  2) samples 15s / 24MB
  3) registers mirror catalog + rank into the live downloader for auto-failover
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8000"
GAME_URL = "https://online-fix.me/games/officialservers/18099-forza-horizon-6-po-seti.html"
SECONDS = 15
MAX_BYTES = 24 * 1024 * 1024


def api(method: str, path: str, body=None, timeout=300):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "replace")
        return json.loads(raw) if raw else {}


def main():
    print("=== Proper multi-hoster speed retest (CDN-resolved) ===", flush=True)
    meta = api("POST", "/api/analyze", {"url": GAME_URL}, timeout=120)
    if not meta.get("success"):
        print("analyze failed", meta)
        return 1
    mirrors = meta.get("mirrors") or []
    print(f"Title={meta.get('title')} mirrors={len(mirrors)}", flush=True)

    catalog = {}
    speeds = {}  # bps
    details = []

    for m in mirrors:
        name = m.get("name") or "?"
        url = m.get("url") or ""
        if "google" in name.lower() or ("own" in name.lower() and "disk" in name.lower()):
            print(f"SKIP {name} (GDrive OAuth)", flush=True)
            continue
        print(f"\n--- {name} ---", flush=True)
        try:
            files_data = api("POST", "/api/analyze", {"url": url}, timeout=120)
        except Exception as e:
            print(f"  resolve files FAIL: {e}", flush=True)
            continue
        files = files_data.get("files") or []
        print(f"  files={len(files)}", flush=True)
        if not files:
            continue
        fmap = {f["filename"]: f["url"] for f in files if f.get("filename") and f.get("url")}
        catalog[name] = fmap

        # Prefer full game part01 over tiny fix rar
        sample = None
        for f in files:
            fn = (f.get("filename") or "").lower()
            if "part01" in fn or ".part1." in fn:
                sample = f
                break
        if sample is None:
            # largest by known size or first non-fix tiny
            non_fix = [f for f in files if "fix" not in (f.get("filename") or "").lower()]
            sample = (non_fix or files)[0]

        print(f"  probe sample: {sample.get('filename')}", flush=True)
        print(f"  page/url: {str(sample.get('url'))[:100]}...", flush=True)
        t0 = time.time()
        try:
            probe = api(
                "POST",
                "/api/speed_probe",
                {
                    "url": sample.get("url"),
                    "seconds": SECONDS,
                    "max_bytes": MAX_BYTES,
                },
                timeout=300,
            )
        except Exception as e:
            print(f"  probe FAIL: {e}", flush=True)
            probe = {"success": False, "error": str(e), "bps": 0, "mib": 0}
        dt = time.time() - t0
        mib = float(probe.get("mib") or 0)
        bps = float(probe.get("bps") or 0)
        speeds[name] = bps
        details.append({"mirror": name, "probe": probe, "sample": sample.get("filename"), "took": dt})
        ok = probe.get("success")
        print(
            f"  → success={ok} {mib:.2f} MiB/s ({bps:.0f} B/s) "
            f"bytes={probe.get('bytes')} hoster={probe.get('hoster')} "
            f"err={probe.get('error')!r}",
            flush=True,
        )
        if probe.get("direct"):
            print(f"  direct: {str(probe.get('direct'))[:120]}", flush=True)

    rank = sorted(speeds.keys(), key=lambda k: speeds[k], reverse=True)
    print("\n=== RANKING (CDN-resolved) ===", flush=True)
    for i, name in enumerate(rank, 1):
        print(f"  #{i} {name}: {speeds[name]/(1024*1024):.2f} MiB/s", flush=True)

    reg = api(
        "POST",
        "/api/register_mirrors",
        {
            "catalog": catalog,
            "speeds": speeds,
            "rank": rank,
            "high_speed_mode": True,
            "min_acceptable_speed": 2 * 1024 * 1024,
        },
        timeout=60,
    )
    print("register:", json.dumps(reg, ensure_ascii=False)[:500], flush=True)

    out = {"rank": rank, "speeds_mib": {k: v / (1024 * 1024) for k, v in speeds.items()}, "details": details}
    with open("_proper_speed_retest_result.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("saved _proper_speed_retest_result.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
