from lab2.server.crypto.Idea import Idea
from lab2.server.utils import to_byte_list, xor_crypt_string, binary_array_to_str


class OFBFileEncryption:
    def __init__(self, key_, data):
        k = key_[:16]
        vi = key_[-8:]

        self.idea = Idea(k)
        self.msg = data
        self.init_vector = vi
        self.msg_encrypted = self.encrypt(data)
        self.msg_decrypted = self.encrypt(self.msg_encrypted, decrypt=True)

    def encrypt(self, data, decrypt=False):
        data = self.str_to_mod_8(data)
        block_num = int(len(data)/8)
        msg_encrypted = []

        # key encrypts by idea cipher
        # first time with init vector
        key_encrypted = self.idea.encrypt(self.init_vector)

        for i in range(0, block_num):

            msg_block = data[i*8:8*i+8]
            msg_xored = xor_crypt_string(key_encrypted, msg_block, decrypt)
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


def encrypt_ofb(file, key):
    plain_text = file
    key = to_byte_list(key)
    ofb = OFBFileEncryption(key, plain_text)

    return ofb.msg_encrypted


def decrypt_ofb(file, key):
    plain_text = file
    key = to_byte_list(key)
    ofb = OFBFileEncryption(key, plain_text)

    return binary_array_to_str(ofb.msg_decrypted)


def encrypt_file(key_, file_name):
    file_path = 'database/' + file_name
    file_read = open(file_path, 'r', encoding='utf-8').read().strip()
    encrypted = encrypt_ofb(file_read, key_)
    encrypted_str = ''
    for x in encrypted:
        encrypted_str += str(x) + ' '
    return encrypted_str
