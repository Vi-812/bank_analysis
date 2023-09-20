import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from .models import create_database
from .summing_results import update_contractor_stats


def handler(excel_file):

    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"FileNotFoundError! Файл '{excel_file}' не найден!")
        return
    except Exception as e:
        print(f"Неизвестное исключение при чтении файла! {excel_file=}, {e=}")
        return

    num_rows = df.shape[0]
    print(f"'{excel_file}' в обработке, количество строк - {num_rows}")

    Contractor, Payment, engine = create_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():

        try:

            if row["Оборот по дебету"] != 0 and row["Оборот по кредиту"] == 0:
                existing_contractor = session.query(Contractor).filter_by(inn=row["ИНН получателя"]).first()

                if existing_contractor:
                    contractor = existing_contractor
                    payment = Payment(payment=row["Оборот по дебету"], debit=True)
                    contractor.payments.append(payment)
                    session.add(payment)
                    session.commit()

                else:
                    contractor = Contractor(inn=row["ИНН получателя"], name=row["Наименование получателя"])
                    payment = Payment(payment=row["Оборот по дебету"], debit=True)
                    contractor.payments.append(payment)
                    session.add(contractor)
                    session.add(payment)
                    session.commit()

            elif row["Оборот по дебету"] == 0 and row["Оборот по кредиту"] != 0:
                existing_contractor = session.query(Contractor).filter_by(inn=row["ИНН плательщика"]).first()

                if existing_contractor:
                    contractor = existing_contractor
                    payment = Payment(payment=row["Оборот по кредиту"], debit=False)
                    contractor.payments.append(payment)
                    session.add(payment)
                    session.commit()

                else:
                    contractor = Contractor(inn=row["ИНН плательщика"], name=row["Наименование плательщика"])
                    payment = Payment(payment=row["Оборот по кредиту"], debit=False)
                    contractor.payments.append(payment)
                    session.add(contractor)
                    session.add(payment)
                    session.commit()

            else:
                print(f"Error! Файл={excel_file}, №_платежа={row['Номер платежного документа']}, "
                      f"дебет={row['Оборот по дебету']}, кредит={row['Оборот по кредиту']}")
                continue

        except Exception as e:
            print(f"Неизвестное исключение при обработке строки! {excel_file=}, {index=}, {e=}")
            continue

    all_contractors = session.query(Contractor).all()

    contractors_df = pd.DataFrame()

    for contractor in all_contractors:

        update_contractor_stats(session=session, contractor=contractor, Payment=Payment)

        contractor_data = {
            "ИНН": contractor.inn,
            "Наименование": contractor.name,
            "Платежей (Дебит)": contractor.num_debit_payments,
            "Сумма (Дебит)": contractor.total_debit_payment,
            "Мин. (Дебит)": contractor.min_debit_payment,
            "Макс. (Дебит)": contractor.max_debit_payment,
            "Медиана (Дебит)": contractor.median_debit_payment,
            "Платежей (Кредит)": contractor.num_credit_payments,
            "Сумма (Кредит)": contractor.total_credit_payment,
            "Мин. (Кредит)": contractor.min_credit_payment,
            "Макс. (Кредит)": contractor.max_credit_payment,
            "Медиана (Кредит)": contractor.median_credit_payment,
        }

        contractors_df = pd.concat([contractors_df, pd.DataFrame([contractor_data])], ignore_index=True)
        contractors_df["Сумма (Дебит)"] = contractors_df["Сумма (Дебит)"].astype(float)
        contractors_df["Сумма (Кредит)"] = contractors_df["Сумма (Кредит)"].astype(float)

    base_name = os.path.splitext(os.path.basename(excel_file))[0]
    folder_name = os.path.join(os.path.dirname(excel_file), base_name)
    output_excel_file = os.path.join(folder_name, f"Отчет {base_name}.xlsx")

    excel_writer = pd.ExcelWriter(output_excel_file, engine='xlsxwriter')

    contractors_df.to_excel(excel_writer, index=False)

    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Sheet1']

    column_widths = [12, 50, 16, 13, 13, 13, 16, 16, 13, 13, 13, 16]

    for i, width in enumerate(column_widths):
        worksheet.set_column(i, i, width)

    excel_writer.close()

    print(f"'{excel_file}' обработка завершена")
    print("--------------------------------------------------")
