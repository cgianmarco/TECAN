from openpyxl import load_workbook

wb = load_workbook(str(filename))
wb = wb['Result sheet']

data_starting_line = 35