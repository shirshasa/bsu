import random


def binary_array_to_str(binary_array):

    c_array = bytearray(binary_array).decode(encoding='utf-8', errors='ignore')
    res = ''.join(c_array)
    return res


def to_byte_list(data):
    return list(bytearray(data, encoding='utf-8'))


def xor_crypt_string(key_, data, decrypt=False):
    """
    :param key_: the same size as data
    :param data:
    :param decrypt: if decrypt then data is bite array
    :return: decrypted data as bite array
    """
    if not decrypt:
        data = to_byte_list(data)
    res = []
    z = zip(data, key_)
    for (x, y) in z:
        res.append(x ^ y)

    return res


s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def get_session_key(length):
    return ''.join(random.sample(s, length))


def full_to_1024(data_):
    delta = 2048 - len(data_)
    delta_str = [' '] * delta
    new_data = data_ + ''.join(delta_str)
    return new_data


def int_list_to_send_format(data):
    data = [str(x) for x in data]
    data = ' '.join(data)
    data = full_to_1024(data)
    return data
