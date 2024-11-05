from scapy.all import ARP, Ether, srp
import threading
import json
import time
import sys

def scan_network(ip_range):
    try:
        arp_request = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        result = srp(packet, timeout=3, verbose=0)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        return devices

    except Exception as e:
        print(f"Error occurred during scanning: {e}")
        return []

def print_devices(devices):
    print("\nDiscovered Devices:")
    print("{:<20} {:<20}".format("IP Address", "MAC Address"))
    print("=" * 40)
    for device in devices:
        print("{:<20} {:<20}".format(device['ip'], device['mac']))

def save_to_json(devices):
    with open('devices.json', 'w') as json_file:
        json.dump(devices, json_file, indent=4)
    print("Device information saved to devices.json")

def progress_indicator(total, current):
    percent = (current / total) * 100
    sys.stdout.write(f"\rScanning... {percent:.2f}% complete")
    sys.stdout.flush()

def main():
    ip_range = input("Enter the IP range to scan (e.g., 192.168.1.1/24): ")

    print(f"Scanning the network for IP range: {ip_range}")
    devices = []
    num_threads = 10
    ip_list = [f"{ip_range.split('/')[0].rsplit('.', 1)[0]}.{i}" for i in range(1, 255)]

    chunk_size = len(ip_list) // num_threads
    threads = []

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = start_index + chunk_size if i < num_threads - 1 else len(ip_list)
        ip_chunk = ip_list[start_index:end_index]

        thread = threading.Thread(target=lambda chunk=ip_chunk: devices.extend(scan_network(",".join(chunk))))
        threads.append(thread)
        thread.start()

    while any(thread.is_alive() for thread in threads):
        progress_indicator(len(ip_list), sum(len(devices) for thread in threads if thread.is_alive()))
        time.sleep(1)

    for thread in threads:
        thread.join()

    print_devices(devices)
    save_to_json(devices)

if __name__ == "__main__":
    main()
