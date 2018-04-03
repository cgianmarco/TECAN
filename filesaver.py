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

