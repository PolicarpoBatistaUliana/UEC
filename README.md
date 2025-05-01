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

