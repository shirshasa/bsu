import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPolygon


from lab0.conv import make_conv
from lab1.algo import get_structure, build_graph, point_location
from lab2.generate_polygon import generatePolygon

MAX_X = 500
MAX_Y = 640


class Canvas(QWidget):

    def __init__(self, d):
        super().__init__()
        self.init_ui()
        self.points = d
        ll = []
        self.s = get_structure(ll, self.points)
        self.T = build_graph(self.s)

        self.cur_point = (234, 566)

    def init_ui(self):

        self.setGeometry(300, 300, MAX_X, MAX_Y)
        self.setWindowTitle('window')

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.show()

    def mousePressEvent(self, e):
        p = e.pos()
        self.cur_point = (p.x(), p.y())

        print('cur point', self.cur_point)
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        colors = [Qt.red, Qt.blue, Qt.black, Qt.gray, Qt.darkYellow]

        for ss in self.s[0]:
            self.draw_polygon(qp, ss, colors[2])

        res = point_location(self.cur_point, self.T)
        if res :
            self.draw_polygon(qp, res, colors[0])
        print('res', res)

        self.draw_points(qp, self.points)
        qp.end()

    def draw_points(self, qp, points):
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        qp.setPen(pen)

        for x in range(0, MAX_X, 10):
            qp.drawPoint(x, MAX_Y)

        for y in range(0, MAX_Y, 10):
            qp.drawPoint(MAX_X, y)

        for (x, y) in points:
            qp.drawPoint(x, y)

    def draw_conv(self, qp, points_):
        pen = QPen(Qt.black, 5, Qt.SolidLine)
        qp.setPen(pen)
        points_conv = make_conv(points_)
        points = []
        for (x, y) in points_conv:
            points.append(QPoint(x, y))
        needle = QPolygon(points)
        qp.drawPolygon(needle)

    def draw_polygon(self, qp, polygon, color = Qt.black):
        pen = QPen(color, 5, Qt.SolidLine)
        qp.setPen(pen)
        points = []
        for x,y in polygon:
            points.append((QPoint(x,y)))
        polygon_to_draw = QPolygon(points)
        qp.drawPolygon(polygon_to_draw)


if __name__ == '__main__':
    file = open('dots.txt', 'r').read()
    prep_str = file.strip(' ').split('), (')
    prep_str = [x.lstrip('(') for x in prep_str]
    prep_str = [x.rstrip(')\n') for x in prep_str]
    dots = []
    for pair in prep_str:
        (x, y) = pair.split(', ')
        dots.append((float(x), float(y)))

    polygon = generatePolygon(MAX_X/2, MAX_Y/2, 100, 0, 0, 26)

    app = QApplication(sys.argv)
    ex = Canvas(polygon)
    sys.exit(app.exec_())
