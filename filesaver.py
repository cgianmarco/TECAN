import xlsxwriter
import numpy as np


class Exporter:

	def export_two_dim_matrix(self, matrix, name):
		workbook   = xlsxwriter.Workbook('filename.xlsx')
		worksheet1 = workbook.add_worksheet(name)
		width, height = matrix.shape
		for row in range(height):
			for col in range(width):
				worksheet1.write(row, col, matrix[col][row])
		workbook.close()

	def print_matrix_on_ws(self, ws, matrix, rowstart=0, columnstart=0):
		width, height = matrix.shape
		for row in range(height):
			for col in range(width):
				if np.isnan(matrix[col][row]):
					value = 'OVER'
				else:
					value = matrix[col][row]
				ws.write( rowstart + row, columnstart + col, value)


	def export_up_to_three_dim_tensor(self, name, tensor):
		workbook   = xlsxwriter.Workbook(name + ".xlsx")
		worksheet1 = workbook.add_worksheet('Results sheet')
		time, depth, width, height = tensor.shape
		row = 0
		column = 0
		for z in range(depth):
			row = z * (height + 1)
			for i in range(time):
				column = i * (width + 1)			
				self.print_matrix_on_ws(worksheet1, tensor[i,z,:,:], row, column)
				print(column, row)
		workbook.close()


if __name__ == "__main__":
	t = np.ones([1,8, 3, 2])

	ex = Exporter()
	ex.export_up_to_three_dim_tensor(t, 'export_test')

