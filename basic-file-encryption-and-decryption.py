from cryptography.fernet import Fernet
import os

def generate_key():
    """Generate and save a new key."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the previously generated key."""
    return open("secret.key", "rb").read()

def encrypt_file(key, filename):
    """Encrypt the given file."""
    fernet = Fernet(key)

    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist.")
        return

    with open(filename, 'rb') as file:
        original = file.read()

    try:
        fernet.decrypt(original)
        print(f"File '{filename}' is already encrypted.")
        return
    except Exception:
        pass

    encrypted = fernet.encrypt(original)
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"File '{filename}' encrypted successfully.")

def decrypt_file(key, filename):
    """Decrypt the given file."""
    fernet = Fernet(key)

    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist.")
        return

    with open(filename, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    try:
        fernet.decrypt(encrypted)
        print(f"File '{filename}' is already decrypted.")
        return
    except Exception:
        pass

    decrypted = fernet.decrypt(encrypted)
    with open(filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    print(f"File '{filename}' decrypted successfully.")

def main():
    """Main function to run the encryption/decryption."""
    action = input("Do you want to encrypt or decrypt a file? (e/d): ").lower()
    filename = input("Enter the filename: ")

    if action == 'e':
        if not os.path.exists("secret.key"):
            generate_key()
        key = load_key()
        encrypt_file(key, filename)
    elif action == 'd':
        if not os.path.exists("secret.key"):
            print("Key file 'secret.key' does not exist. Cannot decrypt.")
            return
        key = load_key()
        decrypt_file(key, filename)
    else:
        print("Invalid action. Please enter 'e' for encrypt or 'd' for decrypt.")

if __name__ == "__main__":
    main()
