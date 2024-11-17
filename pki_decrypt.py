import subprocess
import os
import sys
import argparse

def pki_decrypt(encrypted_file, privkey, output_path=None):
    try:
        # Ensure the encrypted file and private key exist
        if not os.path.isfile(encrypted_file):
            print(f"Error: File '{encrypted_file}' does not exist.")
            sys.exit(1)
        if not os.path.isfile(privkey):
            print(f"Error: Private key '{privkey}' does not exist.")
            sys.exit(1)

        # Remove .enc extension if it exists, otherwise maintain the original filename
        if encrypted_file.endswith(".apg"):
            output_file = encrypted_file[:-4]
        else:
            output_file = encrypted_file

        output_file = os.path.join(
            output_path if output_path else os.getcwd(), os.path.basename(output_file))

        # Decrypt the file using provided private key
        subprocess.run(
            ["openssl", "pkeyutl", "-decrypt",
            "-inkey", privkey, "-in", encrypted_file, "-out", output_file],
            check=True)
        
        print(f"File decrypted successfully: {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt an encrypted file using a private key.")
    parser.add_argument("filename", help="Encrypted file to decrypt")
    parser.add_argument("private_key", help="Private key file used for asymmetric decryption")
    parser.add_argument("-o", "--output", help="Optional output directory to save the decrypted file", default=None)
    args = parser.parse_args()

    pki_decrypt(args.filename, args.private_key, args.output)

