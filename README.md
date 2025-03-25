# Applied Cryptography - TD4 - Private Information Retrieval

Group (OCC3): 
- Colin TANTER
- Ismael TIR
- Romain THIZON

---

## Key Generation

The key generation process involves the following steps:

1. **Generate two large prime numbers**:
   - The primes *p* and *q* are generated using the `number.getPrime` function from the `Crypto.Util` library.
   - The primes must satisfy the condition that : **$$gcd(p \cdot q, (p-1) \cdot (q-1)) = 1$$**

2. **Compute *n*** :
   - $n = p \cdot q $, where *n* is part of the public key.

3. **Compute *g*** :
   - $g = n + 1$, which is also part of the public key.

4. **Compute $\lambda$** :
   - $\lambda = \text{lcm}(p-1, q-1)$, where $\lambda$ is part of the private key.

5. **Compute $\mu$** :
   - $\mu = \lambda^{-1} \mod n$, which is also part of the private key.

The **public key** is $(n, g)$, and the **private key** is $(\lambda, \mu)$.


## Encryption

The encryption process involves the following steps:

1. **Check the message range**:
   - The message *m* must be in the range $[0, n-1]$.

2. **Generate a random number *r***:
   -  *r* is a random integer such that $0 < r < n$ and $\gcd(r, n) = 1$.

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
   - The message *m* is computed as: $$m = L(c^\lambda \mod n^2) \cdot \mu \mod n $$


## Homomorphic Properties

The Paillier cryptosystem supports these homomorphic operations:

1. **Homomorphic Addition of Two Ciphertexts**:
   - Given two ciphertexts $c_1$ and $c_2$ encrypting plaintexts $m_1$ and $m_2$, their sum $m_1 + m_2$ can be obtained by multiplying the ciphertexts: 
      $$c_{\text{sum}} = (c_1 \cdot c_2) \mod n^2$$
   - Decrypting $c_{\text{sum}}$ yields $m_1 + m_2$.

2. **Homomorphic Addition of a Plaintext to a Ciphertext**:
   - Given a ciphertext $c_1$ encrypting plaintext $m_1$ and a plaintext $m_2$, their sum $m_1 + m_2$ can be obtained by multiplying the ciphertext by $g^{m_2}$:
      $$c_{\text{result}} = (c_1 \cdot g^{m_2}) \mod n^2$$
   - Decrypting $c_{\text{result}}$ yields $m_1 + m_2$.

3. **Homomorphic Multiplication of a Ciphertext by a Scalar**:
   - Given a ciphertext $c_1$ encrypting plaintext $m_1$ and a scalar $k$, the product $k \cdot m_1$ can be obtained by raising the ciphertext to the power of $k$:
      $$c_k = c_1^k \mod n^2$$
   - Decrypting $c_k$ yields $k \cdot m_1$.


## PIR Protocol

**1. Compute t homomorphically :**

The server computes the dot product between the encrypted query vector `v` and the database `T` using Paillier's additive homomorphism:

   - t = Enc(0)
   - for each index j in the database :
      - `v[j]^T[j] mod n²`  homomorphic multiplication of ciphertext by plaintext
      - multiply results : `t = (t * v[j]^T[j]) mod n²`


**2. After decrypting `t`, the client gets the exact value `T[i]` from the database at the requested index i.**

**3. Implement [client.py](./client.py)**

   - constructor `__init__` for `Client` : generates Paillier
   - `request` method : creates an encrypted query vector dor index `i`
   - `decrypt_answer` method

**4. Implement [server.py](./server.py)**

   - constructor `__init__` for `Server` : table of a given size
   - `answer_request` method for homomorphic response

**5. Implement [exchanges.py](./exchanges.py)**

   - tests the PIR protocol between Client and Server

**6. Measure Execution Time:** plots in [exchange.py](./exchanges.py)
   - As the database size increases:
      - The client’s execution time grows linearly, since it must generate and encrypt a query vector of size n.
      - The server’s execution time also increases linearly, as it must exponentiate each ciphertext with the corresponding DB value and multiply the results.

**7. Communication Size Analysis:** plots in [exchange.py](./exchanges.py)

   - Client → Server: Sends n ciphertexts, each roughly of size n² bits. Total size scales linearly with n.
   - Server → Client: Sends only one ciphertext, so size is constant regardless of n.
