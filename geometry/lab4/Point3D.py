import sys, math, pygame


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

    def project2(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        z = self.z * factor + win_height / 2
        return Point3D(x, y, z)

    def isometric(self):
        a = [[3 ** 0.5, 0, -1 * (3 ** 0.5)],
             [1, 2, 1],
             [2 ** 0.5, -1 * (2 ** 0.5), 2 ** 0.5]]

        x = (1 / (6 ** 0.5)) * (a[0][0] * self.x + a[0][1] * self.y + a[0][2] * self.z)
        y = (1 / (6 ** 0.5)) * (a[1][0] * self.x + a[1][1] * self.y + a[1][2] * self.z)
        z = (1 / (6 ** 0.5)) * (a[2][0] * self.x + a[2][1] * self.y + a[2][2] * self.z)

        return Point3D(int(x), int(y), int(z))


