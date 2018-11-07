import random
from decimal import Decimal
from math import gcd, log


def is_prime(x):
    if x == 2:
        return True
    if x < 2 or x % 2 == 0:
        return False
    for n in range(3, int(x ** Decimal(0.5)) + 2, 2):
        if x % n == 0:
            return False
    return True


def multiplicative_inverse(e, phi):
    """
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    """
    d, next_d, temp_phi = 0, 1, phi
    while e > 0:
        quotient = temp_phi // e
        d, next_d = next_d, d - quotient * next_d
        temp_phi, e = e, temp_phi - quotient * e
    if temp_phi > 1:
        raise ValueError('e is not invertible by modulo phi.')
    if d < 0:
        d += phi
    return d


def generate_keypair(p, q):
    # if not (is_prime(p)):
    #     print('P: Both numbers must be prime!')
    #
    # if not (is_prime(q)):
    #     raise ValueError('Q: Both numbers must be prime!')
    # elif p == q:
    #     raise ValueError('P and Q cannot be equal!')
    n = p * q
    e = 0
    phi = (p - 1) * (q - 1)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


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


#######################################

def is_probable_prime(n, k=300):
    """
      use Rabin-Miller algorithm to return True (n is probably prime)
      or False (n is definitely composite)
    """
    if n < 6:  # assuming n >= 0 in all cases... shortcut small cases here
        return [False, False, True, True, False, True][n]
    elif n & 1 == 0:  # should be faster than n % 2
        return False
    else:
        s, d = 0, n - 1
        while d & 1 == 0:
            s, d = s + 1, d >> 1
        # Use random.randint(2, n-2) for very large numbers
        tryings = [random.randint(2, n-2) for i in range(k)]
        for a in tryings:
            x = pow(a, d, n)
            if x != 1 and x + 1 != n:
                for r in range(1, s):
                    x = pow(x, 2, n)
                    if x == 1:
                        return False  # composite for sure
                    elif x == n - 1:
                        a = 0  # so we know loop didn't continue to end
                        break  # could be strong liar, try another a
                if a:
                    return False  # composite if we reached end of this loop
        return True  # probably prime if reached end of outer loop


##########################################################

if __name__ == "__main__":

    """
    генирация rsa ключа.
    запись в файл
    в цикле проверка на простоту с помощью теста Миллера-Рабена 
    """
    p_true = 0
    q_true = 0
    hints = 0           # если hints == 2 то оба ключа простые
    degree = 10 ** 10

    while True:
        if p_true == 0:
            p = random.randint(1, degree)
            print(p)
            test = is_probable_prime(p)
            print('p: ', test, p)
            print(p.bit_length())
            if test:
                p_true = p
                hints += 1
        if q_true == 0:
            q = random.randint(1, degree)
            test2 = is_probable_prime(q)
            print('q: ', test2, q)
            if test2:
                q_true = q
                hints += 1

        if hints >= 2:
            break

    public, private = generate_keypair(p_true, q_true)
    e, n = public
    d, n2 = private

    file = open('rsa_key.txt', 'w')
    file.write('public ' + str(e) + ' ' + str(n) + ' \n')
    file.write('private ' + str(d) + ' ' + str(n))
    print('key length: ',len(str(e)))

