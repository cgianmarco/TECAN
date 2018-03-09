class Controller:
	def __init__(self, view, model):
		self.view = view
		self.model = model

		self.view.addMatrixLoadAction(self.matrixLoadAction)
		self.view.addMeanAction(self.meanAction)
		self.view.addStdAction(self.stdAction)
		self.view.addSubtractAction(self.subtractAction)
		self.view.addMoveBackAction(self.moveBackAction)
		self.view.addMoveForwardAction(self.moveForwardAction)
		self.view.addTextChangedAction(self.textChangedAction)
		self.view.addChangedSelectionAction(self.changedSelectionAction)

	def matrixLoadAction(self):
		fname = self.view.getFileName()
		self.model.load_matrix(fname)
		self.view.setDimensions(self.model.width, self.model.height)
		self.view.initUI()
		self.view.updateGrid(self.model.getCurrentMatrix())
		self.view.updateControlValue(self.model.getCurrentWL())

	def meanAction(self):
		mean = self.model.getMean(self.view.getSelected())
		self.view.listValue.addItem("Mean: " +  str(mean))

	def stdAction(self):
		std = self.model.getStd(self.view.getSelected())
		self.view.listValue.addItem("Std: " +  str(std))

	def subtractAction(self):
		v1 = self.model.getSelectedMatrix(self.view.getSelected())
		v2 = self.view.getListSelected()
		result = v1 - v2
		print(result[0][0])
		self.updateSelectedGrid(result)

	def moveBackAction(self):
		if self.model.currentDepth > 0:
			self.model.currentDepth -= 1
			self.view.updateGrid(self.model.getCurrentMatrix())
			self.view.updateControlValue(self.model.getCurrentWL())

	def moveForwardAction(self):
		if self.model.currentDepth < self.model.maxDepth - 1:
			self.model.currentDepth += 1
			self.view.updateGrid(self.model.getCurrentMatrix())
			self.view.updateControlValue(self.model.getCurrentWL())

	def updateSelectedGrid(self, result):
		self.model.updateSelectedMatrix(result, self.view.getSelected())
		self.view.updateGrid(self.model.getCurrentMatrix())

	def textChangedAction(self, text):
		try:
			value = int(text)
			if self.model.wl_start <= value < self.model.wl_end:
				self.model.currentDepth = value - self.model.wl_start
				self.view.updateGrid(self.model.getCurrentMatrix())
		except ValueError:
			pass

	def changedSelectionAction(self):
		startRow, endRow, startColumn, endColumn = [ elem for elem in self.view.getSelected()]
		for elem in self.view.dataGrid.values():
			elem.setStyleSheet("color: rgb(76,76,76);")

		if startRow <= endRow and startColumn <= endColumn:
			for i in range(startRow, endRow+1):
				for j in range(startColumn, endColumn+1):
					self.view.dataGrid[(i,j)].setStyleSheet("color: rgb(255, 0, 255);")


