from ulianovramdompi import get_long_pi,get_one_time_kpi
from ulianovellicripto import (
    CriptoParams, get_public_keys,get_private_keys,
    get_long_pi, calculate_CRC_ID,get_num_digits,cripto_kpi,decripto_kpi,
    criptografar_arq_key_pub
)
import time
from datetime import datetime
import sys

   
print("Test file Encryption with publick key in UEC Model")
print("This practical example works only with text files with up to 2000 characters for user with TOP+ ID and 503 characters for POP ID.")

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
print(f"Private key and Pulick key loaded and tested OK")
User_name="Policarpo Yoshin Ulianov"


time_str ="18/05/2025 10:30:10.1234"
KPI01=get_one_time_kpi(time_str, Kpriv_alpha,long_pi,180)
print(f"time_str ={time_str}\nlen(KPI01)={len(KPI01)} KPI01={KPI01}")

file_name=".\\IMG\\teste3.jpg"
start = time.time()
ok,msg, output_name, crc_orig, crc_cryp=cripto_kpi(file_name, long_pi, KPI01)

end = time.time()
delta = end - start

if ok:
   print(f"OK: {msg}")
   print(f"output_name ={output_name},crc_orig={crc_orig},crc_cryp={crc_cryp},")
   
   print(f"Encryption time with {params.num_digits} digits: {delta:.3f} seconds")
else:
   print(f"ERROR: {msg}")

file_name=".\\IMG\\teste3_jpg.ubin"
start = time.time()
ok,msg,output_name=decripto_kpi(file_name, long_pi, KPI01,crc_orig, crc_cryp)

end = time.time()
delta = end - start

if ok:
   print(f"file {output_name} ,OK: {msg}")
   print(f"Encryption time with {params.num_digits} digits: {delta:.3f} seconds")
else:
   print(f"ERROR: {msg}")
