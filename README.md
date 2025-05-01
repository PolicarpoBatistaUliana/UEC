# UEC
# Ulianov Elliptic Cryptography
#### Ulianov Elliptical Encryption Model

The **Ulianov Elliptical Encryption Model** is an advanced cryptographic framework leveraging high-precision arithmetic (via the `mpmath` library) and Pi-based calculations to enhance complexity and cryptographic security. This model uniquely uses real-number arithmetic rather than traditional integer-based cryptographic methods.

#### Encryption Modes

##### Mode 1: Public-Key Encryption, Private-Key Decryption

- **Purpose**: Secure data storage. Anyone can encrypt data using the public key, but only the owner of the private key can decrypt and read the data.
- **Typical Use Case**: Confidential data exchange where the recipient is the sole entity authorized to access the information.

##### Mode 2: Private-Key Encryption, Public-Key Decryption

- **Purpose**: Digital signature. Only the holder of the private key can encrypt (sign) the data, ensuring authenticity when verified with the public key.
- **Typical Use Case**: Digital signing of documents to guarantee authenticity and non-repudiation.

#### Program Workflow

- **Select Cryptographic ID (Security Level)**: Choose a security tier (POP, VIP, PRIME, etc.), defining key length and security strength (e.g., POP uses 2500 digits ≈ 10,000 bits).
- **Generate Cryptographic Parameters**: Configures internal system parameters (`CriptoParams`), such as header positions and data lengths, according to the selected security level.
- **Load and Verify Cryptographic Keys**: Public and private keys are loaded and validated to ensure correctness.
- **Encrypt/Decrypt Process**: Data (e.g., the value of π in high precision) is transformed into a special encoding format (DIG3), encrypted, and later decrypted, validating integrity and accuracy.

#### Enhanced Key Protection

Private keys receive additional protection through:
- **Password Integration**: Combined with key identifiers and a normalized file path to derive encryption keys from Pi, significantly increasing difficulty for unauthorized access.
- **Path Normalization**: Enables flexibility for demonstration and distribution while maintaining robust security.

#### Practical Applications

- **Secure Sensitive Data Storage**: Public-key encryption for storing, private-key for accessing data.
- **Secure Digital Signatures**: Private-key signing, public-key verification.
- **Digital Certificate and Cryptographic ID Generation**: Secure and verifiable IDs and certificates resistant to forgery.

#### Conclusion

The Ulianov Elliptical Encryption Model provides exceptional security leveraging advanced mathematical techniques and unconventional approaches (high-precision real arithmetic and Pi-based key derivation), making it uniquely robust for digital security contexts.

#### How to Run an Example of the Ulianov Elliptical Encryption Model (UEC)

A simple example is provided to demonstrate how UEC functions, considering seven categories of public and private key sets associated with unique IDs:

- TOP+ (7000 digits)
- TOP (6000 digits)
- PRIME+ (5000 digits)
- PRIME (4000 digits)
- VIP+ (3500 digits)
- VIP (3000 digits)
- POP (2500 digits)

##### Steps to Run the Example:

1. **Download the Repository**: Clone or download all Python source files and the KEYS directory.

2. **Directory Structure**:

```
UEC/
├── KEYS/
│   └── (Key files)
├── CEUEXPING.py
├── ulianovellicripto.py
└── ulianovramdompi.py
```

3. **Install Required Libraries**:

```bash
pip install mpmath numpy
```

4. **Running the Example**:

Open a command line (Windows CMD or Shell) and navigate to the `UEC` directory:

```bash
cd C:\UEC
python CEUEXPING.py
```

You will see the prompt:

```
Ulianov Elliptical Encryption Model Example Program.
Choose ID (1=TOP+;2=TOP;3=PRIME+;4=PRIME;5=VIP+;6=VIP;7=POP):
```

Choose an ID between 1 and 7. For example, selecting "7" (POP) loads:

- Public keys: `Key-Pub-POP 123.456.789.012-345.txt`
- Private key: `Key-Priv-POP 123.456.789.012-345.txt`

The prompt will ask if you want to show a summary of the keys:

```
Show summary of Public and Private Keys? (y/n): y
```

You will see a truncated summary of keys:

```
K PUB (DX)    = -2.23410234724946614000
K PUB (K_ID)  = 0.2730366650858096759254681087004353312282161846377181686077
K PUB (K1_pub)= 1.5246857232480504203876011230417174376755875470511969950621
K PUB (K2_pub)= -2.469563300057765614177022234252027708413988192597070546839
K Priv        = 1.2347816500288828070885111171260138542069940962985352734196
```

##### Encrypting and Decrypting:

You will be prompted to choose encryption with:

- `1`: Public-key encryption, private-key decryption (secure data storage).
- `2`: Private-key encryption, public-key decryption (digital signature).

The example encrypts three fixed items:
- A string (500 digits of Pi).
- A header number (up to 300 digits).
- A header string (up to 180 characters).

After encryption, a 2500-digit encrypted block is produced (for POP). The header data is stored in the first 1000 decimal places, and encrypted data from 1000 to 2500, ensuring secure and independent encryption layers.

**Note**: The provided example handles encryption and decryption in a single process for simplicity, but in real scenarios, these processes are separated. Private keys (`K Priv`) should be securely stored and encrypted with user-specific passwords or sophisticated protection methods incorporating multiple authentication factors.

#### Four Basic Functions for Encryption and Decryption

The UEC model provides four core functions:

##### 1. **encrypt_with_private_key**
Encrypts data using a private key. This method ensures data authenticity by allowing only the private key holder to generate the encrypted content, which can be verified publicly.

##### 2. **decrypt_with_public_key**
Decrypts data using public keys, enabling verification of data authenticity encrypted by a private key.

##### 3. **encrypt_with_public_key**
Encrypts data using public keys. Ideal for securely storing or sending confidential data that only the holder of the corresponding private key can decrypt.

##### 4. **decrypt_with_private_key**
Decrypts data using the private key. Allows secure access to data encrypted with the corresponding public keys.

These functions handle encryption and decryption operations by processing numeric and string headers along with data, leveraging cryptographic keys and parameters to ensure secure and verifiable data exchanges.

##### Example Usage:

###### Case 1: Public-key encryption, Private-key decryption
Used for securely storing data, ensuring only the private key owner can access it.

```python
encrypted_data = encrypt_with_public_key(encoded_text, header_number, header_string, mpf(DX_base), alpha_base, public_key_1, public_key_2, key_ID, params)
_, recovered_dig3_text, recovered_header_number, recovered_header_string = decrypt_with_private_key(encrypted_data, private_key, mpf(DX_base), alpha_base, key_ID, params)
```

###### Case 2: Private-key encryption, Public-key decryption
Used for signing documents, where authenticity can be publicly verified.

```python
encrypted_data = encrypt_with_private_key(encoded_text, header_number, header_string, private_key, mpf(DX_base), alpha_base, key_ID, params)
DX, recovered_dig3_text, recovered_header_number, recovered_header_string = decrypt_with_public_key(encrypted_data, public_key_1, public_key_2, mpf(DX_base), alpha_base, key_ID, params)
```

These functions handle encryption and decryption operations by processing numeric and string headers along with data, leveraging cryptographic keys and parameters to ensure secure and verifiable data exchanges.

#### Elliptical Cryptographic Functions F1 and F2

The Ulianov Elliptical Encryption method uses two distinct cryptographic functions, **F1** and **F2**, characterized by their unique mathematical relationship:

- **F1** operates based on the public key and does not have a complete analytical inverse, only being analytically invertible within specific regions determined during key generation.
- **F2** operates with the private key and is analytically invertible for the chosen range of cryptographic parameters. This allows for exact decryption by the key owner.

The functions follow a mathematical form resembling elliptical equations, such as:

```python
F1: encrypted_data = (AlphaA * Kpub1 + Kpub2) / (DX_base + K_ID)
F2: recovered_data = (encrypted_data * (DX_base + K_ID) - Kpub2) / Kpub1
```

(These Python-like representations simplify understanding; the actual implementation involves high-precision arithmetic.)

The security strength of UEC lies in the complexity of numerically inverting F1 without access to the private key. Numerical inversion or interpolation is computationally impractical due to the high precision required (e.g., 2500 digits in the POP category).

Furthermore, the method is resilient against quantum computing attacks, as it does not rely on factoring large prime numbers, a process easily compromised by quantum algorithms. Instead, UEC uses sophisticated real-number arithmetic and elliptical function complexity, greatly surpassing traditional prime-factorization-based encryption in robustness against quantum attacks.




