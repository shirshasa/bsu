import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from lab3.Casteljau import casteljau


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(self.size())
        self.show()
        self.points = QtGui.QPolygon()
        self.simple_points = []

    def mousePressEvent(self, e):
        self.points << e.pos()
        self.simple_points = []

        for i in range(self.points.count()):
            self.simple_points.append((self.points.point(i).x(),self.points.point(i).y()))
        self.update()

    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.red, 5)
        brush = QtGui.QBrush(QtCore.Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.points.count()):
            qp.drawEllipse(self.points.point(i), 2, 2)

        line = casteljau(self.simple_points)

        pen = QtGui.QPen(QtCore.Qt.black, 5)
        brush = QtGui.QBrush(QtCore.Qt.black)
        qp.setPen(pen)
        qp.setBrush(brush)

        for point in line:
            qp.drawPoint(point[0],point[1])

        # or
        # qp.drawPoints(self.points)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
