import os

FLAG = b"REDACTED"
SEED = 0x4131537b
MASK = 0b10000000000000000000000000000111
ciphertext_hex = "3a62623a64ab321c4edd43f73b8228c971207c5366de57feba1465412a3344beb2"
ciphertext = bytes.fromhex(ciphertext_hex)

class LFSR:
    def __init__(self, seed, mask):
        self.state = seed & 0xFFFFFFFF
        self.mask = mask

    def next_bit(self):
        feedback = bin(self.state & self.mask).count('1') % 2
        out = self.state & 1
        self.state = (self.state >> 1) | (feedback << 31)
        return out

def encrypt():
    lfsr = LFSR(SEED, MASK)
    
    leak = []
    for _ in range(64):
        leak.append(str(lfsr.next_bit()))

    print(f"Public Mask: {hex(MASK)}")
    print(f"Keystream Leak: {''.join(leak)}")
    
    lfsr_enc = LFSR(SEED, MASK)
    ciphertext = []
    for byte in FLAG:
        keystream_byte = 0
        for i in range(8):
            keystream_byte |= (lfsr_enc.next_bit() << i)
        ciphertext.append(byte ^ keystream_byte)
    
    print(f"Ciphertext: {bytes(ciphertext).hex()}")

def decrypt():
    lfsr_dec = LFSR(SEED, MASK)
    flag = []
    for byte in ciphertext:
        keystream_byte = 0
        for i in range(8):
            keystream_byte |= (lfsr_dec.next_bit() << i)
        flag.append(byte ^ keystream_byte)
    
    print(f"flag: {bytes(flag).decode()}")

if __name__ == "__main__":
    decrypt()
