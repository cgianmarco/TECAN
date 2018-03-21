import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from view import View 

app = QApplication(sys.argv)
theView = View()
theView.show()
sys.exit(app.exec_())



