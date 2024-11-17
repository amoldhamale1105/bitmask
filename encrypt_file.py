import os
import subprocess
import hashlib
import sys
import argparse

def encrypt_file(filename, keyphrase_file, output_dir=None):
    try:
        # Check if the encrypted file exists
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)

        # Check if the keyphrase file exists
        if not os.path.exists(keyphrase_file):
            print(f"Error: Key file '{keyphrase_file}' not found.")
            sys.exit(1)
        
        # Set output file path with extension
        encrypted_file = os.path.join(
            output_dir if output_dir else os.getcwd(), os.path.basename(filename) + ".enc")
        
        # Encrypt the file with PBKDF2 KDF
        subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-salt", "-pbkdf2",
            "-in", filename, "-out", encrypted_file, "-pass", f"file:{keyphrase_file}"],
            check=True)
        
        # Generate SHA256 digest of the encrypted file
        sha256_filename = f"{encrypted_file}.sha256"
        with open(encrypted_file, "rb") as enc_file:
            enc_data = enc_file.read()
            sha256_hash = hashlib.sha256(enc_data).hexdigest()
        with open(sha256_filename, "w") as hash_file:
            hash_file.write(sha256_hash)
        
        print(f"File encrypted successfully: {encrypted_file}")
        print(f"SHA256 digest saved: {sha256_filename}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt a file with a key.")
    parser.add_argument("filename", help="File to encrypt")
    parser.add_argument("keyphrase_file", help="Keyphrase file to use for symmetric encryption")
    parser.add_argument("-o", "--output", help="Output directory for the encrypted file")
    args = parser.parse_args()
    
    encrypt_file(args.filename, args.keyphrase_file, args.output)

