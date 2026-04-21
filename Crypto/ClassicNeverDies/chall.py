import base64

FLAG = b"A1S{REDACTED}"

shift = ???

def caesar(data, s):
    res = ""
    for c in data.decode():
        if c.isupper():
            res += chr((ord(c) - ord('A') + s) % 26 + ord('A'))
        elif c.islower():
            res += chr((ord(c) - ord('a') + s) % 26 + ord('a'))
        else:
            res += c
    return res.encode()

enc = caesar(FLAG, shift)
enc = base64.b64encode(enc)

print(enc.decode())
