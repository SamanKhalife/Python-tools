import subprocess
import sys

def run_command(command):
    """Run a shell command and handle errors."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}\n{result.stderr}")
        return False
    return True

def clear_existing_rules(interface):
    """Clear existing traffic control rules for the specified interface."""
    run_command(f"sudo tc qdisc del dev {interface} root")

def limit_speed(interface, download_limit, upload_limit):
    """Limit the download and upload speed for a specified network interface."""
    clear_existing_rules(interface)

    if not run_command(f"sudo tc qdisc add dev {interface} root handle 1: htb default 12"):
        return

    if not run_command(f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate {download_limit}kbps"):
        return

    if not run_command(f"sudo tc class add dev {interface} parent 1:1 classid 1:12 htb rate {upload_limit}kbps"):
        return

    print(f"Traffic control rules set on {interface}:")
    print(f"  Download limit: {download_limit} kbps")
    print(f"  Upload limit: {upload_limit} kbps")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python limit_speed.py <interface> <download_limit_kbps> <upload_limit_kbps>")
        sys.exit(1)

    interface = sys.argv[1]
    download_limit = int(sys.argv[2])
    upload_limit = int(sys.argv[3])

    limit_speed(interface, download_limit, upload_limit)
