import sys

from PyQt5 import QtWidgets

from gui import Gui

app = QtWidgets.QApplication(sys.argv)

# Load GUI
window = Gui()
# model = Model()
# control = Control(model, window)

# Execute application
app.exec()
