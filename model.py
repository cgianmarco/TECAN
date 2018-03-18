from openpyxl import load_workbook
import numpy as np
import fileloader

class Tensor:
	def __init__(self):
		self.data = np.zeros((10,10,10))
		self.wl_start = 0
		self.wl_end = 0
		self.depth = 0
		self.current_depth = 0
		self.width = 0
		self.height = 0

	def load_matrix(self, filename):
		wb = load_workbook(str(filename))
		wb = wb['Result sheet']

		data_starting_line = 35

		# Wavelengths interval
		self.wl_start = wb['E24'].value
		self.wl_end = wb['E25'].value

		self.depth = self.wl_end - self.wl_start

		# Get values
		result = []
		for i in range(self.wl_end - self.wl_start):
			row = list(wb[data_starting_line + i])
			result.append([ cell.value for cell in row[1:] ])

		self.data = np.array(result).reshape([self.wl_end - self.wl_start, 8,8])
		self.width = len(self.data[0])
		self.height = len(self.data[0][0])

	def get_current_matrix(self):
		return self.data[self.current_depth]

	def get_selected_matrix(self, selected):
		start_row, end_row, start_column, end_column = selected
		return self.data[self.current_depth][start_row:end_row+1, start_column:end_column+1]

	def update_selected_matrix(self, result, selected):
		start_row, end_row, start_column, end_column = selected
		self.data[self.current_depth][start_row:end_row+1, start_column:end_column+1] = result

	def get_mean(self, selected):
		return round(self.get_selected_matrix(selected).mean(), 4)

	def get_std(self, selected):
		return round(self.get_selected_matrix(selected).std(), 4)

	def get_current_wl(self):
		return self.wl_start + self.current_depth




class Model(object):
	def __init__(self):
		tensor = Tensor()
		self.tensors = {"Matrix0" : tensor}
		self.currentTensor = "Matrix0"
		self.last_index = 0
		self.initialized = False

	def add_new_tensor(self, filename):
		if self.initialized == True:
			self.last_index += 1
		else:
			self.initialized = True
		new_key = "Matrix" + str(self.last_index)
		self.tensors[new_key] = Tensor()
		self.tensors[new_key].load_matrix(filename)
		self.currentTensor = new_key

	def remove_tensor(self, key):
		del self.tensors[key]


	############################################
	# Interface with current Tensor properties
	############################################
	@property
	def data(self):
		return self.get_current_tensor().data

	@property
	def wl_start(self):
		return self.get_current_tensor().wl_start

	@property
	def wl_end(self):
		return self.get_current_tensor().wl_end

	@property
	def depth(self):
		return self.get_current_tensor().depth

	@property
	def current_depth(self):
		return self.get_current_tensor().current_depth

	@property
	def width(self):
		return self.get_current_tensor().width

	@property
	def height(self):
		return self.get_current_tensor().height

	@data.setter
	def data(self, value):
		self.get_current_tensor().data = value

	@wl_start.setter
	def wl_start(self, value):
		self.get_current_tensor().wl_start = value

	@wl_end.setter
	def wl_end(self, value):
		self.get_current_tensor().wl_end = value

	@depth.setter
	def depth(self, value):
		self.get_current_tensor().depth = value

	@current_depth.setter
	def current_depth(self, value):
		self.get_current_tensor().current_depth = value

	@width.setter
	def width(self, value):
		self.get_current_tensor().width = value

	@height.setter
	def height(self, value):
		self.get_current_tensor().height = value

	############################################
	# Interface with current Tensor methods
	############################################

	def get_current_tensor(self):
		return self.tensors[self.currentTensor]

	def get_current_wl(self):
		return self.get_current_tensor().get_current_wl()

	def get_current_matrix(self):
		return self.get_current_tensor().get_current_matrix()

	def load_matrix(self, filename):
		self.get_current_tensor().load_matrix(filename)	

	def get_selected_matrix(self, selected):
		return self.get_current_tensor().get_selected_matrix(selected)

	def update_selected_matrix(self, result, selected):
		self.get_current_tensor().update_selected_matrix(result, selected)

	def get_mean(self, selected):
		return self.get_current_tensor().get_mean(selected)

	def get_std(self, selected):
		return self.get_current_tensor().get_std(selected)

	