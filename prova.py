from PyQt4 import QtCore, QtGui
from banner import Ui_Banner
from controller import Controller
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time

class Logic(Ui_Banner, QMainWindow):
	def __init__(self, *args, **kwargs):
		QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.move(300, 150)
		self.pushButton.clicked.connect(self.buttonClicked)

	def get_file_name(self):
		filename = QFileDialog.getOpenFileName(self, 'Open file', "Excel files (*.xlsx)")
		return filename

	def buttonClicked(self):
		self.controller = Controller()
		self.controller.load_tensor(str(self.get_file_name()))
		self.controller.show()
		self.hide()




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = Logic()
    MainWindow.show()
    sys.exit(app.exec_())


