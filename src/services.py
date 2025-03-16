import pandas as pd

def load_transactions_from_excel(excel_file):
    """
    Загружает данные транзакций из Excel-файла.

    :param excel_file: Путь к Excel-файлу с транзакциями
    :return: Список транзакций
    """
    df = pd.read_excel(excel_file)
    transactions = df.to_dict('records')
    return transactions

# Пример использования функции
excel_file = './data/operations.xlsx'  # Замените на путь к вашему Excel-файлу
transactions = load_transactions_from_excel(excel_file)

# Проверка результата
expected_columns = ['Дата операции', 'Сумма операции', 'Категория', 'Описание']
for transaction in transactions:
    assert all(column in transaction for column in expected_columns), f"Не хватает столбцов в транзакции: {transaction}"

print("Все транзакции загружены успешно!")
