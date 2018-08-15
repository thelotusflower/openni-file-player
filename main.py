import gui
import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = gui.Player()
app.exec()
sys.exit()
