from scipy.spatial import Delaunay
from scipy.spatial.qhull import Voronoi
import matplotlib.pyplot as plt
import numpy as np

from lab2.Triangle import Triangle, heap_sort
from lab2.generate_polygon import generatePolygon
from lab2.polygon_draw import draw_polygons
from lab2.MYSTAT import count_angles
from lab2.sutherland_hodgman import get_cut
from lab2.utils import vertex_list_to_edge
from lab2.utils import poly_centroid

big_window = [(-5, -5), (5, -5), (5, 5), (-5, 5)]
window_req = [(0, 0), (1, 0), (1, 1), (0, 1)]
WINDOW_SIZE = 5
polygon_ = generatePolygon(0, 0, 5, 0, 0 ,4)
window = vertex_list_to_edge(polygon_)


def voronoi(points, to_plot=False, WINDOW_SIZE=5, width=1):
    vor = Voronoi(points)

    if to_plot:
        arr_temp = np.array(polygon_)

        plt.plot(arr_temp[:, 0], arr_temp[:, 1], 'o', color='green', alpha = 0.5, linewidth = width)
        plt.plot(points[:, 0], points[:, 1], 'o', color='green', alpha = 0.5, linewidth = width)
        # plt.plot(vor.vertices[:, 0], vor.vertices[:, 1], '*')
        '''
        fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
                              line_width=2, line_alpha=0.6, point_size=2)
        '''

    for simplex in vor.ridge_vertices:

        simplex = np.asarray(simplex)

        if to_plot and np.all(simplex >= 0):
            plt.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-', color = 'black', linewidth = width)

            for edge in window:
                plt.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], color='green', alpha = 0.6, linewidth = width)


    '''
    find finite regions
    '''
    finite_regions = []
    for reg in vor.regions:
        if -1 not in reg and len(reg):
            finite_regions.append(reg)
    '''
    cut regions with square window 
    '''
    cut_regions = []
    for reg in finite_regions:
        l = vor.vertices[reg]
        if to_plot: plt.plot(l[:,0],l[:,1], color='black')
        cut_regions.append(get_cut(vor.vertices[reg].tolist(), window))

    if to_plot:   draw_polygons(cut_regions)

    centroids = []
    for reg in cut_regions:
        centroids.append(poly_centroid(reg))
    centroids = np.array(centroids)

    if to_plot:
        plt.plot(centroids[:, 0], centroids[:, 1], 'o', color='green', alpha = 0.6, linewidth = width)
        plt.xlim((-1) * WINDOW_SIZE, WINDOW_SIZE)
        plt.ylim((-1) * WINDOW_SIZE, WINDOW_SIZE)
        plt.show()
        return centroids, cut_regions

    return centroids


# start with random points #######################################################################
points_ = np.random.rand(80, 2)

for i in range(225):

    points_ = np.append(points_, polygon_, axis=0)
    if i in [0, 1]:
        points_ = voronoi(points_, False)
    else:
        points_ = voronoi(points_)

points_ = np.append(points_, polygon_, axis=0)
points_ = np.append(points_, big_window, axis=0)
points_, regions = voronoi(points_, True)
points_ = np.append(points_, polygon_, axis=0)

tri_delaunay = Delaunay(points_)

plt.triplot(points_[:, 0], points_[:, 1], tri_delaunay.simplices.copy())
arr_temp = np.array(polygon_)
plt.plot(arr_temp[:, 0], arr_temp[:, 1], 'o', color='black')
plt.show()


triangle_unsorted = []

for t, index in zip(tri_delaunay.simplices, range(len(tri_delaunay.simplices))):
    t_obj = Triangle(points_[t], index, t, polygon_)
    triangle_unsorted.append(t_obj)

sorted_t = heap_sort(triangle_unsorted)

HUINYA = []
for t in sorted_t:
    HUINYA.extend(count_angles(t.points))

n, bins, patches = plt.hist(HUINYA,  alpha=0.4,bins = 10, color = "skyblue")
cm = plt.cm.get_cmap('RdYlBu_r')
# To normalize your values
col = (n-n.min())/(n.max()-n.min())
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
plt.show()

'''
сортируем по близости  к центру масс полигона их центр масс
стекаем треугольники
поп треугольник 
если у него есть сосед 
выбираем с самым ок характеристикой
если нет - осталвляем

метрика - считаем углы 
считаем оставшиеся треугольники
'''
