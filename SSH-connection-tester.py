import paramiko
import getpass

def test_ssh_connection(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        print(f"Connection to {host} successful!")
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH error occurred: {ssh_exception}")
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    host = input("Enter the SSH host (e.g., 192.168.1.1): ")
    username = input("Enter SSH username: ")
    password = getpass.getpass("Enter SSH password: ")
    test_ssh_connection(host, username, password)
