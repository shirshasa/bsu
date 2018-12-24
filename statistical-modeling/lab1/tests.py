# import os
# from bisect import bisect_right
# import numpy as np
#
#
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.sys.path.insert(0, parent_dir)
#
# from lab1.chi_square import DELTA, MAX_K
#
# PEARSON_THRESHOLD = 0.01
#
#
# def get_frequency(sorted_seq, k):
#     min_el = sorted_seq[0]
#     max_el = sorted_seq[-1]
#     step = (max_el - min_el) / (k + 1)
#     segments = np.arange(min_el, max_el, step)
#
#     freq_list = [0] * k
#     last_position = 0
#     for i in range(k):
#         position = bisect_right(sorted_seq, segments[i + 1])
#         freq_list[i] = position - last_position
#         last_position = position
#     return freq_list, segments
#
#
# def count_elements(seq) -> dict:
#     """Tally elements from `seq`."""
#     hist = {}
#     for i in seq:
#         hist[i] = hist.get(i, 0) + 1
#     return hist
#
#
# def get_probabilities(segments, f):
#
#     print(f)
#     k = len(segments)
#     p = [0] * (k - 1)
#     for i in range(k - 1):
#         p[i] = f[int(round(segments[i + 1]))] - f[int(round(segments[i]))]
#         if i == 0:
#             p[i] = f[segments[i + 1] - 1]
#
#         if i == k - 2:
#             p[i] = 1 - f[segments[i - 1]]
#
#     return p
#
#
# def pearson(sorted_seq, p_list=None, discrete=False,k = 30):
#     """
#
#     :param sorted_seq: experimented sequence
#     :param p_list: dict of theory distribution
#     :param discrete: is discrete
#     :param k: for pearson
#     :return: value of pearson
#     """
#     n = len(sorted_seq)
#
#     if discrete:
#
#         keys = list(p_list.keys())
#         real_freq = count_elements(sorted_seq) # dict
#
#         for key in keys:
#             if key not in real_freq.keys():
#                 real_freq[key] = 0
#
#         # bin_edges = np.histogram(sorted_seq, bins=k)
#         theory_freq = list(p_list.values())
#         real_freq = list(real_freq.values())
#         print(len(theory_freq))
#         print(real_freq)
#
#     else:
#         real_freq, segments = get_frequency(sorted_seq, k)
#         theory_freq = p_list
#
#     # объеденим интервалы в которые меньше 5
#
#     for index in range(len(real_freq)):
#         if index == 1:
#             if real_freq[index] < 5:
#                 b = real_freq[index]
#                 real_freq[index - 1] += b
#                 real_freq[index] = 0
#
#                 b = theory_freq[index]
#                 theory_freq[index - 1] += b
#                 theory_freq[index] = 0
#             break
#
#         if real_freq[index] < 5:
#             b = real_freq[index]
#             real_freq[index - 1] += b
#             real_freq[index] = 0
#
#     for index in range(len(real_freq)):
#
#         if real_freq[index] < 5:
#             b = real_freq[index + 1]
#             real_freq[index] += b
#             real_freq[index + 1] = 0
#
#             b2 = theory_freq[index + 1]
#             theory_freq[index] += b2
#             theory_freq[index + 1] = 0
#
#     theory_freq = [elem for elem in theory_freq if elem != 0]
#     real_freq = [elem for elem in real_freq if elem != 0]
#
#     print(len(theory_freq))
#     print(real_freq)
#     k = len(real_freq)
#     delta = DELTA[k]
#     l = [0] * (len(real_freq))
#     for i in range(len(real_freq)):
#         if real_freq[i] - n * theory_freq[i] == 0.0:
#             l[i] = 0
#             continue
#         l[i] = (real_freq[i] - n * theory_freq[i]) ** 2 / (n * theory_freq[i])
#
#     value = sum(l)
#     return value, delta, k

import os
from bisect import bisect_right
import numpy as np
from math import factorial

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_dir)

from .chi_square import DELTA, MAX_K

PEARSON_THRESHOLD = 0.01


def C(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


def get_frequency(sorted_seq, k):
    min_el = sorted_seq[0]
    max_el = sorted_seq[-1]
    step = (max_el - min_el) / (k + 1)
    segments = np.arange(min_el, max_el, step)

    freq_list = [0] * k
    last_position = 0
    for i in range(k):
        position = bisect_right(sorted_seq, segments[i + 1])
        freq_list[i] = position - last_position
        last_position = position
    return freq_list, segments


def get_discrete_frequency(sorted_seq, p, max_k):
    k = 0
    while k < max_k and p[k] > PEARSON_THRESHOLD:
        k += 1
    v = [0] * (k + 1)
    for el in sorted_seq:
        i = el if el < k else k
        v[i] += 1
    return v, k


def get_probabilities(segments, f):
    k = len(segments)
    p = [0] * k
    for i in range(k - 1):
        p[i] = f(segments[i + 1]) - f(segments[i])
    return p


def pearson(sorted_seq, distr_f=None, p_list=None, discrete=False):
    """
    Pearson's chi-squared test
    :param sorted_seq: sorted random sequence to test
    :param distr_f: optional distribution function
    :param p_list: optional distribution list
    :param discrete: flag for discrete distributions
    :return: test value, pearson delta for k, k
    """
    n = len(sorted_seq)
    if discrete:
        v, k = get_discrete_frequency(sorted_seq, p_list)
        p = p_list
    else:
        k = MAX_K
        v, segments = get_frequency(sorted_seq, k)
        p = p_list if p_list else get_probabilities(segments, distr_f)
    delta = DELTA[k]
    value = sum([(v[i] - n * p[i]) ** 2 / (n * p[i]) for i in range(k)])
    return value, delta, k
