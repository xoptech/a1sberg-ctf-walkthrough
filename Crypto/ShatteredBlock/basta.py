import socket
import binascii

HOST = "178.128.110.55"
PORT = 4323
BLOCK_SIZE = 16

# --- Helper Functions for Raw Sockets ---

def recv_until(sock, suffix):
    """Reads from the socket one byte at a time until the suffix is found."""
    data = b""
    while not data.endswith(suffix):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data

def recv_line(sock):
    """Reads a single line from the socket."""
    return recv_until(sock, b"\n")

def split_blocks(data):
    """Splits data into 16-byte chunks."""
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def get_oracle_response(sock, payload_bytes):
    """Sends a hex payload to the server and checks if padding is valid."""
    # Wait for the prompt
    recv_until(sock, b"> ")
    
    # Send our tampered hex string with a newline character
    hex_payload = binascii.hexlify(payload_bytes) + b"\n"
    sock.sendall(hex_payload)
    
    # Read the server's response
    response = recv_line(sock).decode().strip()
    
    # Return True if the Oracle says "Success", False otherwise
    return "Success" in response

# --- Main Exploit Logic ---

def main():
    print("[*] Connecting to the server...")
    
    # Create a TCP socket and connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # 1. Grab the encrypted flag from the server
        recv_until(sock, b"Encrypted Flag: ")
        encrypted_hex = recv_line(sock).decode().strip()
        print(f"[+] Captured Encrypted Flag: {encrypted_hex}")

        # Convert hex to raw bytes and split into 16-byte blocks
        encrypted_bytes = binascii.unhexlify(encrypted_hex)
        blocks = split_blocks(encrypted_bytes)
        
        print(f"[*] Flag is {len(blocks)} blocks long (including IV). Starting attack...\n")
        
        recovered_flag = b""

        # 2. Decrypt block by block
        for block_idx in range(1, len(blocks)):
            target_block = blocks[block_idx]
            prev_block = blocks[block_idx - 1]
            
            intermediate_state = bytearray(BLOCK_SIZE)
            decrypted_block = bytearray(BLOCK_SIZE)
            
            print(f"[*] Cracking Block {block_idx}...")

            # 3. Guess byte by byte, moving backward
            for byte_idx in range(BLOCK_SIZE - 1, -1, -1):
                padding_value = BLOCK_SIZE - byte_idx
                tampered_prev_block = bytearray(BLOCK_SIZE)
                
                # Set known bytes to produce valid padding
                for k in range(byte_idx + 1, BLOCK_SIZE):
                    tampered_prev_block[k] = intermediate_state[k] ^ padding_value

                # 4. Try all 256 possible bytes
                for guess in range(256):
                    tampered_prev_block[byte_idx] = guess
                    payload = tampered_prev_block + target_block
                    
                    if get_oracle_response(sock, payload):
                        # Math time: calculate the intermediate state and the plaintext char
                        intermediate_state[byte_idx] = guess ^ padding_value
                        decrypted_char = intermediate_state[byte_idx] ^ prev_block[byte_idx]
                        decrypted_block[byte_idx] = decrypted_char
                        
                        print(f"    Found byte {byte_idx}: {chr(decrypted_char)} (Hex: {hex(decrypted_char)})")
                        break
            
            recovered_flag += decrypted_block
            print(f"[+] Decrypted so far: {recovered_flag}\n")

        # Clean up the padding
        padding_len = recovered_flag[-1]
        final_flag = recovered_flag[:-padding_len]
        
        print("=========================================")
        print(f"[*] FINAL RECOVERED FLAG: {final_flag.decode('utf-8', errors='ignore')}")
        print("=========================================")

if __name__ == "__main__":
    main()