# Applied Cryptography - TD4 - Private Information Retrieval

Group (OCC3): 
- Colin TANTER
- Ismael TIR

---

## Key Generation

The key generation process involves the following steps:

1. **Generate two large prime numbers**:
   - The primes *p* and *q* are generated using the `number.getPrime` function from the `Crypto.Util` library.
   - The primes must satisfy the condition that :**$$gcd(p \cdot q, (p-1) \cdot (q-1)) = 1$$**

2. **Compute *n*** :
   - $n = p \cdot q $, where *n* is part of the public key.

3. **Compute *g*** :
   - $g = n + 1$, which is also part of the public key.

4. **Compute *$\lambda$*** :
   - $\lambda = \text{lcm}(p-1, q-1)$, where $\lambda$ is part of the private key.

5. **Compute *$\mu$*** :
   - * $\mu = \lambda^{-1} \mod n$, which is also part of the private key.

The **public key** is $ (n, g) $, and the **private key** is $ (\lambda, \mu) $.


## Encryption

The encryption process involves the following steps:

1. **Check the message range**:
   - The message *m* must be in the range $ [0, n-1] $.

2. **Generate a random number *r***:
   -  *r* is a random integer such that $0 < r < n$ and $ \gcd(r, n) = 1 $.

3. **Compute the ciphertext**:
   - The ciphertext *c* is computed as: $$c = (g^m \cdot r^n) \mod n^2$$

## Decryption

The decryption process involves the following steps:

1. **Compute $c^\lambda \mod n^2$**:
   - This step uses the private key $\lambda$.

2. **Compute $L(x)$**:
   - The function $L(x)$ is defined as: $$L(x) = \frac{x - 1}{n}$$
   - This is used to recover the plaintext.

3. **Recover the message**:
   - The message * m * is computed as: $$m = L(c^\lambda \mod n^2) \cdot \mu \mod n $$


## Homomorphic Properties

The Paillier cryptosystem supports two homomorphic operations:

1. **Homomorphic Addition**:
   - Given two ciphertexts $c_1$ and $c_2$, the sum of the plaintexts $m_1 + m_2$ can be obtained by multiplying the ciphertexts:$$c_{\text{sum}} = (c_1 \cdot c_2) \mod n^2 $$
   - Decrypting $c_{\text{sum}}$ yields $ m_1 + m_2 $.

2. **Scalar Multiplication**:
   - Given a ciphertext $c_1$ and a scalar $k$, the product $k \cdot m_1 $ can be obtained by raising the ciphertext to the power of $k$ : $$c_k = c_1^k \mod n^2 $$
   - Decrypting $c_k$ yields $ k \cdot m_1 $


## Testing

The implementation includes several test cases to verify correctness:

1. **Encryption and Decryption**:
   - A message is encrypted and then decrypted to ensure the original message is recovered.

2. **Homomorphic Addition**:
   - Two messages are encrypted, and their ciphertexts are multiplied. The result is decrypted to verify that it equals the sum of the original messages.

3. **Scalar Multiplication**:
   - A message is encrypted, and the ciphertext is raised to the power of a scalar. The result is decrypted to verify that it equals the scalar multiplied by the original message.

## Usage

To use the Paillier cryptosystem, follow these steps:

1. **Initialize the Paillier object**:
   ```python
   phe = Paillier(1024)  # 1024-bit key size
   ```

2. **Encrypt a message**:
   ```python
   message = "flag{paillier_encryption}"
   ciphertext = phe.encrypt(string_to_int(message))
   ```

3. **Decrypt the ciphertext**:
   ```python
   decrypted_message = int_to_string(phe.decrypt(ciphertext))
   ```

4. **Perform homomorphic operations**:
   - Homomorphic addition:
     ```python
     c_sum = (c1 * c2) % (phe.n**2)
     decrypted_sum = phe.decrypt(c_sum)
     ```
   - Scalar multiplication:
     ```python
     c_k = gmpy2.powmod(c1, k, phe.n**2)
     decrypted_k = phe.decrypt(c_k)
     ```

