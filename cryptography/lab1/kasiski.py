from itertools import count

import numpy as np


from lab1.crypto.algo import encrypt, decrypt, prepare_text
from lab1.crypto.alphabet import ALPHABET
from lab1.crypto.corr_analysis import get_key_codes_corr_analysis

text = ''' 
Истоки  современного,  так  сказать, ди-джейского  отношения  к  музыке
следует искать на Ямайке. Там уже в  середине  50-х  годов действовало более
250  саундсистем.  Они   состояли  из   колонок,  усилителя,
проигрывателя грампластинок и грузовика, на котором все это добро разъезжало
по дорогам. Но саундсистема -  это,  разумеется, не столько гора аппаратуры,
сколько  кустарное  предприятие  по организации дискотек на  свежем воздухе.
Саундсистемы заводили ритм-н-блюз, изготовленный в южных штатах США. Почему,
'''


def func(t, block):
    dist = []
    for i in range(len(t)):
        target = t[i:i + len(block)]
        if target == block:
            dist.append(i + len(block))

    return dist


def func2(t):
    dist = []
    for i in range(len(t) - 3):
        r = func(t, t[i:i+3])
        if len(r) > 1:
            dist.append(r)

    return dist



encrypted_text = encrypt(text, 'ОЛОЗВУФРНЕПАЕЛОЩДУ')
decrypted = decrypt(encrypted_text, 'ОЛОЗВУ')

pos = func2(encrypted_text)
dist = []

for elem in pos:
    d = None
    for i in range( len(elem)-1):
        d = elem[i+1] - elem[i]
    dist.append(d)

m = dict()      # растояние - количество таких расстояний

for d in dist:
    if d not in m:
        m[d] =1
    else:
        m[d] += 1

for mm in m.items():
    print(mm)