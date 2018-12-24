import numpy as np
import matplotlib.pyplot as plt


def draw_freq(real, theory, segments, plt = plt):
    plt.hist(x=real, label='real', bins=len(segments), color='green', alpha=0.7, rwidth=0.85)
    plt.plot(segments, theory, label='theory')
    # plt.xlabel('x', fontsize=10)
    # plt.ylabel('frequency', fontsize=10)
    plt.legend()
    # plt.show()


def draw_cdf(f1, f2, x, plt=plt):
    plt.plot(f1, label='real', color='green')
    plt.plot([f2(i, 0, 1) for i in x], label='theory')
    # plt.xlabel('x', fontsize=10)
    # plt.ylabel('Cumulative distribution function', fontsize=10)
    plt.legend()
    # plt.show()


def draw_scatter(x1, x2, plt = plt):
    plt.plot(x1, x2, 'bo', label='values')
    # plt.xlabel('x1', fontsize=20)
    # plt.ylabel('x2', fontsize=20)
    plt.legend()
    # plt.show()


def draw_autocorr(x, plt= plt):
    plt.bar(np.arange(len(x)), x, label='autocorr', color='green')
    # plt.xlabel('t', fontsize=20)
    # plt.title('autocorr, t = 0..30')
    plt.legend()
    # plt.show()


def draw_intervals(i1, i2, m):
    plt.figure(figsize=(5, 3))
    plt.plot(i1, label='lower', color='green')
    plt.plot(i2, label='upper', color='blue')
    plt.plot(m, label='mean or var', color='red')
    plt.xlabel('population number', fontsize=20)
    plt.legend()
    plt.show()
