import subprocess

def run_command(command):
    """Execute a shell command and return the output and error, if any."""
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    return process.stdout.strip(), process.stderr.strip()

def block_ip(ip_address):
    """Block an IP address using iptables."""
    stdout, stderr = run_command(f"sudo iptables -A INPUT -s {ip_address} -j DROP")
    if stderr:
        print(f"Error blocking IP: {stderr}")
    else:
        print(f"Blocked IP: {ip_address}")

def unblock_ip(ip_address):
    """Unblock an IP address using iptables."""
    stdout, stderr = run_command(f"sudo iptables -D INPUT -s {ip_address} -j DROP")
    if stderr:
        print(f"Error unblocking IP: {stderr}")
    else:
        print(f"Unblocked IP: {ip_address}")

def list_blocked_ips():
    """List currently blocked IPs."""
    stdout, stderr = run_command("sudo iptables -L INPUT -v -n")
    if stderr:
        print(f"Error fetching blocked IPs: {stderr}")
    else:
        print("Currently blocked IPs:\n", stdout)

def main():
    action = input("Do you want to (block/unblock/list) an IP address? ").strip().lower()
    if action == "block":
        ip_address = input("Enter the IP address to block: ").strip()
        block_ip(ip_address)
    elif action == "unblock":
        ip_address = input("Enter the IP address to unblock: ").strip()
        unblock_ip(ip_address)
    elif action == "list":
        list_blocked_ips()
    else:
        print("Invalid action. Please choose 'block', 'unblock', or 'list'.")

if __name__ == "__main__":
    main()
