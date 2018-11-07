from lab2.server.crypto.Idea import Idea


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


class OFBFileEncryption:
    def __init__(self, key_, data):
        k = key_[:16]
        vi = key_[-8:]

        self.idea = Idea(k)
        self.msg = data
        self.init_vector = vi

        self.msg_encrypted = data
        self.msg_decrypted = self.decrypt(self.msg_encrypted)

    def decrypt(self, data):

        block_num = int(len(data)/8)
        msg_encrypted = []

        # key encrypts by idea cipher
        # first time with init vector
        key_encrypted = self.idea.encrypt(self.init_vector)

        for i in range(0, block_num):

            msg_block = data[i*8:8*i+8]
            msg_xored = xor_crypt_string(key_encrypted, msg_block, True)
            msg_encrypted.extend(msg_xored)

            # key encrypts on each step of block algorithm
            key_encrypted = self.idea.encrypt(key_encrypted)
        return msg_encrypted

    @staticmethod
    def str_to_mod_8(msg):
        if len(msg) % 8 != 0:
            m = len(msg) % 8
            adding = ['.']*(8-m)
            adding = ''.join(adding)
            return msg + adding
        return msg


def decrypt_ofb(key, file):
    plain_text = file
    key = to_byte_list(key)
    if len(key) < 16:
        print('KEY LENGTH ERROR')
    ofb = OFBFileEncryption(key, plain_text)

    return binary_array_to_str(ofb.msg_decrypted)
