def full_1024(data_):
    delta = 1024 - len(data_)
    delta_str = [' '] * delta
    new_data = data_ + ''.join(delta_str)
    return new_data


def get_rsa_key():
    file_rsa = open('crypto/rsa_key.txt', 'r').readlines()
    public = file_rsa[0].split(' ')
    private = file_rsa[1].split(' ')
    public = (public[1], public[2])
    private = (int(private[1]), int(private[2]))
    return public, private


def get_public_rsa_to_send():
    public_rsa, private_rsa = get_rsa_key()
    d, n = public_rsa
    rsa_to_send = str(d) + ' ' + str(n)
    rsa_to_send = full_1024(rsa_to_send)
    return rsa_to_send


def get_private_rsa():
    _, private_rsa = get_rsa_key()
    return private_rsa
