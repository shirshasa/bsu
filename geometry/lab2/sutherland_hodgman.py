from lab2 import poly_point_isect


def rotate(A, B, C):
    """
    :param A: segment
    :param B: segment point
    :param C: point
    :return: positive if C -- AB , negative value if AB -- C
    """
    res = (B[0] - A[0]) * (C[1] - B[1])
    res2 = (B[1] - A[1]) * (C[0] - B[0])
    return res - res2


def is_inside(edge, vertex):
    A, B = edge
    res = rotate(A, B, vertex)
    return res >= 0


def get_cut(polygon, window):
    """

    :param polygon: list of points
    :param window: list of edges
    :return: list of vertices of cliped polygon
    """
    polygon = [tuple(elem) for elem in polygon]
    output = polygon  # new polygon
    window = list(window)

    for clip_edge in window:
        input_list = output.copy()

        output.clear()
        if len(input_list) == 0:
            return [(0.0, 0.0)]
        s = input_list[-1]

        for e in input_list:
            if is_inside(clip_edge, e):
                if not is_inside(clip_edge, s):
                    # print('# q ')
                    q = poly_point_isect.isect_segments(((s, e), clip_edge))
                    if len(q) == 0:
                        pass
                    else:
                        output.append(q[0])
                output.append(e)

            elif is_inside(clip_edge, s):
                # print('# q')
                q = poly_point_isect.isect_segments(((s, e), clip_edge))
                if len(q) == 0:
                    pass
                else:
                    output.append(q[0])

            s = e

    return output
