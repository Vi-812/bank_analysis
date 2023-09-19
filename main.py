from app.find_files import find_excel_files
from app.file_handler import handler


excel_files_list = find_excel_files()

for excel_file in excel_files_list:
    handler(excel_file=excel_file)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# while True:
#     print("\n----- Меню сортировки и вывода информации -----")
#     print("1. Отсортировать по количеству платежей")
#     print("2. Отсортировать по сумме платежей")
#     print("3. Отсортировать по максимальному платежу")
#     print("0. Выход")
#     choice = input("Выберите пункт меню: ")
#
#     if choice == "1":
#         contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
#             func.count().desc())
#         sort_column = "Количество платежей"
#     elif choice == "2":
#         contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
#             func.sum(Payment.payment).desc())
#         sort_column = "Сумма всех платежей"
#     elif choice == "3":
#         contractors = session.query(Contractor).join(Contractor.payments).group_by(Contractor.id).order_by(
#             func.max(Payment.payment).desc())
#         sort_column = "Максимальный платеж"
#     elif choice == "0":
#         break
#     else:
#         print("Неверный выбор. Попробуйте еще раз.")
#         continue
#
#     total_contractors = contractors.count()
#     print(f"Общее количество контрагентов: {total_contractors}")
#
#     num_records = int(input("Введите количество записей для вывода: "))
#
#     if num_records < 1:
#         print("Неверное количество записей. Попробуйте еще раз.")
#         continue
#
#     contractors = contractors.limit(num_records).all()
#
#     table = PrettyTable()
#     # Создание таблицы с правильными заголовками
#     # Создание таблицы с правильными заголовками
#     table.field_names = ["№", "Наименование контрагента", "ИНН контрагента", "Количество платежей",
#                          "Сумма всех платежей", "Минимальный платеж", "Максимальный платеж",
#                          "Средний платеж", "Медиана платежей"]
#
#     for i, contractor in enumerate(contractors, start=1):
#         payments = [payment.payment for payment in contractor.payments]
#         num_payments = len(payments)
#         total_payment = round(sum(payments), 2)
#         min_payment = round(min(payments), 2) if payments else 0.0
#         max_payment = round(max(payments), 2) if payments else 0.0
#         median_payment = round(statistics.median(payments), 2) if payments else 0.0
#         mean_payment = round(statistics.mean(payments), 2) if payments else 0.0
#
#         # Форматирование строки с двумя знаками после запятой для столбца "Сумма всех платежей"
#         total_payment_str = "{:.2f}".format(total_payment)
#         # Форматирование строки с двумя знаками после запятой для столбца "Средний платеж"
#         mean_payment_str = "{:.2f}".format(mean_payment)
#         # Форматирование строки с двумя знаками после запятой для столбца "Минимальный платеж"
#         min_payment_str = "{:.2f}".format(min_payment)
#         # Форматирование строки с двумя знаками после запятой для столбца "Максимальный платеж"
#         max_payment_str = "{:.2f}".format(max_payment)
#         # Форматирование строки с двумя знаками после запятой для столбца "Медиана платежей"
#         median_payment_str = "{:.2f}".format(median_payment)
#
#         table.add_row([i, contractor.name, contractor.inn, num_payments, total_payment_str, min_payment_str,
#                        max_payment_str, mean_payment_str, median_payment_str])
#
#     print("\n----- Результаты -----")
#     print(f"Отсортировано по: {sort_column}")
#     print(f"Количество записей для вывода: {num_records}")
#     print(table)
#
#     user_choice = input("Желаете ли вы сохранить результаты в файл? (y/n): ")
#     if user_choice.lower() == "y":
#         file_name = input("Введите имя файла для сохранения: ")
#         file_name += ".txt"
#         with open(file_name, "w") as file:
#             file.write(table.get_string())
#         print(f"Результаты сохранены в файл '{file_name}'")
