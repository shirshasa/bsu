"""

triangle_unsorted = []

for t, index in zip(tri_delaunay.simplices, range(len(tri_delaunay.simplices))):
    t_obj = Triangle(points_[t], index, t, polygon_)
    triangle_unsorted.append(t_obj)

sorted_t = heap_sort(triangle_unsorted)
visited_t = []
neighbors = tri_delaunay.neighbors

PRE_FINAL = []
for i in range(len(sorted_t)):
    if i in visited_t: continue
    t1 = sorted_t[i]
    visited_t.append(i)

    for j in range(1, len(sorted_t)):
        if j not in visited_t:
            t2 = sorted_t[j]
            t1_points = t1.points
            t2_points = t2.points
            same = [point for point in t1_points if point in t2_points]
            if len(same) == 2:
                visited_t.append(j)
                quad = set()
                x = []
                y = []
                for point in t1_points:
                    quad.add(tuple(point))
                    x.append(point[0])
                    y.append(point[1])
                for point in t2_points:
                    quad.add(tuple(point))
                    x.append(point[0])
                    y.append(point[1])

                plt.plot(x,y,color = 'orange')
                plt.show()

                PRE_FINAL.append(quad)
                break

FINAL = []
for ppp in PRE_FINAL:
    conved_points = make_conv(list(ppp))
    FINAL.append(conved_points)
    print(len(ppp), ppp)

for quad in PRE_FINAL:
    edged_quad = vertex_list_to_edge(list(quad))
    for edge_ in edged_quad:
        plt.plot([edge_[0][0], edge_[1][0]], [edge_[0][1], edge_[1][1]], color='pink')

plt.show()
"""