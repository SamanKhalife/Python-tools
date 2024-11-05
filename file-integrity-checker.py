import hashlib
import os

def file_hash(filepath, algorithm):
    if not os.path.isfile(filepath):
        print(f"The file '{filepath}' does not exist.")
        return None

    if algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'md5':
        hasher = hashlib.md5()
    else:
        print(f"Unsupported hashing algorithm: {algorithm}")
        return None

    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()

def main():
    filepath = input("Enter the path to the file: ")
    algorithm = input("Enter the hashing algorithm (sha256, md5): ").lower()

    file_hash_result = file_hash(filepath, algorithm)

    if file_hash_result:
        print(f"The {algorithm.upper()} hash of the file is: {file_hash_result}")
        save_results(filepath, algorithm, file_hash_result)

def save_results(filepath, algorithm, hash_value):
    with open('hash_results.txt', 'a') as f:
        f.write(f"File: {filepath}\n")
        f.write(f"Algorithm: {algorithm.upper()}\n")
        f.write(f"Hash: {hash_value}\n\n")

if __name__ == "__main__":
    main()
