import os
import subprocess
import pyudev
import stat

def logout_non_root_users():
    try:
        users = subprocess.check_output(['who']).decode().splitlines()

        for user_info in users:
            user = user_info.split()[0]
            if user != 'root':
                print(f"Logging out user: {user}")
                subprocess.run(['pkill', '-KILL', '-u', user])
    except Exception as e:
        print(f"Error logging out users: {e}")

def set_files_read_only(file_paths):
    for file_path in file_paths:
        try:
            if os.path.isfile(file_path):
                print(f"Setting {file_path} to read-only")
                os.chmod(file_path, stat.S_IREAD)
            else:
                print(f"{file_path} is not a valid file")
        except Exception as e:
            print(f"Error setting {file_path} to read-only: {e}")

def monitor_usb():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')

    for device in monitor:
        if 'ID_BUS' in device and device['ID_BUS'] == 'usb':
            print(f"USB device detected: {device.device_node}")
            logout_non_root_users()
            set_files_read_only(['/path/to/file1', '/path/to/file2'])

if __name__ == "__main__":
    print("Monitoring for USB devices...")
    monitor_usb()
