import os
import subprocess
import sys
import argparse

def decrypt_file(encrypted_filename, keyphrase_file, output_path=None):
    try:
        # Check if the encrypted file exists
        if not os.path.exists(encrypted_filename):
            print(f"Error: Encrypted file '{encrypted_filename}' not found.")
            sys.exit(1)

        # Check if the keyphrase file exists
        if not os.path.exists(keyphrase_file):
            print(f"Error: Key file '{keyphrase_file}' not found.")
            sys.exit(1)

        # Remove .enc extension if it exists, otherwise maintain the original filename
        if encrypted_filename.endswith(".enc"):
            output_filename = encrypted_filename[:-4]
        else:
            output_filename = encrypted_filename

        # If an output path is provided, use it; otherwise, output to the current directory
        output_filename = os.path.join(
            output_path if output_path else os.getcwd(), os.path.basename(output_filename))

        # Decrypt the file with PBKDF2 KDF
        subprocess.run(
            ["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-in", encrypted_filename, 
             "-out", output_filename, "-pass", f"file:{keyphrase_file}"],
            check=True)

        print(f"File decrypted successfully: {output_filename}")

    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt an encrypted file using a keyphrase file.")
    parser.add_argument("filename", help="Encrypted file to decrypt")
    parser.add_argument("keyphrase_file", help="Keyphrase file used for symmetric decryption")
    parser.add_argument("-o", "--output", help="Optional output directory to save the decrypted file", default=None)
    args = parser.parse_args()
    
    decrypt_file(args.filename, args.keyphrase_file, args.output)

