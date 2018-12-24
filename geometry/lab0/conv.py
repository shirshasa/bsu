import math


def rotate(A, B, C):
    return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])


def grahamscan(A):
    n = len(A)  # число точек
    P = list(range(n))  # список номеров точек
    n = len(P)
    for i in range(1, n):
        if A[P[i]][0] < A[P[0]][0]:  # если P[i]-ая точка лежит левее P[0]-ой точки
            P[i], P[0] = P[0], P[i]  # меняем местами номера этих точек

    for i in range(2, n):  # сортировка вставкой
        j = i
        while j > 1 and (rotate(A[P[0]], A[P[j - 1]], A[P[j]]) < 0):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1
    add = []
    S = [P[0], P[1]]  # создаем стек
    add.extend(S)
    for i in range(2, n):
        while rotate(A[S[-2]], A[S[-1]], A[P[i]]) < 0:
            x = S[-1]  # pop(S)
            del S[-1]
            add.append(x)
        S.append(P[i])  # push(S,P[i])

    return S, add


def make_conv(dots_):
    sequenced_index_dots, more_lines = grahamscan(dots_)
    seq_dots = []

    for index in range(len(sequenced_index_dots)):
        if index == len(sequenced_index_dots) - 1:
            p1 = dots_[sequenced_index_dots[index]]
            p2 = dots_[sequenced_index_dots[0]]
            seq_dots.extend([p1, p2])
            break

        p1 = dots_[sequenced_index_dots[index]]
        p2 = dots_[sequenced_index_dots[index + 1]]
        seq_dots.extend([p1, p2])

    return seq_dots
