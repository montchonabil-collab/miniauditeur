import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((target, port))
        s.close()
        return port, "open"
    except socket.timeout:
        return port, "filtered"
    except:
        return port, "closed"

def scan_range(target, start_port, end_port, workers=100):
    results = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(scan_port, target, port)
            for port in range(start_port, end_port + 1)
        ]

        for f in futures:
            results.append(f.result())

    return results
