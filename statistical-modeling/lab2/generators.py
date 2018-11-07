from math import factorial

from lab1.generators import mcg


def uniform():
    N = 50000
    M = 2.0 ** 31 - 1
    C = 1231
    alpha0 = beta = 16807.0
    l = list(mcg(alpha0, beta, M, N, C))
    for i in range(N):
        yield l[i]


y = uniform()


def bernoulli(p):
    boundary = 1 - p
    x = y.__next__() > boundary
    return x


def get_next_hyper_geom(D, N, n):
    sum_ = 0
    p = D / N

    for i in range(1, n + 1):
        y = bernoulli(p)
        if y:
            sum_ += 1
            if sum_ == D:
                return sum_
        p = (D - sum_) / (N - i)

    return sum_


def HG(D, N, n, observed):
    """
    Hypergeometric binomial distribution
    """
    for i in range(observed):
        yield get_next_hyper_geom(D, N, n)


def C(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


def hyper_geom_distribution(D, N, n, k):
    return C(D, k) * C(N - D, n - k) / C(N, n)


def hyper_geom_dstr(D, N, n):
    p = [hyper_geom_distribution(D, N, n, i) for i in range(max(0, D + n - N), min(n, D))]

    keys = [elem for elem in range(max(0, D + n - N), min(n, D))]

    return dict(zip(keys, p))


def hyper_geom_cum(D, N, n):
    p = [hyper_geom_distribution(D, N, n, i) for i in range(max(0, D + n - N), min(n, D))]

    keys = [elem for elem in range(max(0, D + n - N), min(n, D))]
    f = [0] * len(p)
    for i in range(len(p)):
        if i - 1 >= 0:
            f[i] += f[i - 1]
        f[i] += p[i]

    return dict(zip(keys, f))
