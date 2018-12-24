
import numpy as np

from lab1.crypto.algo import get_char_index
from lab1.crypto.alphabet import ALPHABET, ALPHABET_FREQ


def get_text_chunks(text,key_len):
    texts = []
    for i in range(0,key_len):
        x = []
        start = i
        while start < len(text):
            x.append(get_char_index(text[start]))
            start += key_len
        texts.append(x)
    return texts


def shift(l, n):
    return l[n:] + l[:n]


def corr(x, y):
    corr_coefs = []
    for delta in range(0, 33):
        corr_coef = np.corrcoef(x, shift(y, delta))[0][1]
        corr_coefs.append(corr_coef)

    return corr_coefs


def get_key_codes_corr_analysis(encrypted_text, key_length):
    codes_encrypted = get_text_chunks(encrypted_text, key_length)

    encrypted_codes_histograms = []

    for codes in codes_encrypted:
        histogram, bins = np.histogram(codes, bins=range(0, len(ALPHABET) + 1), density=True)
        encrypted_codes_histograms.append(histogram)

    alphabet_distribution = list(ALPHABET_FREQ.values())

    key_code = []
    for code in encrypted_codes_histograms:
        corr_coefs = corr(code, alphabet_distribution)
        max_corr = max(corr_coefs)
        index_max_corr = corr_coefs.index(max_corr)
        code_alpha = 33 - index_max_corr
        key_code.append(code_alpha if code_alpha < 33 else 0)

    return key_code
