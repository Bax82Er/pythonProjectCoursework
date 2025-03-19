import pandas as pd
from typing import Optional
import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Декоратор для записи результата функции в файл
def write_to_file(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename is not None:
                file_path = f"{filename}.txt"
            else:
                current_date = datetime.now().strftime("%Y-%m-%d")
                file_path = f"report_{current_date}.txt"

            with open(file_path, 'w') as file:
                file.write(json.dumps(result.to_dict(), indent=4))

            logger.info(f"Результат сохранен в файл {file_path}")
            return result

        return wrapper

    return decorator


@write_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция для получения трат по заданной категории за последние три месяца.

    :param transactions: DataFrame с транзакциями
    :param category: категория расходов
    :param date: дата отсчета трехмесячного периода (по умолчанию текущая дата)
    :return: DataFrame с тратами по категории за последние три месяца
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    start_date = (pd.to_datetime(date) - pd.DateOffset(months=3)).strftime('%Y-%m-%d')

    # Фильтруем транзакции по дате и категории
    filtered_transactions = transactions.query(
        f"date >= '{start_date}' & category == '{category}'"
    )

    # Возвращаем агрегированные расходы по месяцам
    grouped_transactions = filtered_transactions.groupby('month').agg({
        'amount': ['sum']
    }).reset_index()

    return grouped_transactions
