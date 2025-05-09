from mpmath import mp, sqrt, sin, cos,acos,  mpf,fabs
from datetime import datetime, timedelta
import numpy as np
import sys
import re
import os

from ulianovramdompi import (num_pi_str,str_pi_str,get_long_pi,save_private_keys,
                             save_public_keys,load_public_keys,load_private_keys)


sys.set_int_max_str_digits(40000)    

CRC_GOD="6310636865110644549013799157636795217998769163492863332006603677195259622169147260438022342574632533" 

CRC_CRC_GOD=10

# Class representing cryptographic layout parameters based on the number of digits (num_digits)
class CriptoParams:
    def __init__(self, num_digits):
        self.num_digits = num_digits
        self.separator = 10  # General separator between sections
        self.separator_init = 100  # Initial separator for alignment or reserved space

        # Use expanded headers if num_digits > 7000 to allow for larger metadata fields
        if num_digits > 7000:
            self.len_header_num = 500           # Numeric header length
            self.len_header_str_char = 500      # Character header length (number of chars)
        else:
            self.len_header_num = 300
            self.len_header_str_char = 180

        self.len_header_str_dig = 3 * self.len_header_str_char  # Each char = 3 digits in DIG3 format
        self.pos_head_num = self.separator_init + self.len_header_num +  self.separator
        self.pos_head_str = self.separator_init + self.len_header_str_dig + self.len_header_num + 2 * self.separator
        self.pos_data = self.num_digits -  self.separator
        self.len_data_str = int((self.num_digits - self.pos_head_str -3*self.separator)/ 3)
        self.len_data_dig3 = self.len_data_str*3   # Each char = 3 digits in DIG3
        self.ini_data = self.pos_data-self.len_data_dig3
        self.ini_head_num = self.pos_head_num-self.len_header_num
        self.ini_head_str = self.pos_head_str-self.len_header_str_dig
        
    def __str__(self):
        return (f"CriptoParams(num_digits={self.num_digits},ini_head_num={self.ini_head_num},pos_head_num={self.pos_head_num}, "
                f"ini_head_str={self.ini_head_str}, pos_head_str={self.pos_head_str},ini_data={self.ini_data}, pos_data={self.pos_data}, "
                f"len_data_dig3={self.len_data_dig3}, len_data_str={self.len_data_str})")


# Table defining levels, types, and numeric ID ranges
levels = [
    (20000, "GOD", None),
    (9000, "ARC", None),
    (8500, "ANG", None),
    (8000, "DAE", None),
    (7000, "TOP+", (100, 999)),
    (6000,  "TOP",  (1000, 9999)),
    (5000,  "PRIME+",  (100000, 999999)),
    (4000,  "PRIME",   (1000000, 9999999)),
    (3500,  "VIP+",    (10000000, 99999999)),
    (3000,  "VIP",    (100000000, 999999999)),
    (2500,  "POP",    (1000000000, 999999999999)),
]

# Returns the category name based on num_digits (number of digits)
def get_tipo_key(num_digits):
    for limite, nome, _ in levels:
        if num_digits >= limite:
            return nome
    return "UNKNOWN"

# Returns the number of digits based on the prefix of the ID
def get_num_digits(ID):
    prefixo = ID[:3]
    for num_digits, nome, _ in levels:
        if nome.startswith(prefixo):
            return num_digits
    return None  # Unknown prefix

# Returns the numeric range (min, max) of an ID based on its prefix
def get_id_num_range(ID):    
    prefixo = ID[:3]
    for _, nome, faixa in levels:
        if nome.startswith(prefixo):
            return faixa
    return None, None  # Unknown prefix


# Removes all non-alphanumeric characters from a string
def clear_str(string):
    new_str = re.sub(r'[^A-Za-z0-9]', '', string)
    num_char = len(new_str)

    # Prepare bytes for CRC (padding with 0 if odd length)
    bytes_ascii = [ord(c) for c in new_str]
    if len(bytes_ascii) % 2 != 0:
        bytes_ascii.append(0)

    # Calculate 16-bit CRC using XOR of each pair of bytes
    crc = 0
    for i in range(0, len(bytes_ascii), 2):
        pair = (bytes_ascii[i] << 8) | bytes_ascii[i+1]
        crc ^= pair

    return new_str, num_char, crc

def calculate_CRC_ID(id_type, id_number, long_pi):
    """
    Calcula o CRC para um ID de forma inteligente, com exceções específicas.
    """
    numeros = ''.join(re.findall(r'\d', id_number))

    # Se tiver exatamente 3 dígitos (como FUT 123)
    if len(numeros) == 3:
        return numeros

    # Se todos os dígitos forem iguais
    if len(set(numeros)) == 1:
        return numeros[:3]

    # Se o número final for uma sequência crescente exata
    try:
        ultimos3 = numeros[-3:]
        ult = int(ultimos3[-1])
        sequencia = "012345678901234567890123456789"
        idx = sequencia.index(str(ult))
        crc_seq = sequencia[idx+1:idx+4]
        if len(crc_seq) == 3:
            return crc_seq
    except:
        pass

    # CRC padrão via PI
    ID_completo = f"{id_type} {id_number}"
    CRC = str_pi_str(ID_completo, long_pi, 100, 0)
    return CRC[:3]

def calc_crc_key_pub(K1, K2, kID, DX, nd):
    Sum = K1 + K2 + kID + DX
    str_Sum = str(Sum)
    str_Sum = str_Sum[10:]
    bk = (nd - 10) // 120
    CRC = 0
    for i in range(bk):
        if i * 120 + 120 < len(str_Sum):
            Ni = mp.mpf("0.00" + str_Sum[i * 120:i * 120 + 120])
            CRC += Ni
    CRC = str(CRC)
    return CRC[10:110]  # Taking the first 100 characters of CRC

def timecode(time_str):
    # Remove non-numeric characters
    time_code = ''.join(filter(str.isdigit, time_str))
    return time_code

def get_dig3(num_digits, cut, value):
    # Convert value to string and remove sign, decimal point, and exponent
    value_str = str(value)
    if value_str.startswith('-'):
        value_str = value_str[1:]  # Remove negative sign
    value_str = value_str.replace('.', '').split('e')[0]  # Remove decimal point and exponent

    # Remove leading zeros
    value_str = value_str.lstrip('0')

    # Cut the first `cut` digits, if necessary
    value_str = value_str[cut:]

    # If the number of digits is less than required, repeat until reaching num_digits
    if len(value_str) < num_digits:
        repetitions = (num_digits // len(value_str)) + 1
        value_str *= repetitions

    # Return only the required num_digits digits
    return value_str[:num_digits]

def validate_id(ID, long_pi, msg=False):
    parts = ID.strip().split()
    if len(parts) != 2:
        if msg: print(f"[ERROR] Invalid format (expected: 'TYPE NUMBER[-CRC]'): '{ID}'")
        return False, f"Invalid format: '{ID}'"

    type_, remainder = parts
    type_ = type_.strip()

    # Check if the type is defined in the levels table
    level_info = next((level for level in levels if level[1] == type_), None)
    if level_info is None:
        if msg: print(f"[ERROR] Unknown type: '{type_}'")
        return False, f"Unknown type: '{type_}'"

    range_min, range_max = level_info[2] if level_info[2] else (None, None)

    # Check if there is exactly one hyphen separating number and CRC
    split_crc = remainder.split('-')
    if len(split_crc) != 2:
        if msg: print(f"[ERROR] Incorrect format (expected: number-CRC): '{remainder}'")
        return False, f"Incorrect format in field '{remainder}'"

    number, crc = split_crc
    pure_num = number.replace('.', '').replace(',', '')

    if not pure_num.isdigit():
        if msg: print(f"[ERROR] Invalid number in ID: {number}")
        return False, f"Invalid number: '{number}'"

    numeric_value = int(pure_num)

    # Check if the number is within the expected range
    if range_min is not None and range_max is not None:
        if not (range_min <= numeric_value <= range_max):
            if msg: print(f"[ERROR] Number out of range for type '{type_}': {numeric_value}")
            return False, f"Number {numeric_value} out of range for '{type_}'"

    # CRC validation
    expected_crc = calculate_CRC_ID(f"{type_}",f"{number}", long_pi)
   
    if crc != expected_crc:
        if msg: print(f"[ERROR] Invalid CRC. Expected: {expected_crc}, found: {crc}")
        return False, f"Incorrect CRC. Expected: {expected_crc}, found: {crc}"

    return True, "Valid ID"

def convert_str_to_dig3(val_str):
    """
    Converts a string into a sequence of 3-digit ASCII values.

    Parameters:
    - s (str): Input string to be converted.

    Returns:
    - str: String representation of ASCII values, each padded to 3 digits.
    """
    val_dig3 =''.join(f'{ord(c):03}' for c in val_str)
    return val_dig3

def convert_dig3_to_str(val_dig3):
    """
    Converts a sequence of 3-digit ASCII values back into a string.

    Parameters:
    - val_dig3(str): String containing concatenated 3-digit ASCII values.

    Returns:
    - tuple: (Decoded string, success flag, number of bytes processed)
    """
    
    chars = [val_dig3[i:i+3] for i in range(0, len(val_dig3), 3)]
    result = ""
    nbytes = 0
    for c in chars:
        try:
            val = int(c)
            if 0 <= val <= 255:
                if val!=0:
                   result += chr(val)
                nbytes += 1
            else:
                break  # Value out of ASCII range
        except ValueError:
            break  # Conversion error, stop processing
    return result, True, nbytes

# Reexecutando após reset do ambiente

def conv_str_to_compac_dig3(val_str):
    def ascii3(c): return f'{ord(c):03}'

    val_dig3_compac = ""
    i = 0
    special_blocks = 0

    while i < len(val_str):
        if val_str[i].isdigit():
            # Início de uma sequência de dígitos
            while i < len(val_str) and val_str[i].isdigit():
                start = i
                count = 0
                segment = ""
                # Pega até 999 dígitos
                while i < len(val_str) and val_str[i].isdigit() and count < 999:
                    segment += val_str[i]
                    i += 1
                    count += 1

                if count < 10:
                    for c in segment:
                        val_dig3_compac += ascii3(c)
                else:
                    special_blocks += 1
                    val_dig3_compac += "688"
                    val_dig3_compac += f'{count:03}'
                    val_dig3_compac += segment
                    resto = count % 3
                    if resto == 1:
                        val_dig3_compac += "00"
                    elif resto == 2:
                        val_dig3_compac += "0"
                    val_dig3_compac += "528"
        else:
            val_dig3_compac += ascii3(val_str[i])
            i += 1

    return val_dig3_compac


def conv_compac_dig3_to_str(seq_dig3):
    i = 0
    texto = ""

    def bloco(i): return seq_dig3[i:i+3]

    while i < len(seq_dig3):
        bloco_atual = bloco(i)
        i += 3

        if not bloco_atual.isdigit():
            return False, f"[ERRO] Bloco inválido: {bloco_atual}"

        cod = int(bloco_atual)

        if cod == 688:
            tam_digitos = int(bloco(i))
            i += 3
            digitos = ""
            blocos_necessarios = (tam_digitos + 2) // 3
            total_ler = blocos_necessarios * 3
            while len(digitos) < total_ler and i < len(seq_dig3):
                digitos += bloco(i)
                i += 3
            digitos = digitos[:tam_digitos]
            texto += digitos
            if i >= len(seq_dig3):
                return False, "[ERRO] Esperado separador final (528) após bloco 688, mas fim alcançado"
            fim_bloco = int(bloco(i))
            i += 3
            if fim_bloco != 528:
                return False, f"[ERRO] Separador final 528 esperado, encontrado: {fim_bloco}"
        elif 0 <= cod <= 255:
            texto += chr(cod)
        else:
            return False, f"[ERRO] Código não reconhecido: {cod}"

    if not texto:
        return False, ""

    return True, texto


def conv_compac_dig3_to_str(seq_dig3):
    i = 0
    texto = ""

    def bloco(i): return seq_dig3[i:i+3]

    while i < len(seq_dig3):
        bloco_atual = bloco(i)
        i += 3

        if not bloco_atual.isdigit():
            return False, f"[ERRO] Bloco inválido: {bloco_atual}"

        cod = int(bloco_atual)

        if cod == 688:
            # Bloco especial
            tam_digitos = int(bloco(i))
            i += 3
            digitos = ""

            blocos_necessarios = (tam_digitos + 2) // 3
            total_ler = blocos_necessarios * 3

            while len(digitos) < total_ler and i < len(seq_dig3):
                digitos += bloco(i)
                i += 3

            digitos = digitos[:tam_digitos]
            texto += digitos

            if i >= len(seq_dig3):
                return False, "[ERRO] Esperado separador final (528) após bloco 688, mas fim alcançado"

            fim_bloco = int(bloco(i))
            i += 3

            if fim_bloco != 528:
                return False, f"[ERRO pos{i}] Separador final 528 esperado, encontrado: {fim_bloco}"
        elif 0 <= cod <= 255:
            texto += chr(cod)
        else:
            return False, f"[ERRO] Código não reconhecido: {cod}"

    if not texto:
        return False, ""

    return True, texto



def conv_str_to_dig3_bit4(val_str):
    """
    Converte uma string de dígitos em formato dig3 (grupos de 3 dígitos) para bytes compactados em grupos de 6 dígitos.
    Retorna o cabeçalho e os dados codificados em bytes.
    """
    # Filtra apenas dígitos
    digitos = ''.join(filter(str.isdigit, val_str))

    # Agrupa em sextuplas de 6 dígitos
    grupos = []
    i = 0
    while i < len(digitos):
        grupo = digitos[i:i+6]
        if len(grupo) < 6:
            grupo += "528"  # Fim de bloco
            grupo = grupo.ljust(6, "0")
        grupos.append(grupo)
        i += 6

    # Converte sextuplas para bytes
    bytes_compactados = bytearray()
    for g in grupos:
        for j in range(0, 6, 2):
            a = int(g[j:j+2])
            bytes_compactados.append(a)

    # Calcula CRC de 16 bits
    crc = 0
    for i in range(0, len(bytes_compactados), 2):
        pair = (bytes_compactados[i] << 8)
        if i + 1 < len(bytes_compactados):
            pair |= bytes_compactados[i + 1]
        crc ^= pair
    crc_hex = f"{crc:04X}"

    header = f'TYPE="Dig3_bit4",DATA_LEN="{len(bytes_compactados)}",DATA_CRC="{crc_hex}",DATA='
    final  = ']'
    return header.encode('utf-8') + bytes_compactados+final.encode('utf-8')

def conv_dig3_bit4_to_str(file_path):
    """
    Lê um arquivo codificado no formato Dig3_bit4 e reconstrói a string de dígitos.
    
    Valida:
    - Cabeçalho com TYPE, DATA_LEN e DATA_CRC
    - Finalização correta com ']' (byte final)
    - Tamanho real dos dados conforme DATA_LEN
    - CRC (XOR 16-bit) dos dados
    
    Retorna:
    - (True, string) se sucesso
    - (False, msg_erro) se falha
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        return False, f"[ERRO] Falha ao abrir o arquivo: {str(e)}"

    header_end = content.find(b'DATA=')
    if header_end == -1:
        return False, "[ERRO] Cabeçalho malformado (DATA= não encontrado)."

    header_text = content[:header_end].decode('utf-8')
    data_bytes = content[header_end + 5:]

    if not header_text.startswith('TYPE="Dig3_bit4"'):
        return False, "[ERRO] Tipo inválido no cabeçalho."

    try:
        len_part = header_text.split('DATA_LEN="')[1].split('"')[0]
        crc_part = header_text.split('DATA_CRC="')[1].split('"')[0]
        expected_len = int(len_part)
        expected_crc = int(crc_part, 16)
    except Exception:
        return False, "[ERRO] Campos DATA_LEN ou DATA_CRC inválidos."

    if len(data_bytes) < expected_len + 1:
        return False, f"[ERRO] Arquivo incompleto. Esperado {expected_len+1} bytes, encontrado {len(data_bytes)}."

    if data_bytes[-1] != ord("]"):
        return False, "[ERRO] Arquivo não termina com byte ']' (93)."

    dados_puros = data_bytes[:expected_len]

    # Valida CRC
    crc = 0
    for i in range(0, len(dados_puros), 2):
        pair = dados_puros[i] << 8
        if i + 1 < len(dados_puros):
            pair |= dados_puros[i + 1]
        crc ^= pair

    if crc != expected_crc:
        return False, f"[ERRO] CRC inválido. Esperado {expected_crc:04X}, calculado {crc:04X}"

    # Reconstrói string de dígitos a partir dos bytes (grupos de 3)
    digitos = ""
    for i in range(0, expected_len, 3):
        a = dados_puros[i] if i < expected_len else 0
        b = dados_puros[i + 1] if i + 1 < expected_len else 0
        c = dados_puros[i + 2] if i + 2 < expected_len else 0
        digitos += f"{a:02}{b:02}{c:02}"

    # Remove 528 final, se presente
    if digitos.endswith("528"):
        digitos = digitos[:-3]

    return True, digitos


def conv_file_dig3_str(folder, filename):
    """
    Reads a file and converts its content into a sequence of 3-digit ASCII values.

    Parameters:
    - folder (str): Folder path where the file is located.
    - filename (str): Name of the file to be processed.

    Returns:
    - tuple: (Converted ASCII string, original content length, converted content length)
    """
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return  False,f"[ERROR] File not found: {path}"

    with open(path, 'r') as f:
        content = f.read()

    ok, val_str = conv_compac_dig3_to_str(content)
    if ok:
       return  True , val_str
    return  False,f"erro na conversao {val_str}"

def conv_file_str_dig3(directory, filename):
    """
    Reads an encoded file, decodes its content using the 'dig3' encoding scheme, and returns the decoded text.

    Parameters:
    - directory (str): The directory where the file is located.
    - filename (str): The name of the file to be decoded.

    Returns:
    - tuple: A tuple containing:
        - decoded_content (str): The decoded content of the file.
        - total_bytes (int): The total number of bytes processed.
        - original_length (int): The original length of the encoded content.
    """
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return "", 0, 0

    with open(filepath, 'r') as f:
        content = f.read()

    coded_content = conv_str_to_compac_dig3(content)
    print(f"[OK] File successfully decoded: {len(coded_content)} bytes")
    return coded_content, len(coded_content), len(content)


#Simple crypt rotine used only to teste Kpub1, Kpub2 keys
def tst_F1_crypts(Alpha, Kpub1, Kpub2, K_ID):
    Alpha_rad = mp.radians(Alpha)
    DX = K_ID - sqrt(Kpub1 + cos(Alpha_rad)**2 + Kpub2 * cos(Alpha_rad))
    return DX

#Simple decrypt rotine used only to teste Kpriv_alpha key
def tst_F2_decrypts(DX, Kpriv_alpha, K_ID):
    cos_Alpha = DX + Kpriv_alpha - K_ID
    Alpha = mp.degrees(acos(cos_Alpha))
    return Alpha



def F1_3keys_crypts(de_crip, Kpub1, Kpub2, Kpub3, DX_base, K_ID):
    """
    Encrypts an angle Alpha into a DX value using elliptic public key parameters.

    Args:
        Alpha (mpf): The input angle in degrees to be encrypted.
        Kpub1 (mpf): Public key coefficient 1.
        Kpub2 (mpf): Public key coefficient 2.
        Kpub3 (mpf): Precomputed constant (Ue - 1)/R0 ÷ [Ue - (1/(2 - Ue))].
        DX_base (mpf): Base DX value.
        K_ID (mpf): Identifier constant.

    Returns:
        mpf: Encrypted value DX (used in the elliptic encryption process).
    """
    Alpha = mp.acos(de_crip * Kpub3 ) 
    DX = K_ID - DX_base - mp.sqrt(Kpub1 + mp.cos(Alpha)**2 + Kpub2 * mp.cos(Alpha))
    return DX


def F2_4keys_decrypts(DX, Kpriv_alpha, Kpriv_x, Kpriv_y, Kpriv_de, DX_base, K_ID):
    """
    Decrypts the encrypted elliptic DX value into an angle Alpha using the private key components.

    Args:
        DX (mpf): Encrypted DX value.
        Kpriv_alpha (mpf): Private key component for angle shift.
        Kpriv_x (mpf): Private key component for x (ellipse parameter a).
        Kpriv_y (mpf): Private key component for y (ellipse parameter b).
        DX_base (mpf): Base DX offset.
        Alpha_base (mpf): Base angle in degrees.
        K_ID (mpf): Identifier key.

    Returns:
        Alpha (mpf): Decrypted angle in degrees.
    """
    cos_Alpha = DX + DX_base + Kpriv_alpha - K_ID
    Alpha = mp.acos(cos_Alpha)
    x_data = Kpriv_x * (mp.cos(Alpha) - 1) + Kpriv_x - mp.sqrt(Kpriv_x**2 - Kpriv_y**2)
    y_data = Kpriv_y * mp.sin(Alpha)
    de_crip = mp.sqrt(x_data**2 + y_data**2)+Kpriv_de
    return de_crip



def F2_4keys_crypts(DX,  Kpriv_alpha,  Kpriv_x,  Kpriv_y,Kpriv_de, K_ID):
    """
    Encrypts a DX value using a complex non-invertible private key scheme.

    Args:
        DX (mpf): Value to encrypt.
         Kpriv_alpha (mpf): Private key component for angle.
         Kpriv_x (mpf): Private key component for x.
         Kpriv_y (mpf): Private key component for y.
        Alpha_base (mpf): Base angle in degrees.
        K_ID (mpf): Identifier key.

    Returns:
        mpf: Encrypted elliptic distance (de_crip).
    """
    Alpha = mp.acos(DX + Kpriv_alpha)
    x_data =  Kpriv_x * (mp.cos(Alpha) - 1) +  Kpriv_x - mp.sqrt(Kpriv_x**2 - Kpriv_y**2)
    y_data =  Kpriv_y * mp.sin(Alpha)
    de_crip = mp.sqrt(x_data**2 + y_data**2)+Kpriv_de+K_ID
    return de_crip


def F1_3keys_decrypts(de_crip, Kpub1, Kpub2, Kpub3, K_ID):
    """
    Decrypts a DX value using non-invertible elliptic decoding with public keys.

    Args:
        de_crip (mpf): Encrypted value (distance).
        Kpub1 (mpf): Public key coefficient 1.
        Kpub2 (mpf): Public key coefficient 2.
        Kpub3 (mpf): Precomputed = (Ue - 1)/R0 ÷ [Ue - (1/(2 - Ue))].
        Alpha_base (mpf): Base angle in degrees.
        K_ID (mpf): Identifier key.

    Returns:
        mpf: Decrypted DX value.
    """
    Alpha = mp.acos((de_crip-K_ID) * Kpub3)
    DX = -mp.sqrt(Kpub1 + mp.cos(Alpha)**2 + Kpub2 * mp.cos(Alpha))
    return DX
   

def encrypt_with_private_key(
    Dad_Num_str, Head_NUM_str, Head_str,
    Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str,Kpriv_de_str,
    DX_base_str, Alpha_base_str, K_ID_str,
    params, MSG=False):
    """
    Encrypts data using an extended private key scheme (3 components).

    Parameters:
    - Dad_Num_str (str): Numeric data to be encrypted.
    - Head_NUM_str (str): Numeric header value.
    - Head_str (str): String header.
    - Kpriv_alpha_str (str): Private key component (for DX).
    - Kpriv_x_str (str): Private key component (elliptic param x).
    - Kpriv_y_str (str): Private key component (elliptic param y).
    - DX_base_str (str): DX base.
    - Alpha_base_str (str): Base alpha.
    - K_ID_str (str): Key identifier.
    - params (CriptoParams): Cryptographic parameters and positions.
    - MSG (bool): Enable debug output.

    Returns:
    - str: Encrypted elliptic value as string (de_crip).
    """
    # Setup precision
    original_dps = mp.dps
    mp.dps = params.num_digits

    # Convert inputs to mpf
    Kpriv_alpha = mpf(Kpriv_alpha_str)
    Kpriv_x = mpf(Kpriv_x_str)
    Kpriv_y = mpf(Kpriv_y_str)
    Kpriv_de = mpf(Kpriv_de_str)
    DX_base = mpf(DX_base_str)
    Alpha_base = mpf(Alpha_base_str)
    K_ID = mpf(K_ID_str)

    # Process and scale input data
    Dad_Num = mpf(Dad_Num_str[:params.len_data_dig3] + ".000005")
    Head_NUM = mpf(Head_NUM_str[:params.len_header_num])
    Head_str = Head_str[:params.len_header_str_char]
    Num_Head_str = convert_str_to_dig3(Head_str)[:params.len_header_str_dig]

    Head_NUM_E10 = Head_NUM * mpf(f'1E-{params.pos_head_num}')
    Num_Head_str_E10 = mpf(Num_Head_str) * mpf(f'1E-{params.pos_head_str}')
    Dad_Num_E10 = Dad_Num * mpf(f'1E-{params.pos_data}')

    DX_data = Head_NUM_E10 + Num_Head_str_E10 + Dad_Num_E10
    DX = DX_base - DX_data
    

    if MSG:
        print(f"DX_data = {str(DX_data)[:60]}")

    # Encrypt using the updated F2 function
 
    de_Crip = F2_4keys_crypts(DX, Kpriv_alpha, Kpriv_x, Kpriv_y,Kpriv_de,K_ID)
 
   
    str_de_Crip =str(de_Crip)
    # Restore original precision
    mp.dps = original_dps
    return str_de_Crip


def decrypt_with_public_key(de_crip_str, Kpub1_str, Kpub2_str, Kpub3_str,
                            DX_base_str, Alpha_base_str, K_ID_str, params, MSG=False):
    """
    Decrypts elliptically encrypted data using public keys.

    Parameters:
    - de_crip_str (str): Encrypted elliptic value.
    - Kpub1_str to Kpub3_str (str): Public key parameters.
    - DX_base_str (str): DX base value.
    - Alpha_base_str (str): Alpha base value.
    - K_ID_str (str): Key ID.
    - params (CriptoParams): Cryptographic parameters.
    - MSG (bool): Enable debug output.

    Returns:
    - tuple:
        - str: Full decoded DX value string.
        - str: Recovered data in DIG3.
        - str: Recovered numeric header.
        - str: Recovered string header.
    """
    original_dps = mp.dps
    mp.dps = params.num_digits

    # Convert inputs
    de_crip = mpf(de_crip_str)
    Kpub1 = mpf(Kpub1_str)
    Kpub2 = mpf(Kpub2_str)
    Kpub3 = mpf(Kpub3_str)
    DX_base = mpf(DX_base_str)
    Alpha_base = mpf(Alpha_base_str)
    K_ID = mpf(K_ID_str)

    # Decrypt DX
    Decod_X = fabs( F1_3keys_decrypts(de_crip, Kpub1, Kpub2, Kpub3,  K_ID) - DX_base)
    decod_7keys_str = str(Decod_X) + "000000000000"

    if MSG:
        print(f"\nRecovered DX = {Decod_X}")

    if len(decod_7keys_str) < params.pos_data:
        mp.dps = original_dps
        return str(Decod_X), "0", "0", "ERROR in Head_str"

    # Extract positions
    deshead_num = params.pos_head_num + 2 - params.len_header_num
    delodata = params.pos_data + 2 - params.len_data_dig3
    deslhead_str = params.pos_head_str + 2 - params.len_header_str_dig

    # Extract DIG3 data
    data_rec_dig3 = decod_7keys_str[delodata:]
    ud1_V0 = decod_7keys_str[delodata + params.len_data_dig3:delodata + params.len_data_dig3 + 1]
    ud = decod_7keys_str[delodata + params.len_data_dig3 - 1:delodata + params.len_data_dig3]

    if ud1_V0 == "9":
        ud1 = chr(ord(ud) + 1)
        ud = ud1

    data_rec_dig3 = (data_rec_dig3 + ud)[:params.len_data_dig3]

    # Reconstruct headers
    Head_num_str = decod_7keys_str[deshead_num:deshead_num + params.len_header_num]
    Num_Head_str = decod_7keys_str[deslhead_str:deslhead_str + params.len_header_str_dig]
    Head_str_rec, _, _ = convert_dig3_to_str(Num_Head_str)

    Head_num_val = mpf(Head_num_str) if len(Head_num_str) > 10 else 0

    mp.dps = original_dps
    return decod_7keys_str, data_rec_dig3, Head_num_val, Head_str_rec

def encrypt_with_public_key(Dad_Num_str, Head_NUM_str, Head_str,
                            DX_base_str, De_base_str,
                            Kpub1_str, Kpub2_str, Kpub3_str, 
                            K_ID_str, params: CriptoParams, MSG=False):
    """
    Encrypts data using updated public key method with 4 Kpub components.

    Parameters:
    - Dad_Num_str (str): Data to encrypt.
    - Head_NUM_str (str): Header number.
    - Head_str (str): Header string.
    - DX_base_str (str): Base DX value.
    - De_base_str (str): Base de value.
    - Kpub1_str to Kpub3_str (str): Public key parameters.
    - K_ID_str (str): Key ID.
    - params (CriptoParams): Crypto configuration.
    - MSG (bool): Debug output flag.

    Returns:
    - str: Encrypted DX string.
    """
    original_precision = mp.dps
    mp.dps = params.num_digits

    # Parse inputs
    Dad_Num = mpf(Dad_Num_str[:params.len_data_dig3] + ".000005")
    Head_NUM = mpf(Head_NUM_str[:params.len_header_num])
    Head_str = Head_str[:params.len_header_str_char]
    Num_Head_str = convert_str_to_dig3(Head_str)[:params.len_header_str_dig]

    Kpub1 = mpf(Kpub1_str)
    Kpub2 = mpf(Kpub2_str)
    Kpub3 = mpf(Kpub3_str)
    DX_base = mpf(DX_base_str)
    De_base = mpf(De_base_str)
    K_ID = mpf(K_ID_str)

    # Compute components
    Head_NUM_E10 = Head_NUM * mpf(f'1E-{params.pos_head_num}')
    Num_Head_str_E10 = mpf(Num_Head_str) * mpf(f'1E-{params.pos_head_str}')
    Dad_Num_E10 = Dad_Num * mpf(f'1E-{params.pos_data}')

    # De_base
    de_data = De_base + Head_NUM_E10 + Num_Head_str_E10 + Dad_Num_E10
    if MSG:
        print(f"de_data to encrypt = {de_data}")

    # Encrypt using public keys
    DX_crip = F1_3keys_crypts(de_data, Kpub1, Kpub2, Kpub3, DX_base, K_ID)
    mp.dps = original_precision
    return str(DX_crip)

def decrypt_with_private_key(data_7keys_Crip_str,  Kpriv_alpha_str,  Kpriv_x_str,  Kpriv_y_str,DX_de_str,
                              DX_base_str, Alpha_base_str, K_ID_str, params, MSG=False):
    """
    Decrypts data using extended private key (3 components).

    Parameters:
    - data_7keys_Crip_str (str): Encrypted DX value.
    -  Kpriv_alpha_str (str): Private key component alpha.
    -  Kpriv_x_str (str): Private key component x.
    -  Kpriv_y_str (str): Private key component y.
    - DX_base_str (str): Base DX.
    - Alpha_base_str (str): Base Alpha.
    - K_ID_str (str): Identifier.
    - params (CriptoParams): Parameters.
    - MSG (bool): Debug flag.

    Returns:
    - decod_Alpha_str (str)
    - data_rec_dig3 (str)
    - Head_num_str_rec (mpf)
    - Head_str_rec (str)
    """
    original_precision = mp.dps
    mp.dps = params.num_digits

    # Convert inputs
    DX = mpf(data_7keys_Crip_str)
    Kpriv_alpha = mpf( Kpriv_alpha_str)
    Kpriv_x = mpf( Kpriv_x_str)
    Kpriv_y = mpf( Kpriv_y_str)
    DX_base = mpf(DX_base_str)
    Kpriv_de = mpf(DX_de_str)
    K_ID = mpf(K_ID_str)

    # Recover Alpha
    Alpha_rec = F2_4keys_decrypts(DX,  Kpriv_alpha,  Kpriv_x,  Kpriv_y,Kpriv_de, DX_base, K_ID)
    decod_Alpha_str = str(Alpha_rec) + "000000000000"

    if len(decod_Alpha_str) < params.pos_data:
        mp.dps = original_precision
        return str(Alpha_rec), "0", "0", "ERROR in Head_str"

    if MSG:
        print(f"\nRecovered Alpha = {Alpha_rec}")

    # Extract fields
    deshead_num = params.pos_head_num + 2 - params.len_header_num
    delodata = params.pos_data + 2 - params.len_data_dig3
    deslhead_str = params.pos_head_str + 2 - params.len_header_str_dig

    data_rec_dig3 = decod_Alpha_str[delodata:]
    ud1_V0 = decod_Alpha_str[delodata + params.len_data_dig3: delodata + params.len_data_dig3 + 1]
    ud = decod_Alpha_str[delodata + params.len_data_dig3 - 1: delodata + params.len_data_dig3]

    if ud1_V0 == "9":
        ud1 = chr(ord(ud) + 1)
        ud = ud1
    data_rec_dig3 += ud
    data_rec_dig3 = data_rec_dig3[:params.len_data_dig3]

    Head_num_str_rec_str = decod_Alpha_str[deshead_num: deshead_num + params.len_header_num]
    Num_Head_str = decod_Alpha_str[deslhead_str: deslhead_str + params.len_header_str_dig]
    Head_str_rec, OK, Nbrec = convert_dig3_to_str(Num_Head_str)

    if len(Head_num_str_rec_str) > 10:
        Head_num_str_rec = mpf(Head_num_str_rec_str)
    else:
        Head_num_str_rec = 0

    mp.dps = original_precision
    return decod_Alpha_str, data_rec_dig3, Head_num_str_rec, Head_str_rec


def calculate_pub_priv_keys(Ke_str, R0_str, K_ID_str, num_digits):
    """
    ESTA ROTINA ESTA ERRADA DE PROPÓSITO
    SE TENTAREM USAR ISSO NAO VAI FUNCIONAR...
    ENTRETANTO A COMPLEXXIDADE COMPUTACIONAL 
    É QUASE IGUAL A ROTINA VERDADEIRA
    A ROTINA VERDADEIRA HOJE EXISTE APENAS
    NA MENTE DO DR. ULIANOV E SERÁ LIBERADA EM FASE POSTERIOR (EM 2026 OU 2027)
    OU SERA LIBERADA EM 07/12/2030 QUE SE O DR. ULIANOV ESTIVER VIVO
    NESTA DATA SERÁ O 64 ANIVERSARIO DELE. SE ELE ESTIVER MORTO ISSO VAI
    SER DIVULGADO IGUAL NO GITHUB, FORUM FISICA 2100 E VARIOS OUTROS FORUNS
    DE CRIPTOGRAFIA QUE EXISTEM NO MUNDO...
    EM 07/12/2030 ESTA ROTINA VERDADEIRA TAMBEM SERA ENVIADA POR EMIL PARA VARIOS
    ESPECIALISTAS EM CRIPTOGRAFI A JORNLISTAS ESPALHADOS PELO MUNDO. 
    """

    # Salva a precisão original e define a nova
    original_dps = mp.dps
    mp.dps = num_digits

    # Conversões iniciais
    Ke = mpf(Ke_str)
    K_ID = mpf(K_ID_str)
    R0 = mpf(R0_str)
    
    # Chave pública original (Kpub2, Kpub1)
    K_ID_Pub_denominator = Ke**2(1 - (1 / (Ke * (1 / Ke - 2))))
    KX = K_ID / K_ID_Pub_denominator
    K3_Pub_denominator = 2 - (Ke**2 / (Ke * (1 / Ke - 2)))
    K1 = K3_Pub_denominator * KX**2
    K0 = K1 / ((mpf(1) / Ke**2) - 2)**2
    K2 = K1 / sqrt(Ke**2 * ((mpf(1) / Ke**2) - 2))
    K3 = (Ke - 2) * KX**2
  
    Kpub2 = (2*K0 + K1) / (2*K2 - K0*K1)
    Kpub1 = ( K1 * K2**2) / (2*K2 - K0*K1)
    Kpriv_alpha = K3 / K_ID

    # Cálculo de Kpub3 e Kpub3 para a parte elíptica
    KK1 = (mpf("2") / (mpf("1") - Ke)) - mpf("2")
    KK2 = Ke - (mpf("2") / (mpf("1") - Ke))
    KK3 = (Ke - 2) / R0
    Kpub3 = KK3 / KK2
    kp4 = KK1/KK2
    Kpriv_de = - kp4 /KK3
     
    # Parâmetros elípticos a e b
    Kpriv_x = R0 / (mpf("1") - Ke)**2
    Kpriv_y = R0 / ((mpf("1") / Ke) - mpf("2"))
   
    # Restaura a precisão original
    mp.dps = original_dps
    print("This function cannot be used because the formulas for generating private keys have been modified for security and copyright reasons.")
    exit(0)
 
    return  str(Kpub3),str(Kpub2),str(Kpub1),str(Kpriv_alpha),str(Kpriv_de),str(Kpriv_y),str(Kpriv_x)


def test_keys(
    Kpub1_str, Kpub2_str, Kpub3_str,
    Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str,Kpriv_de_str,
    alpha_base_str, K_ID_str,
    num_digits
):
    """
    Testa se o par de chaves públicas e privadas criptografa e decriptografa corretamente.

    Parâmetros:
    - Kpub1_str a Kpub3_str: componentes da chave pública (como string)
    - Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str: componentes da chave privada (como string)
    - alpha_base_str: ângulo base em graus (como string)
    - DX_base_str: valor base DX usado na criptografia (como string)
    - K_ID_str: identificador da chave (como string)
    - num_digits: precisão numérica

    Retorna:
    - (True, DX_base calculado) se a criptografia e decriptografia forem compatíveis
    - (False, None) caso contrário
    """
    # Salva precisão atual e ajusta
    original_dps = mp.dps
    mp.dps = num_digits

    # Conversão de strings para mpf
    Kpub1 = mpf(Kpub1_str)
    Kpub2 = mpf(Kpub2_str)
    Kpub3 = mpf(Kpub3_str)
    Kpriv_alpha = mpf(Kpriv_alpha_str)
    Kpriv_x = mpf(Kpriv_x_str)
    Kpriv_y = mpf(Kpriv_y_str)
    Kpriv_de = mpf(Kpriv_de_str)
    Alpha_base = mpf(alpha_base_str)
    K_ID = mpf(K_ID_str)

    # Etapa de criptografia com F1
    #print("TESTE DE Kpub1, Kpub2,Kpriv_alpha ")
    #print(f"alpha ={str(Alpha_base)[:80]}")
    DX_X = tst_F1_crypts(Alpha_base,Kpub1, Kpub2,K_ID)
    #print(f"DX_X ={str(DX_X)[:80]}")
    Alpha_X= tst_F2_decrypts(DX_X, Kpriv_alpha,K_ID)
    #print(f"Alpha_X ={str(Alpha_X)[:80]}")
    erro= fabs(Alpha_base-Alpha_X)
    #print(f"erro={str(erro+1)[:60]}")
    if erro>mpf("1e-2400"): 
        #print("Erro testando Kpub1, Kpub2,Kpriv_alpha")
        mp.dps = original_dps
        return False,None,None
    #print("TESTE DE TODAS AS CHAVES ")
    x_data = Kpriv_x * (cos(mp.radians(Alpha_base)) - 1) + 1
    y_data = Kpriv_y * sin(mp.radians(Alpha_base))
    #print(f"x_data={str(x_data)[:60]}")
    #print(f"y_data={str(y_data)[:60]}")
    De_base = sqrt(x_data**2 + y_data**2)
    #print(f"De_base={str(De_base)[:60]}")
    DX_crip = F1_3keys_crypts(De_base, Kpub1, Kpub2, Kpub3, mpf("1.0"), K_ID)
    #print(f"DX_crip={str(DX_crip)[:60]}")
    # Etapa de decriptografia com F2
    de_rec = F2_4keys_decrypts(DX_crip, Kpriv_alpha, Kpriv_x, Kpriv_y,Kpriv_de,mpf("1.0"), K_ID)
    #print(f"de_rec={str(de_rec)[:60]}")
   
    # Verifica erro absoluto
    erro = fabs(de_rec - De_base)
    #print(f"erro={str(erro+1)[:60]}")
    
    if erro > mpf("1e-2400"):
        #print("Erro testando TODAS AS CHAVES")
        mp.dps = original_dps
        return False, None,None
    #print("TESTE DE F2_4keys_crypts e F1_3keys_decrypts ")
    DX_base=DX_X
    #print(f"DX_base={str(DX_base)[:60]}")
    de_crip = F2_4keys_crypts(DX_base, Kpriv_alpha, Kpriv_x, Kpriv_y,Kpriv_de, K_ID)
    #print(f"de_crip={str(de_crip)[:60]}")
   
    Decod_DX = F1_3keys_decrypts(de_crip, Kpub1, Kpub2, Kpub3,  K_ID)
    #print(f"Decod_DX={str(Decod_DX)[:60]}")
    #Verifica erro absoluto
    erro = fabs(Decod_DX - DX_base)
    #print(f"erro={str(erro+1)[:60]}")
    if erro > mpf("1e-2400"):
        #print("Erro testando F2_4keys_crypts e F1_3keys_decrypts")
        mp.dps = original_dps
        return False, None,None
    dx_base_str = str(DX_base)[:20]
    De_base_str = str(De_base)[:20]
    mp.dps = original_dps

    return True, dx_base_str,De_base_str

def get_k_id(user_id, long_pi):
    """
    Generates the K_ID based on the provided user ID.

    Parameters:
    - user_id (str): The user identifier.
    - long_pi (str): The long Pi value for key generation.

    Returns:
    - str: The generated K_ID.
    """
    num_digits = get_num_digits(user_id)
    original_dps = mp.dps
    mp.dps = num_digits
   # print(f"User ID={user_id}, Number of Digits={num_digits}")
    if user_id == "GOD 001":
        k_id = str(mp.pi)  # K_ID for GOD is Pi
    else:
        k_id = num_pi_str(user_id, long_pi, num_digits, 0)  # Pi-based key for the user ID
    k_id = str(mp.mpf(k_id)* mp.mpf("0.0001"))
    #print(f"user_id={user_id}")
    #print(f"KID={k_id[:80]}")
    mp.dps = original_dps
    return k_id


def gera_K_ID_temporario(ID, valor, unidade):
    """
    Gera um K_ID temporário com base em um ID e um tempo de validade especificado.

    Args:
        ID (str): Identificador base (como 'TOP 123.456-789').
        valor (int): Quantidade de tempo (em minutos ou horas).
        unidade (str): Unidade de tempo ('minutos' ou 'horas').

    Returns:
        str: K_ID temporário com máscara apropriada.
    """
    # Converte para minutos
    if unidade == "horas":
        total_segundos = valor * 3600
    elif unidade == "minutos":
        total_segundos = valor * 60
    else:
        raise ValueError("Unidade deve ser 'minutos' ou 'horas'")

    # Limite máximo de 48 horas
    if total_segundos > 48 * 3600:
        raise ValueError("Tempo máximo permitido é 48 horas (2880 minutos)")

    # Obtem o tempo atual em segundos desde epoch
    agora_segundos = int(datetime.utcnow().timestamp())

    # Define o nível de máscara
    if total_segundos <= 100:
        nivel = 1  # 1 minuto
        mascara = str(agora_segundos // 10) + "X"
    elif total_segundos <= 1000:
        nivel = 2  # 15 minutos
        mascara = str(agora_segundos // 100) + "XX"
    elif total_segundos <= 10000:
        nivel = 3  # 2 horas
        mascara = str(agora_segundos // 1000) + "XXX"
    else:
        nivel = 4  # 2 dias
        mascara = str(agora_segundos // 10000) + "XXXX"

    # Concatena ID com máscara
    K_ID_temp = f"{ID}_{mascara}"
    return K_ID_temp, nivel


def gera_K_ID_temporario_past(ID, valor, unidade, delta):
    """
    Gera uma K_ID temporária com base em um tempo no passado ajustado por delta.
    
    Args:
        ID (str): Identificador base.
        valor (int): Quantidade de tempo.
        unidade (str): 'minutos' ou 'horas'.
        delta (int): Deslocamento para trás no tempo (0 a 9).

    Returns:
        str: K_ID temporário gerado com base no tempo ajustado.
        int: Nível da máscara usada.
    """
    # Converte valor para segundos
    if unidade == "minutos":
        segundos = valor * 60
    elif unidade == "horas":
        segundos = valor * 3600
    else:
        raise ValueError("Unidade deve ser 'minutos' ou 'horas'.")

    # Limita a validade máxima a 48 horas
    segundos = min(segundos, 48 * 3600)

    # Determina o nível e o fator da máscara
    if segundos <= 100:
        fator = 10
        nivel = 1
    elif segundos <= 1000:
        fator = 100
        nivel = 2
    elif segundos <= 10000:
        fator = 1000
        nivel = 3
    else:
        fator = 10000
        nivel = 4

    # Ajusta o tempo atual com delta para o passado
    agora = int(datetime.utcnow().timestamp())
    tempo_ajustado = agora - (delta * fator)
    tempo_mascara = tempo_ajustado // fator

    K_ID_temp = f"{ID}_{tempo_mascara:08d}{'X' * nivel}"
    return K_ID_temp, nivel


def get_public_keys(long_pi, keys_path, user_id):
    """
    Retrieves the public keys associated with the given user ID.

    Parameters:
    - long_pi (str): The long Pi value for key generation.
    - keys_path (str): The directory path where keys are stored.
    - user_id (str): The user identifier.

    Returns:
    - tuple: (K1_pub, K2_pub, K_ID, DX, success flag, message)
    """
    num_digits = get_num_digits(user_id)
    public_key_filename = f"{keys_path}/Key-Pub-{user_id}.txt"
    
    k_id = get_k_id(user_id, long_pi)
  
    K1_pub, K2_pub, K3_pub,_, DX_base,De_base, success = load_public_keys(
        "K1", "K2", "K3", "K4", "DX", "DE", public_key_filename, num_digits)

    if not success:
        error_message = f"Error reading public key: {public_key_filename}"
        return 0, 0, 0, 0, False, error_message
    success_message = "Public keys successfully read"
    return K1_pub, K2_pub, K3_pub, k_id, DX_base,De_base, True, success_message


def get_private_keys(long_pi,path_keys,ID,pass_word):
    ndig = get_num_digits(ID)
    undig = mp.dps
    mp.dps = ndig
    name_priv = f"{path_keys}/Key-Priv-{ID}.txt"
    
    Kpriv_alpha, Kpriv_x, Kpriv_y, kpriv_de, _, _, OK = load_private_keys(
        pass_word, long_pi,"K1", "K2", "K3", "K4", "DX","DE", name_priv, ndig)
   
   
    if not OK:
       mserror = f"Erro lendo chave prublica:{name_priv}"
       return 0,False,mserror
    mserror = "Chave Privada do usuario lidas"
    mp.dps=undig
    return  Kpriv_alpha, Kpriv_x, Kpriv_y, kpriv_de,True,mserror


def calculate_all_keys(long_pi, path, pass_word1,pass_word2, time, id_without_crc, MSG=False):
    """
    Generates all cryptographic keys for a given user ID and password.

    Parameters:
    - long_pi (str): The long Pi value for key generation.
    - path (str): The directory path where keys will be stored.
    - password (str): The user's password.
    - timestamp (str): The current timestamp.
    - id_no_crc (str): The user ID without CRC.
    - display_messages (bool): Flag to indicate whether to display messages.

    Returns:
    - tuple: (success flag, message)
    """
    alpha_base = mpf("17.888")  # Fixed alpha value within the routine
    id_type, id_number = id_without_crc.split()
    crc = calculate_CRC_ID(f"{id_type}",f"{id_number}", long_pi)
    complete_id = f"{id_type} {id_number}-{crc}"
    valid, error_msg = validate_id(complete_id, long_pi)
    if not valid:
        return False, f"Invalid ID: {complete_id}. {error_msg}"

    num_digits = get_num_digits(complete_id)
    mp.dps = num_digits
    # Generate K_ID and ke_Pub
    str_txt = pass_word1 + time + complete_id
    ke_str = num_pi_str(str_txt, long_pi, num_digits, 0)
    ke_str = str(mpf("1.8") + mpf(ke_str) * mpf("0.01"))

    str_txt = pass_word2 + time + complete_id
    R0_str = num_pi_str(str_txt, long_pi, num_digits, 0)
    R0_str = str(mpf("1.1") + mpf(R0_str) * mpf("0.01"))
    K_ID = get_k_id(complete_id, long_pi)

    # Calculate keys (now with 7 components)
   

    Kpub1_str, Kpub2_str, Kpub3_str,Kpriv_de_str, Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str = calculate_pub_priv_keys(
        ke_str,R0_str, K_ID, num_digits)

    # Optional: show summary
    if MSG:
        opstr = input("Show SUMMARY of Public and Private Keys? (y/n): ")
        if opstr.lower() == "y":
            #print(f"\nK PUB (DX)     = {str(DX_base)[:60]}")
            print(f"K PUB (K_ID)   = {str(K_ID)[:60]}")
            print(f"K PUB (K1_pub) = {str(Kpub1_str)[:60]}")
            print(f"K PUB (K2_pub) = {str(Kpub2_str)[:60]}")
            print(f"K PUB (K3_pub) = {str(Kpub3_str)[:60]}")
            print(f"K PRIV (alpha) = {str(Kpriv_alpha_str)[:60]}")
            print(f"K PRIV (de)    = {str(Kpriv_de_str)[:60]}")
            print(f"K PRIV (x)     = {str(Kpriv_x_str)[:60]}")
            print(f"K PRIV (y)     = {str(Kpriv_y_str)[:60]}")

    # Test the keys using all 7 components
    key_ok, DX_base,De_base = test_keys(
        Kpub1_str, Kpub2_str, Kpub3_str,
        Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str,Kpriv_de_str,
        str(alpha_base), str(K_ID), num_digits
    )

    if not key_ok:
        return False, "Error testing the keys"
    else:
        print("Key test ok")      

    # Save the keys using the new format
    name_priv = f"{path}/Key-Priv-{complete_id}.txt"
    name_pub = f"{path}/Key-Pub-{complete_id}.txt"

    save_public_keys("K1", "K2", "K3", "K4", "DX","DE", name_pub,
                     Kpub1_str, Kpub2_str, Kpub3_str, Kpub3_str, DX_base,De_base, display_msg=MSG)

    save_private_keys(pass_word1, long_pi,"K1", "K2", "K3", "K4", "DX","DE", 
                      name_priv,Kpriv_alpha_str, Kpriv_x_str, Kpriv_y_str,Kpriv_de_str, DX_base,De_base,
                      num_digits, display_msg=MSG)

    # Read again to confirm
    K1_pub, K2_pub, K3_pub,_, DX_base,De_base, ok1 = load_public_keys(
        "K1", "K2", "K3", "K4", "DX", "DE", name_pub, num_digits, display_msg=MSG)

    Kpriv_alpha, Kpriv_x, Kpriv_y, kpriv_de, _, _, ok2 = load_private_keys(
        pass_word1, long_pi,
        "K1", "K2", "K3", "K4", "DX","DE", name_priv, num_digits,
        display_msg=MSG)

    if not ok1 or not ok2:
        return False, "Error rereading the saved keys"

    # Confirm again
    key_ok, _ , _ = test_keys(
        K1_pub, K2_pub, K3_pub,
        Kpriv_alpha, Kpriv_x, Kpriv_y,kpriv_de,
        str(alpha_base),str(K_ID), num_digits
    )
    if not key_ok:
        return False, "Final error confirming the keys"

    return True, f"Keys for ID {complete_id} successfully generated and verified."
