from Crypto.Util.number import *
import random

FLAG = b"REDACTED"

p = getPrime(256)
q = getPrime(256)

n = p * q
phi = (p-1)*(q-1)

d = random.randint(1, 2**16)
e = inverse(d, phi)

m = bytes_to_long(FLAG)

c = pow(m, e, n)

print("n =", n)
print("e =", e)
print("c =", c)
