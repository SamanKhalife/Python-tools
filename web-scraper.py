from scapy.all import sniff
import datetime

traffic_log = []

def log_packet(packet):
    """Log packet summary and print it."""
    traffic_log.append(packet.summary())
    print(packet.summary())

def report_traffic():
    """Generate a traffic report and save it to a file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'traffic_report_{timestamp}.txt'

    try:
        with open(filename, 'w') as file:
            for entry in traffic_log:
                file.write(f"{entry}\n")
        print(f"Traffic report generated: {filename}")
    except Exception as e:
        print(f"Error writing report: {e}")

def main(packet_count=100):
    """Start sniffing packets and generate a report."""
    print(f"Sniffing {packet_count} packets...")
    sniff(prn=log_packet, count=packet_count)
    report_traffic()

if __name__ == "__main__":
    main()
