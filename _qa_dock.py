from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1400, "height": 900})
    page.goto("http://127.0.0.1:8000/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("#games-grid-container > .game-card", timeout=25000)
    page.wait_for_timeout(800)
    page.query_selector("#games-grid-container > .game-card").click(force=True)
    page.wait_for_timeout(5000)
    for _ in range(25):
        vis = page.evaluate(
            "() => { const b = document.getElementById('details-bottom-bar');"
            " return !!(b && getComputedStyle(b).display !== 'none'); }"
        )
        if vis:
            break
        page.wait_for_timeout(400)

    def metrics():
        return page.evaluate(
            """() => {
            const bar = document.getElementById('details-bottom-bar');
            if (!bar) return {error:'none'};
            const r = bar.getBoundingClientRect();
            const cs = getComputedStyle(bar);
            return {
              parent: bar.parentElement && bar.parentElement.tagName,
              position: cs.position,
              leftCss: cs.left,
              transform: cs.transform,
              left: r.left,
              width: r.width,
              top: r.top,
              bottom: r.bottom,
              vh: innerHeight,
              vw: innerWidth,
              centerX: r.left + r.width / 2,
              distBottom: innerHeight - r.bottom
            };
            }"""
        )

    top = metrics()
    page.evaluate(
        "() => { const el = document.getElementById('game-details-container');"
        " if (el) el.scrollTop = el.scrollHeight; }"
    )
    page.wait_for_timeout(500)
    scrolled = metrics()
    page.screenshot(path="_qa_details_fixed.png")
    print(json.dumps({"top": top, "scrolled": scrolled}, indent=2))
    ok = (
        top.get("position") == "fixed"
        and top.get("parent") == "BODY"
        and abs(top.get("centerX", 0) - top.get("vw", 0) / 2) < 30
        and top.get("distBottom", 99) < 40
        and abs(scrolled.get("top", -1) - top.get("top", -2)) < 2
    )
    print("PASS" if ok else "FAIL")
    b.close()
    raise SystemExit(0 if ok else 1)
