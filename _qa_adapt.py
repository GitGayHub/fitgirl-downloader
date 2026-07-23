"""Headless QA: adaptive catalog rows + fixed Download dock."""
import json
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"
VIEWPORTS = [
    {"name": "900", "width": 900, "height": 900},
    {"name": "1280", "width": 1280, "height": 800},
    {"name": "1600", "width": 1600, "height": 900},
    {"name": "1920", "width": 1920, "height": 1080},
]


def card_metrics(page):
    return page.evaluate(
        """() => {
        const grid = document.getElementById('games-grid-container');
        if (!grid) return {error: 'no grid'};
        const cards = [...grid.querySelectorAll(':scope > .game-card')];
        const cols = getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length;
        const cs = getComputedStyle(grid);
        const rects = cards.map(c => {
            const r = c.getBoundingClientRect();
            return {x: r.x, y: r.y, w: r.width, h: r.height, right: r.right, bottom: r.bottom};
        });
        // Overlap detection (ignore tiny float error)
        let overlaps = 0;
        for (let i = 0; i < rects.length; i++) {
            for (let j = i + 1; j < rects.length; j++) {
                const a = rects[i], b = rects[j];
                const ox = Math.min(a.right, b.right) - Math.max(a.x, b.x);
                const oy = Math.min(a.bottom, b.bottom) - Math.max(a.y, b.y);
                if (ox > 2 && oy > 2) overlaps++;
            }
        }
        // Count unique row Y (rounded)
        const rowYs = [...new Set(rects.map(r => Math.round(r.y / 4) * 4))].sort((a,b)=>a-b);
        const rows = rowYs.length;
        // Full rows: every row should have same count except maybe last
        const counts = rowYs.map(y => rects.filter(r => Math.abs(r.y - y) < 6).length);
        const fullRows = counts.filter(c => c === cols).length;
        const lastPartial = counts.length && counts[counts.length-1] !== cols;
        return {
            colsCss: cols,
            cssVars: {
                cols: grid.style.getPropertyValue('--catalog-cols'),
                gap: grid.style.getPropertyValue('--catalog-gap')
            },
            cardCount: cards.length,
            rows,
            counts,
            fullRows,
            lastPartial,
            overlaps,
            expectedPageSize: cols * (rows >= 4 ? 4 : (rows >= 3 ? 3 : rows)),
            sample: rects.slice(0, 3)
        };
    }"""
    )


def download_bar_metrics(page):
    return page.evaluate(
        """() => {
        const bar = document.getElementById('details-bottom-bar');
        if (!bar) return {error: 'no bar'};
        const r = bar.getBoundingClientRect();
        const cs = getComputedStyle(bar);
        return {
            parent: bar.parentElement && bar.parentElement.tagName,
            display: cs.display,
            position: cs.position,
            bottom: cs.bottom,
            top: r.top,
            barBottom: r.bottom,
            vh: window.innerHeight,
            distFromViewportBottom: window.innerHeight - r.bottom,
            left: r.left,
            width: r.width,
            height: r.height,
            zIndex: cs.zIndex,
            isVisible: bar.classList.contains('is-visible'),
            aria: bar.getAttribute('aria-hidden')
        };
    }"""
    )


def main():
    report = {"catalog": [], "details": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for vp in VIEWPORTS:
            page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
            # wait for cards
            try:
                page.wait_for_selector("#games-grid-container > .game-card", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(800)
            m = card_metrics(page)
            m["viewport"] = vp["name"]
            report["catalog"].append(m)
            page.screenshot(path=f"_qa_catalog_{vp['name']}.png", full_page=False)
            page.close()

        # Details + scroll download dock
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
        try:
            page.wait_for_selector("#games-grid-container > .game-card", timeout=25000)
        except Exception:
            pass
        page.wait_for_timeout(1000)
        # open first game
        card = page.query_selector("#games-grid-container > .game-card")
        if card:
            card.click(force=True)
            page.wait_for_timeout(4000)
            # wait for download bar
            for _ in range(30):
                vis = page.evaluate(
                    "() => { const b=document.getElementById('details-bottom-bar'); return b && getComputedStyle(b).display !== 'none'; }"
                )
                if vis:
                    break
                page.wait_for_timeout(500)

            top = download_bar_metrics(page)
            page.screenshot(path="_qa_details_top.png", full_page=False)

            # scroll details container down
            page.evaluate(
                """() => {
                const el = document.getElementById('game-details-container');
                if (el) el.scrollTop = el.scrollHeight;
                window.scrollTo(0, document.body.scrollHeight);
            }"""
            )
            page.wait_for_timeout(600)
            bot = download_bar_metrics(page)
            page.screenshot(path="_qa_details_scrolled.png", full_page=False)

            report["details"] = {
                "atTop": top,
                "afterScroll": bot,
                "stayedFixed": (
                    abs(top.get("distFromViewportBottom", 99) - bot.get("distFromViewportBottom", 0)) < 4
                    and top.get("position") == "fixed"
                    and bot.get("position") == "fixed"
                    and top.get("parent") == "BODY"
                ),
            }
        else:
            report["details"] = {"error": "no card to open"}

        browser.close()

    print(json.dumps(report, indent=2))
    # Fail criteria
    bad = False
    for c in report["catalog"]:
        if c.get("overlaps", 0) > 0:
            print(f"FAIL {c.get('viewport')}: overlaps={c['overlaps']}", file=sys.stderr)
            bad = True
        if c.get("cardCount", 0) > 0 and c.get("rows", 0) not in (2, 3, 4):
            # allow 2 only on tiny; prefer 3-4
            if c.get("viewport") not in ("900",) and c.get("rows", 0) < 3:
                print(f"WARN {c.get('viewport')}: rows={c.get('rows')}", file=sys.stderr)
        # page should be full rows: cardCount == cols * rows (no partial)
        cols = c.get("colsCss") or 0
        rows = c.get("rows") or 0
        if cols and rows and c.get("cardCount"):
            if c["cardCount"] % cols != 0:
                print(f"FAIL {c.get('viewport')}: partial row cardCount={c['cardCount']} cols={cols}", file=sys.stderr)
                bad = True
    if report.get("details") and not report["details"].get("stayedFixed") and "error" not in report["details"]:
        print("FAIL: download bar not fixed to viewport on scroll", file=sys.stderr)
        print(json.dumps(report["details"], indent=2), file=sys.stderr)
        bad = True
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
