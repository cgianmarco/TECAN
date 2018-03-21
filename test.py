import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from view import View 

app = QApplication(sys.argv)
theView = View()
theView.show()
theView.add_new_stack(3,6)
theView.add_new_stack(6,3)
sys.exit(app.exec_())



