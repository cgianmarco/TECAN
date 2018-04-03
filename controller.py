from model import Model
from view import View
from fileloader import *
from filesaver import *


class Listener:
	def __init__(self, view):
		self.view = view

	def on_tensor_loaded(self, event):
		shape = event['shape']
		axis_values = event['axis_values']
		# self.view.add_new_stack(shape)
		self.view.add_new_stack(shape, axis_values)

	def on_matrix_changed(self, event):
		matrix = event['matrix']
		depth = event['wavelength']
		time = event['time']
		self.view.update_grid(matrix)
		self.view.update_control_value('depth', depth)
		self.view.update_control_value('time', time)

	def on_changed_current_tensor(self, event):
		i = event['i']
		self.view.set_stack_index(i)

	def on_values_list_changed(self, event):
		values = event['values']
		self.view.update_values_list(values)

	def on_selected_changed(self, event):
		self.view.clear_datagrid_color()
		selected = event
		self.view.update_datagrid_color(selected)


class ViewListener():
	def __init__(self):
		self.model = None

	def add_model(self, model):
		self.model = model

	def on_tensor_load(self, filename):
		fileloader = FileLoader(filename)
		# fileloader = TwoDimFileLoader()
		# fileloader = ThreeDimFileLoader()
		for tensor in fileloader.parse():
			self.model.add_new_tensor(tensor)

	def on_mean_action(self, selected):
		mean = self.model.get_mean(selected)
		self.model.add_value("Mean: " +  str(mean))

	def on_std_action(self, selected):
		std = self.model.get_std(selected)
		self.model.add_value("Std: " +  str(std))

	def on_subtract_action(self, selected, value):
		v1 = self.model.get_selected_matrix(selected)
		v2 = value
		result = self.model.subtract(v1, v2)
		self.model.update_selected_matrix(result, selected)

	def on_move_back(self, dim):
		if dim == 'depth':
			if self.model.current_depth > 0:
				self.model.change_current_depth(self.model.current_depth - 1)
		if dim == 'time':
			if self.model.current_time > 0:
				self.model.change_current_time(self.model.current_time - 1)

	def on_move_forward(self, dim):
		
		if dim == 'depth':
			if self.model.current_depth < self.model.depth - 1:
				self.model.change_current_depth(self.model.current_depth + 1)
		if dim == 'time':
			if self.model.current_time < self.model.time - 1:
				self.model.change_current_time(self.model.current_time + 1)

	def on_text_changed(self, text, dim, axis_values):
		try:
			value = int(text)
			if axis_values[0] <= value <= axis_values[:1]:
				self.model.change_current_dim(dim, value - axis_values[0])
		except ValueError:
			pass

	def on_changed_selection(self, selected):
		self.model.update_selected(selected)

	def on_changed_stack(self, i):
		self.model.change_current_tensor("Tensor" + str(i))

	def on_export_current_matrix(self):
		exporter = Exporter()
		exporter.export_two_dim_matrix(self.model.get_current_matrix(), self.model.currentTensor)






class Controller:
	def __init__(self):
		viewListener = ViewListener()
		self.view = View(viewListener)
		self.model = Model(Listener(self.view))
		viewListener.add_model(self.model)
		


