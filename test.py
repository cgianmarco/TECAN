import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from view import View 

app = QApplication(sys.argv)
theView = View()
def prova(x):
	print(x)
theView.addChangedStackAction(prova)
theView.changedStackAction(1)



