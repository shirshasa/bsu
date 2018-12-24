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
собственно,  именно   его?   А   потому,   что   причиной   возникновения  и
распространения  саундсистем  было то,  что  далеко  не  все  жители  Ямайки
обладали Портативными  радиоприемниками.  Особенным шиком считалось  слушать
транзистор  на  улице. А из  ямайских радиоприемников  неслись,  разумеется,
программы  южных  радиостанций  США.  Устроить саундсистему,  чтобы  орошать
модной музыкой всю улицу, - это довольно логичный шаг.

'''


def test(text_, key_length):

    key = ''.join(np.random.choice(list(ALPHABET), key_length, replace=True))

    key_length = len(key)
    encrypted = encrypt(text_, key)

    key_code = get_key_codes_corr_analysis(encrypted, key_length)
    result_key = ''
    for index in key_code:
        result_key += ALPHABET[index]

    count = 0
    for a, b in zip(result_key, key):
        if a == b:
            count += 1

    print('text size: ', len(text_), 'key size: ', key_length, ': ', 'accuracy: ', count / key_length * 100)
    return count/key_length


if __name__ == "__main__":

    TEST_KEY = False

    print('text size: ', len(text))
    if TEST_KEY:
        for i in range(5, 500):
            test(text, i)

    file = open('book2.txt', 'r', encoding='utf-8').read()
    file = prepare_text(file)
    print('file size: ', len(file))
    book = ''
    for line in file:
        book += line

    for size in range(1000, 17000, 200):
        test(book[0:size], int(size * 0.1))

    t = book[100:200]
    encrypted_text = encrypt(t, 'ОЛО')
    decrypted = decrypt(encrypted_text, 'ОЛО')
    print(decrypted)
    print(prepare_text(t))
    print(prepare_text(t) == decrypted)


