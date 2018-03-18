class Controller:
	def __init__(self, view, model):
		self.view = view
		self.model = model

		self.view.add_matrix_load_action(self.matrix_load_action)
		self.view.add_mean_action(self.mean_action)
		self.view.add_std_action(self.std_action)
		self.view.add_subtract_action(self.subtract_action)
		self.view.add_move_back_action(self.move_back_action)
		self.view.add_move_forward_action(self.move_forward_action)
		self.view.add_text_changed_action(self.text_changed_action)
		self.view.add_changed_selection_action(self.changed_selection_action)
		self.view.addchanged_stack_action(self.changed_stack_action)
		# self.view.changed_stack_action(1)
		# self.view.stackList.currentRowChanged.connect(self.changed_stack_action)
		

	def matrix_load_action(self):
		fname = self.view.get_file_name()
		self.model.add_new_tensor(fname)
		self.view.set_dimensions(self.model.width, self.model.height)
		self.view.add_new_stack(self.model.width, self.model.height)
		# self.view.init_ui()
		self.view.update_grid(self.model.get_current_matrix())
		self.view.update_control_value(self.model.get_current_wl())

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
		print(result[0][0])
		self.update_selected_grid(result)

	def move_back_action(self):
		if self.model.current_depth > 0:
			self.model.current_depth -= 1
			self.view.update_grid(self.model.get_current_matrix())
			self.view.update_control_value(self.model.get_current_wl())

	def move_forward_action(self):
		if self.model.current_depth < self.model.depth - 1:
			self.model.current_depth += 1
			self.view.update_grid(self.model.get_current_matrix())
			self.view.update_control_value(self.model.get_current_wl())

	def update_selected_grid(self, result):
		self.model.update_selected_matrix(result, self.view.get_selected())
		self.view.update_grid(self.model.get_current_matrix())

	def text_changed_action(self, text):
		try:
			value = int(text)
			if self.model.wl_start <= value < self.model.wl_end:
				self.model.current_depth = value - self.model.wl_start
				self.view.update_grid(self.model.get_current_matrix())
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
		self.view.stackedWidget.setCurrentIndex(i)
		self.view.currentStack = "Matrix" + str(i)
		self.model.currentTensor = "Matrix" + str(i)
		print(self.model.currentTensor)
		print(self.view.currentStack)
		for tensor in self.model.tensors.values():
			print(tensor.data.shape)


