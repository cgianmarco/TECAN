from openpyxl import load_workbook
import numpy as np

def filter_empty(value):
			if value == '':
				return 0.0
			else:
				return value

def get_two_dim_matrix(doc, data_starting_line):
	result = []
	for line in range(data_starting_line + 1, data_starting_line + 9):
		row = list(doc[line])
		result.append([ filter_empty(cell.value) for cell in row[1:] ])
	return result

def get_dims(doc, data_starting_line):
	data_starting_line -= 1
	width = len([cell for cell in doc[data_starting_line][1:] if 'A' in cell.value])
	height = len(doc[data_starting_line][1:])/width
	return width, height





class FileLoader:
	def __init__(self, filename):
		self.filename = filename
		self.doc = load_workbook(str(filename))
		self.filetypes = [ ODSpectrum(), ODSingle(), ODTime()]
		self.doc = self.doc['Result sheet']
		

	def parse(self):
		for filetype in self.filetypes:
			if filetype.test(self.doc) :
				return filetype.parse(self.doc)
		raise NotImplementedError('FileType not implemented')



class ODSpectrum():
	def test(self, doc):
		return doc['A24'].value == 'Wavelength start'

	def parse(self, doc):
		data_starting_line = 35
		wl_start = int(str(doc['E24'].value).replace('L', ''))
		wl_end = int(str(doc['E25'].value).replace('L', ''))

		depth = wl_end - wl_start + 1
		width, height = get_dims(doc, data_starting_line)
		time = 1

		# Get values
		result = []
		for i in range(depth):
			row = list(doc[data_starting_line + i])
			result.append([ cell.value for cell in row[1:] ])

		data = np.transpose(np.array(result).reshape([1, depth, width, height]), (0,1,3,2))

		axis_values = { 'time' : range(time), 
						'depth' : range(wl_start,wl_end), 
						'width' : range(width), 
						'height' : range(height) }

		return {"data" : data, 'axis_values':axis_values}



class ODSingle():
	def test(self, doc):
		return doc['A24'].value == 'Measurement wavelength'

	def parse(self, doc):
		data_starting_line = 32
		axis_values = []

		depth = 1
		time = 1
		width = 12
		height = 8

		# Get values
		result = get_two_dim_matrix(doc, data_starting_line)

	

		axis_values = { 'time' : range(time), 
						'depth' : range(depth), 
						'width' : range(width), 
						'height' : range(height) }

		data = np.array(result).T
		data = np.expand_dims(data, axis=0)
		data = np.expand_dims(data, axis=0)

		return {"data" : data, 'axis_values':axis_values}



class ODTime:

	def test(self, doc):
		print(doc['A106'].value)
		return doc['A106'].value == 'OD600'

	def parse(self, doc):
		data_starting_line = 110

		# Get values
		result = []
		time_values = []
		line = data_starting_line
		while doc[line][0].value == '<>':
			result.append(get_two_dim_matrix(doc, line))
			# time_values.append(doc['B' + str(line - 3)].value)
			line += 13



		data = np.array(result)
		data = np.transpose(data, (0,2,1))
		data = np.expand_dims(data, axis=1)

		time, depth, width, height = data.shape
		print(data.shape)

		axis_values = { 'time' : range(time), 
						'depth' : range(depth), 
						'width' : range(width), 
						'height' : range(height) }
		print(axis_values)

		return {"data" : data, 'axis_values':axis_values}




	