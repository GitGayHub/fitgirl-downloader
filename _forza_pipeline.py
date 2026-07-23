#!/usr/bin/env python3
"""Forza Horizon 6 Online-Fix long test orchestrator.

1) Search Online-Fix for Forza Horizon 6
2) Analyze page → list hoster mirrors
3) Speed-test each mirror (sample first file, ~8s)
4) confirm_config + start on fastest
5) Watch every 5 minutes until done
6) Trigger extract if not auto; verify unpack
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
import urllib.error
import urllib.request
from typing import Any

BASE = "http://127.0.0.1:8000"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(OUT_DIR, "_forza_pipeline.log")
STATE_PATH = os.path.join(OUT_DIR, "_forza_pipeline_state.json")
DOWNLOAD_BASE = r"C:\Games"
GAME_QUERY = "Forza Horizon 6"
WATCH_EVERY_SEC = 5 * 60
SPEED_TEST_SEC = 8
SPEED_TEST_MAX_BYTES = 12 * 1024 * 1024  # 12 MB sample


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def save_state(obj: Any) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def api(method: str, path: str, body: dict | None = None, timeout: float = 120) -> dict:
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "replace")
        if not raw:
            return {"success": True, "_empty": True}
        return json.loads(raw)


def api_ok() -> bool:
    try:
        api("GET", "/api/status", timeout=8)
        return True
    except Exception as e:
        log(f"API down: {e}")
        return False


def ensure_server() -> None:
    if api_ok():
        log("Server already up")
        return
    log("Starting server...")
    import subprocess

    py = os.path.join(OUT_DIR, ".venv", "Scripts", "python.exe")
    if not os.path.exists(py):
        py = sys.executable
    # Detached process on Windows
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    out = open(os.path.join(OUT_DIR, "_server_out.txt"), "a", encoding="utf-8")
    err = open(os.path.join(OUT_DIR, "_server_err.txt"), "a", encoding="utf-8")
    subprocess.Popen(
        [py, "-u", "main.py"],
        cwd=OUT_DIR,
        stdout=out,
        stderr=err,
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
        close_fds=False,
    )
    for i in range(30):
        time.sleep(1)
        if api_ok():
            log(f"Server up after {i+1}s")
            return
    raise RuntimeError("Server failed to start")


def search_forza() -> list[dict]:
    log(f"Searching Online-Fix for: {GAME_QUERY}")
    data = api(
        "POST",
        "/api/search",
        {"query": GAME_QUERY, "provider": "onlinefix", "page": 1},
        timeout=120,
    )
    results = data.get("results") or []
    log(f"Search returned {len(results)} results (success={data.get('success')})")
    for i, r in enumerate(results, 1):
        log(f"  [{i}] {r.get('title')} | {r.get('url')}")
    return results


def pick_forza(results: list[dict]) -> dict:
    if not results:
        raise RuntimeError("No search results")
    # Prefer exact / close title match
    for r in results:
        t = (r.get("title") or "").lower()
        if "forza horizon 6" in t:
            return r
    for r in results:
        t = (r.get("title") or "").lower()
        if "forza" in t and "6" in t:
            return r
    return results[0]


def analyze(url: str) -> dict:
    log(f"Analyze: {url}")
    data = api("POST", "/api/analyze", {"url": url}, timeout=120)
    if not data.get("success"):
        raise RuntimeError(f"Analyze failed: {data}")
    mirrors = data.get("mirrors") or []
    log(f"Title={data.get('title')} size={data.get('repack_size')} mirrors={len(mirrors)}")
    for m in mirrors:
        log(f"  mirror: {m.get('name')} files≈{m.get('num_files')} url={str(m.get('url'))[:120]}")
    return data


def resolve_mirror_files(mirror: dict) -> list[dict]:
    url = mirror.get("url") or ""
    name = mirror.get("name") or "?"
    log(f"Resolve files for mirror: {name}")
    data = api("POST", "/api/analyze", {"url": url}, timeout=120)
    if not data.get("success"):
        raise RuntimeError(f"Resolve files failed for {name}: {data}")
    files = data.get("files") or []
    log(f"  → {len(files)} files")
    return files


def speed_test_url(url: str, seconds: float = SPEED_TEST_SEC) -> float:
    """Return bytes/sec sample download speed (0 on failure)."""
    if not url or url.startswith("online-fix-hoster:"):
        return 0.0
    # Skip Google Drive copy flow for speed test (needs account)
    if "drive.online-fix.me" in url or "drive.google.com" in url:
        return 0.0
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Range": f"bytes=0-{SPEED_TEST_MAX_BYTES - 1}",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    t0 = time.time()
    total = 0
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            while True:
                chunk = resp.read(256 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if time.time() - t0 >= seconds or total >= SPEED_TEST_MAX_BYTES:
                    break
    except Exception as e:
        log(f"  speed-test error: {e}")
        return 0.0
    elapsed = max(0.001, time.time() - t0)
    return total / elapsed


def pick_best_mirror(mirrors: list[dict]) -> tuple[dict, list[dict], float]:
    results = []
    for m in mirrors:
        name = m.get("name") or "?"
        # Skip own Google Disk for automated speed test (needs OAuth)
        if "google" in name.lower() or "own" in name.lower() and "disk" in name.lower():
            log(f"Skipping mirror (needs GDrive auth): {name}")
            continue
        try:
            files = resolve_mirror_files(m)
        except Exception as e:
            log(f"  resolve failed for {name}: {e}")
            continue
        if not files:
            log(f"  no files for {name}")
            continue
        # Prefer a mid-size game part for testing
        sample = None
        for f in files:
            fn = (f.get("filename") or "").lower()
            if "part" in fn and fn.endswith(".rar"):
                sample = f
                break
        if sample is None:
            sample = files[0]
        url = sample.get("url") or ""
        log(f"Speed-testing {name} via {sample.get('filename')} ...")
        bps = speed_test_url(url)
        mib = bps / (1024 * 1024)
        log(f"  → {mib:.2f} MiB/s ({bps:.0f} B/s)")
        results.append({"mirror": m, "files": files, "bps": bps, "mib": mib})

    if not results:
        raise RuntimeError("No mirrors could be speed-tested")

    results.sort(key=lambda x: x["bps"], reverse=True)
    log("=== Speed ranking ===")
    for i, r in enumerate(results, 1):
        log(f"  #{i} {r['mirror'].get('name')}: {r['mib']:.2f} MiB/s")

    best = results[0]
    return best["mirror"], best["files"], best["bps"]


def wipe_forza() -> None:
    import shutil

    path = os.path.join(DOWNLOAD_BASE, "Forza Horizon 6")
    if os.path.isdir(path):
        log(f"Deleting {path} ...")
        shutil.rmtree(path, ignore_errors=True)
    # also session
    try:
        api("POST", "/api/pause", {})
    except Exception:
        pass
    try:
        api("POST", "/api/reset", {})
        log("Session reset OK")
    except Exception as e:
        log(f"Reset warn: {e}")
        sp = os.path.join(OUT_DIR, "session_state.json")
        if os.path.exists(sp):
            os.remove(sp)
            log("Removed session_state.json manually")


def configure_and_start(title: str, mirror_name: str, files: list[dict]) -> None:
    log(f"confirm_config title={title} mirror={mirror_name} files={len(files)}")
    # Normalize file objects for queue
    queue = []
    for f in files:
        queue.append(
            {
                "filename": f.get("filename"),
                "url": f.get("url"),
                "type": f.get("type") or "game_part",
                "status": "waiting",
                "progress": 0,
                "downloaded": 0,
                "size": int(f.get("size") or 0),
                "speed": 0,
                "time_left": -1,
                "error": "",
            }
        )
    data = api(
        "POST",
        "/api/confirm_config",
        {
            "game_title": title,
            "base_download_dir": DOWNLOAD_BASE,
            "download_dir": DOWNLOAD_BASE,
            "files": queue,
            "active_mirror": mirror_name,
            "original_size": "",
        },
        timeout=60,
    )
    if not data.get("success"):
        raise RuntimeError(f"confirm_config failed: {data}")
    log("Config OK, starting download...")
    api("POST", "/api/start", {})
    log("Download started")


def status_snapshot() -> dict:
    return api("GET", "/api/status", timeout=30)


def watch_until_done() -> dict:
    log(f"Watcher every {WATCH_EVERY_SEC // 60} minutes until complete...")
    last_extract_try = 0
    while True:
        try:
            st = status_snapshot()
        except Exception as e:
            log(f"Status error: {e} — will retry in 60s")
            time.sleep(60)
            if not api_ok():
                try:
                    ensure_server()
                except Exception as e2:
                    log(f"Restart failed: {e2}")
            continue

        files = st.get("files") or []
        n = len(files)
        finished = sum(1 for f in files if f.get("status") == "finished")
        failed = sum(1 for f in files if f.get("status") == "failed")
        active = sum(1 for f in files if f.get("status") in ("downloading", "connecting", "copying"))
        waiting = sum(1 for f in files if f.get("status") == "waiting")
        prog = st.get("total_progress", 0)
        speed = st.get("total_speed", 0) or 0
        mib = speed / (1024 * 1024)
        extracting = st.get("is_extracting")
        extracted = st.get("is_extracted")
        running = st.get("is_running")
        ddir = st.get("download_dir") or ""

        # disk size
        disk = 0
        if ddir and os.path.isdir(ddir):
            for root, _dirs, names in os.walk(ddir):
                for name in names:
                    try:
                        disk += os.path.getsize(os.path.join(root, name))
                    except OSError:
                        pass
        disk_gb = disk / (1024**3)

        log(
            f"PROGRESS {prog}% | {finished}/{n} finished, {active} active, "
            f"{waiting} waiting, {failed} failed | speed={mib:.2f} MiB/s | "
            f"disk={disk_gb:.2f} GB | running={running} extracting={extracting} extracted={extracted}"
        )
        # Log failed files
        for f in files:
            if f.get("status") == "failed":
                log(f"  FAIL: {f.get('filename')}: {f.get('error')}")

        save_state(
            {
                "ts": time.time(),
                "progress": prog,
                "finished": finished,
                "failed": failed,
                "n": n,
                "speed_mib": mib,
                "disk_gb": disk_gb,
                "extracting": extracting,
                "extracted": extracted,
                "download_dir": ddir,
            }
        )

        all_done = n > 0 and finished == n
        if all_done:
            log("All files finished!")
            if extracted:
                log("Already extracted.")
                return st
            if extracting:
                log("Extraction in progress...")
            else:
                now = time.time()
                if now - last_extract_try > 30:
                    last_extract_try = now
                    log("Triggering /api/extract ...")
                    try:
                        api("POST", "/api/extract", {})
                    except Exception as e:
                        log(f"Extract API error: {e}")
            # poll extract
            for _ in range(120):  # up to ~2h if 60s
                time.sleep(30)
                try:
                    st2 = status_snapshot()
                except Exception as e:
                    log(f"extract poll error: {e}")
                    continue
                log(
                    f"EXTRACT poll extracting={st2.get('is_extracting')} "
                    f"progress={st2.get('extraction_progress')} extracted={st2.get('is_extracted')}"
                )
                if st2.get("is_extracted") and not st2.get("is_extracting"):
                    log("Extraction complete and game content detected.")
                    return st2
                if not st2.get("is_extracting") and st2.get("extraction_progress", 0) >= 100:
                    log("Extraction worker finished (check is_extracted flag).")
                    return st2
            return st

        # If queue idle with failures, try retry all failed once in a while
        if not running and failed and waiting == 0 and active == 0 and not all_done:
            log("Queue idle with failures — retrying failed files...")
            for idx, f in enumerate(files):
                if f.get("status") == "failed":
                    try:
                        api("POST", "/api/retry", {"index": idx})
                    except Exception as e:
                        log(f"retry {idx} error: {e}")
            try:
                api("POST", "/api/start", {})
            except Exception:
                pass

        time.sleep(WATCH_EVERY_SEC)


def verify_install(st: dict) -> None:
    ddir = st.get("download_dir") or ""
    log(f"Verify install/extract at: {ddir}")
    if not ddir or not os.path.isdir(ddir):
        log("Download dir missing!")
        return
    entries = os.listdir(ddir)
    rars = [e for e in entries if e.lower().endswith(".rar")]
    exes = [e for e in entries if e.lower().endswith(".exe")]
    dirs = [e for e in entries if os.path.isdir(os.path.join(ddir, e))]
    log(f"  entries={len(entries)} rars={len(rars)} exes={len(exes)} dirs={len(dirs)}")
    for d in dirs[:20]:
        log(f"  dir: {d}")
    for e in exes[:20]:
        log(f"  exe: {e}")

    # Try install API (FitGirl setup) — Online-Fix often has no setup
    try:
        api("POST", "/api/install", {})
        log("Install API accepted (launched setup if found).")
    except Exception as e:
        log(f"Install API: {e} (expected for Online-Fix if no setup.exe)")

    # FAQ reminder
    log("Online-Fix FAQ: password=online-fix.me; unpack first part only; game usually playable after extract.")


def main() -> int:
    log("=== Forza Online-Fix pipeline start ===")
    try:
        ensure_server()
        wipe_forza()
        if not api_ok():
            ensure_server()

        results = search_forza()
        game = pick_forza(results)
        log(f"Picked: {game.get('title')} | {game.get('url')}")
        meta = analyze(game["url"])
        mirrors = meta.get("mirrors") or []
        if not mirrors:
            raise RuntimeError("No mirrors on game page")

        best_mirror, files, bps = pick_best_mirror(mirrors)
        log(
            f"WINNER: {best_mirror.get('name')} at {bps/(1024*1024):.2f} MiB/s "
            f"({len(files)} files)"
        )
        save_state(
            {
                "game": game,
                "best_mirror": best_mirror.get("name"),
                "bps": bps,
                "file_count": len(files),
            }
        )

        title = meta.get("title") or game.get("title") or GAME_QUERY
        configure_and_start(title, best_mirror.get("name") or "Unknown", files)
        st = watch_until_done()
        verify_install(st)
        log("=== Pipeline finished ===")
        return 0
    except Exception:
        log("FATAL:\n" + traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
