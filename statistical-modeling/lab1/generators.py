# cryptographically secure pseudorandom number generators


def mcg(alpha, beta, m, n, c):

    for i in range(n):
        alpha = (beta * alpha + c) % m
        yield alpha / m


def mmg(b, c, k, n):
    """
    MacLaren-Marsaglia generator (MMG)
    """
    v = b[:k]
    for i in range(n):
        s = int(c[i] * k)
        yield v[s]
        v[s] = b[i + k]