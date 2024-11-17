# bitmask
This repository provides a set of scripts for securely exchanging files and text messages using Public Key Infrastructure (PKI) and symmetric encryption. For small files and text messages we can use asymmetric encryption directly but larger files like binaries, images and videos demand a different solution for which we use hybrid encryption.  

For asymmetric encryption, I use a 2048-bit RSA keypair with the private key further encrypted by AES-256 cipher. This adds an additional layer of security so that private key files cannot be read in plain text on the filesystem and mitigates risk of data breach in case of key leaks. The private key can be used for decryption with a passphrase.

> [!CAUTION]
> Keep your private key with yourself only. Don't share it with anyone.

> [!CAUTION]
> Keep your private key safe. There is no way to recover your data if you erase/modify your private key or forget your key passphrase.

> [!WARNING]
> Don't set a predictable or short passphrase. Your encrypted data may be compromised in event of a key leak.

Symmetric encryption uses random base64 encoded keyphrase. Note that this is not the actual key used for symmetric encryption but a password or passphrase which is used by openssl's PBKDF2 KDF (Key Derivation Function) to derive a symmetric key. Further, the encryption is carried out using the AES-256 algorithm and salt to eliminate determinism in the encrypted output. Salt ensures randomness but it is stored in the encrypted file.

## How it works
### You send me a file
- Generate a PKI keypair **generate/generate_pki_keypaur.py** if you don't already have one
- Share the public key with it's sha256 fingerprint over [email](amoldhamale1105@gmail.com)
- Decrypt the received file `*.apg` from me with your private key using **decrypt/pki_decrypt.py**
- Encrypt the file you want to send me with the decrypted `*.bin` keyphrase file using **encrypt/encrypt_file.py**
- Send me the encrypted file `*.enc` with sha256 digest on any medium

### I send you a file
- Generate a unique keyphrase for me with **generate/generate_keyphrase.py**
- Encrypt the `*.bin` keyphrase file with my public key **keys/entropy.pem** using **encrypt/pki_encrypt.py**
- Share the encrypted keyphrase file with it's sha256 fingerprint over [email](amoldhamale1105@gmail.com)
- Decrypt the received file `*.enc` from me with your keyphrase file using **decrypt/decrypt_file.py**

> [!NOTE]
> These scripts have been validated on Linux, yet to be tested on Windows, Mac and BSD but the whole purpose of writing it in python was to make it platform agnostic. Feel free to test them on other platforms and create issues/pull requests accordingly.  