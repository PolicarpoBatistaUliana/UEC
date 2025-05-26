from ulianovramdompi import get_long_pi,get_one_time_kpi
from ulianovellicripto import (
    CriptoParams, get_public_keys,get_private_keys,
    get_long_pi, calculate_CRC_ID,get_num_digits,test_keys,
    sign_file_with_private_key
)
import time

print("Test program that sing small text files (<100k bytes) with private keys in UEC Model")
print("This practical example works only with text files stored im folder /EXP")

# Load the long π value used for ID generation and cryptographic parameters
long_pi, piok = get_long_pi(".//KEYS//", 1000000, generate=False)
if not piok:
    print(f"Error reading long pi: {long_pi}")
    exit()
# Fix ID for test
id_without_crc ="TOP+ 333"
num_digits = get_num_digits(id_without_crc)
id_TY, id_number = id_without_crc.split()
crc = calculate_CRC_ID(f"{id_TY}",f"{id_number}", long_pi)
ID = f"{id_TY} {id_number}-{crc}"
print(f"ID={ID}, = Number of digits={num_digits},(encryption of {num_digits*4} bits)")
params = CriptoParams(num_digits)
print("Cryptographic parameters loaded:")
print(params)
# Define password and path to keys
senha = "POLICARPO77777777"
path_keys = "./KEYS"
# Load the public key
K1_pub, K2_pub, K3_pub, K_ID, DX_base,De_base, ok_pub, msg_pub = get_public_keys(long_pi, path_keys, ID)
# Define a base value for Alpha (used in encryption)
alpha_base_str = "17.888"
# Check whether keys were correctly loaded
if not ok_pub:
    print(f"Error in public key: {msg_pub}")
    exit()
load_priv_keys=True
need_test_keys = True    
if load_priv_keys:
    # Load the private key
    Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de, ok_priv, msg_priv = get_private_keys(long_pi, path_keys, ID, senha)
    if not ok_priv:
        print(f"Error in private key: {msg_priv}")
        exit()
    if need_test_keys:
       # Test if the private and public keys match (only the key owner can perform this)
        print("\nTesting Keys (Only the owner of the keys can do this):")
        keyok, DX_base,De_base = test_keys(K1_pub, K2_pub, K3_pub,
            Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de, alpha_base_str,
            str(K_ID), num_digits)

        if not keyok:
           print("Error testing keys")
           exit()

print("Keys successfully loaded and verified\n")
User_name="Policarpo Yoshin Ulianov"
file_name=".\\TEXT\\teste1.txt"
print("Keys successfully loaded and verified\n")

signer_ID = "TOP+ 333-333"
signer_name = "Policarpo Yoshin Ulianov"

# Primeiro teste com 7000 dígitos
params = CriptoParams(7000)
file_name = ".\\TEXT\\teste1.txt"
print(f"Signing {file_name} With {signer_ID} Private Keys using {params.num_digits} digits")
start = time.time()

ok, msg, out_file = sign_file_with_private_key(
    file_name, signer_ID, signer_name,
    Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
    DX_base, alpha_base_str, K_ID, params
)

end = time.time()
delta = end - start

if ok:
    print(f"OK: {msg}")
    print(f"File {out_file} generated and available for verification")
    print(f"Signing time with {params.num_digits} digits: {delta:.3f} seconds")
else:
    print(f"ERROR: {msg}")

file_name = ".\\TEXT\\teste2.txt"
print(f"Signing {file_name} With {signer_ID} Private Keys using {params.num_digits} digits")
start = time.time()

ok, msg, out_file = sign_file_with_private_key(
    file_name, signer_ID, signer_name,
    Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
    DX_base, alpha_base_str, K_ID, params
)

end = time.time()
delta = end - start

if ok:
    print(f"OK: {msg}")
    print(f"File {out_file} generated and available for verification")
    print(f"Signing time with {params.num_digits} digits: {delta:.3f} seconds")
else:
    print(f"ERROR: {msg}")
