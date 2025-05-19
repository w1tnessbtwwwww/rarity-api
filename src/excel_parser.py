import openpyxl
import os
path = os.path.join(os.path.dirname(__file__), 'excels\\processed_porcelain_marks_final.xlsx')

workbook = openpyxl.load_workbook(path)
sheet = workbook.active

for row in sheet.iter_rows(min_row=2, values_only=True):
    print(row)