import os

import numpy as np

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_dir)

from lab1.chi_square import MAX_K
from lab1.tests import pearson
from lab1.utils import format_test_result

TABLE = '\t\t\tActual\tTheory\t| Residual\nMean\t\t{0:.4f}\t{2:.4f}\t| {4:.2E}\nVariance\t{1:.4f}\t{3:.4f}\t| {5:.2E}'


def print_separator():
    print('---' * 17)


def print_table(actual, theory_mean, theory_var):
    mean_diff = abs(actual.mean() - theory_mean)
    var_diff = abs(actual.var() - theory_var)
    print(TABLE.format(actual.mean(), actual.var(), theory_mean, theory_var, mean_diff, var_diff))
    print_separator()


def run(
        title,
        generator,
        distr,
        args,
        mean,
        var,
        size,
        enable_pearson=True,
        discrete=False,
):
    """
    Tests runner
        :param title: distribution name
        :param generator: distribution generator function
        :param distr: theory distribution function
        :param mean: theory distribution mean
        :param var: theory distribution variance
        :param size: size of generated sequence
        :param args: generator and dist positional arguments
        :param enable_pearson: flag to perform pearson test (default=True)
        :param discrete: flag for use discrete pearson test (default=False)
    """
    pearson_successes = 0
    actual = None
    for i in range(size):
        actual = np.array(list(generator(*args, size)))
        if i == 0:
            print('\n> {}:'.format(title))
            print_table(actual, mean, var)
        sorted_actual = sorted(actual)

        p = None
        distr_f = lambda x: distr(*args, x)
        if discrete:
            p = [distr_f(i) for i in range(MAX_K)]
        p_value, p_delta, k = pearson(sorted_actual, distr_f, p, discrete)
        pearson_successes += int(p_value < p_delta)
        if i == size - 1:
            if enable_pearson:
                print('Pearson:\t' + format_test_result(p_value, p_delta, k))
                print('Success:\t{}%'.format(pearson_successes * 100 / size))
                print_separator()
    return  actual