import sys

from PyQt5 import QtWidgets

from comparecities.comparer import Comparer
from comparecities.gui import Gui


def run_app():
    app = QtWidgets.QApplication(sys.argv)

    # Load GUI
    window = Gui()
    comparer = Comparer(window)

    # Execute application
    app.exec()
