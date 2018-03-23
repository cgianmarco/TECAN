from openpyxl import load_workbook
import numpy as np

class FileLoader:
	def __init__(self, filename):
		self.doc = load_workbook(str(filename))['Result sheet']

	def test(self):
		pass

	def parse(self):
		data_starting_line = 35
		wl_start = self.doc['E24'].value
		wl_end = self.doc['E25'].value

		depth = wl_end - wl_start
		time = 1

		# Get values
		result = []
		for i in range(depth):
			row = list(self.doc[data_starting_line + i])
			result.append([ cell.value for cell in row[1:] ])

		width = 8
		height = 8
		data = np.array(result).reshape([1, depth, width, height])
		return {"data" : data, 'wl_start' : wl_start, 'wl_end' : wl_end, 'time':time, 'depth': depth, 'width': width, 'height':height}


class TwoDimFileLoader:
	def __init__(self, filename):
		self.doc = load_workbook(str(filename))['Result sheet']

	def test(self):
		pass

	def parse(self):
		data_starting_line = 35
		wl_start = 0
		wl_end = 0

		depth = 1
		time = 1

		# Get values
		result = []
		row = list(self.doc[data_starting_line])
		result.append([ cell.value for cell in row[1:] ])

		width = 8
		height = 8
		data = np.array(result).reshape([1, depth, width, height])
		return {"data" : data, 'wl_start' : wl_start, 'wl_end' : wl_end, 'time':time, 'depth': depth, 'width': width, 'height':height}

