import urllib.request

def fetch(path):
    url = f"http://127.0.0.1:8000{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as res:
            content = res.read()
            print(f"Path: {path} - Status: {res.status} - Length: {len(content)}")
            if path == "/app.js":
                print("app.js snippet (first 100 chars):")
                print(content.decode()[:100])
    except Exception as e:
        print(f"Error fetching {path}: {e}")

fetch("/")
fetch("/style.css")
fetch("/app.js")
fetch("/api/status")
