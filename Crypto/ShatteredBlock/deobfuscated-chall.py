import sys
import os
import binascii
from Crypto.Cipher import AES

# Global variables
SECRET_KEY = os.urandom(16)
IV = os.urandom(16) # Initialization Vector
FLAG = b"REDACTED"
BLOCK_SIZE = 16

def encrypt(data):
    """Encrypts data using AES-CBC and adds PKCS#7 padding."""
    # Calculate how many padding bytes we need to reach a multiple of 16
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    
    # Create the padding (e.g., if we need 4 bytes, we add 0x04 0x04 0x04 0x04)
    padding = bytes([padding_len]) * padding_len
    padded_data = data + padding
    
    # Encrypt using AES in CBC mode (mode 2)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(padded_data)
    
    # Prepend the IV to the ciphertext so the verifier can use it to decrypt
    return IV + encrypted_data

def verify_padding(ciphertext):
    """Decrypts ciphertext and validates if the PKCS#7 padding is mathematically correct."""
    # The ciphertext must be at least 32 bytes (16-byte IV + 16-byte block) 
    # and its length must be an exact multiple of the 16-byte block size.
    if len(ciphertext) < 32 or len(ciphertext) % BLOCK_SIZE != 0:
        return False
        
    try:
        # Split the ciphertext into the IV (first 16 bytes) and the actual encrypted data
        iv = ciphertext[:16]
        encrypted_data = ciphertext[16:]
        
        # Decrypt the data
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Look at the very last byte to see what the padding length claims to be
        last_byte = decrypted_data[-1]
        
        # The padding length must be between 1 and 16 bytes
        if last_byte == 0 or last_byte > BLOCK_SIZE:
            return False
            
        # Verify that all the padding bytes match the value of the last byte
        expected_padding = bytes([last_byte]) * last_byte
        return decrypted_data[-last_byte:] == expected_padding
        
    except Exception:
        return False

def main():
    print("--- Welcome to the Secure Encryption Service ---")
    
    # Encrypt the flag and show it to the user in hexadecimal format
    encrypted_flag = encrypt(FLAG)
    hex_encrypted_flag = binascii.hexlify(encrypted_flag).decode()
    print(encrypted_flag)
    print(f"Encrypted Flag: {hex_encrypted_flag}")

    while True:
        print("\nSend me a hex-encoded ciphertext to verify:")
        user_input = input("> ").strip()
        
        if not user_input:
            break
            
        try:
            # Convert the user's hex string back into raw bytes
            ciphertext_bytes = binascii.unhexlify(user_input)
            
            # Check if the padding is valid (Padding Oracle vulnerability setup)
            if verify_padding(ciphertext_bytes):
                print("Success: Padding is valid.")
            else:
                print("Error: Invalid padding!")
                
        except Exception:
            print("Invalid hex input.")

if __name__ == "__main__":
    main()