from model import Model


class Listener:
	def __init__(self, view):
		self.view = view

	def on_tensor_loaded(self, event):
		matrix = event['matrix']
		wavelength = event['wavelength']
		self.view.add_new_stack(len(matrix), len(matrix[0]))

	def on_matrix_changed(self, event):
		matrix = event['matrix']
		wavelength = event['wavelength']
		self.view.update_grid(matrix)
		self.view.update_control_value(wavelength)

	def on_changed_current_tensor(self, event):
		i = event['i']
		self.view.stacked_widget.setCurrentIndex(i)
		self.view.current_stack = "Matrix" + str(i)



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
		

	def tensor_load_action(self):
		fname = self.view.get_file_name()
		self.model.add_new_tensor(fname)

	def remove_zero_matrix(self):
		self.view.stackList.takeItem(0)

	def mean_action(self):
		mean = self.model.get_mean(self.view.get_selected())
		self.view.listValue.addItem("Mean: " +  str(mean))

	def std_action(self):
		std = self.model.get_std(self.view.get_selected())
		self.view.listValue.addItem("Std: " +  str(std))

	def subtract_action(self):
		v1 = self.model.get_selected_matrix(self.view.get_selected())
		v2 = self.view.get_list_selected()
		result = v1 - v2
		self.update_selected_grid(result)

	def move_back_action(self):
		if self.model.current_depth > 0:
			self.model.change_current_depth(self.model.current_depth - 1)

	def move_forward_action(self):
		if self.model.current_depth < self.model.depth - 1:
			self.model.change_current_depth(self.model.current_depth + 1)

	def update_selected_grid(self, result):
		self.model.update_selected_matrix(result, self.view.get_selected())

	def text_changed_action(self, text):
		try:
			value = int(text)
			if self.model.wl_start <= value < self.model.wl_end:
				self.model.change_current_depth(value - self.model.wl_start)
		except ValueError:
			pass

	def changed_selection_action(self):
		start_row, end_row, start_column, end_column = [ elem for elem in self.view.get_selected()]
		for elem in self.view.datagrid.values():
			elem.setStyleSheet("color: rgb(76,76,76);")

		if start_row <= end_row and start_column <= end_column:
			for i in range(start_row, end_row+1):
				for j in range(start_column, end_column+1):
					self.view.datagrid[(i,j)].setStyleSheet("color: rgb(255, 0, 255);")

	def changed_stack_action(self, i):
		self.model.change_current_tensor("Matrix" + str(i))


