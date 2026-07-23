"""Try multiple VikingFile extraction strategies."""
from playwright.sync_api import sync_playwright
import re
import json
import time
import requests

URL = "https://vikingfile.com/f/u3TD5B1VIt"
SITEKEY = "0x4AAAAAAAgbsMNBuk2d3Qp6"


def try_playwright(channel=None, headless=True, wait_s=45):
    print(f"\n=== playwright channel={channel} headless={headless} ===")
    with sync_playwright() as p:
        kwargs = {
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }
        if channel:
            kwargs["channel"] = channel
        try:
            browser = p.chromium.launch(**kwargs)
        except Exception as e:
            print("launch fail", e)
            return None
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1400, "height": 900},
            java_script_enabled=True,
        )
        page = context.new_page()
        page.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            """
        )
        found = {"link": None, "posts": []}

        def on_response(resp):
            try:
                if resp.request.method == "POST" and (
                    "vik1ngfile.site" in resp.url or "vikingfile.com" in resp.url
                ):
                    txt = resp.text()
                    found["posts"].append((resp.status, resp.url[:80], txt[:300]))
                    try:
                        data = resp.json()
                        link = data.get("link") or data.get("direct-link") or data.get("url")
                        if link:
                            found["link"] = link
                    except Exception:
                        pass
            except Exception:
                pass

        page.on("response", on_response)
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        except Exception as e:
            print("goto", e)

        # wait for captcha widget + try click
        for i in range(wait_s):
            if found["link"]:
                break
            # try read hidden token
            try:
                tok = page.evaluate(
                    """() => {
                    const el = document.querySelector('[name="cf-turnstile-response"]');
                    return el ? el.value : '';
                }"""
                )
                if tok and len(tok) > 20:
                    print("got token len", len(tok), "at", i)
                    # POST ourselves
                    post_url = page.url
                    r = requests.post(
                        post_url,
                        data={"cf-turnstile-response": tok},
                        headers={
                            "User-Agent": "Mozilla/5.0",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Referer": post_url,
                        },
                        timeout=30,
                    )
                    print("manual post", r.status_code, r.text[:200])
                    try:
                        data = r.json()
                        link = data.get("link") or data.get("direct-link")
                        if link:
                            found["link"] = link
                    except Exception:
                        pass
                    break
            except Exception:
                pass
            # click turnstile iframe checkbox if visible
            try:
                for frame in page.frames:
                    if "challenges.cloudflare.com" in (frame.url or ""):
                        box = frame.locator("input, body")
                        if box.count():
                            box.first.click(timeout=500)
            except Exception:
                pass
            page.wait_for_timeout(1000)

        print("posts", found["posts"][:5])
        print("link", (found["link"] or "")[:120])
        browser.close()
        return found["link"]


if __name__ == "__main__":
    for ch, hl in [(None, True), ("chrome", True), ("chrome", False)]:
        try:
            link = try_playwright(channel=ch, headless=hl, wait_s=35)
            if link:
                print("SUCCESS", ch, hl, link[:100])
                break
        except Exception as e:
            print("strategy fail", ch, hl, e)
