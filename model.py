import numpy as np

class Tensor:
	def __init__(self, ):
		self.current_depth = 0
		self.current_time = 0

	def change_current_depth(self, value):
		self.current_depth = value

	def change_current_time(self, value):
		self.current_time = value

	def load(self, loadedfile):
		# Wavelengths interval
		self.wl_start = loadedfile['wl_start']
		self.wl_end = loadedfile['wl_end']

		self.depth = loadedfile['depth']
		self.time = loadedfile['time']

		self.data = loadedfile['data']
		self.width = loadedfile['width']
		self.height = loadedfile['height']
		self.selected = { 'start_width':0, 'end_width':0, 'start_height':0, 'end_height':0, 'start_depth':self.wl_start, 'end_depth':self.wl_start, 'start_time':0, 'end_time':0}

	def get_current_matrix(self):
		return self.data[self.current_time][self.current_depth]

	def get_selected(self):
		selected = self.selected
		return selected

	def get_selected_matrix(self, selected):
		start_row = selected['start_width']
		end_row = selected['end_width']
		start_column = selected['start_height']
		end_column = selected['end_height']
		start_depth = selected['start_depth'] - self.wl_start # remove this
		end_depth = selected['end_depth'] - self.wl_start # remove this
		start_time = selected['start_time']
		end_time = selected['end_time']
		return self.data[self.current_time, start_depth:end_depth+1, start_row:end_row+1, start_column:end_column+1]

	def update_selected_matrix(self, result, selected):
		start_row = selected['start_width']
		end_row = selected['end_width']
		start_column = selected['start_height']
		end_column = selected['end_height']
		start_depth = selected['start_depth'] - self.wl_start # remove this
		end_depth = selected['end_depth'] - self.wl_start # remove this
		start_time = selected['start_time']
		end_time = selected['end_time']
		self.data[self.current_time, start_depth:end_depth+1, start_row:end_row+1, start_column:end_column+1] = result

	def get_mean(self, selected):
		return round(self.get_selected_matrix(selected).mean(), 4)

	def get_std(self, selected):
		return round(self.get_selected_matrix(selected).std(), 4)

	def get_current_wl(self):
		return self.wl_start + self.current_depth

	def get_current_time(self):
		return self.current_time

	def update_selected(self, selected):
		self.selected = selected


class Model(object):
	def __init__(self, listener):
		tensor = Tensor()
		self.tensors = {}
		self.currentTensor = ""
		self.values = []
		self.last_index = -1
		self.listener = listener

	def add_value(self, value):
		self.values.append(value)
		self.listener.on_values_list_changed({'values':self.values})

	def add_new_tensor(self, loadedfile):
		self.last_index += 1
		new_key = "Matrix" + str(self.last_index)
		self.tensors[new_key] = Tensor()
		self.currentTensor = new_key
		self.tensors[new_key].load(loadedfile)
		self.listener.on_tensor_loaded({'shape':{"width":self.width, "height":self.height, "depth":self.depth, "time":self.time}})
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl(), "time":self.get_current_time()})
		self.listener.on_selected_changed(self.get_current_tensor().get_selected())
		

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
	def time(self):
		return self.get_current_tensor().time

	@property
	def current_depth(self):
		return self.get_current_tensor().current_depth

	@property
	def current_time(self):
		return self.get_current_tensor().current_time

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

	def get_current_time(self):
		return self.get_current_tensor().get_current_time()

	def get_current_matrix(self):
		return self.get_current_tensor().get_current_matrix()


	def change_current_depth(self, value):
		self.get_current_tensor().change_current_depth(value)
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl(), "time":self.get_current_time()})
		self.listener.on_selected_changed(self.get_current_tensor().get_selected())

	def change_current_time(self, value):
		self.get_current_tensor().change_current_time(value)
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl(), "time":self.get_current_time()})
		self.listener.on_selected_changed(self.get_current_tensor().get_selected())

	def change_current_tensor(self, value):
		self.currentTensor = value
		i = int(value.replace("Matrix", ""))
		self.listener.on_changed_current_tensor({"i":i})

	def get_selected_matrix(self, selected):
		return self.get_current_tensor().get_selected_matrix(selected)

	def update_selected_matrix(self, result, selected):
		self.get_current_tensor().update_selected_matrix(result, selected)
		self.listener.on_matrix_changed({"matrix":self.get_current_matrix(), "wavelength":self.get_current_wl(), "time":self.get_current_time()})
		self.listener.on_selected_changed(self.get_current_tensor().get_selected())

	def get_mean(self, selected):
		return self.get_current_tensor().get_mean(selected)

	def get_std(self, selected):
		return self.get_current_tensor().get_std(selected)

	def subtract(self, x, y):
		return x - y

	def update_selected(self, selected):
		self.get_current_tensor().update_selected(selected)
		self.listener.on_selected_changed(self.get_current_tensor().get_selected())

	