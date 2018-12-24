from lab1.crypto.alphabet import ALPHABET


def prepare_text(text):
    return ''.join(ch for ch in text.upper() if ch in ALPHABET)


def get_char_index(c):
    return ALPHABET.index(c)


def to_int_array(text):
    l = []
    for elem in text:
        l.append(get_char_index(elem))
    return l


def encrypt(text, key):
    encrypted = ''
    N = len(ALPHABET)
    text = prepare_text(text)
    key = to_int_array(key)
    text = to_int_array(text)

    for i in range(len(text)):
        key_index = i % len(key)
        new_index = (text[i] + key[key_index]) % N  # +1, enumeration from 1
        new_letter = ALPHABET[new_index]
        encrypted += new_letter
    return encrypted


def decrypt(text, key, is_int=False):
    decrypted = ''
    N = len(ALPHABET)
    if not is_int:
        text = to_int_array(text)
        key = to_int_array(key)
    for i in range(len(text)):
        key_index = i % len(key)
        new_index = (text[i] - key[key_index]) % N  # +1, enumeration from 1
        new_letter = ALPHABET[new_index]
        decrypted += new_letter
    return decrypted
