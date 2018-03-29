from openpyxl import load_workbook
import numpy as np

class FileLoader:
	def __init__(self, filename):
		self.filename = filename
		self.doc = load_workbook(str(filename))
		self.doc.guess_types = False
		self.doc = self.doc['Result sheet']

	def test(self):
		pass

	def parse(self):
		print(self.filename)
		if self.filename == '/home/gianmarco/Desktop/50 ul.xlsx':
			data_starting_line = 35
			wl_start = int(str(self.doc['E24'].value).replace('L', ''))
			wl_end = int(str(self.doc['E25'].value).replace('L', ''))

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

		elif self.filename == '/home/gianmarco/Desktop/200 ul.xlsx':
			data_starting_line = 35
			wl_start = int(str(self.doc['E24'].value).replace('L', ''))
			wl_end = int(str(self.doc['E25'].value).replace('L', ''))

			depth = wl_end - wl_start
			time = 10
			width = 12
			height = 8

			data = np.zeros((time, depth, width, height))

		else:
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


class TwoDimFileLoader:
	def __init__(self, filename):
		self.doc = load_workbook(str(filename))['Result sheet']

	def test(self):
		pass

	def parse(self):
		data_starting_line = 32
		wl_start = 0
		wl_end = 0

		depth = 1
		time = 1

		def filter_empty(value):
			if value == '':
				return 0.0
			else:
				return value

		# Get values
		result = []
		for line in range(data_starting_line + 1, data_starting_line + 9):
			row = list(self.doc[line])
			result.append([ filter_empty(cell.value) for cell in row[1:] ])

		width = 12
		height = 8
		data = np.array(result)
		data = np.expand_dims(data, axis=0)
		data = np.expand_dims(data, axis=0)
		print(data)
		return {"data" : data, 'wl_start' : wl_start, 'wl_end' : wl_end, 'time':time, 'depth': depth, 'width': width, 'height':height}

