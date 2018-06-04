import numpy as np
from openpyxl import load_workbook, Workbook
import os

class ODSingle:
	# Test if document belongs to template
	def test(self, doc):
		return len(doc.cells_of_value('<>')) == 1

	# Parse data from document
	def parse(self, doc):
		data_starting_line = doc.row_of(doc.cell_of_value('<>'))
		axis_values = []

		depth = 1
		time = 1
		width = 12
		height = 8

		# Get values
		result = doc.get_two_dim_matrix(data_starting_line)

	

		axis_values = { 'time' : range(time), 
						'depth' : range(depth), 
						'width' : range(width), 
						'height' : range(height) }

		data = np.array(result).T
		data = np.expand_dims(data, axis=0)
		data = np.expand_dims(data, axis=0)

		return {"data" : data, 'axis_values':axis_values}


class ODSpectrum:
	def test(self, doc):
		return len(doc.cells_of_value('Wavel.')) == 1

	def parse(self, doc):
		data_starting_line = doc.row_of(doc.cell_of_value('Wavel.'))

		# To be changed
		wl_start = doc.doc['A' + str(data_starting_line + 1)].value
		# wl_end = int(str(doc['E25'].value).replace('L', ''))

		
		width, height = doc.get_dims(data_starting_line)
		time = 1

		# Get values
		result = []
		line = data_starting_line + 1
		
		while str(doc.doc['A' + str(line)].value).isdigit():
			row = list(doc.doc[line])
			result.append([ cell.value for cell in row[1:] ])
			print( doc.doc['A' + str(line)].value)
			line += 1

		wl_end = int(doc.doc['A' + str(line - 1)].value)
		depth = wl_end - wl_start + 1

		result = np.array(result)
		data = np.transpose(result.reshape([1, depth, width, height]), (0,1,3,2))



		axis_values = { 'time' : range(time), 
						'depth' : range(wl_start,wl_end), 
						'width' : range(width), 
						'height' : range(height) }

		return {"data" : data, 'axis_values':axis_values}


class ODTime:

	def test(self, doc):
		return len(doc.cells_of_value('<>')) > 1

	def parse(self, doc):

		# Get values
		result = []
		time_values = []
		matrix = doc.cell_of_value('<>')
		line = doc.row_of(matrix)
		while doc.doc[line][0].value == '<>':
			result.append(doc.get_two_dim_matrix(line))
			line += 13



		data = np.array(result)
		data = np.transpose(data, (0,2,1))
		data = np.expand_dims(data, axis=1)

		time, depth, width, height = data.shape
		for t in range(time):
			for z in range(depth):
				for i in range(width):
					for j in range(height):
						if data[t,z,i,j] == 'OVER':
							data[t,z,i,j] = np.nan

		data = data.astype('float32')

		axis_values = { 'time' : range(time), 
						'depth' : range(depth), 
						'width' : range(width), 
						'height' : range(height) }
		print(axis_values)

		return {"data" : data, 'axis_values':axis_values}


class ODTimeSpectrum:

	def test(self, doc):
		for cell in doc.doc['A']:
			if cell.value == 'A1':
				return True
		return False

	def parse(self, doc):
		data_starting_line = doc.row_of(doc.cell_of_value('Well / Wavelength'))

		# Get values
		result = []
		for matrix in doc.cells_of_value('Well / Wavelength'):
			result.append(doc.get_two_dim_time_spectrum_matrix(doc.row_of(matrix)))

		data = np.array(result)
		print(data.shape)
		newshape = (8, 12, data.shape[1], data.shape[2])
		data = data.reshape(newshape)
		data = np.transpose(data, (3,2,1,0))

		time, depth, width, height = data.shape

		for t in range(time):
			for z in range(depth):
				for i in range(width):
					for j in range(height):
						if data[t,z,i,j] == 'OVER':
							data[t,z,i,j] = np.nan

		data = data.astype('float32')

		axis_values = { 'time' : range(time), 
						'depth' : range(depth), 
						'width' : range(width), 
						'height' : range(height) }

		return {"data" : data, 'axis_values':axis_values}


