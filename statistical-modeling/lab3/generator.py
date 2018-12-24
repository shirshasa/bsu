from math import sqrt, erf, log, exp,pi
from random import random


# Gauss

def get_next_standard_gauss():
    return sum([random() for _ in range(12)]) - 6


def get_next_gauss(m, s):
    return m + s * get_next_standard_gauss()


def gauss(m, s, n):
    """
    N(m, s^2)
        :param m: mean
        :param s: dispersion
        :param n: size
    """
    for _ in range(n):
        yield get_next_gauss(m, s)


def gauss_distribution(m, s, x):
    return 0.5 * (1 + erf((x - m) / (sqrt(2) * s)))


# Lognormal

def get_next_lognormal(mu, sigma):
    m = log(mu)
    general_gauss = get_next_gauss(m, sigma)
    return exp(general_gauss)


def lognormal(m, s, n):
    """
    Lognormal(m, s^2)
        :param m: mean
        :param s: dispersion
        :param n: size
    """
    for _ in range(n):
        yield get_next_lognormal(m, s)


def lognormal_distribution(mu, s, x):
    if x == 0:
        x += 10 ** (-6)
    return 0.5 + 0.5 * erf((log(x) - mu) / (sqrt(2) * s))

def lognormal_prob(mu,sigma,x):
    return exp((-((log(x) - mu)/ sigma) ** 2) * 2) / (x * sigma * (2* pi) ** 0.5)