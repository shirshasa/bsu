
def encrypt(public_key, text):
    """
    :param public_key: (e, n)
    :param text: text to encrypt
    :return: list of encrypted bytes
    """
    e, n = public_key

    encrypted = [pow(ord(x), e, n) for x in text]
    return encrypted


def decrypt(private_key, encrypted):
    """
    :param private_key: (d, n)
    :param encrypted: list of encrypted bytes
    :return: decrypted string
    """
    d, n = private_key
    plain = [chr(int(pow(x, d, n))) for x in encrypted]
    return ''.join(plain)


