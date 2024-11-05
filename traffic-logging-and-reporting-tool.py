from scapy.all import sniff
import time

traffic_log = []

def log_packet(packet):
    """Log packet summary with a timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    entry = f"{timestamp} - {packet.summary()}"
    traffic_log.append(entry)
    print(entry)

def report_traffic(filename='traffic_report.txt'):
    """Generate a traffic report and save it to a file."""
    try:
        with open(filename, 'w') as file:
            for entry in traffic_log:
                file.write(f"{entry}\n")
        print(f"Traffic report generated: {filename}")
    except Exception as e:
        print(f"Error generating report: {e}")

def main(count):
    """Start sniffing packets and generate a traffic report."""
    print(f"Sniffing {count} packets...")
    sniff(prn=log_packet, count=count)
    report_traffic()

if __name__ == "__main__":
    try:
        packet_count = int(input("Enter the number of packets to capture (e.g., 100): "))
        main(packet_count)
    except ValueError:
        print("Invalid input! Please enter a valid number.")
