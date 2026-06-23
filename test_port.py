import socket

def test_conn(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((host, port))
        print(f"Connected successfully to {host}:{port}")
        s.close()
    except Exception as e:
        print(f"Failed to connect to {host}:{port}: {e}")

print("Testing loopback connections...")
test_conn("127.0.0.1", 8000)
test_conn("localhost", 8000)
test_conn("0.0.0.0", 8000)
