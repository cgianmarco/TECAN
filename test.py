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

#########################
# Tests listener
#########################
# When on_action gets called
# View changes in the right way

# self.view.update_control_value('depth', value)
# assert(int(self.view.control_value['depth'].text()) == value)



#########################
# Tests Controller
#########################
# When action gets called
# Model changes in the right way


#########################



