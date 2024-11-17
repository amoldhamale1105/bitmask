import subprocess
import os
import sys
import argparse

def pki_encrypt(filename, pubkey, output_path=None):
    try:
        # Ensure the input file and public key exist
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' does not exist.")
            sys.exit(1)
        if not os.path.isfile(pubkey):
            print(f"Error: Public key '{pubkey}' does not exist.")
            sys.exit(1)

        # Determine the output file name
        output_file = os.path.join(
            output_path if output_path else os.getcwd(), os.path.basename(filename) + ".apg")

        # Encrypt the file using provided public key
        subprocess.run(
            ["openssl", "pkeyutl", "-encrypt",
            "-inkey", pubkey, "-pubin", "-in", filename, "-out", output_file],
            check=True)

        print(f"File encrypted successfully: {output_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed: {e}")
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt a file with a public key.")
    parser.add_argument("filename", help="File to encrypt")
    parser.add_argument("public_key", help="Public key file to use for asymmetric encryption")
    parser.add_argument("-o", "--output", help="Output directory for the encrypted file")
    args = parser.parse_args()

    pki_encrypt(args.filename, args.public_key, args.output)

