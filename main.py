import argparse
import pandas as pd
import sys
from sqlalchemy.orm import sessionmaker
from models import create_database
import time

parser = argparse.ArgumentParser(description="Файл для анализа")
parser.add_argument("file", nargs="?", default="test-", help="Имя файла")
args = parser.parse_args()
file_name = args.file

if not file_name.endswith(".xlsx"):
    file_name += ".xlsx"

try:
    df = pd.read_excel(file_name)
except FileNotFoundError:
    print(f"FileNotFoundError! Файл '{file_name}' не найден!")
    sys.exit()

Contractor, Payment, engine = create_database()

Session = sessionmaker(bind=engine)
session = Session()

print(f"Аналитика по файлу {file_name}:")

num_rows = df.shape[0]
print(f"Количество строк в обработке - {num_rows}")

start_time = time.time()

for index, row in df.iterrows():
    if index == 99:
        processing_time = time.time() - start_time
        block_rows = (num_rows // 100) + 1
        print(f"{processing_time=}, {block_rows=}")
        print(f"Ориенировочное время ожидания - {int(block_rows * processing_time)} сек")
    if row["Оборот по дебету"] != 0 and row["Оборот по кредиту"] == 0:
        existing_contractor = session.query(Contractor).filter_by(inn=row["ИНН получателя"]).first()
        if existing_contractor:
            payment = Payment(payment=row["Оборот по дебету"])
            existing_contractor.payments.append(payment)
            session.add(payment)
            session.commit()
        else:
            contractor = Contractor(inn=row["ИНН получателя"], name=row["Наименование получателя"])
            payment = Payment(payment=row["Оборот по дебету"])
            contractor.payments.append(payment)
            session.add(contractor)
            session.commit()

    elif row["Оборот по дебету"] == 0 and row["Оборот по кредиту"] != 0:
        pass

    else:
        print(f"Error! № платежа={row['Номер платежного документа']}, "
              f"дебет={row['Оборот по дебету']}, кредит={row['Оборот по кредиту']}")
        continue

# Получение всех контрагентов из базы данных
all_contractors = session.query(Contractor).all()

# Вывод информации о каждом контрагенте
for contractor in all_contractors:
    print("----------------------------------------------")
    print("Имя:", contractor.name)
    print("ИНН:", contractor.inn)
    print("Количество платежей:", len(contractor.payments))

    if contractor.payments:
        # Вычисление суммы всех платежей контрагента
        total_payment = sum(payment.payment for payment in contractor.payments)
        print("Сумма всех платежей:", total_payment)

        # Нахождение минимального и максимального платежей контрагента
        min_payment = min(payment.payment for payment in contractor.payments)
        max_payment = max(payment.payment for payment in contractor.payments)
        print("Минимальный платеж:", min_payment)
        print("Максимальный платеж:", max_payment)
    else:
        print("Сумма всех платежей: 0")
        print("Минимальный платеж: Нет данных")
        print("Максимальный платеж: Нет данных")
