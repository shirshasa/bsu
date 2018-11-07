import socket

from lab2.client.crypto.ofb import decrypt_ofb
from lab2.client.crypto import rsa
from lab2.client.utils import full_1024, get_public_rsa_to_send, get_private_rsa

DEBUG = False

FILE_NAME = 'f1.txt'
FILE_NAME = full_1024(FILE_NAME)

public_rsa = get_public_rsa_to_send()
private_rsa = get_private_rsa()

sock = socket.socket()
sock.connect(('localhost', 9090))

sock.send(public_rsa.encode('utf-8'))     # send rsa open key
sock.send(FILE_NAME.encode('utf-8'))      # send file name

session_key_encrypted = sock.recv(2048).decode('utf-8').rstrip(' ')  # receive ofb key in str format
session_key_encrypted = session_key_encrypted.split(' ')
session_key_encrypted = [int(x) for x in session_key_encrypted]
session_key = rsa.decrypt(private_rsa, encrypted=session_key_encrypted)  # decrypt key ofb  with rsa key


data = b""
tmp = sock.recv(1024)                      # receive first portion of data
while tmp:
    data += tmp
    tmp = sock.recv(1024)                  # get full file

file = open('database/output.txt', 'w')
data = data.decode('utf-8')
data = data.rstrip(' ').split(' ')
data = [int(x) for x in data]              # decrypt file with ofb + idea
data_decrypted = decrypt_ofb(session_key, data)
file.write(data_decrypted.encode('cp850', 'replace').decode('cp850'))

print('client session key: ', session_key)
print('client session key encrypted: ', session_key_encrypted)

if DEBUG:
    print()
    print(data)

sock.close()


