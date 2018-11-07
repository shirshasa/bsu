import socket

from lab2.server.utils import get_session_key, int_list_to_send_format
from lab2.server.crypto import rsa
from lab2.server.crypto import ofb

KEY_OFB_LENGTH = 16
VI_IDEA_LENGTH = 8
DEBUG = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 9090))
sock.listen(socket.SOMAXCONN)
conn, address = sock.accept()

file = None

while True:
    list_rsa_key = conn.recv(1024).decode('utf-8').rstrip(' ').split(' ')
    rsa_key = (int(list_rsa_key[0]), int(list_rsa_key[1]))         # receive open rsa key
    requested_file = conn.recv(1024).decode('utf-8')               # receive file name

    if not requested_file:
        break

    if 'txt' in requested_file:
        session_key = get_session_key(KEY_OFB_LENGTH + VI_IDEA_LENGTH)
        encrypted_file = ofb.encrypt_file(session_key, requested_file)  # encrypt file with ofb + idea + session key

        session_key_encrypted = rsa.encrypt(rsa_key, session_key)       # encrypt session key with rsa
        session_key_encrypted = int_list_to_send_format(session_key_encrypted)
        conn.send(session_key_encrypted.encode('utf-8'))                # send encrypted by rsa key for ofb
        conn.send(encrypted_file.encode('utf-8'))                       # send encrypted by ofb file
        if DEBUG:
            print('encrypted file: \n')
            print(encrypted_file)

        print('server session key:', session_key)
        print('server session key encrypted:', session_key_encrypted)
        break

conn.close()
sock.close()
