from openpyxl import load_workbook
import numpy as np

class Model:
	def __init__(self):
		self.data = np.zeros((10,8,8))
		self.storedValues = {}
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

