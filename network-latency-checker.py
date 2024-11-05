import subprocess
import platform
import re
import time

def ping(host, count=4):
    """Ping a host and return the output."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to ping {host}: {e}")
        return None

def parse_ping_output(output):
    """Parse the output of the ping command."""
    if not output:
        return {}

    avg_time = re.search(r'avg = ([\d.]+) ms', output) if platform.system().lower() == 'windows' else re.search(r'avg = ([\d.]+) ms', output)
    min_time = re.search(r'min/avg/max = ([\d.]+)/([\d.]+)/([\d.]+)', output) if platform.system().lower() != 'windows' else re.search(r'Minimum = ([\d.]+)ms', output)

    stats = {}
    if avg_time:
        stats['average'] = float(avg_time.group(1))
    if min_time:
        stats['min'] = float(min_time.group(1)) if platform.system().lower() != 'windows' else float(min_time.group(1))
        stats['max'] = float(min_time.group(3)) if platform.system().lower() != 'windows' else None

    return stats

def log_results(host, stats):
    """Log the ping results to a file."""
    with open("ping_results_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: Ping results for {host}: {stats}\n")

def main():
    host = input("Enter the host to ping (e.g., google.com): ")
    count = input("Enter number of pings (default 4): ")
    count = int(count) if count.isdigit() else 4

    output = ping(host, count)
    stats = parse_ping_output(output)
    log_results(host, stats)

    if stats:
        print(f"Ping statistics for {host}:")
        print(f"Average time: {stats.get('average', 'N/A')} ms")
        print(f"Minimum time: {stats.get('min', 'N/A')} ms")
        print(f"Maximum time: {stats.get('max', 'N/A')} ms" if 'max' in stats else '')

if __name__ == "__main__":
    main()
