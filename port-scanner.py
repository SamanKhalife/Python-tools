import socket
import threading
import queue


def scan_port(target, port, q):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    if result == 0:
        q.put(f"Port {port}: Open")
    else:
        q.put(f"Port {port}: Closed")
    s.close()


def port_scan(target, start_port, end_port):
    print(f"Scanning {target} from port {start_port} to {end_port}...")

    q = queue.Queue()
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port, q))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not q.empty():
        print(q.get())

if __name__ == "__main__":
    target = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port (1-65535): "))
    end_port = int(input("Enter the ending port (1-65535): "))

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Invalid port range. Please enter ports between 1 and 65535.")
    else:
        port_scan(target, start_port, end_port)
