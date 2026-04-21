import base64

FLAG = b"P1H{r43h4g_4cs_q345i64}"

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

for shift in range(26):
    enc = caesar(FLAG, shift)
    enc = base64.b64encode(enc)
    print(base64.b64decode(enc.decode()))
