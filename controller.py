from model import Model
from fileloader import FileLoader, TwoDimFileLoader


class Listener:
	def __init__(self, view):
		self.view = view

	def on_tensor_loaded(self, event):
		shape = event['shape']
		self.view.add_new_stack(shape)

	def on_matrix_changed(self, event):
		matrix = event['matrix']
		wavelength = event['wavelength']
		time = event['time']
		self.view.update_grid(matrix)
		self.view.update_control_value('depth', wavelength)
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





class Controller:
	def __init__(self, view):
		self.view = view
		self.model = Model(Listener(view))

		self.view.add_tensor_load_action(self.tensor_load_action)
		self.view.add_mean_action(self.mean_action)
		self.view.add_std_action(self.std_action)
		self.view.add_subtract_action(self.subtract_action)
		self.view.add_move_back_action(self.move_back_action)
		self.view.add_move_forward_action(self.move_forward_action)
		self.view.add_text_changed_action(self.text_changed_action)
		self.view.add_changed_selection_action(self.changed_selection_action)
		self.view.add_changed_stack_action(self.changed_stack_action)
		# self.view.changed_stack_action(1)
		# self.view.stackList.currentRowChanged.connect(self.changed_stack_action)
		
	#This should be tensor_load_action(self, filename)
	def tensor_load_action(self, filename):
		fileloader = FileLoader(filename)
		# fileloader = TwoDimFileLoader(self.view.get_file_name())
		self.model.add_new_tensor(fileloader.parse())

	# This should be method(selected)
	def mean_action(self, selected):
		mean = self.model.get_mean(selected)
		self.model.add_value("Mean: " +  str(mean))

	# This should be method(selected)
	def std_action(self, selected):
		std = self.model.get_std(selected)
		self.model.add_value("Std: " +  str(std))

	# This should be subtract_action(selected, selected_value)
	def subtract_action(self, selected, value):
		v1 = self.model.get_selected_matrix(selected)
		v2 = value
		result = self.model.subtract(v1, v2)
		self.model.update_selected_matrix(result, self.view.get_selected())

	def move_back_action(self, dim):
		if dim == 'depth':
			if self.model.current_depth > 0:
				self.model.change_current_depth(self.model.current_depth - 1)
		if dim == 'time':
			if self.model.current_time > 0:
				self.model.change_current_time(self.model.current_time - 1)

	def move_forward_action(self, dim):
		
		if dim == 'depth':
			if self.model.current_depth < self.model.depth - 1:
				self.model.change_current_depth(self.model.current_depth + 1)
		if dim == 'time':
			if self.model.current_time < self.model.time - 1:
				self.model.change_current_time(self.model.current_time + 1)

	def text_changed_action(self, text):
		try:
			value = int(text)
			if self.model.wl_start <= value < self.model.wl_end:
				self.model.change_current_depth(value - self.model.wl_start)
		except ValueError:
			pass

	def changed_selection_action(self):
		self.model.update_selected(self.view.get_selected())

	def changed_stack_action(self, i):
		self.model.change_current_tensor("Matrix" + str(i))


