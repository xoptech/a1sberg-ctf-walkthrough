import sys, os, binascii
from Crypto.Cipher import AES as _A

_k = os.urandom(16)
_i = os.urandom(16)
_f = b"REDACTED"

def _e(d):
    return _i + _A.new(_k, 2, _i).encrypt(d + (lambda b: (b - len(d) % b) * bytes([b - len(d) % b]))(16))

def _v(d):
    if len(d) < 32 or len(d) % 16: return 0
    try:
        _r = _A.new(_k, 2, d[:16]).decrypt(d[16:])
        return _r[-1] > 0 and _r[-1] <= 16 and _r[-_r[-1]:] == bytes([_r[-1]]) * _r[-1]
    except: return 0

def main():
    _w = lambda x: (sys.stdout.write(x), sys.stdout.flush())
    _w("--- Welcome to the Secure Encryption Service ---\n")
    _w(f"Encrypted Flag: {binascii.hexlify(_e(_f)).decode()}\n")

    while True:
        _w("\nSend me a hex-encoded ciphertext to verify:\n> ")
        _u = sys.stdin.readline().strip()
        if not _u: break
        try:
            _w("Success: Padding is valid.\n" if _v(binascii.unhexlify(_u)) else "Error: Invalid padding!\n")
        except:
            _w("Invalid hex input.\n")

if __name__ == "__main__":
    main()
