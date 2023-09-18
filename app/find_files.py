import os
import sys


def find_excel_files():
    folder_path = "."
    excel_files_list = []

    try:
        for file in os.listdir(folder_path):
            if file.endswith(".xlsx"):
                excel_files_list.append(file)

        if not excel_files_list:
            print("В текущей папке не найдено Excel файлов (*.xlsx)")
            print("Работа программы завершена")
            sys.exit()

        print("В работу приняты Excel файлы:")
        for file in excel_files_list:
            print(file)
            base_name = os.path.splitext(file)[0]
            folder_name = os.path.join("..", base_name)
            os.makedirs(folder_name, exist_ok=True)

        print(f"Общее количество файлов - {len(excel_files_list)}")
        print("--------------------------------------------------")

    except OSError as e:
        print(f"Ошибка при обработке файлов: {e}")
        sys.exit()
    except Exception as e:
        print(f"Неизвестное исключение: {e}")
        sys.exit()

    return excel_files_list
