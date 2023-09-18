import pandas as pd
import sys
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import time
import statistics
from prettytable import PrettyTable
from models import create_database
from find_files import find_excel_files


excel_files_list = find_excel_files()

for excel_file in excel_files_list:








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
        print(f"Ориентировочное время ожидания - {int(block_rows * processing_time)} сек")
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

while True:
    print("\n----- Меню сортировки и вывода информации -----")
    print("1. Отсортировать по количеству платежей")
    print("2. Отсортировать по сумме платежей")
    print("3. Отсортировать по максимальному платежу")
    print("0. Выход")
    choice = input("Выберите пункт меню: ")

    if choice == "1":
        contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
            func.count().desc())
        sort_column = "Количество платежей"
    elif choice == "2":
        contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
            func.sum(Payment.payment).desc())
        sort_column = "Сумма всех платежей"
    elif choice == "3":
        contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
            func.max(Payment.payment).desc())
        sort_column = "Максимальный платеж"
    elif choice == "0":
        break
    else:
        print("Неверный выбор. Попробуйте еще раз.")
        continue

    total_contractors = contractors.count()
    print(f"Общее количество контрагентов: {total_contractors}")

    num_records = int(input("Введите количество записей для вывода: "))

    if num_records < 1:
        print("Неверное количество записей. Попробуйте еще раз.")
        continue

    contractors = contractors.limit(num_records).all()

    table = PrettyTable()
    # Создание таблицы с правильными заголовками
    # Создание таблицы с правильными заголовками
    table.field_names = ["№", "Наименование контрагента", "ИНН контрагента", "Количество платежей",
                         "Сумма всех платежей", "Минимальный платеж", "Максимальный платеж",
                         "Средний платеж", "Медиана платежей"]

    for i, contractor in enumerate(contractors, start=1):
        payments = [payment.payment for payment in contractor.payments]
        num_payments = len(payments)
        total_payment = round(sum(payments), 2)
        min_payment = round(min(payments), 2) if payments else 0.0
        max_payment = round(max(payments), 2) if payments else 0.0
        median_payment = round(statistics.median(payments), 2) if payments else 0.0
        mean_payment = round(statistics.mean(payments), 2) if payments else 0.0

        # Форматирование строки с двумя знаками после запятой для столбца "Сумма всех платежей"
        total_payment_str = "{:.2f}".format(total_payment)
        # Форматирование строки с двумя знаками после запятой для столбца "Средний платеж"
        mean_payment_str = "{:.2f}".format(mean_payment)
        # Форматирование строки с двумя знаками после запятой для столбца "Минимальный платеж"
        min_payment_str = "{:.2f}".format(min_payment)
        # Форматирование строки с двумя знаками после запятой для столбца "Максимальный платеж"
        max_payment_str = "{:.2f}".format(max_payment)
        # Форматирование строки с двумя знаками после запятой для столбца "Медиана платежей"
        median_payment_str = "{:.2f}".format(median_payment)

        table.add_row([i, contractor.name, contractor.inn, num_payments, total_payment_str, min_payment_str,
                       max_payment_str, mean_payment_str, median_payment_str])

    print("\n----- Результаты -----")
    print(f"Отсортировано по: {sort_column}")
    print(f"Количество записей для вывода: {num_records}")
    print(table)

    user_choice = input("Желаете ли вы сохранить результаты в файл? (y/n): ")
    if user_choice.lower() == "y":
        file_name = input("Введите имя файла для сохранения: ")
        file_name += ".txt"
        with open(file_name, "w") as file:
            file.write(table.get_string())
        print(f"Результаты сохранены в файл '{file_name}'")
