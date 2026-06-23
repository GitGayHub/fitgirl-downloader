import threading
import time
from curl_cffi import requests

def run_request():
    try:
        print("Thread starting request...")
        res = requests.get("https://fuckingfast.co/t2c2tubk1dc1", impersonate="chrome120", timeout=10)
        print("Thread response status:", res.status_code)
    except Exception as e:
        print("Thread error:", e)

print("Starting test...")
t = threading.Thread(target=run_request)
t.start()
t.join()
print("Test completed.")
