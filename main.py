from app.find_files import find_excel_files
from app.file_handler import handler


excel_files_list = find_excel_files()

for excel_file in excel_files_list:
    handler(excel_file=excel_file)
