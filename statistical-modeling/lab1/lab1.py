from random import random

import numpy as np

from lab1.chi_square import MAX_K
from lab1.generators import mcg
from lab1.tests import pearson
from lab1.utils import format_test_result

N = 100
K = 64
M = 2.0 ** 31 - 1
C = 1231
alpha0 = beta = 16807.0
a = 0
b = 1
uniform_mean = (a + b) / 2
uniform_variance = (b - a) ** 2 / 12

generated_numbers = list(mcg(alpha0, beta, M, N,C))
gen_numbers_n = generated_numbers
print('mcg:\t{}'.format(gen_numbers_n))

c = [random() for _ in range(N)]
print('random:\t{}'.format(c))

p = [1.0 / MAX_K] *MAX_K
gen_numbers_result = pearson(sorted(gen_numbers_n), p_list=p)
c_result = pearson(sorted(c), p_list=p)

print('\npearson, chi:')
print('\tmcg:\t' + format_test_result(*gen_numbers_result))
print('\trandom:\t' + format_test_result(*c_result), '\n')

print('generated set')
print('\tmean:\t', np.mean(gen_numbers_n))
print('\tvarience:\t', np.var(gen_numbers_n), '\n')

print('python random set')
print('\tmean:\t', np.mean(c))
print('\tvarience:\t', np.var(c), '\n')

print('theory')
print('\tmean:\t', 0.5)
print('\tvarience:\t', 1 / 12, '\n')
