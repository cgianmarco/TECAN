import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from controller import Controller
import numpy as np



def test():
	app = QApplication(sys.argv)
	controller = Controller()


	controller.view.listener.on_tensor_load('/home/gianmarco/Desktop/50 ul.xlsx')


	selected = {}
	selected['start_width'] = 0
	selected['end_width'] = 3
	selected['start_height'] = 0
	selected['end_height'] = 3
	selected['start_depth'] = 0
	selected['end_depth'] = 2
	selected['start_time'] = 0
	selected['end_time'] = 0

	controller.view.listener.on_changed_selection(selected)



	controller.view.listener.on_mean_action(selected)

	controller.view.listValue.setCurrentRow(0)

	controller.view.listener.on_subtract_action(selected, controller.view.get_list_selected())

	expected_result = np.array([[[[ 0.0756,  0.0037, -0.0342, -0.0482],
  						[ 0.0786,  0.008,  -0.0312, -0.0496],
  						[ 0.0818,  0.003,  -0.0289, -0.0513],
  						[ 0.075,   0.0069, -0.038,  -0.0489]],

 						[[ 0.0755,  0.0034, -0.0342, -0.0486],
  						[ 0.078,   0.0078, -0.0315, -0.0495],
  						[ 0.0813,  0.0023, -0.0293, -0.0516],
  						[ 0.0747,  0.0071, -0.0381, -0.0489]],

 						[[ 0.0756,  0.0041, -0.0339, -0.0483],
  						[ 0.0769,  0.0083, -0.0309, -0.0491],
  						[ 0.0804,  0.0024, -0.0293, -0.0506],
  						[ 0.0744,  0.0062, -0.0379, -0.0479]]]])

	expected_result = np.transpose(expected_result, (0,1,3,2))
	np.testing.assert_allclose(controller.model.get_selected_matrix(selected), expected_result)



test()



