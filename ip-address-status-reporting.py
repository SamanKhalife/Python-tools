import os
import subprocess
import threading
from queue import Queue

def check_ip_status(ip):
    """Check the status of an IP address using ping."""
    try:
        result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False

def worker(queue, report):
    """Thread worker function to process IPs."""
    while not queue.empty():
        ip = queue.get()
        report[ip] = 'Online' if check_ip_status(ip) else 'Offline'
        queue.task_done()

def report_ip_status(ip_list):
    """Generate a report of IP statuses."""
    report = {}
    queue = Queue()


    for ip in ip_list:
        queue.put(ip)

    threads = []
    for _ in range(min(10, len(ip_list))):
        thread = threading.Thread(target=worker, args=(queue, report))
        thread.start()
        threads.append(thread)


    queue.join()


    for thread in threads:
        thread.join()

    return report

def save_report(report, filename='ip_status_report.txt'):
    """Save the IP status report to a file."""
    with open(filename, 'w') as f:
        for ip, status in report.items():
            f.write(f"{ip}: {status}\n")
    print(f"Report saved to {filename}")

def main():
    ip_list = input("Enter IP addresses separated by commas: ").strip().split(',')
    ip_list = [ip.strip() for ip in ip_list if ip.strip()]

    if not ip_list:
        print("No valid IP addresses provided.")
        return

    status_report = report_ip_status(ip_list)

    print("IP Address Status Report:")
    for ip, status in status_report.items():
        print(f"{ip}: {status}")

    save_report(status_report)

if __name__ == "__main__":
    main()
