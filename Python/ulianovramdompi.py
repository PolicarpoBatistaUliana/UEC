from mpmath import mp, sqrt, sin, cos,acos, radians, mpf,fabs
import os
import re
import sys

import os
import re
import sys
from mpmath import mp, mpf

def normalize_protection_path(path):
    """
    Normalizes and sanitizes a file path by converting it to an absolute path,
    uppercasing all characters, and removing non-alphanumeric characters.

    :param path: The file path to normalize.
    :return: A sanitized string representing the normalized path.
    """
    # Convert to absolute path
    absolute_path = os.path.abspath(path)
    # Convert to uppercase to avoid case sensitivity issues
    absolute_path = absolute_path.upper()
    # Remove non-alphanumeric characters
    normalized_path = re.sub(r'[^A-Z0-9]', '', absolute_path)
    return normalized_path

def limit_k(k_str, num_digits):
    """
    Limits the number of decimal places in a numeric string to 'num_digits'.

    :param k_str: String representing the number.
    :param num_digits: Desired number of decimal places.
    :return: String with the number adjusted to the specified decimal places.
    """
    if '.' in k_str:
        integer_part, decimal_part = k_str.split('.')
        current_decimals = len(decimal_part)
        if current_decimals > num_digits:
            # Truncate the decimal part
            decimal_part = decimal_part[:num_digits]
        else:
            # Pad with zeros if necessary
            decimal_part = decimal_part.ljust(num_digits, '0')
        return f"{integer_part}.{decimal_part}"
    else:
        # If no decimal point, add one and pad with zeros
        return f"{k_str}.{''.ljust(num_digits, '0')}"

def save_public_keys(name_K1, name_K2, name_K3, name_K4, name_DX, name_DE, filename,
                               K1_str, K2_str, K3_str, K4_str, DX_str, DE_str, display_msg=False):
    """
    Saves extended public keys (4 keys + DX) to a specified file.
    """
    with open(filename, 'w') as file:
        file.write(f'{name_K1} = "{K1_str}"\n')
        file.write(f'{name_K2} = "{K2_str}"\n')
        file.write(f'{name_K3} = "{K3_str}"\n')
        file.write(f'{name_K4} = "{K4_str}"\n')
        file.write(f'{name_DX} = "{DX_str}"\n')
        file.write(f'{name_DE} = "{DE_str}"\n')
    if display_msg:
        print(f"Saved: {filename}")

def load_public_keys(name_K1, name_K2, name_K3, name_K4, name_DX,name_DE,
                              filename, num_digits, display_msg=False):
    """
    Loads extended public keys (4 keys + DX) from a specified file.
    """
    if display_msg:
        print(f"Reading: {filename}")
    if not os.path.exists(filename):
        return "", "", "", "", "", False
    with open(filename, 'r') as file:
        content = file.read()

    K1_match = re.search(f'{name_K1} = "(.*?)"', content)
    K2_match = re.search(f'{name_K2} = "(.*?)"', content)
    K3_match = re.search(f'{name_K3} = "(.*?)"', content)
    K4_match = re.search(f'{name_K4} = "(.*?)"', content)
    DX_match = re.search(f'{name_DX} = "(.*?)"', content)
    DE_match = re.search(f'{name_DE} = "(.*?)"', content)

    if K1_match and K2_match and K3_match and K4_match and DX_match:
        K1_str = limit_k(K1_match.group(1), num_digits)
        K2_str = limit_k(K2_match.group(1), num_digits)
        K3_str = limit_k(K3_match.group(1), num_digits)
        K4_str = limit_k(K4_match.group(1), num_digits)
        DX_str = limit_k(DX_match.group(1), 20)
        DE_str = limit_k(DE_match.group(1), 20)
        return K1_str, K2_str, K3_str, K4_str, DX_str,DE_str, True
    else:
        return "", "", "", "", "", False

#Use this to allow save Private Key in anny directory
#Applied only in example case softare


def corrige_normalized_path(normalized_path):
    marcador = 'KEYPRIV'
    prefixo_novo = 'CGPTCEUKEYS'
    
    idx = normalized_path.find(marcador)
    if idx == -1:
        raise ValueError("A string 'KEYPRIV' não foi encontrada em normalized_path.")
    
    # Reconstrói a nova string mantendo 'KEYPRIV' e tudo após
    normalized_path_new = prefixo_novo + normalized_path[idx:]
    return normalized_path_new

def save_private_keys(pass_word, long_pi, 
                      name_K1, name_K2, name_K3, name_K4, name_DX,name_DE,
                      filename,K1_str, K2_str, K3_str, K4_str, DX_str,DE_str,
                      num_digits, display_msg=False, software_example=True):
    """
    Saves extended private keys (4 keys + DX) to a specified file, encrypted using a password and Pi digits.

    Parameters:
    - pass_word: Password for encryption.
    - long_pi: Long string of Pi digits used as seed for encryption.
    - name_K1..K4: Labels for each key to be stored.
    - name_DX: Label for DX base.
    - filename: Output file name.
    - K1_str..K4_str: Keys in string format.
    - DX_str: DX base string.
    - num_digits: Precision (number of digits).
    - display_msg: Optional message display toggle.
    - software_example: Path normalization toggle (used when testing or running examples).
    """
    
    normalized_path = normalize_protection_path(filename)
    if software_example:
        normalized_path = corrige_normalized_path(normalized_path)

    str_combined = pass_word + name_K1 + name_K2 + name_K3 + name_K4 + name_DX + normalized_path
    original_dps = mp.dps
    mp.dps = num_digits

    N1 = mpf(num_pi_str(str_combined, long_pi, num_digits, 0))
    K1_str_enc = limit_k(str(mpf(K1_str) * N1), num_digits + 10)
    K2_str_enc = limit_k(str(mpf(K2_str) * N1), num_digits + 10)
    K3_str_enc = limit_k(str(mpf(K3_str) * N1), num_digits + 10)
    K4_str_enc = limit_k(str(mpf(K4_str) * N1), num_digits + 10)
    
    save_public_keys(name_K1, name_K2, name_K3, name_K4, name_DX, name_DE,
                     filename,K1_str_enc, K2_str_enc, K3_str_enc, K4_str_enc,
                     DX_str,DE_str,display_msg=display_msg)

    mp.dps = original_dps

def load_private_keys(pass_word, long_pi,name_K1, name_K2, name_K3, 
                      name_K4, name_DX,name_DE,filename, num_digits,
                      display_msg=False, software_example=True):
    """
    Loads private keys from a specified file, decrypting them with a password.

    :param pass_word: Password for decrypting the keys.
    :param long_pi: A long string of digits from Pi used for decryption.
    :param name_K1: Identifier for the first key.
    :param name_K2: Identifier for the second key.
    :param name_K3: Identifier for the third key.
    :param name_K4: Identifier for the fourth key.
    :param name_DX: Identifier for the DX value.
    :param filename: The name of the file containing the encrypted keys.
    :param num_digits: Number of decimal places for precision.
    :param display_msg: If True, prints additional information.
    :param software_example: If True, corrects the normalized path for demo environment.
    :return: Tuple containing K1_str, K2_str, K3_str, K4_str, DX_str, and a boolean indicating success.
    """
    normalized_path = normalize_protection_path(filename)
    if software_example:
        normalized_path = corrige_normalized_path(normalized_path)

    original_dps = mp.dps
    mp.dps = num_digits


    # Load encrypted strings
    K1_str, K2_str, K3_str, K4_str, DX_str,DE_str,read_ok = load_public_keys(
        name_K1, name_K2, name_K3, name_K4, name_DX,name_DE, 
        filename, num_digits + 10, display_msg=display_msg)

    if read_ok:
        str_key = pass_word + name_K1 + name_K2 + name_K3 + name_K4 + name_DX + normalized_path
        N1 = mp.mpf(num_pi_str(str_key, long_pi, num_digits, 0))

        K1_str = limit_k(str(mp.mpf(K1_str) / N1), num_digits)
        K2_str = limit_k(str(mp.mpf(K2_str) / N1), num_digits)
        K3_str = limit_k(str(mp.mpf(K3_str) / N1), num_digits)
        K4_str = limit_k(str(mp.mpf(K4_str) / N1), num_digits)

        mp.dps = original_dps
        return K1_str, K2_str, K3_str, K4_str, DX_str,DE_str, True

    mp.dps = original_dps
    return "", "", "", "", "", False


def ger_num_byte(num):
    return ''.join(f'{n:03}' for n in num)


# Function to convert a string into DIG3 format (each character -> 3 digits)
def conv_str_dig3(s):
    return ''.join(f'{ord(c):03}' for c in s)

# Converts the value to a string and removes the sign, decimal point, and exponent
def get_dig3(num_digits, cutoff, value):
    value_str = str(value)
    if value_str.startswith('-'):
        value_str = value_str[1:]  # Remove negative sign
    value_str = value_str.replace('.', '').split('e')[0]  # Remove decimal point and exponent

    # Remove leading zeros
    value_str = value_str.lstrip('0')

    # Skip the first `cutoff` digits, if necessary
    value_str = value_str[cutoff:]

    # If the digit count is less than needed, repeat until reaching num_digits
    if len(value_str) < num_digits:
        repetitions = (num_digits // len(value_str)) + 1
        value_str *= repetitions

    # Return only the first `num_digits` digits
    return value_str[:num_digits]

# Function to calculate the CRC of a DIG3 long_pi string
def calc_crc_dig3(long_pi_str, lencrc=10):
    num_digits = len(long_pi_str)
    crc_chunks = []

    # Divide long_pi_str into chunks of size lencrc * 3
    for i in range(0, num_digits, lencrc * 3):
        chunk = long_pi_str[i:i + lencrc * 3]
        if len(chunk) < lencrc * 3:
            chunk += "0" * (lencrc * 3 - len(chunk))  # Pad with zeros if needed
        crc_chunks.append(chunk)

    saved_dps = mp.dps
    mp.dps = lencrc * 3 + 30  # Set precision

    total = mpf(0)
    for chunk in crc_chunks:
        total += mpf("0." + chunk)

    crc = str(total)[10:10 + lencrc * 3]

    # Insert dots every 3 digits
    crc_with_dots = '.'.join([crc[i:i+3] for i in range(0, len(crc), 3)])

    mp.dps = saved_dps  # Restore original precision
    return crc_with_dots

# Function: save_pi
# Description: Saves a file containing digits of PI, the digit count (num_digits), and CRC.
def save_pi(filename, num_digits, crc, longpi):
    with open(filename, 'w') as file:
        file.write(f"num_digits = \"{num_digits}\"\n")
        file.write(f"crc  = \"{crc}\"\n")
        file.write(f"pi = \"{longpi}\"\n")
    print(f"File saved: {filename}")

# Function: load_pi
# Description: Loads a file with PI, validates digit count and CRC.
def load_pi(filename, expected_num_digits, lencrc=10):
    if not os.path.exists(filename):
        return "Error: File does not exist.", False

    with open(filename, 'r') as file:
        lines = file.readlines()

    if not (lines[0].startswith("ndig =") and lines[1].startswith("crc  =") and lines[2].startswith("pi =")):
        return "Error: Incorrect file format.", False

    num_digits = int(lines[0].split('"')[1])
    crc = lines[1].split('"')[1]
    long_pi = lines[2].split('"')[1]

    if num_digits != expected_num_digits:
        return f"Error: Wrong num_digits. Expected {expected_num_digits}, found {num_digits}.", False

    calculated_crc = calc_crc_dig3(long_pi, lencrc)
    if crc != calculated_crc:
        return "Error: CRC mismatch.", False

    return long_pi, True

# Function: get_long_pi
# Description: Generates or loads the long PI value, validates with CRC.
def get_long_pi(filepath, num_digits, generate=False):
    filename = filepath + f"/pi{num_digits}.txt"
    long_pi = None
    if (not generate) and os.path.exists(filename):
        long_pi, valid = load_pi(filename, num_digits, lencrc=10)
        if not valid:
            return long_pi, False
        else:
            return long_pi, True
    else:
        if generate:
            print(f"Generating PI with {num_digits} digits, this may take a few minutes.")
            udps = mp.dps
            mp.dps = num_digits + 10
            long_pi = "3" + str(mp.pi)[2:num_digits + 1]
            mp.dps = udps
            crc = calc_crc_dig3(long_pi, lencrc=10)
            save_pi(filename, num_digits, crc, long_pi)
            long_pi1, valid = load_pi(filename, num_digits, lencrc=10)
            if not valid or long_pi1 != long_pi:
                print("ERROR generating PI")
                return "ERROR generating PI", False
            else:
                return long_pi, True
        else:
            if not os.path.exists(filename):
                return f"Error: File {filename} not found", False
    return "Error loading PI", False

def encolhe_chave(key_str, ndig):
    """
    Reduz uma string decimal com muitos dígitos para uma nova string com ndig dígitos,
    pulando de forma uniforme pela cadeia original.
    
    Exemplo: key_str com 250000 dígitos e ndig = 2500 => passo = 100
    """
    key_str = str(key_str).replace('.', '')  # remove o ponto se houver
    len_original = len(key_str)
    passo = (len_original-100) // ndig
    reduzida = ''.join(key_str[i * passo] for i in range(ndig))
    return reduzida

# x.y = 35  x=7 y=5 
# x*y = 937978843229852958454395196768038647708119996215817080944398958038250707
# 113582707983347809856610300809248363340106643785171705008672856057256658249006
# 303816659250276035940142072432533503290715340643720991049554417219296172851893
# 187876675409135877109975306839422832961708480658343497111814009227825302615934
# 8139475517360355840894266447493309584619986206812924842999006904953095601991673
# 59270034227705807777257942989192483507500026253575382687483236342276724808711441393032576445162636301415773729913585526476183106154750550543500397887915345327702159604456635703067706610019201793214017147969716738469733339707056058598922830925312952649427953618367607928799401770860176084753039347911247886123969453298233627503274176462432178205058631210032808102535309052281

# Function: str_pi_4dig3 123.456.765.087
# Description: Derives a DIG3-format string from PI based on a key and pattern.
def str_pi_4dig3(str_pi_key, long_pi, num_digits, blk):
    def validate_key(str_pi_key):
        if str_pi_key[0] == '.' or str_pi_key[-1] == '.':
            return False
        if '..' in str_pi_key:
            return False
        parts = str_pi_key.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 9999:
                return False
        return True

    if not validate_key(str_pi_key):
        return None, False

    inipi, jumppi1, jumppi2, jumppi3 = map(int, str_pi_key.split('.'))
    jumppi2 = 10 * jumppi2
    if jumppi2 == jumppi3:
        jumppi3 *= 2

    result_str = ""
    p = inipi * 1000 + jumppi1 + blk * num_digits
    for _ in range(num_digits // 2):
        result_str += long_pi[p % len(long_pi)]
        p += jumppi2
        result_str += long_pi[p % len(long_pi)]
        p -= jumppi3

    return result_str[:num_digits], True

# Function: str_pi_dig3
# Description: Generates a pseudo-random digit string from a dotted digit string key.
def str_pi_dig3(key_pi_dig3, LongPi, num_digits, blk):
    tam = (len(key_pi_dig3.replace('.', '')) - 1) // 3 + 1
    extended_key = key_pi_dig3 + '.' + key_pi_dig3 + '.' + key_pi_dig3 + '.' + key_pi_dig3
    parts = extended_key.split('.')

    PiKeyJumps = []
    for i in range(tam):
        ch = parts[i * 4].zfill(3) + "." + parts[i * 4 + 1].zfill(3) + "." + parts[i * 4 + 2].zfill(3) + "." + parts[i * 4 + 3].zfill(3)
        if len(PiKeyJumps) < 150:
            PiKeyJumps.append(ch)

    SumPi = mpf("0.0")
    udps = mp.dps
    mp.dps = num_digits + 10
    for key_jump in PiKeyJumps:
        segment, _ = str_pi_4dig3(key_jump, LongPi, num_digits + 200, blk)
        SumPi += mpf("0." + segment)

    result = str(SumPi)[150:num_digits + 150]
    mp.dps = udps
    return result

# Function: str_pi_str
# Description: Converts a string into a pseudo-random digit sequence using PI.
def str_pi_str(key_pi_str, LongPi, num_digits, blk):
    PiKeyJumps = []
    num_dig3 = conv_str_dig3(key_pi_str)
    tam = len(key_pi_str)
    num_dig3 = num_dig3 * 4

    ct = 0
    while ct < tam * 3 and len(PiKeyJumps) < 150:
        ch = num_dig3[ct:ct+3] + '.' + num_dig3[ct+3:ct+6] + '.' + num_dig3[ct+6:ct+9] + '.' + num_dig3[ct+9:ct+12]
        PiKeyJumps.append(ch)
        ct += 12

    SumPi = mpf("0.0")
    udps = mp.dps
    mp.dps = num_digits + 10
    for key_jump in PiKeyJumps:
        segment, _ = str_pi_4dig3(key_jump, LongPi, num_digits + 150, blk)
        SumPi += mpf("0." + segment)

    result = str(SumPi)[100:num_digits + 100]
    mp.dps = udps
    return result

# Function: num_pi_str
# Description: Converts a string into a number based on PI digits.
def num_pi_str(key_pi_str, LongPi, num_digits, blk):
    udps = mp.dps
    mp.dps = num_digits
    str_pi = str_pi_str(key_pi_str, LongPi, num_digits, blk)
    val = mpf("0." + str_pi)
    val_str = str(val)
    mp.dps = udps
    return val_str

# Function: num_pi_dig3
# Description: Converts a dotted digit key into a number based on PI digits.
def num_pi_dig3(key_pi_dig3, LongPi, num_digits, blk):
    udps = mp.dps
    mp.dps = num_digits
    result = mpf("0." + str_pi_dig3(key_pi_dig3, LongPi, num_digits, blk))
    mp.dps = udps
    return result

# Function: str_pi_dig
# Description: Converts a flat digit string into a dotted key, then into a pseudo-random digit sequence using PI.
def str_pi_dig(key_pi_dig, LongPi, num_digits, blk):
    tam = len(key_pi_dig)
    key_pi_dig3 = key_pi_dig[:3]
    key_pi_dig = key_pi_dig * 3
    i = 3
    while i < tam:
        key_pi_dig3 += "." + key_pi_dig[i:i+3]
        i += 3
    return str_pi_dig3(key_pi_dig3, LongPi, num_digits, blk)

# Function: num_pi_dig
# Description: Converts a flat digit string into a number based on PI digits.
def num_pi_dig(key_pi_dig, LongPi, num_digits, blk):
    udps = mp.dps
    mp.dps = num_digits
    result = mpf("0." + str_pi_dig(key_pi_dig, LongPi, num_digits, blk))
    mp.dps = udps
    return result

def get_one_time_kpi(time_str: str, kpriv: str, long_pi: str, num_dig_key: int):
    """
    Generates a unique one-time key (KPI - Key Per Instance) using:
    - A time-based string (time_str)
    - A private base key (kpriv), which is a long secret numeric string
    - A long π (pi) string (long_pi), typically containing millions of digits

    This method ensures that the generated KPI is deterministic and reproducible
    only by someone who has access to the full kpriv.

    Parameters:
    ----------
    time_str : str
        A unique time-related string (e.g., timestamp or session ID)

    kpriv : str
        A long, secret base key from which the KPI will be derived
        (typically 2500 to 7000 digits or more)

    long_pi : str
        A very long string containing digits of pi, used as cryptographic entropy

    num_dig_key : int
        The number of digits for the final one-time KPI key

    Returns:
    -------
    kpi : str
        A numeric string of length `num_dig_key` representing the one-time use key
    """

    # Step 1: Generate a deterministic offset index using time_str and pi
   
    k1str = num_pi_str(time_str, long_pi, 100, 0)
    #print(f"k1str={k1str}")
    k1 =5+int(k1str[3:13]) % (len(kpriv) - 110)  # Ensure safe indexing
    #print(f"k1={k1}")
    
    # Step 2: Extract a seed slice from the private key
    k2str = kpriv[k1 : k1 + 100]
    #print(f"k2str={k2str}")
    
    # Step 3: Generate the final KPI using this seed and pi digits
    kpi = num_pi_str(k2str, long_pi, num_dig_key+100, 0)
    kpi = kpi[5:num_dig_key+5]
    return kpi

