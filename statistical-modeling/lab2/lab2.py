from lab1.tests import pearson
from lab1.utils import format_test_result
from lab2.generators import HG, hyper_geom_distribution, hyper_geom_cum, hyper_geom_dstr

D = 20
N = 70
n = 30
gen_numbers = list(HG(D, N, n, 3000))

p = hyper_geom_dstr(D,N,n)

gen_numbers_result = pearson(sorted(gen_numbers),  discrete=True, p_list = p)

print('\npearson, chi:')
print('\tmcg:\t' + format_test_result(*gen_numbers_result))
