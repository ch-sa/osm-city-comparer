from PyQt5 import QtWidgets, uic, QtGui, QtWebEngineWidgets


class Gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        uic.loadUi('resources/gui.ui', self)
        self.setWindowIcon(QtGui.QIcon("resources/icon.png"))

        self.show()
