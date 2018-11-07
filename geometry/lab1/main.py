import math

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor


MAX_X = 500
MAX_Y = 640


class Example(QWidget):

    def __init__(self, d, p):
        super().__init__()
        self.init_ui()
        self.dots = d
        self.lines = p

    def init_ui(self):
        self.setGeometry(300, 300, MAX_X, MAX_Y)
        self.setWindowTitle('window')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        colors = [Qt.red, Qt.blue, Qt.green, Qt.gray, Qt.darkYellow]
        index = -1
        for line in self.lines:
            index += 1
            pen = QPen(colors[index], 2, Qt.SolidLine)
            self.draw_line(qp, line, pen)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        qp.setPen(pen)
        size = self.size()

        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)

        for (x, y) in self.dots:
            qp.drawPoint(x, MAX_Y - y)

    def draw_line(self, qp, points, pen):
        qp.setPen(pen)
        for ((x, y), (v, w)) in points:
            b = math.fabs(v - x)
            a = math.fabs(w - y)
            if math.tan(1.39626) < a / b:
                pen2 = QPen(Qt.black, 3, Qt.SolidLine)
                qp.setPen(pen2)

                #qp.drawLine(x, MAX_Y - y, v, MAX_Y - w)
                qp.setPen(pen)
            else:
                qp.drawLine(x, MAX_Y - y, v, MAX_Y - w)

