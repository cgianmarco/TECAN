import numpy as np

class Tensor:
	def __init__(self, ):
		self.data = np.zeros((10,10,10))
		self.wl_start = 0
		self.wl_end = 0
		self.depth = 0
		self.current_depth = 0
		self.width = 0
		self.height = 0

	def change_current_depth(self, value):
		self.current_depth = value

	def load(self, loadedfile):
		# Wavelengths interval
		self.wl_start = loadedfile['wl_start']
		self.wl_end = loadedfile['wl_end']

		self.depth = loadedfile['depth']

		self.data = loadedfile['data']
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
	def __init__(self, listener):
		tensor = Tensor()
		self.tensors = {}
		self.currentTensor = ""
		self.last_index = 0
		self.initialized = False
		self.listener = listener

	def add_new_tensor(self, loadedfile):
		self.last_index += 1
		new_key = "Matrix" + str(self.last_index)
		self.tensors[new_key] = Tensor()
		self.currentTensor = new_key
		self.tensors[new_key].load(loadedfile)
		self.listener.on_tensor_loaded({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl()})
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl()})
		

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


	def change_current_depth(self, value):
		self.get_current_tensor().change_current_depth(value)
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl()})

	def change_current_tensor(self, value):
		self.currentTensor = value
		print(self.tensors.keys())
		i = int(value.replace("Matrix", ""))
		self.listener.on_changed_current_tensor({"i":i})


	def get_selected_matrix(self, selected):
		return self.get_current_tensor().get_selected_matrix(selected)

	def update_selected_matrix(self, result, selected):
		self.get_current_tensor().update_selected_matrix(result, selected)
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl()})

	def get_mean(self, selected):
		return self.get_current_tensor().get_mean(selected)

	def get_std(self, selected):
		return self.get_current_tensor().get_std(selected)

	