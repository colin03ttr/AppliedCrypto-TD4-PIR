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
        print(f"Keys generated.")

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
print("\n")
phe = Paillier(1024)
print("\nStarting tests...")

# Encryption and decryption test
print("\n---- Test encryption and decryption ----")
m = "flag{paillier_encryption}"
c = phe.encrypt(string_to_int(m))
decrypted_m = int_to_string(phe.decrypt(c))
print(f"Original message: {m}")
print(f"Decrypted message: {decrypted_m}")
assert decrypted_m == m, "FAIL : Original and decrypted messages are different!"
print("SUCCESS")

# Homomorphic addition (Paillier Cryptosystem - Question 2)
#  ---->  multiplying ciphertexts results in an encryption of the sum of the plaintexts
print("\n---- Test homomorphic addition ----")
m1 = 123
m2 = 456
c1 = phe.encrypt(m1)
c2 = phe.encrypt(m2)
c_product = (c1 * c2) % (phe.n**2)
decrypted_sum = phe.decrypt(c_product)
decrypted_product = phe.decrypt(c1 * c2)
print(f"Decrypted(c1·c2 mod n²): {decrypted_product}\nExpected: m1 + m2 = {m1 + m2}" )
assert decrypted_sum == m1 + m2, "FAIL: Homomorphic addition"
print("SUCCESS")

# Homomorphic addition of a plaintext to a ciphertext (Paillier Cryptosystem - Question 3)
# ---->  multiplying a ciphertext by an encryption of a plaintext results in an encryption of the sum of the two plaintexts
print("\n---- Test homomorphic addition of a plaintext to a ciphertext ----")
m1 = 30
m2 = 15
c1 = phe.encrypt(m1)
g_m2 = gmpy2.powmod(phe.g, m2, phe.n**2)
c_result = (c1 * g_m2) % phe.n**2
decrypted_result = phe.decrypt(c_result)
expected_result = m1 + m2
print(f"Decrypted(c1 * g^m2 mod n²): {decrypted_result}\nExpected: m1 + m2 = {expected_result}")
assert decrypted_result == expected_result, "Homomorphic plaintext addition failed!"
print("SUCCESS")

# Homomorphic multiplication of a ciphertext by a plaintext (Paillier Cryptosystem - Question 4)
# ---->  raising a ciphertext to the power of a plaintext m2 homomorphically multiplies the encrypted message by m2
print("\n---- Test homomorphic multiplication of a ciphertext by a plaintext ----")
m1 = 5
m2 = 3
c1 = phe.encrypt(m1)
c_result = gmpy2.powmod(c1, m2, phe.n**2)
decrypted_result = phe.decrypt(c_result)
expected_result = m1 * m2
print(f"Decrypted(c1^m2 mod n²): {decrypted_result}\nExpected: m1 * m2 = {expected_result}")
assert decrypted_result == expected_result, "FAIL: Homomorphic multiplication of a ciphertext by a plaintext"
print("SUCCESS")
print("\nAll tests passed!!!!\n")