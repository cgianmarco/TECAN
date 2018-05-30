import numpy as np

class ODSingle:
	def test(self, doc):
		return len(doc.cells_of_value('<>')) == 1

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

		data = np.transpose(np.array(result).reshape([1, depth, width, height]), (0,1,3,2))

		axis_values = { 'time' : range(time), 
						'depth' : range(wl_start,wl_end), 
						'width' : range(width), 
						'height' : range(height) }

		return {"data" : data, 'axis_values':axis_values}