from Crypto.Util import number
from utils import *
import gmpy2

class Paillier:
    def __init__(self, bits):
        print(f"Initializing Paillier with key size: {bits} bits")
        self.keyGen(bits)

    def keyGen(self, bits):
        print("Generating keys...")
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        
        while gmpy2.gcd(p * q, (p - 1) * (q - 1)) != 1: # Ensure p and q are coprime
            p = number.getPrime(bits)
            q = number.getPrime(bits)
        
        self.n = p * q
        self.g = self.n + 1
        self.lambda_n = gmpy2.lcm(p - 1, q - 1)
        self.mu = gmpy2.invert(self.lambda_n, self.n) # mu = lambda_n^-1 mod n
        print(f"Keys generated. Public key: (n: {self.n}, g: {self.g})")

    def encrypt(self, message: int):
        if message < 0 or message >= self.n:
            raise ValueError("Message must be between 0 and n-1")
        
        while True:
            r = number.getRandomRange(1, self.n) # 0 < r < n
            if gmpy2.gcd(r, self.n) == 1: # Ensure r is coprime with n
                break
        
        # cipher = (g^m * r^n) mod n^2
        cipher = (gmpy2.powmod(self.g, message, self.n**2) * gmpy2.powmod(r, self.n, self.n**2)) % self.n**2
        return cipher

    def decrypt(self, ciphertext: int):
        # message = L(c_lambda mod n^2) * lambda_n mod n          where L(x) = (x-1)/n
        c_lambda = gmpy2.powmod(ciphertext, self.lambda_n, self.n**2)
        L = (c_lambda - 1) // self.n
        m = (L * self.mu) % self.n
        return m

# Tests
print("Starting tests...")
phe = Paillier(1024)

# Encryption and decryption test
m = "flag{paillier_encryption}"
c = phe.encrypt(string_to_int(m))
decrypted_m = int_to_string(phe.decrypt(c))
print(f"Original message: {m}")
print(f"Decrypted message: {decrypted_m}")
assert(decrypted_m == m)

# Homomorphic addition
m1 = 123
m2 = 456
c1 = phe.encrypt(m1)
c2 = phe.encrypt(m2)
c_sum = (c1 * c2) % (phe.n**2)
decrypted_sum = phe.decrypt(c_sum)
print(f"Homomorphic addition: {m1} + {m2} = {decrypted_sum}")
assert(decrypted_sum == m1 + m2)

# Scalar multiplication
k = 3
c_k = gmpy2.powmod(c1, k, phe.n**2)
decrypted_k = phe.decrypt(c_k)
print(f"Scalar multiplication: {m1} * {k} = {decrypted_k}")
assert(decrypted_k == k * m1)