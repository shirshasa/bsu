import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QLabel

from lab1.controller import Controller
from lab1.model import generate_base


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.text = ""
        self.left = 500
        self.top = 500
        self.width = 640
        self.height = 480
        self.base = generate_base()
        self.controller = None
        self.aims = None
        self.i = 0
        self.label = QtWidgets.QLabel()
        self.timer = QtCore.QTimer()
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Машина дедуктивного вывода')

        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.label)
        self.setLayout(lay)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

        self.show()

        self.controller = Controller(self.base, self)
        self.aims = self.controller.get_list_aims()

        aim = self.get_choice()
        self.controller.run(aim)

    def get_choice(self):
        items = []
        for item in self.aims:
            items.append(item)
        items = tuple(items)
        item, ok = QInputDialog.getItem(self, "Выберите вопрос", "объект вопроса:", items, 0, False)
        if ok and item:
            return item

    def get_text(self, question):
        items = tuple(self.controller.features[question])
        item, ok = QInputDialog.getItem(self, "Вас просят ответить", "объект вопроса: " + question, items, 0, False)
        if ok and item:
            return item

    def set_text(self, text):
        self.text += text

    def tick(self):
        self.i += 1
        self.label.setText("МАШИНА ДЕДУКТИВНОГО ВЫВОДА \n {}".format(self.text))
        if self.i == 100000000:
            self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
