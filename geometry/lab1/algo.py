import numpy as np
from scipy.spatial import Delaunay

from lab2.generate_polygon import generatePolygon
from lab2.sutherland_hodgman import get_cut
from lab2.utils import vertex_list_to_edge

MAX_X = 500
MAX_Y = 640

BORDER = border = generatePolygon(MAX_X/2, MAX_Y/2, 200, 0, 0, 3)


def get_triangulation(points, is_numpy=False):
    """
    :param is_numpy:
    :param points: polygon array
    :return:       triangulated polygon - array of triangles
    """
    points = np.array(points)
    tri = Delaunay(points)
    if not is_numpy:
        tri = points[tri.simplices].tolist()
        points = points.tolist()

    return tri, points


def add_triangle_border(max_x, max_y):
    return BORDER


def delete_v(p):
    if len(p) == 2:
        return [p[0]]
    if len(p) <= 1:
        return []
    t, points = get_triangulation(p, True)  # use points without border
    neighbors = t.neighbors
    source = points[t.simplices[0]].tolist()  # next, search for right vertex
    look_neighbors_index = [elem for elem in neighbors[0] if elem > 0]
    if len(look_neighbors_index) == 0:
        return [source[0]]
    neighbor_index = look_neighbors_index[0]
    target = points[t.simplices[neighbor_index]].tolist()
    point_to_delete1 = [point for point in source if point not in target]
    point_to_delete2 = [point for point in target if point not in source]
    point_to_delete = [tuple(point_to_delete1[0]), tuple(point_to_delete2[0])]

    return [pp for pp in p if pp not in point_to_delete]


def get_structure(s: list, p: list):
    """
    recursiv function
    :S: array of triangulations
    :p: simple points[]
    :return:  graph T
              where vertex is triangle in triangulation s_i
              edges are  ( rk rj)
                          rj deleted from s_i-1 on step 1
                          rk creates in s_i on step 2
                          rj and rk have common points
    """
    points_with_border = p + add_triangle_border(MAX_X, MAX_Y)
    triangulation, _ = get_triangulation(points_with_border, is_numpy=False)
    s.append(triangulation)
    if len(p) <= 0:
        return

    new_vertexes = delete_v(p)
    get_structure(s, new_vertexes)

    return s


def build_edges(list_big_triangles, list_small):
    edges = []

    for T in list_big_triangles:
        for t in list_small:
            if T == t:
                continue
            xxx= list(set(get_cut(t,vertex_list_to_edge(T))))

            if len(xxx)> 2:
                edges.append((T, t))
    return edges


def is_in_triangle(t, point):
    if not point : return False
    p1, p2, p3 = t
    a = (p1[0] - point[0]) * (p2[1] - p1[1]) - (p2[0] - p1[0]) * (p1[1] - point[1])
    b = (p2[0] - point[0]) * (p3[1] - p2[1]) - (p3[0] - p2[0]) * (p2[1] - point[1])
    c = (p3[0] - point[0]) * (p1[1] - p3[1]) - (p1[0] - p3[0]) * (p3[1] - point[1])
    a = int(a)
    b = int(b)
    c = int(c)

    if (a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0):
        return True
    else:
        return False


def build_graph(s_):
    graph = {}
    for i in range(len(s_) - 1, 0, -1):
        print('cur triangles: ')
        for t in s_[i]:
            print(t)

        new_edges = build_edges(s_[i], s_[i - 1])

        print('cur edges')

        for e in new_edges:
            print(e)

        for (a, b) in new_edges:
            a = [tuple(aa) for aa in a]
            a = tuple(a)
            b = [tuple(bb) for bb in b]
            b = tuple(b)
            if a not in graph:
                graph[a] = [b]
            else:
                graph[a].append(b)

    return graph


def point_location(point,T):
    root_triangle = list(T.keys())[0]
    if not is_in_triangle(root_triangle,point) : return None

    while root_triangle in list(T.keys()):
        tris = T[root_triangle]
        for tri in tris:
            if is_in_triangle(tri, point):
                root_triangle = (tuple(tri[0]), tuple(tri[1]), tuple(tri[2]))
                break

    return root_triangle


if __name__ == '__main__':
    file = open('dots.txt', 'r').read()
    prep_str = file.strip(' ').split('), (')
    prep_str = [x.lstrip('(') for x in prep_str]
    prep_str = [x.rstrip(')\n') for x in prep_str]
    dots = []

    for pair in prep_str:
        (x, y) = pair.split(', ')
        dots.append((float(x), float(y)))

    s = []
    get_structure(s, dots)

    for lll in s:
        print('s_i: ', len(lll))

    m = build_graph(s)

    for mm in m.keys():
        print(mm, 'triangle\'s edges: ', len(m[mm]))


