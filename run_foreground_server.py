import main
import sys
import time
import threading

print("Starting server in foreground test...")
t = threading.Thread(target=main.start_server, daemon=True)
t.start()

# Wait 5 seconds
time.sleep(5)
print("Foreground test complete.")
