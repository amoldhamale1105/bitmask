import subprocess
import argparse
import sys

def generate_keypair(private_key_base, public_key_base):
    private_key_file = f"{private_key_base}.pem"
    public_key_file = f"{public_key_base}.pem"
    
    try:
        # Generate the private key with AES-256 cipher
        subprocess.run(
            ["openssl", "genrsa", "-aes256", "-out", private_key_file, "2048"],
            check=True,
        )
        print(f"Private key generated: {private_key_file}")
        
        # Generate the public key from the private key
        subprocess.run(
            ["openssl", "rsa", "-in", private_key_file,
             "-pubout", "-out", public_key_file],
            check=True,
        )
        print(f"Public key generated: {public_key_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: OpenSSL command failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a PKI keypair using OpenSSL.")
    parser.add_argument(
        "-s",
        "--priv",
        type=str,
        default="secretkey",
        help="Base name for the private key file without extension.",
    )
    parser.add_argument(
        "-p",
        "--pub",
        type=str,
        default="publickey",
        help="Base name for the public key file without extension.",
    )
    args = parser.parse_args()
    
    generate_keypair(args.priv, args.pub)

