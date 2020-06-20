import sys

from PyQt5 import QtWidgets

from comparer import Comparer
from gui import Gui

app = QtWidgets.QApplication(sys.argv)

# Load GUI
window = Gui()
comparer = Comparer(window)

# Execute application
app.exec()
