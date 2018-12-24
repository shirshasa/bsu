from math import acos, degrees

A = 4
B = 4
C = 4


def count_angle(A, B, C):
    return degrees(acos((A * A + B * B - C * C) / (2.0 * A * B)))


def count_dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def count_angles(tri):
    angles = []
    A = count_dist(tri[0], tri[1])
    B = count_dist(tri[1], tri[2])
    C = count_dist(tri[2], tri[0])

    angles.append(count_angle(A, B, C))
    angles.append(count_angle(C, A, B))
    angles.append(count_angle(B, C, A))

    return angles
