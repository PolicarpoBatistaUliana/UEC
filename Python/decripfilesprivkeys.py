from ulianovramdompi import get_long_pi
from ulianovellicripto import (
    CriptoParams, get_public_keys,get_private_keys,test_keys,
    get_long_pi, calculate_CRC_ID,get_num_digits,
    decryp_file_key_priv)

print("Test program that dencrypt small text files with publick key in UEC Model")
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

User_name="Policarpo Yoshin Ulianov"

#file_name="teste1.txt"
#ok,msg = criptografar_arq_key_pub(file_name,ID,User_name,ID,User_name,DX_base,De_base,K1_pub,K2_pub,K3_pub,K_ID,params)


file_name=".\\TEXT\\teste1_txt.uec"
print(f"Decrypting {file_name} With {ID} Private Keys")


ok,msg= decryp_file_key_priv(file_name, ID, User_name,
                                Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
                                DX_base, alpha_base_str, K_ID, params)
if ok:
   print(f"OK: {msg}")  
else:
   print(f"ERRO: {msg}")       


file_name=".\\TEXT\\teste2_txt.uec"
print(f"Decrypting {file_name} With {ID} Private Keys")
ok,msg= decryp_file_key_priv(file_name, ID, User_name,
                                Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de,
                                DX_base, alpha_base_str, K_ID, params)
if ok:
   print(f"OK: {msg}")  
else:
   print(f"ERRO: {msg}")          