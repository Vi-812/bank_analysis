import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import create_database


def handler(excel_file):

    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"FileNotFoundError! Файл '{excel_file}' не найден!")
        return
    except Exception as e:
        print(f"Неизвестное исключение: {e}")
        return

    num_rows = df.shape[0]
    print(f"Обработка файла '{excel_file}', {num_rows} строк")

    Contractor, Payment, engine = create_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
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
            print(f"Error! Файл={excel_file}, №_платежа={row['Номер платежного документа']}, "
                  f"дебет={row['Оборот по дебету']}, кредит={row['Оборот по кредиту']}")
            continue

