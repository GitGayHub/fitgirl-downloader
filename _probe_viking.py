from playwright.sync_api import sync_playwright
import re

url = "https://vikingfile.com/f/u3TD5B1VIt"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
    )
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        locale="en-US",
        viewport={"width": 1365, "height": 900},
    )
    page = context.new_page()
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    hits = []

    def on_resp(r):
        u = r.url
        if any(
            x in u
            for x in (
                "vik1ng",
                "viking",
                "turnstile",
                "cloudflare",
                "download",
                "api",
                "challenges",
            )
        ):
            hits.append((r.request.method, r.status, u[:180]))

    page.on("response", on_resp)
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    html = page.content()
    open("_viking_page.html", "w", encoding="utf-8").write(html)

    keys = re.findall(r'data-sitekey=["\']([^"\']+)', html)
    keys2 = re.findall(r'sitekey["\']?\s*[:=]\s*["\']([^"\']+)', html)
    print("sitekeys", keys, keys2)
    print("title", page.title())
    print("hits", len(hits))
    for h in hits[:40]:
        print(h)
    for pat in [
        "direct-link",
        "download",
        "cf-turnstile",
        "turnstile",
        "vik1ngfile",
        "getLink",
        "api",
        "file_code",
        "hash",
    ]:
        if pat.lower() in html.lower():
            print("found", pat)

    # dump interesting scripts/attrs
    for sel in ["#download-link", "form", ".cf-turnstile", "[data-sitekey]", "button"]:
        try:
            n = page.locator(sel).count()
            print("sel", sel, "count", n)
            if n and n < 5:
                for i in range(n):
                    el = page.locator(sel).nth(i)
                    print(" ", sel, i, (el.inner_html()[:200] if False else el.evaluate("e => e.outerHTML")[:250]))
        except Exception as e:
            print("sel err", sel, e)

    browser.close()
print("saved _viking_page.html")
