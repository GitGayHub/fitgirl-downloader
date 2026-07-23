from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1600, "height": 900})
    page.goto("http://127.0.0.1:8000/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("#games-grid-container > .game-card", timeout=25000)
    page.wait_for_timeout(800)

    # open first game
    page.query_selector("#games-grid-container > .game-card").click(force=True)
    page.wait_for_timeout(6000)

    primary_game = page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()"
    )
    page.click("#btn-back-to-catalog-top")
    samples = []
    for ms in (0, 200, 500, 1000, 1800):
        page.wait_for_timeout(ms if ms == 0 else ms - (samples[-1][0] if samples else 0))
        samples.append(
            (
                ms,
                page.evaluate(
                    """() => ({
                    p: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim(),
                    h: document.getElementById('haze-background').className,
                    body: getComputedStyle(document.body).backgroundColor
                })"""
                ),
            )
        )
    # fix sampling - redo cleaner
    page.query_selector("#games-grid-container > .game-card").click(force=True)
    page.wait_for_timeout(5000)
    page.click("#btn-back-to-catalog-top")
    timeline = []
    for t in range(0, 20):
        timeline.append(
            page.evaluate(
                """() => getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()"""
            )
        )
        page.wait_for_timeout(100)

    # page 2
    page.wait_for_timeout(500)
    page.click("#btn-next-page")
    page.wait_for_timeout(1000)
    p2 = page.evaluate(
        """() => {
        const grid = document.getElementById('games-grid-container');
        const cards = [...grid.querySelectorAll(':scope > .game-card')];
        const rects = cards.map(c => {
            const r = c.getBoundingClientRect();
            return {x:r.x,y:r.y,right:r.right};
        });
        const wr = document.getElementById('games-grid-section').getBoundingClientRect();
        const rowYs = [...new Set(rects.map(r => Math.round(r.y/3)*3))].sort((a,b)=>a-b);
        const counts = rowYs.map(y => rects.filter(r => Math.abs(r.y-y)<6).length);
        const lastY = rowYs[rowYs.length-1];
        const last = rects.filter(r => Math.abs(r.y-lastY)<6);
        const mid = (Math.min(...last.map(r=>r.x)) + Math.max(...last.map(r=>r.right))) / 2;
        return {
            n: cards.length,
            counts,
            lastN: last.length,
            offset: Math.round(mid - (wr.left+wr.right)/2)
        };
    }"""
    )
    page.screenshot(path="_qa6_p2.png")

    print("game_primary", primary_game)
    print("timeline_unique", list(dict.fromkeys(timeline)))
    print("timeline_first_last", timeline[0], timeline[-1])
    print("p2", json.dumps(p2))
    changed = timeline[0] != timeline[-1]
    print("color_tweened", changed)
    b.close()
