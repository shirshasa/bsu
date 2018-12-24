from lab3.sha1 import sha1
from lab2.client.crypto import rsa


def get_rsa_key():
    file_rsa = open('C:/Users/PC/PycharmProjects/bsu/cryptography/lab2/client/crypto/rsa_key.txt', 'r').readlines()
    public_ = file_rsa[0].split(' ')
    private_ = file_rsa[1].split(' ')
    public_ = (int(public_[1]), int(public_[2]))
    private_ = (int(private_[1]), int(private_[2]))
    return public_, private_


def sign(text):
    # User A
    pub, priv = get_rsa_key()
    sign_ = sha1(bytes(text, 'utf-8'))
    encr = rsa.encrypt(priv, sign_)
    return encr, pub


def validate_sign(encr, text, pub):
    # User B
    sign_decrypted = rsa.decrypt(pub,encr)
    h = sha1(bytes(text, 'utf-8'))
    return h == sign_decrypted



msg = 'fdhjvflkjfljfdsvd'

encrypted, public_key = sign(msg)
print(msg)
msg += '1'
print(validate_sign(encrypted, msg, public_key))