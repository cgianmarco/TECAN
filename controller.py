from model import Model
from fileloader import FileLoader, TwoDimFileLoader
from view import View


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


class ViewListener():
	def __init__(self):
		self.model = None

	def add_model(self, model):
		self.model = model

	def on_tensor_load_action(self):
		fileloader = FileLoader(self.view.get_file_name())
		# fileloader = TwoDimFileLoader(self.view.get_file_name())
		self.model.add_new_tensor(fileloader.parse())

	def on_mean_action(self):
		mean = self.model.get_mean(self.view.get_selected())
		self.model.add_value("Mean: " +  str(mean))

	def on_std_action(self):
		std = self.model.get_std(self.view.get_selected())
		self.model.add_value("Std: " +  str(std))

	def on_subtract_action(self):
		v1 = self.model.get_selected_matrix(self.view.get_selected())
		v2 = self.view.get_list_selected()
		result = self.model.subtract(v1, v2)
		self.model.update_selected_matrix(result, self.view.get_selected())


class Controller:
	def __init__(self):
		viewListener = ViewListener()
		self.view = View(viewListener)
		self.model = Model(Listener(self.view))
		viewListener.add_model(self.model)

		self.view.add_move_back_action(self.move_back_action)
		self.view.add_move_forward_action(self.move_forward_action)
		self.view.add_text_changed_action(self.text_changed_action)
		self.view.add_changed_selection_action(self.changed_selection_action)
		self.view.add_changed_stack_action(self.changed_stack_action)
	

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
		print(self.view.get_selected())

	def changed_stack_action(self, i):
		self.model.change_current_tensor("Matrix" + str(i))


