from scapy.all import sniff, IP
import logging
import signal
import sys

logging.basicConfig(filename='packet_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

packet_count = 0
ip_statistics = {}

def signal_handler(sig, frame):
    print("\nExiting...")
    print(f"Total packets captured: {packet_count}")
    print("IP Statistics:")
    for ip, count in ip_statistics.items():
        print(f"{ip}: {count} packets")
    sys.exit(0)

def analyze_packet(packet):
    global packet_count
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        ip_proto = packet[IP].proto
        packet_size = len(packet)
        ttl = packet[IP].ttl

        logging.info(f"Packet: {ip_src} -> {ip_dst}, Protocol: {ip_proto}, Size: {packet_size} bytes, TTL: {ttl}")

        packet_count += 1
        ip_statistics[ip_src] = ip_statistics.get(ip_src, 0) + 1
        ip_statistics[ip_dst] = ip_statistics.get(ip_dst, 0) + 1

        print(f"Packet: {ip_src} -> {ip_dst}, Protocol: {ip_proto}, Size: {packet_size} bytes, TTL: {ttl}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting packet sniffing... Press Ctrl+C to stop.")
    sniff(prn=analyze_packet, filter="ip")
