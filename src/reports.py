import datetime
import json
import logging
from datetime import timedelta
from functools import wraps
from typing import Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_REPORT_FILE = "report.json"


def report_decorator(filename: Optional[str] = None):
    """
    Декоратор для функций-отчетов, записывающий результат в файл.

    Args:
        filename: Необязательное имя файла для записи отчета.
                  Если не указано, используется имя файла по умолчанию (DEFAULT_REPORT_FILE).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                file_to_use = filename if filename else DEFAULT_REPORT_FILE
                with open(file_to_use, 'w') as f:
                    json.dump(result, f, indent=4, default=str)  # Используем default=str для сериализации datetime
                logging.info(f"Отчет из {func.__name__} записан в файл: {file_to_use}")  # Fixed func.__name__
                return result
            except Exception as e:
                logging.error(f"Ошибка при выполнении функции {func.__name__}: {e}")  # Fixed func.name to func.__nam_
                raise  # Re-raise exception to not hide it

        return wrapper

    return decorator


@report_decorator()  # Использование декоратора без параметров
def spending_by_category(transactions_df, category, end_date_str):
    """
    Вычисляет общие расходы для определенной категории за последние 90 дней.

    Args:
        transactions_df: Pandas DataFrame со столбцами 'date', 'category' и 'amount'.
        category: Категория для фильтрации транзакций.
        end_date_str: Конечная дата для расчета (YYYY-MM-DD).

    Returns:
        Словарь, содержащий category, start_date, end_date и total_spending.
    """
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()  # Fixed this to co the end date
    start_date = end_date - timedelta(days=90)

    # Преобразуйте столбец 'date' в объекты datetime для сравнения
    transactions_df = transactions_df.copy()  # Added copy to avoid side effects
    transactions_df.loc[:, 'date'] = pd.to_datetime(transactions_df['date']).dt.date  # Fixed

    # Фильтруйте по дате и категории
    filtered_transactions = transactions_df[
        (transactions_df['date'] >= start_date) &
        (transactions_df['date'] <= end_date) &
        (transactions_df['category'] == category)
    ]

    # Вычислите общие расходы
    total_spending = filtered_transactions['amount'].sum()

    report = {
        'category': category,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_spending': total_spending
    }

    return report


@report_decorator("food_spending.json")
def food_spending_report(transactions_df):  # Changed transactions to transactions_df
    """
    Generates a food spending report for a given DataFrame of transactions.
    """
    category = 'Food'
    date = '2023-10-31'
    report = spending_by_category(transactions_df, category, date)
    return report


if __name__ == "__main__":
    # Example Usage (Replace with your actual data)
    data = {'date': ['2023-07-01', '2023-07-15', '2023-08-15', '2023-09-01', '2023-10-01', '2023-10-15'],
            'category': ['Food', 'Transportation', 'Food', 'Entertainment', 'Food', 'Transportation'],
            'amount': [50.0, 30.0, 60.0, 40.0, 70.0, 35.0]}
    transactions_df = pd.DataFrame(data)

    food_spending_report(transactions_df)  # Creates food_spending.json
