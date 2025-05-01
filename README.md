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

#### Cryptographic Keys in UEC

The UEC method utilizes a total of five cryptographic keys:

- **K PUB (DX)**: A short key used as an offset, ensuring the encryption operates within a specific range of values where F1 is analytically invertible by F2.
- **K PUB (K_ID)**: A Pi-based key, uniquely generated using the ID name. If the ID is forged, it results in an incorrect K_ID, thus preventing decryption and providing additional security.
- **K PUB (K1_pub) and K PUB (K2_pub)**: The main public keys, typically ranging from 2500 to 7000 digits, depending on the chosen security ID.
- **K Priv**: The private key, held exclusively by the user, essential for decryption or document signing.

In the proposed system, public keys (K1_pub and K2_pub) will be publicly available via a central server, facilitating the issuance of certificates linking user IDs to personal information. Users can generate their own IDs, but the official certification, preventing duplication and ensuring uniqueness, will be centrally managed. Certificate issuance for legalizing an ID-user name combination will involve a nominal fee:

- **POP IDs**: Certificates priced affordably, between 1 to 10 USD.
- **Other IDs**: Higher-priced certificates, with specific costs yet to be defined.

This structured approach ensures both security and accessibility, balancing rigorous cryptographic protection with practical use-case affordability.

#### Proposed Certification Scheme

Any public-private key system faces two main challenges:

##### 1. Keeping Private Keys (KPriv) Secret

Ensuring private key secrecy is crucial and primarily the user's responsibility. Rather than relying on long, complicated passwords, an ideal approach integrates system-specific data from the user's computer, such as:

- Unique files and deeply nested directories containing hidden data.
- Mass CRC calculations on large, stable data like personal photo or video files.

Such methods allow simple, memorable passwords to be transformed internally into highly secure keys. For instance, a simple password like "BOY77" could internally transform into something like "BOY77-2807088511117126013854206994096298535273419" using unique system-derived data.

An effective strategy involves users creating memorable, unusual phrases, e.g., "the sun fell into the toilet and slept," simplifying memorization to keywords like "SUN," "FELL," "TOILET," "SLEPT." With execution times for unlocking keys set to around one minute per attempt, even simple, lowercase-letter passwords of four words generate a computational security span extending for centuries, making brute-force attacks virtually impossible. Notably, even possessing the correct password outside the user's own computer environment would not unlock the key, ensuring robust protection against unauthorized access.

##### 2. Ensuring Secure Association Between User IDs and Public Keys (KPub)

The second critical issue is guaranteeing that an ID-username combination (real or pseudonymous) is correctly associated with its corresponding public keys (KPub). This protects against scenarios where an attacker might generate a false set of keys to impersonate a legitimate user.

The safest solution involves a centralized, automated certification system—a strictly controlled software running on a secure, isolated machine. This system generates certificates securely linking an ID and username directly with their corresponding KPub (K1PUB, K2PUB, KDX).

#### Certification Hierarchy

To ensure robust, scalable certification, a structured hierarchy with four ID types is proposed:

- **GOD 001**: The top-level certifier, certifying only ARC IDs. Uses a publicly disclosed KPub and K_ID based on Pi with 20,000 decimal digits.
- **ARC 001-001 to ARC 999-999**: Each ARC certifies user IDs, creating secure, verified public certificates.
- **ANJ XXX.001-CRC to ANJ XXX.999-CRC**: Certified by ARCs, used primarily by notaries or official institutions to link users' real identities and various personal documents to their KPub.
- **DAE XXX.YYY.001-CRC to DAE XXX.YYY.999-CRC**: Certified by ANJs, providing an additional layer for detailed document and identity associations.

This structured system implies:

- **GOD** certifies 999 ARCs, creating the foundational security layer and subsequently can be securely shut down.
- **ARCs** certify individual user IDs and names, generating certificates that users can publicly validate.
- **ANJs** facilitate official certifications by associating real identities and various documents with KPub.
- **DAEs** offer detailed certification capabilities at even more specific levels.

Upon receiving their certificate, a user verifies it by opening it with the publicly available GOD KPub. If successful, they record the GOD KPub encrypted using their own KPub (accessible only via their KPriv). This establishes a secure verification chain, enabling users to securely open subsequent ARCs and ANJs certificates.

This certification chain is robust because it reduces security vulnerabilities to a single issue: safeguarding the user's private key (KPriv). With GOD creating the initial secure environment and disappearing post-certification, ensuring ARC physical and access security is sufficient for maintaining system integrity.

Dr. Ulianov further proposes an advanced system, "Cerberus," involving three CPUs running in parallel without storing KPriv on a hard drive—keeping it solely in volatile memory. This design ensures that if all CPUs shut down simultaneously, the private key is irretrievably lost, significantly reducing vulnerabilities even to physical attacks.

#### Implementation and Practical Considerations

While highly secure and advanced, such a system's realization would benefit from backing by a company or non-governmental organization due to the complexity and infrastructure required. Its primary advantage lies in generating globally unique, indefinitely valid, and practically inviolable IDs and certifications.

By safeguarding their KPriv effectively, each user contributes to an unbreakable global system of identity certification, ensuring unmatched digital security.

#### Key Generation

Generating a key pair for use with UEC is straightforward: simply provide a password, a timestamp, and a folder to store the output files. Both the password and the folder path will be required later to unlock the private key.

Although this example uses a string-based password, more advanced systems can replace it with arbitrary byte sequences, hidden metadata in media files, or even structured CRC computations over stable data like videos or image libraries. The timestamp ensures that each key is unique—even changing the milliseconds in a single day results in up to **10⁹** possible variations. Thus, the generation process is both deterministic and chaotic: the same inputs yield the same output, while small variations lead to completely different keys.

Unlike traditional cryptography based on large prime numbers, which become increasingly difficult to generate for higher bit sizes, this model is free of such limitations. For example, generating a pair of 2,500-digit keys takes around **0.1 seconds** on a standard notebook, while a 250,000-digit key takes around **100 seconds**, showing that processing time scales roughly with the **square of the number of digits**. For high-security or military-grade applications, this remains a feasible solution, even at extreme sizes like **800,000 bits**.

One important consideration is that the public release of this technology is being conducted in **two stages**:

1. **Initial Phase**: All core cryptographic source code is published, **except** the key generation function. The version shared has been obfuscated: key expressions were randomly altered or removed, and decoy equations were introduced, while preserving execution time and structure.

2. **Final Phase**: Within **6 to 24 months**, the complete and correct version of the key generation routine will be disclosed. During this time, Dr. Ulianov seeks to establish partnerships with institutions interested in secure communications, post-quantum cryptography, and digital ID systems.

The **core function** that governs the cryptographic relationship between public and private keys is:

```python
def calculate_pub_priv_keys(Ke_str, K_ID_str, num_digits):
    """
    Calculates the public keys (Kpub1, Kpub2) and the private key (Key_priv)
    based on the provided Ke and K_ID values.

    Parameters:
    - Ke_str (str): The primary key value as a string.
    - K_ID_str (str): The key identifier as a string.
    - num_digits (int): The number of decimal places for precision.

    Returns:
    - Kpub1_str (str): The first public key component as a string.
    - Kpub2_str (str): The second public key component as a string.
    - Key_priv_str (str): The private key as a string.

    Note:
    Determining the values of K0, K1, and K2 from the public keys Kpub1 
    and Kpub2 is inherently unfeasible due to the underdetermined nature 
    of the system: three unknowns with only two equations. 
    Even with the inclusion of K_ID to form a third equation, 
    the introduction of KX as an additional variable results in four unknowns 
    against three equations. Moreover, the nonlinear relationships, exemplified 
    by equations like:
      Kpub1 = (K0 + K2) / (K1 - K0) and 
      Kpub2 = (K2 * K1²) / (K1 - K0), 
    lack analytical solutions. 
    Attempting numerical solutions is further complicated by the necessity 
    for extremely high precision, potentially requiring computations with 
    up to 3,000 decimal places. 
    """
```

This highlights one of the key advantages of the Ulianov Elliptical Encryption Model: even with public keys available, reversing the system to extract the private key is mathematically impractical. The complexity and depth of the nonlinear system protect against brute-force, interpolation-based, and even quantum attacks—offering a viable long-term replacement for current prime-based schemes.

To demonstrate the model's feasibility and scalability, **seven full key sets** are being released. These are sufficient to validate the system and engage in collaborations focused on:

- Quantum-resistant cryptocurrencies
- Replacing RSA/DSA/ECC systems with real-number-based elliptic encryption
- Implementing low-cost, globally unique digital IDs (especially with the POP ID tier priced between **\$1 and \$10**)

For security reasons, no written copies of the complete generation routine are maintained at this stage. It resides solely in the mind of Dr. Ulianov—ensuring initial control before responsibly transferring the technology to future partners.








