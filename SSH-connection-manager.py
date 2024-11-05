import paramiko
import getpass

def ssh_connect(host, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print("Command Output:")
            print(output)

        if error:
            print("Command Error:")
            print(error)

    except paramiko.SSHException as ssh_exception:
        print(f"SSH connection error: {ssh_exception}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    host = "192.168.1.1"
    username = input("Enter SSH username: ")
    password = getpass.getpass("Enter SSH password: ")
    command = 'ls'

    ssh_connect(host, username, password, command)
