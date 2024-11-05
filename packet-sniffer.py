from scapy.all import sniff, IP
import logging
import signal
import sys

logging.basicConfig(filename='packet_sniffer_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

packet_count = 0
protocol_count = {}

def signal_handler(sig, frame):
    """Handle exit signals gracefully."""
    print("\nExiting...")
    print(f"Total packets captured: {packet_count}")
    print("Protocol statistics:")
    for proto, count in protocol_count.items():
        print(f"{proto}: {count} packets")
    sys.exit(0)

def packet_callback(packet):
    """Process each captured packet."""
    global packet_count
    packet_count += 1

    print(packet.summary())

    logging.info(packet.show())

    if packet.haslayer(IP):
        proto = packet[IP].proto
        protocol_count[proto] = protocol_count.get(proto, 0) + 1

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting packet sniffing... Press Ctrl+C to stop.")
    sniff(prn=packet_callback)
