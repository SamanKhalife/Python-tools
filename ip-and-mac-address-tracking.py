import subprocess
from tabulate import tabulate

def get_ip_mac_pairs():
    """Retrieve the IP and MAC address pairs from the ARP table."""
    try:
        output = subprocess.check_output(["arp", "-a"]).decode()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching ARP table: {e}")
        return {}

    devices = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[1].strip("()")
            mac = parts[3]
            devices[ip] = mac
    return devices

def search_device(devices, search_term):
    """Search for a specific IP or MAC address in the device list."""
    results = {ip: mac for ip, mac in devices.items() if search_term in ip or search_term in mac}
    return results

def save_report(devices, filename='ip_mac_report.txt'):
    """Save the IP and MAC address report to a file."""
    with open(filename, 'w') as f:
        for ip, mac in devices.items():
            f.write(f"IP: {ip}, MAC: {mac}\n")
    print(f"Report saved to {filename}")

def main():
    devices = get_ip_mac_pairs()

    if not devices:
        print("No devices found or an error occurred.")
        return

    print("\nIP and MAC Addresses:")
    print(tabulate(devices.items(), headers=["IP Address", "MAC Address"], tablefmt="grid"))


    search_term = input("\nEnter an IP address or MAC address to search (or press Enter to skip): ").strip()
    if search_term:
        search_results = search_device(devices, search_term)
        if search_results:
            print("\nSearch Results:")
            print(tabulate(search_results.items(), headers=["IP Address", "MAC Address"], tablefmt="grid"))
        else:
            print("No matches found.")

    save_report(devices)

if __name__ == "__main__":
    main()
