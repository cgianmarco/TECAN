import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from view import View
from model import Model
from controller import Controller

def main():
	app = QApplication(sys.argv)
	theView = View()

	theController = Controller(theView)
	theView.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()