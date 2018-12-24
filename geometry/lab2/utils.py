import numpy as np


def r8vec_uniform_01(n, seed):
    # *****************************************************************************80
    #  Parameters:
    #    Input, integer N, the number of entries in the vector.
    #    Input, integer SEED, a seed for the random number generator.
    #    Output, real X(N), the vector of pseudorandom values.
    #    Output, integer SEED, an updated seed for the random number generator.
    #
    import numpy
    from math import floor
    from sys import exit

    i4_huge = 2147483647

    seed = floor(seed)

    if seed < 0:
        seed = seed + i4_huge
    if seed == 0:
        exit('R8VEC_UNIFORM_01 - Fatal error!')

    x = numpy.zeros(n)

    for i in range(0, n):
        k = floor(seed / 127773)
        seed = 16807 * (seed - k * 127773) - k * 2836
        if seed < 0:
            seed = seed + i4_huge
        x[i] = seed * 4.656612875E-10

    return x, seed


def timestamp():
    import time
    t = time.time()
    print(time.ctime(t))


def vertex_list_to_edge(l):
    edge_list = []
    for index in range(len(l)-1):
        edge_list.append(( tuple(l[index]), tuple(l[index+1]) ))

    edge_list.append((tuple(l[-1]),tuple( l[0])))
    return edge_list


def poly_centroid(arr):
    arr = np.array(arr)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return [sum_x/length, sum_y/length]