from scapy.all import *
import argparse
import time

def packet_handler(packet):
    """Handle the packet and print detected device information."""
    if packet.haslayer(Dot11):
        addr = packet[Dot11].addr2
        if addr not in detected_devices:
            detected_devices.add(addr)
            print(f"Detected device: {addr}")

def main(interface):
    """Main function to start sniffing on the specified interface."""
    global detected_devices
    detected_devices = set()

    print(f"Sniffing on interface: {interface}")

    try:
        sniff(iface=interface, prn=packet_handler, store=0)
    except PermissionError:
        print("Permission denied: Run this script with elevated privileges (e.g., sudo).")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wi-Fi Device Sniffer")
    parser.add_argument("interface", type=str, help="Wireless interface to sniff on (e.g., wlan0).")
    args = parser.parse_args()

    main(args.interface)
