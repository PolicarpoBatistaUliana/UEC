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

### References

1. Ulianov, P. Y. (2025). *Ulianov Elliptic Trigonometry: A New Approach to the Exact Calculation of Ellipse Perimeters*. American Journal of Mathematical and Computer Applications, 1(1), 01–11.  
   [Link to publication](https://www.academia.edu/128382884/)

2. Ulianov, P. Y. (2024). *Ulianov Elliptical Transform: A New Paradigm for Ellipse Manipulation*. Journal of Mathematical Techniques and Computational Mathematics.  
   [Link to publication](https://www.academia.edu/123488483/)

3. Ulianov, P. Y. (2024). *Ulianov Orbital Model: Describing Kepler Orbits Using Only Five Parameters and the Ulianov Elliptical Trigonometric Function – Elliptical Cosine and Elliptical Sine*. Physics & Astronomy International Journal.  
   [Link to publication](https://www.academia.edu/123102792)



### Example of Small Keys 

POP ID Keys - Only 2500 digits  (10kbits)

A single bit changing in this keys tranform the data into randon noise.
So the Publick Keys and the Private Key used in the crypto/decrypto functions need e exact until the last decimal place


``` 
K PUB (DX)    = -2.23410234724946614000
```
```
K PUB (K_ID)  = 0.27303666508580967592546810870043533122821618463771816860771876157619602746045062710523031717492828800881325281397063931182527407404880963258532673053166566054129457438473324325304900918608508657334975400756854403985468896454367819330093985971810732110702962925757682918411327781485246375643658442033650788491389466044044003181335727154446303664768420071612516976236166953315330990622483243371005639071723467313948647221175974885934617043310427850582842817950521013723986191950853093432738761074465063591423520089918445226707515603613657959007728312237048767573759930279817638103179920378920129895161108525239580240277974312811120773050819678261630084406737220159503802864864296123577881193125833397009115595350302430550694344139911399545804318730176554993425040105892847308452667065752191638068331370538137952427807344750042401255496557388908802174597029624857894988719719327932714634705162337300265437198070971947436041773203539320250093818421193659453580899833191298347211921995244715834825742543361346176040128696387688725830656096469819164357926855215129530454638516410354684188352216876325173641457208998054896457476447210929612327090833509421927901984046268618566311013424912844511892093752328936184935601781003331968621274062258242384029302635274618162078807238600404322041256492083701275442519048431684569961114611808097050969922123371005415101263134950250593169392195622119372329496767512955028553778945390321839907128115640944364647880520288094458590758040509224662386022525441084753530672732042273259966483073276455773329314755096981824660795371146325395264033193218887574288838653455163847306752666501681337964061961187236872117890991925220309299232837730803134049284250376577224779824808133074841899845277158087233667418613748167511712535293033051170493833140523469931474473278224304563401100061035555823099665921868208223781570413601870267901446281405260647779338730242558437091879032512632122657395677093620915648507869636434330561076788878769756881942341420810620204810385343318115367100918881533857512220582669203507416533803022614845216234170184744439865786799335824713838938365693138832325750024623553539086287297808943444788789801322617664484220441728113323628678266512863366520551542819215956558369724292445483292245090491782204283305011402534435985242453050481308315421916909109441076077853547159525375837197423424042393892945600951335954565819330603585657673700249462218806651366085171645
```

```
K PUB (K1_pub)= 1.5246857232480504203876011230417174376755875470511969950621232759394322991429417423470455160166563072389328179203194309192995055643393915113685517749334545399804097546066396539126107858122494188657649077703351679108182784693992110258855695032480084804229598396531244919024349202422673938908566058728886543334847428206478692922814962596875040722176138759912870530458849555454554204336305939094272567028627880163940477679389125348006460084161636972883687250784685471334341959750810463946503872758506467950430207155023549691711443267902854106682370289923022013979954135002164174755031351956714712842432402035923118180585827262045134572567604060919108275344017731270570866563834907438270457507736921237716492152237375194004827298318326791964395607491312575734779255777004243786993523020530926625645274152042200192281332116121307506862034069057327306969717936039403618653018870483664636939324440872590138480419917614706332287195964236919717491179793218815634203221979064011206021994899601553799246303038841038336510796570973345578928274972292794439853161294186247865745366136708523651941075393561345853446040577292204742665257117625138857581676386409627034360070859921405111813779229432036960373671183802022387649180333764248304213320031050371957747367426632443531485833513013527708186006331393214038768485665018932468978286426353426466366931342558898636682284651972655921691378052265608469202371987300309208532342325485631732047273507827094768600842440679488255023852922801036406333123355593990135467123630418859327234728750280488496400686783223974039855879417715675405352145320306138056984383303445239469257770763443444826091328089874002179111042753755279267412444267249979140051601210134949394308953231350477017424045112237874737527483210811846037689803093203915811192650224059096040034465227762184628304476607891529108334010683750943076684222382173879106609688101870500301017124851344491487699257151609341726325831281235573840255151304401685366995603160144757908288391905605524600387176027405438045006422552140767496362233916176627347347620976906999172875499127997007836537282960019667156219427523767353059317207812972127751574832692782369329202483975001236915524291219369180334123606464518535752857302441143263776811366469848798367821429352177935769304614770840625206633153747431957982684627640031087958155202261205857332724851746194908897696698219180763619640547258147696489579643007117250934353297736020131646643803408034654695267566948518597883379772585430358633816410485189888344360238183955698740
```

```
K PUB (K2_pub)= -2.4695633000577656141770222342520277084139881925970705468392013873594669767781775824342783593913856113840500744022864163376953932096011315662778930516209461735593648640086788557287660879848973579246529294450296918838916582348879128782361949429520805736476704828124772586335378018255648069212860915998953122876410700529579924389383851544085278949027276484094361098191187154686255886347415781182374441292978345779726091825554697101172350158736858868233464704945620894114498699701524826289249994625294294263437399806786924280181496055123024984324301072854142682805664240930558026884469688539205378767548273686649948623944618970249579207430517431933238843450627858816470754834989031177249993892767858475943366603939405353031642128035297045751466551852273589686844646130341126161598086673920664535276433825166779464296998371628299048885789967142974380084403956890853523044671271159501333172707153072377919469309926698631866302880437207328697674257436373153016454726490240354545896470159827910279823979156912209239392121103164146097436769565430664649846349798727384208624335861604691511372140203047548407740433032434066969220548373715698709690129772048058077213882079479237605557227064757564059858623670715879894765524814143923195825406175179646487026868703871102376228783722444266779250908434419941344161842022413386412848742863580784467364128683992401577400852339564137500808192209531787227840900424645380101041240461257690299694433736386270065255065449955918855553619875736240230373367090849665085339176690851889587590348180446499164783925373290503234390084851973636045294733017084051733287884823155563520185027198759136686968422630461758216803410619875281763974230165465061687781323126466721179667012176940695993070596192349212652103015869342520092508761658263933184879003922320379445007550949023221880302280777951875774639296208631627129740325536374234551994867414018864786955381387561542377211345622000250573257032205698628671450807537168548919282852693458626445504274851914389274832402349310236603835719282364185661985885145731781518518641629868520694270301966537908055756789321271583031039309440556427024916207925865678179726986925521688856775552565382226958309095111941330732990069975295164345934308185603051040659197462436048776303318975818290387140958152133343237457691659864449863260457215187655337233341512331045646131569895602818230887519920848817825556865309185946125214500013306824163204807710998403181181952951416113077799504883849104523838022207213229941478455798733405831025763261458904390
```

```
K Priv        = 1.2347816500288828070885111171260138542069940962985352734196006936797334883890887912171391796956928056920250372011432081688476966048005657831389465258104730867796824320043394278643830439924486789623264647225148459419458291174439564391180974714760402868238352414062386293167689009127824034606430457999476561438205350264789962194691925772042639474513638242047180549095593577343127943173707890591187220646489172889863045912777348550586175079368429434116732352472810447057249349850762413144624997312647147131718699903393462140090748027561512492162150536427071341402832120465279013442234844269602689383774136843324974311972309485124789603715258715966619421725313929408235377417494515588624996946383929237971683301969702676515821064017648522875733275926136794843422323065170563080799043336960332267638216912583389732148499185814149524442894983571487190042201978445426761522335635579750666586353576536188959734654963349315933151440218603664348837128718186576508227363245120177272948235079913955139911989578456104619696060551582073048718384782715332324923174899363692104312167930802345755686070101523774203870216516217033484610274186857849354845064886024029038606941039739618802778613532378782029929311835357939947382762407071961597912703087589823243513434351935551188114391861222133389625454217209970672080921011206693206424371431790392233682064341996200788700426169782068750404096104765893613920450212322690050520620230628845149847216868193135032627532724977959427776809937868120115186683545424832542669588345425944793795174090223249582391962686645251617195042425986818022647366508542025866643942411577781760092513599379568343484211315230879108401705309937640881987115082732530843890661563233360589833506088470347996535298096174606326051507934671260046254380829131966592439501961160189722503775474511610940151140388975937887319648104315813564870162768187117275997433707009432393477690693780771188605672811000125286628516102849314335725403768584274459641426346729313222752137425957194637416201174655118301917859641182092830992942572865890759259320814934260347135150983268954027878394660635791515519654720278213512458103962932839089863493462760844428387776282691113479154547555970665366495034987647582172967154092801525520329598731218024388151659487909145193570479076066671618728845829932224931630228607593827668616670756165522823065784947801409115443759960424408912778432654592973062607250006653412081602403855499201590590976475708056538899752441924552261919011103606614970739227899366702915512881630729452190
```








