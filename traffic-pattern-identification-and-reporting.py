from scapy.all import sniff, IP

traffic_patterns = {}

def packet_callback(packet):
    """Callback function to process each captured packet."""
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        traffic_patterns.setdefault(src, {}).setdefault(dst, 0)
        traffic_patterns[src][dst] += 1

def report_traffic_patterns():
    """Generate a report of traffic patterns."""
    print("\nTraffic Patterns:")
    for src, dsts in traffic_patterns.items():
        destinations = ', '.join(f"{dst} ({count})" for dst, count in dsts.items())
        print(f"Source: {src}, Destinations: {destinations}")

def main():
    print("Starting to sniff packets...")
    sniff(prn=packet_callback, count=100)
    report_traffic_patterns()

if __name__ == "__main__":
    main()
