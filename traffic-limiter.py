import subprocess
import re

def is_valid_interface(interface):
    """Check if the network interface is valid."""
    try:
        output = subprocess.check_output("ip link show", shell=True).decode()
        return interface in output
    except Exception as e:
        print(f"Error checking interface: {e}")
        return False

def is_valid_limit(limit):
    """Check if the limit is a positive integer."""
    return isinstance(limit, int) and limit > 0

def set_traffic_limit(interface, limit):
    """Set traffic limit using iptables."""
    if not is_valid_interface(interface):
        print(f"Invalid network interface: {interface}")
        return
    if not is_valid_limit(limit):
        print(f"Invalid traffic limit: {limit}. It must be a positive integer.")
        return

    subprocess.run(f"sudo iptables -F", shell=True)

    try:
        subprocess.run(f"sudo iptables -A INPUT -i {interface} -m limit --limit {limit}/second -j ACCEPT", shell=True, check=True)
        subprocess.run(f"sudo iptables -A INPUT -i {interface} -j DROP", shell=True, check=True)
        print(f"Traffic limit set to {limit} packets per second on interface {interface}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set traffic limit: {e}")

if __name__ == "__main__":
    interface = input("Enter the network interface (e.g., wlp2s0): ")
    limit = int(input("Enter the traffic limit (packets per second): "))
    set_traffic_limit(interface, limit)
