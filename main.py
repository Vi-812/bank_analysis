import argparse
import pandas as pd


parser = argparse.ArgumentParser(description="Файл для анализа")
parser.add_argument("file", nargs="?", default="test.xlsx", help="Имя файла")
args = parser.parse_args()
file_name = args.file

print(f"Аналитика по файлу {file_name}")

df = pd.read_excel(file_name)

for index, row in df.iterrows():
    print(index, row['Наименование плательщика'])
