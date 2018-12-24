

def casteljau(points):
    NEW_POINTS = []
    n = len(points)
    if n < 3: return [(3, 3)]

    def B(coor_arr, i, j, t):
        if j == 0:
            return coor_arr[i]
        return B(coor_arr, i, j - 1, t) * (1 - t) + B(coor_arr, i + 1, j - 1, t) * t

    coordinates_X = []
    coordinates_Y = []
    for k in range(len(points)):
        x = points[k][0]
        y = points[k][1]
        coordinates_X.append(x)
        coordinates_Y.append(y)

    # plot the curve
    numSteps = 100
    for k in range(numSteps):
        t = float(k) / (numSteps - 1)
        x = int(B(coordinates_X, 0, n - 1, t))
        y = int(B(coordinates_Y, 0, n - 1, t))

        NEW_POINTS.append((x, y))

    return NEW_POINTS
