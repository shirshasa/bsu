from _heapq import heappop
from heapq import heappush

from lab2.utils import poly_centroid


class Triangle:
    def __init__(self, p,id, index, polygon):
        self.points  = p
        self.index = index
        self.index = tuple(index)
        self.id = id
        polygon_centroid = poly_centroid(polygon)
        centroid = poly_centroid(p.tolist())
        x1 = centroid[0]
        y1 = centroid[1]
        x2 = polygon_centroid[0]
        y2 = polygon_centroid[1]
        self.dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def __eq__(self, other):
        return self.dist == self.dist

    def __cmp__(self, other):
        return self.dist < other.dist

    def print(self):
        print(self.dist)

    def __lt__(self, other):
        return self.dist < other.dist


def heap_sort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for ii in range(len(h))]