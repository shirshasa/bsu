from lab1.generators import mcg
from lab1.graph import draw_freq, draw_cdf, draw_scatter, draw_autocorr
from lab1.tests import get_frequency
import numpy as np
import matplotlib.pyplot as plt

TEST_TEMPLATE = '{value:.3f} {sign} {delta:.3f} | test {result}'


def get_test_result(value, delta):
    return ['<', 'passed '] if value < delta else ['>=', 'failed 😭']


def format_test_result(value, delta, k=None):
    template = TEST_TEMPLATE
    if k:
        template = 'k = {k} | ' + TEST_TEMPLATE
    sign, result = get_test_result(value, delta)
    return template.format(k=k, value=value, sign=sign, delta=delta, result=result)


def generate_results_lab1(N=100, k=30):
    m = 2.0 ** 31 - 1
    alpha0 = beta = 16807.0
    c = 3

    grid_size = (3, 2)
    fig = plt.figure(figsize=(10, 8))
    ax1 = plt.subplot2grid(grid_size, (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid(grid_size, (2, 0))
    ax3 = plt.subplot2grid(grid_size, (2, 1))

    gen_numbers_n = list(mcg(alpha0, beta, m, N, c))
    sorted_seq = sorted(gen_numbers_n)

    freq_real, segments = get_frequency(sorted_seq, k)
    print('распрделение для выборки размера \t ', N)
    draw_freq(sorted_seq, [N / k] * (len(segments)), segments, plt=ax1)

    x_1 = [gen_numbers_n[i] for i in range(N) if i % 2 == 1]
    x_2 = [gen_numbers_n[i] for i in range(N) if i % 2 == 0]
    draw_scatter(x_1, x_2, plt=ax3)

    def autocorrelation(x, t=1):
        for i in range(0, t):
            y = x + [0] * i
            y = [y[j + i] for j in range(len(x))]
            correlation = np.corrcoef([x, y])
            yield correlation[0][1]

    corr = list(autocorrelation(gen_numbers_n, t=50))
    draw_autocorr(corr, plt=ax2)
    plt.show()
