import os
from bisect import bisect_right
import numpy as np


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_dir)

from lab1.chi_square import DELTA, MAX_K

PEARSON_THRESHOLD = 0.01


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


def count_elements(seq) -> dict:
    """Tally elements from `seq`."""
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
    return hist


def get_probabilities(segments, f):

    print(f)
    k = len(segments)
    p = [0] * (k - 1)
    for i in range(k - 1):
        p[i] = f[int(round(segments[i + 1]))] - f[int(round(segments[i]))]
        if i == 0:
            p[i] = f[segments[i + 1] - 1]

        if i == k - 2:
            p[i] = 1 - f[segments[i - 1]]

    return p


def pearson(sorted_seq, p_list=None, discrete=False,k = 30):

    n = len(sorted_seq)

    if discrete:
        keys = list(p_list.keys())
        k = len(keys)

        dict1 = count_elements(sorted_seq)

        for key in keys:
            if key not in dict1.keys():
                dict1[key] = 0

        real_freq = dict1   # bin_edges = np.histogram(sorted_seq, bins=k)
        theory_freq = list(p_list.values())
        x = [elem * n for elem in p_list.values()]
        y = [(real_freq[i]-x[i])**2/(n*theory_freq[i]) for i in range(k)]

    else:
        real_freq, segments = get_frequency(sorted_seq, k)
        theory_freq = p_list

    delta = DELTA[k]
    l = [0] * k
    for i in range(k):
        if real_freq[i] - n * theory_freq[i] == 0.0:
            l[i] = 0
            continue
        l[i] = (real_freq[i] - n * theory_freq[i]) ** 2 / (n * theory_freq[i])

    value = sum(l)
    return value, delta, k
