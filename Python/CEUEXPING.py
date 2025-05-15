from mpmath import mp, sqrt, sin, cos, acos, radians, mpf, fabs
from datetime import datetime
from ulianovramdompi import get_long_pi,load_public_keys,load_private_keys
from ulianovellicripto import (
    CriptoParams, encrypt_with_public_key, encrypt_with_private_key,
    decrypt_with_private_key, decrypt_with_public_key,get_public_keys,get_private_keys,
    get_long_pi, calculate_CRC_ID,validate_id,get_num_digits,
    convert_str_to_dig3, convert_dig3_to_str,test_keys
)

# Case 1: Encrypt with public key and decrypt with private key
def case_1(params, DX_base,De_base, alpha_base,
           Kpub1, Kpub2, Kpub3,
           Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
           K_ID,num_digits):
    print(f"Case 1: Encrypt with public key => Decrypt with private key")
    print(f"        Used to securely store data: only the owner of the private key can read the data.")
    max_text_length = params.len_data_str
    print(f"Maximum text length that can be transmitted = {max_text_length}")
    max_text_length =503
    print(f"Text length used in this example = {max_text_length}")
  
    # Generating pi with max_text_length total digits
    mp.dps = max_text_length
    original_text = str(mp.pi)[:max_text_length]
    print(f"Original text (length={len(original_text)}) = {original_text}")
    encoded_text = convert_str_to_dig3(original_text)
    mp.dps =num_digits
    print(f"Original text in dig3 code (length={len(encoded_text)})  = {encoded_text}")
    header_number = '12345678912345678901.0'
    print(f"Original header number = {header_number}")
    header_string = "Policarpo Yoshin Ulianov - Criciuma - Santa Catarina - BRAZIL, April - 2025"
    print(f"Original header string = {header_string}")

    print("Data encrypted with public key (only private key can decrypt):")
    encrypted_data = encrypt_with_public_key(encoded_text, header_number, header_string,
                                             DX_base, De_base,
                                             Kpub1, Kpub2, Kpub3, K_ID, params,MSG=True)
    print(f"Encrypted data = {encrypted_data}")

    print("\nDecrypting with private key:")
    _, recovered_dig3_text, recovered_header_number, recovered_header_string = decrypt_with_private_key(
        encrypted_data,
        Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
        DX_base, alpha_base, K_ID, params
    )

    recovered_text, _, _ = convert_dig3_to_str(recovered_dig3_text)
    print(f"Recovered dig3 data: {recovered_dig3_text}")
    print(f"Recovered data: {recovered_text}")
    print(f"Since the data is a string containing the value of pi, the error can be calculated:")
    print(f"recovered data - original data: {mpf(recovered_text) - mpf(original_text)}")
    print(f"Header text: {recovered_header_string}")
    print(f"Header number: {recovered_header_number}")
    
# Case 2: Encrypt with private key and decrypt with public key (updated to 7-key model)
def case_2(params, DX_base,De_base, alpha_base,
           Kpub1, Kpub2, Kpub3,
           Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
           K_ID,num_digits):
    print(f"Case 2: Encrypt with private key => Decrypt with public key")
    print(f"        Used to sign documents: only the owner of the private key can generate this.")
    max_text_length = params.len_data_str
    print(f"Maximum text length that can be transmitted = {max_text_length}")
    max_text_length =503
    print(f"Text length used in this example = {max_text_length}")
    
    # Generate original text (e.g. value of π)
    mp.dps = max_text_length
    original_text = str(mp.pi)[:max_text_length]
    print(f"Original text (π) = {original_text}")
    encoded_text = convert_str_to_dig3(original_text)
    print(f"Encoded DIG3 text = {encoded_text}")
    mp.dps =num_digits
 
    header_number = '12345678912345678901.0'
    header_string = "Policarpo Yoshin Ulianov - Criciuma - Santa Catarina - BRAZIL, April - 2025"
    print(f"Header number = {header_number}")
    print(f"Header string = {header_string}")

    # Encrypt using private key (F2-based)
    encrypted_data = encrypt_with_private_key(
        encoded_text, header_number, header_string,
        Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
        DX_base, alpha_base, K_ID, params,MSG=True
    )

    print(f"\nEncrypted data with private key: {encrypted_data}")

    # Decrypt using public key (F1-based)
    print("\nDecrypting with public key...")
    _ , recovered_dig3_text, recovered_header_number, recovered_header_string = decrypt_with_public_key(
        encrypted_data,
        Kpub1, Kpub2, Kpub3,
        DX_base, alpha_base,K_ID,
        params
    )

    # Convert recovered data
    recovered_text, _, _ = convert_dig3_to_str(recovered_dig3_text)
    print(f"Recovered DIG3 data: {recovered_dig3_text}")
    print(f"Recovered text: {recovered_text}")
    print(f"Error = recovered - original = {mpf(recovered_text) - mpf(original_text)}")
    print(f"Recovered header string: {recovered_header_string}")
    print(f"Recovered header number: {recovered_header_number}")

# Function to generate an ID based on the selected option and long_pi value
def generate_id(option, long_pi):

    id_table = {
       "1":"TOP+ 333",          
       "2":"TOP 1.111",          
       "3":"PRIME+ 345.678",     
       "4":"PRIME 1.134.567",    
       "5":"VIP+ 89.012.345",   
       "6":"VIP 123.456.789",    
       "7":"POP 123.456.789.012" 
    }
    id_without_crc = id_table.get(option)
    if id_without_crc is None:
        return None, None

    num_digits = get_num_digits(id_without_crc)
    id_type, id_number = id_without_crc.split()
    crc = calculate_CRC_ID(f"{id_type}",f"{id_number}", long_pi)
    complete_id = f"{id_type} {id_number}-{crc}"
    print(f"complete_id={complete_id}")
    is_valid, error_msg = validate_id(complete_id, long_pi)
    if not is_valid:
        return False, f"Invalid ID: {complete_id}. {error_msg}"

    return complete_id, num_digits

print("Ulianov Elliptical Encryption Model Example Program.")
# Load the long π value used for ID generation and cryptographic parameters
long_pi, piok = get_long_pi(".//KEYS//", 1000000, generate=False)
if not piok:
    print(f"Error reading long pi: {long_pi}")
    exit()

# Ask user to choose an ID level (e.g., ELITE+, VIP, POP)
ID, num_digits = generate_id(input("Choose ID (1=TOP+;2=TOP;3=PRIME+;4=PRIME;5=VIP+;6=VIP;7=POP): "), long_pi)
print(f"ID={ID}, = Number of digits={num_digits},(encryption of {num_digits*4} bits)")
if ID is None:
    print("Invalid option.")
    exit()

# Initialize cryptographic parameters based on the chosen security level
params = CriptoParams(num_digits)
print("Cryptographic parameters loaded:")
print(params)

# Define password and path to keys
senha = "POLICARPO77777777"
path_keys = "./KEYS"

K1_pub, K2_pub, K3_pub, K_ID, DX_base,De_base, ok_pub, msg_pub = get_public_keys(long_pi, path_keys, ID)

# Load the private key
Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de, ok_priv, msg_priv = get_private_keys(long_pi, path_keys, ID, senha)

# Define a base value for Alpha (used in encryption)
alpha_base_str = "17.888"

# Check whether keys were correctly loaded
if not ok_pub:
    print(f"Error in public key: {msg_pub}")
    exit()
if not ok_priv:
    print(f"Error in private key: {msg_priv}")
    exit()

# Ask if the user wants to display a summary of the loaded keys
opstr = input("Show summary of Public and Private Keys? (y/n): ")
if 0 and opstr.lower() == "y":
    print(f"DX_base     = {str(DX_base)}")
    print(f"De_base     = {str(De_base)}")
    print(f"K_ID        = {str(K_ID)[:60]}")
    print(f"Kpub(K1_pub)= {str(K1_pub)[:60]}")
    print(f"Kpub(K2_pub)= {str(K2_pub)[:60]}")
    print(f"Kpub(K3_pub)= {str(K3_pub)[:60]}")
    print(f"Kpriv(alpha)= {str(Kpriv_alpha)[:60]}")
    print(f"Kpriv(de)   = {str(Kpriv_de)[:60]}")
    print(f"Kpriv(x)    = {str(Kpriv_x)[:60]}")
    print(f"Kpriv(y)    = {str(Kpriv_y)[:60]}")

if 1 and opstr.lower() == "y":
    print(f"DX_base     = {str(DX_base)}")
    print(f"De_base     = {str(De_base)}")
    print(f"K_ID        = {str(K_ID)}")
    print(f"Kpub(K1_pub)= {str(K1_pub)}")
    print(f"Kpub(K2_pub)= {str(K2_pub)}")
    print(f"Kpub(K3_pub)= {str(K3_pub)}")
    print(f"Kpriv(alpha)= {str(Kpriv_alpha)}")
    print(f"Kpriv(de)   = {str(Kpriv_de)}")
    print(f"Kpriv(x)    = {str(Kpriv_x)}")
    print(f"Kpriv(y)    = {str(Kpriv_y)}")


# Test if the private and public keys match (only the key owner can perform this)
print("\nTesting Keys (Only the owner of the keys can do this):")
keyok, DX_base,De_base = test_keys(
        K1_pub, K2_pub, K3_pub,
        Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de, alpha_base_str,
        str(K_ID), num_digits)

if not keyok:
    print("Error testing keys")
    exit()
else:
    print("Keys successfully loaded and verified\n")

# Main menu: user chooses the encryption/decryption case
while True:
    op = input("Case 1 (encrypt with public key) or 2 (encrypt with private key)? ")
    if op == "1":
        case_1(params, DX_base,De_base, alpha_base_str,
               K1_pub, K2_pub, K3_pub,Kpriv_alpha, 
               Kpriv_x, Kpriv_y, Kpriv_de, K_ID,num_digits)
        
    elif op == "2":
       case_2(params, DX_base,De_base, alpha_base_str,
               K1_pub, K2_pub, K3_pub,Kpriv_alpha, 
               Kpriv_x, Kpriv_y, Kpriv_de, K_ID,num_digits)
    else:
        print("Invalid option.")
        exit(0)
