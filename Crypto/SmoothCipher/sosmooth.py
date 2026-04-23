from binascii import hexlify
from gmpy2 import *
import math
import os
import sys

if sys.version_info < (3, 9):
    math.gcd = gcd
    math.lcm = lcm

SECRET = "REDACTED"
SECRET = mpz(hexlify(SECRET.encode()), 16)

RANDOM_SEED = mpz(hexlify(os.urandom(32)).decode(), 16)
RAND_STATE = random_state(RANDOM_SEED)

def generate_prime(state, bit_len):
    return next_prime(mpz_urandomb(state, bit_len) | (1 << (bit_len - 1)))

def generate_smooth_prime(state, bit_len, smooth_bits=16):
    base = mpz(2)
    base_factors = [base]

    while base.bit_length() < bit_len - 2 * smooth_bits:
        factor = generate_prime(state, smooth_bits)
        base_factors.append(factor)
        base *= factor

    dynamic_bits = (bit_len - base.bit_length()) // 2

    while True:
        prime_a = generate_prime(state, dynamic_bits)
        prime_b = generate_prime(state, dynamic_bits)
        candidate = base * prime_a * prime_b
        if candidate.bit_length() < bit_len:
            dynamic_bits += 1
            continue
        if candidate.bit_length() > bit_len:
            dynamic_bits -= 1
            continue
        if is_prime(candidate + 1):
            base_factors.append(prime_a)
            base_factors.append(prime_b)
            base = candidate + 1
            break

    base_factors.sort()
    return (base, base_factors)

while True:
    prime1, factors1 = generate_smooth_prime(RAND_STATE, 1024, 16)
    if len(factors1) != len(set(factors1)):
        continue
    prime2, factors2 = generate_smooth_prime(RAND_STATE, 1024, 17)
    if len(factors2) == len(set(factors2)):
        break

modulus = prime1 * prime2
ciphertext = pow(3, SECRET, modulus)

print(f'n = {modulus.digits(16)}')
print(f'c = {ciphertext.digits(16)}')
