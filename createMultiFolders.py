#! python3
# create multi folder follow names in excel file

import os
import openpyxl


def folder_creation(EXCEL_FILE_DIRECTORY, FOLDER_CREATION_LOCATION,  EXCEL_FILE_NAME):
    os.chdir(EXCEL_FILE_DIRECTORY)
    workbook = openpyxl.load_workbook(EXCEL_FILE_NAME)
    sheet = workbook.get_sheet_by_name('Sheet1')

    col_values = [cell.value for col in sheet.iter_cols(
        min_row=2, max_row=None, min_col=1, max_col=1) for cell in col]
    for value in col_values:       
        folderName = value
        baseDir = FOLDER_CREATION_LOCATION
        os.makedirs(os.path.join(baseDir, folderName))
        print("\nFolder created in: ", os.path.join(baseDir, folderName))

EXCEL_FILE_DIRECTORY = "E:\\PythonRun"
FOLDER_CREATION_LOCATION = "E:\\PythonRun"
EXCEL_FILE_NAME = "folder_name.xlsx"
folder_creation(EXCEL_FILE_DIRECTORY, FOLDER_CREATION_LOCATION,  EXCEL_FILE_NAME)