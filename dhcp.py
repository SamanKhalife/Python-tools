import random

class IPAssigner:
    def __init__(self, base_ip, used_ips=None):
        self.base_ip = base_ip
        self.used_ips = used_ips if used_ips is not None else set()

    def assign_ip(self):
        if len(self.used_ips) >= 254:
            print("No more IPs available to assign.")
            return None

        while True:
            assigned_ip = f"{self.base_ip}{random.randint(1, 254)}"
            if assigned_ip not in self.used_ips:
                self.used_ips.add(assigned_ip)
                self.log_ip(assigned_ip)
                print(f"Assigned IP: {assigned_ip}")
                return assigned_ip

    def log_ip(self, ip):
        with open("assigned_ips.log", "a") as log_file:
            log_file.write(f"{ip}\n")

    def reset_ips(self):
        self.used_ips.clear()
        print("Resetting assigned IPs.")

def main():
    base_ip = input("Enter the base IP (default is 192.168.1.): ") or "192.168.1."
    ip_assigner = IPAssigner(base_ip)

    while True:
        action = input("Type 'assign' to assign an IP, 'reset' to reset assigned IPs, or 'exit' to quit: ").strip().lower()
        if action == 'assign':
            ip_assigner.assign_ip()
        elif action == 'reset':
            ip_assigner.reset_ips()
        elif action == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
