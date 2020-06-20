from PyQt5 import QtWidgets, uic, QtGui, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        uic.loadUi('resources/gui.ui', self)
        self.setWindowIcon(QtGui.QIcon("resources/icon.png"))

        # city input
        self.compare_button = self.findChild(QtWidgets.QPushButton, "compare_button")
        self.city1_input = self.findChild(QtWidgets.QComboBox, "first_city")
        self.city2_input = self.findChild(QtWidgets.QComboBox, "second_city")

        # presentation
        self.browser = self.findChild(QWebEngineView, "ctable")

        self.show()
