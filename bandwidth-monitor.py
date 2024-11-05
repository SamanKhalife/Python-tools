import psutil
import time
import csv
import threading

class BandwidthMonitor:
    def __init__(self, interfaces, interval=1):
        self.interfaces = interfaces
        self.interval = interval
        self.data = {interface: [] for interface in interfaces}

    def monitor_interface(self, interface):
        previous_data = psutil.net_io_counters(pernic=True)[interface]
        while True:
            time.sleep(self.interval)
            current_data = psutil.net_io_counters(pernic=True)[interface]

            sent_bytes = current_data.bytes_sent - previous_data.bytes_sent
            recv_bytes = current_data.bytes_recv - previous_data.bytes_recv

            self.data[interface].append((sent_bytes, recv_bytes))
            previous_data = current_data

            print(f"{interface} - Sent: {sent_bytes} bytes, Received: {recv_bytes} bytes")

    def start_monitoring(self):
        threads = []
        for interface in self.interfaces:
            thread = threading.Thread(target=self.monitor_interface, args=(interface,))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def log_to_csv(self):
        with open('bandwidth_log.csv', 'w', newline='') as csvfile:
            fieldnames = ['Interface', 'Sent Bytes', 'Received Bytes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            while True:
                time.sleep(self.interval)
                for interface, usage in self.data.items():
                    if usage:
                        sent, recv = usage[-1]
                        writer.writerow({'Interface': interface, 'Sent Bytes': sent, 'Received Bytes': recv})

def main():
    interfaces = input("Enter the network interfaces separated by commas (e.g., wlp2s0, eth0): ").split(',')
    interfaces = [iface.strip() for iface in interfaces]
    interval = int(input("Enter monitoring interval in seconds (default is 1): ") or 1)

    monitor = BandwidthMonitor(interfaces, interval)

    threading.Thread(target=monitor.start_monitoring, daemon=True).start()

    monitor.log_to_csv()

if __name__ == "__main__":
    main()
