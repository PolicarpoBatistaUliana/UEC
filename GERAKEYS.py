import os 
from ulianovramdompi import get_long_pi
from ulianovellicripto import calculate_all_keys

# IDs to generate
ids_to_generate = [
    "TOP+ 333",            
    "TOP 1.234",         
    "TOP 1.111",          
    "PRIME+ 345.678",     
    "PRIME+ 123.456",     
    "PRIME 7.777.777",   
    "PRIME 1.134.567",    
    "VIP+ 89.012.345",    # $1,000.00
    "VIP+ 12.345.678",    # $1,000.00
    "VIP 222.222.222",    # $100.00
    "VIP 123.456.789",    # $100.00
    "POP 123.456.789.012" # $10.00
]

ids_to_generate1 = [
    "POP 123.456.789.012" # $10.00
]

# Load Pi (do this only once before making calls)
path_to_pi = "./KEYS"
long_pi, pi_loaded_successfully = get_long_pi(path_to_pi, 1000000, generate=False)
if not pi_loaded_successfully:
    print("Error loading long pi")
    exit()

# Basic definitions
password1 = "POLICARPO77777777"
password2 = "ULIANOV1234567890"
timestamp = "31/07/2024 13:57:18.387"
keys_path = "./KEYS"

os.makedirs(keys_path , exist_ok=True)

# Generate keys for each ID
for base_id in ids_to_generate:
    display_messages = base_id=="POP 123.456.789.012"
    success, message = calculate_all_keys(long_pi, keys_path, password1,password2, timestamp, base_id, MSG=display_messages)
    if success:
        print(f"[SUCCESS]: {message}")
    else:
        print(f"[ERROR]: {message}")

