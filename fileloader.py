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

		# Get values
		result = []
		for i in range(depth):
			row = list(self.doc[data_starting_line + i])
			result.append([ cell.value for cell in row[1:] ])

		data = np.array(result).reshape([depth, 8,8])
		return {"data" : data, 'wl_start' : wl_start, 'wl_end' : wl_end, 'depth': depth}

