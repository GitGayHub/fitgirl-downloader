"""QA: haze blobs, details media+desc, catalog fill+center last row."""
import json
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/"


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1500)

        # --- Catalog fill + metrics ---
        try:
            page.wait_for_selector("#games-grid-container > .game-card", timeout=25000)
        except Exception:
            pass
        page.wait_for_timeout(600)

        cat = page.evaluate(
            """() => {
            const grid = document.getElementById('games-grid-container');
            const cards = [...grid.querySelectorAll(':scope > .game-card')];
            const rects = cards.map(c => {
                const r = c.getBoundingClientRect();
                return {x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom};
            });
            const wrapper = document.getElementById('games-grid-section');
            const wr = wrapper.getBoundingClientRect();
            const lastBottom = rects.length ? Math.max(...rects.map(r => r.bottom)) : 0;
            const emptyBelow = wr.bottom - lastBottom;
            const rowYs = [...new Set(rects.map(r => Math.round(r.y/3)*3))].sort((a,b)=>a-b);
            const rows = rowYs.length;
            const colsVar = grid.style.getPropertyValue('--catalog-cols');
            const cardW = grid.style.getPropertyValue('--catalog-card-w');
            // overlaps
            let overlaps = 0;
            for (let i=0;i<rects.length;i++) for (let j=i+1;j<rects.length;j++) {
                const a=rects[i], b=rects[j];
                if (Math.min(a.right,b.right)-Math.max(a.x,b.x)>2 && Math.min(a.bottom,b.bottom)-Math.max(a.y,b.y)>2) overlaps++;
            }
            // last row centering: compute midpoint of last row vs grid center
            const lastY = rowYs[rowYs.length-1];
            const lastRow = rects.filter(r => Math.abs(r.y-lastY)<6);
            const lastLeft = Math.min(...lastRow.map(r=>r.x));
            const lastRight = Math.max(...lastRow.map(r=>r.right));
            const rowMid = (lastLeft+lastRight)/2;
            const gridMid = (wr.left+wr.right)/2;
            return {
                cardCount: cards.length, rows, colsVar, cardW,
                emptyBelow: Math.round(emptyBelow),
                overlaps,
                lastRowCount: lastRow.length,
                lastRowCenterOffset: Math.round(rowMid - gridMid),
                hazeBlobs: document.querySelectorAll('.haze-blob').length,
                hazeActive: document.getElementById('haze-background')?.className
            };
        }"""
        )
        page.screenshot(path="_qa6_catalog_p1.png")
        report["catalog_p1"] = cat

        # Page 2 last row center
        nxt = page.query_selector("#btn-next-page")
        if nxt and nxt.is_enabled():
            nxt.click()
            page.wait_for_timeout(1200)
            cat2 = page.evaluate(
                """() => {
                const grid = document.getElementById('games-grid-container');
                const cards = [...grid.querySelectorAll(':scope > .game-card')];
                const rects = cards.map(c => { const r=c.getBoundingClientRect(); return {x:r.x,y:r.y,right:r.right,bottom:r.bottom}; });
                const wrapper = document.getElementById('games-grid-section').getBoundingClientRect();
                const rowYs = [...new Set(rects.map(r => Math.round(r.y/3)*3))].sort((a,b)=>a-b);
                const lastY = rowYs[rowYs.length-1];
                const lastRow = rects.filter(r => Math.abs(r.y-lastY)<6);
                const lastLeft = Math.min(...lastRow.map(r=>r.x));
                const lastRight = Math.max(...lastRow.map(r=>r.right));
                const rowMid = (lastLeft+lastRight)/2;
                const gridMid = (wrapper.left+wrapper.right)/2;
                return {
                    cardCount: cards.length,
                    rows: rowYs.length,
                    lastRowCount: lastRow.length,
                    lastRowCenterOffset: Math.round(rowMid - gridMid)
                };
            }"""
            )
            page.screenshot(path="_qa6_catalog_p2.png")
            report["catalog_p2"] = cat2
            # back
            page.query_selector("#btn-prev-page").click()
            page.wait_for_timeout(800)

        # --- Details ---
        page.query_selector("#games-grid-container > .game-card").click(force=True)
        page.wait_for_timeout(5000)
        for _ in range(20):
            ready = page.evaluate(
                "() => document.getElementById('details-bottom-bar') && getComputedStyle(document.getElementById('details-bottom-bar')).display !== 'none'"
            )
            if ready:
                break
            page.wait_for_timeout(400)

        det = page.evaluate(
            """() => {
            const preview = document.querySelector('.details-media-header');
            const showcase = document.getElementById('screenshot-main-showcase-container');
            const thumbs = document.getElementById('game-screenshots-container');
            const desc = document.getElementById('details-desc-section');
            const right = document.querySelector('.details-right-column');
            const haze = document.getElementById('haze-background');
            const blob0 = document.querySelector('.haze-blob');
            const sr = showcase?.getBoundingClientRect();
            const rr = right?.getBoundingClientRect();
            const tr = thumbs?.getBoundingClientRect();
            const dr = desc?.getBoundingClientRect();
            const gapThumbsToDesc = (dr && tr) ? (dr.top - tr.bottom) : null;
            const mediaFill = (sr && rr) ? (sr.width / rr.width) : null;
            const anim = blob0 ? getComputedStyle(blob0).animationName : null;
            return {
                previewHidden: !preview || getComputedStyle(preview).display === 'none' || !document.body.contains(preview),
                mediaWidth: sr && Math.round(sr.width),
                rightWidth: rr && Math.round(rr.width),
                mediaFillPct: mediaFill != null ? Math.round(mediaFill*100) : null,
                gapThumbsToDesc: gapThumbsToDesc != null ? Math.round(gapThumbsToDesc) : null,
                descTop: dr && Math.round(dr.top),
                thumbsBottom: tr && Math.round(tr.bottom),
                hazeClass: haze?.className,
                blobAnim: anim,
                blobCount: document.querySelectorAll('.haze-blob').length,
                barFixed: (() => {
                    const b=document.getElementById('details-bottom-bar');
                    const r=b.getBoundingClientRect();
                    return { pos: getComputedStyle(b).position, distBot: Math.round(innerHeight-r.bottom), center: Math.round(r.left+r.width/2) };
                })()
            };
        }"""
        )
        page.screenshot(path="_qa6_details.png")
        report["details"] = det

        # scroll and bar
        page.evaluate(
            "() => { const el=document.getElementById('game-details-container'); if(el) el.scrollTop=el.scrollHeight; }"
        )
        page.wait_for_timeout(400)
        bar2 = page.evaluate(
            """() => {
            const b=document.getElementById('details-bottom-bar');
            const r=b.getBoundingClientRect();
            return { distBot: Math.round(innerHeight-r.bottom), top: Math.round(r.top) };
        }"""
        )
        page.screenshot(path="_qa6_details_scroll.png")
        report["details_scroll"] = bar2

        # back to catalog — smooth clear
        page.click("#btn-back-to-catalog-top")
        page.wait_for_timeout(400)
        mid = page.evaluate(
            "() => ({ haze: document.getElementById('haze-background')?.className, primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary') })"
        )
        page.wait_for_timeout(1500)
        after = page.evaluate(
            "() => ({ haze: document.getElementById('haze-background')?.className, primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary') })"
        )
        report["leave_details"] = {"mid": mid, "after": after}

        browser.close()

    print(json.dumps(report, indent=2))

    bad = False
    if report.get("catalog_p1", {}).get("overlaps", 0) > 0:
        print("FAIL overlaps", file=sys.stderr)
        bad = True
    if report.get("catalog_p1", {}).get("emptyBelow", 999) > 120:
        print(f"FAIL empty below catalog: {report['catalog_p1']['emptyBelow']}", file=sys.stderr)
        bad = True
    if report.get("catalog_p2") and abs(report["catalog_p2"].get("lastRowCenterOffset", 99)) > 40:
        # only fail if last row is partial
        if report["catalog_p2"].get("lastRowCount", 9) < 7:
            print(f"FAIL last row not centered: offset={report['catalog_p2']['lastRowCenterOffset']}", file=sys.stderr)
            bad = True
    if report.get("details", {}).get("gapThumbsToDesc", 999) is not None and report["details"]["gapThumbsToDesc"] > 40:
        print(f"FAIL gap thumbs→desc: {report['details']['gapThumbsToDesc']}", file=sys.stderr)
        bad = True
    if report.get("details", {}).get("mediaFillPct", 0) is not None and report["details"]["mediaFillPct"] < 85:
        print(f"FAIL media not full width: {report['details']['mediaFillPct']}%", file=sys.stderr)
        bad = True
    if report.get("details", {}).get("blobCount", 0) < 4:
        print("FAIL haze blobs missing", file=sys.stderr)
        bad = True
    if report.get("details", {}).get("blobAnim") in (None, "none"):
        print("FAIL blob animation not running", file=sys.stderr)
        bad = True

    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
