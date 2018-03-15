from openpyxl import load_workbook
import numpy as np

class Tensor:
	def __init__(self):
		self.data = np.zeros((10,10,10))
		self.wl_start = 0
		self.wl_end = 0
		self.maxDepth = 0
		self.currentDepth = 0
		self.width = 0
		self.height = 0

	def load_matrix(self, filename):
		wb = load_workbook(str(filename))
		wb = wb['Result sheet']

		data_starting_line = 35

		# Wavelengths interval
		self.wl_start = wb['E24'].value
		self.wl_end = wb['E25'].value

		self.maxDepth = self.wl_end - self.wl_start

		# Get values
		result = []
		for i in range(self.wl_end - self.wl_start):
			row = list(wb[data_starting_line + i])
			result.append([ cell.value for cell in row[1:] ])

		self.data = np.array(result).reshape([self.wl_end - self.wl_start, 8,8])
		self.width = len(self.data[0])
		self.height = len(self.data[0][0])

	def getCurrentMatrix(self):
		return self.data[self.currentDepth]

	def getSelectedMatrix(self, selected):
		startRow, endRow, startColumn, endColumn = selected
		return self.data[self.currentDepth][startRow:endRow+1, startColumn:endColumn+1]

	def updateSelectedMatrix(self, result, selected):
		startRow, endRow, startColumn, endColumn = selected
		self.data[self.currentDepth][startRow:endRow+1, startColumn:endColumn+1] = result

	def getMean(self, selected):
		return round(self.getSelectedMatrix(selected).mean(), 4)

	def getStd(self, selected):
		return round(self.getSelectedMatrix(selected).std(), 4)

	def getCurrentWL(self):
		return self.wl_start + self.currentDepth




class Model(object):
	def __init__(self):
		tensor = Tensor()
		self.tensors = {"Matrix0" : tensor}
		self.currentTensor = "Matrix0"
		self.lastIndex = 0
		self.initialized = False

	def addNewTensor(self, filename):
		if self.initialized == True:
			self.lastIndex += 1
		else:
			self.initialized = True
		newKey = "Matrix" + str(self.lastIndex)
		self.tensors[newKey] = Tensor()
		self.tensors[newKey].load_matrix(filename)
		self.currentTensor = newKey

	def removeTensor(self, key):
		del self.tensors[key]

	@property
	def data(self):
		return self.getCurrentTensor().data

	@property
	def wl_start(self):
		return self.getCurrentTensor().wl_start

	@property
	def wl_end(self):
		return self.getCurrentTensor().wl_end

	@property
	def maxDepth(self):
		return self.getCurrentTensor().maxDepth

	@property
	def currentDepth(self):
		return self.getCurrentTensor().currentDepth

	@property
	def width(self):
		return self.getCurrentTensor().width

	@property
	def height(self):
		return self.getCurrentTensor().height

	@data.setter
	def data(self, value):
		self.getCurrentTensor().data = value

	@wl_start.setter
	def wl_start(self, value):
		self.getCurrentTensor().wl_start = value

	@wl_end.setter
	def wl_end(self, value):
		self.getCurrentTensor().wl_end = value

	@maxDepth.setter
	def maxDepth(self, value):
		self.getCurrentTensor().maxDepth = value

	@currentDepth.setter
	def currentDepth(self, value):
		self.getCurrentTensor().currentDepth = value

	@width.setter
	def width(self, value):
		self.getCurrentTensor().width = value

	@height.setter
	def height(self, value):
		self.getCurrentTensor().height = value

	# def __getattr__(self, name):
	# 	return getattr(self.getCurrentTensor(), name)

	def getCurrentTensor(self):
		return self.tensors[self.currentTensor]

	def load_matrix(self, filename):
		self.getCurrentTensor().load_matrix(filename)

	def getCurrentMatrix(self):
		return self.getCurrentTensor().getCurrentMatrix()

	def getSelectedMatrix(self, selected):
		return self.getCurrentTensor().getSelectedMatrix(selected)

	def updateSelectedMatrix(self, result, selected):
		self.getCurrentTensor().updateSelectedMatrix(result, selected)

	def getMean(self, selected):
		return self.getCurrentTensor().getMean(selected)

	def getStd(self, selected):
		return self.getCurrentTensor().getStd(selected)

	def getCurrentWL(self):
		return self.getCurrentTensor().getCurrentWL()