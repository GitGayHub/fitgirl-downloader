import re

html = open("_viking_page.html", encoding="utf-8").read()
for m in re.findall(r'src=["\']([^"\']+)["\']', html):
    if any(x in m for x in ("vik", "custom", "turnstile", "captcha", "assets")):
        print("src", m)

for i, s in enumerate(re.findall(r"<script[^>]*>([\s\S]*?)</script>", html)):
    if s.strip() and any(
        x in s
        for x in (
            "turnstile",
            "download",
            "sitekey",
            "direct",
            "showCaptcha",
            "captcha",
            "file",
        )
    ):
        print("--- inline", i, "len", len(s))
        print(s[:2000])
        print("...")

for pat in [
    "file_code",
    "hash",
    "fileId",
    "file_id",
    "showCaptcha",
    "direct-link",
    "vik1ngfile",
    "0x4AAAA",
    "download-link",
]:
    if pat in html:
        idx = html.find(pat)
        print("ctx", pat, repr(html[max(0, idx - 60) : idx + 140]))
