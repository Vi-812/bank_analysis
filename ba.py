import argparse
import pandas as pd


parser = argparse.ArgumentParser(description="Файл для анализа")
parser.add_argument('file', nargs='?', default='test.xlsx', help='Имя файла')
args = parser.parse_args()
file_name = args.file

print(file_name)

data = pd.read_excel(file_name)

print(data)
