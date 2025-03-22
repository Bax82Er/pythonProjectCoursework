import json
import logging
from datetime import datetime
from typing import Any, Dict, List

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Функция для вычисления суммы, которую можно было бы отложить в Инвесткопилку
    :param month:param Месяц для расчета ('YYYY-MM')
    :param transactions: Список транзакций (список словарей)
    :param limit: Предел округления (целое число)
    :return: Сумма, которую можно отложить
    """

    # Преобразуем строку месяца в объект даты
    try:
        target_month = datetime.strptime(month, '%Y-%m').date()
    except ValueError as e:
        logger.error(f"Неверный формат строки месяца: {e}")
        return 0.0

    total_saved = 0.0  # Переменная для накопления суммы

    # Проверка на нулевой лимит
    if limit == 0:
        logger.warning("Предел округления равен 0. Возвращаем 0.0")
        return 0.0

    for transaction in transactions:
        # Извлекаем дату и сумму транзакции
        date_str = transaction['Дата операции']
        amount = transaction['Сумма операции']

        # Проверяем, относится ли транзакция к нужному месяцу
        try:
            trans_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            logger.warning(f"Ошибка парсинга даты транзакции: {e}. Пропускаем транзакцию.")
            continue

        if trans_date.month == target_month.month and trans_date.year == target_month.year:
            # Округляем сумму до ближайшего значения лимита
            rounded_amount = round(amount / limit) * limit
            saved_amount = rounded_amount - amount
            total_saved += saved_amount
            logger.info(f"Транзакция {trans_date}: экономия {saved_amount:.2f} руб.")
        else:
            logger.debug(f"Пропущена транзакция за другой месяц: {trans_date}")

    return total_saved


if __name__ == "__main__":
    # Тестовый пример
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": 1256},
        {"Дата операции": "2023-07-15", "Сумма операции": 3412},
        {"Дата операции": "2023-08-12", "Сумма операции": 1789}
    ]

    result = investment_bank("2023-08", transactions, 50)
    print(json.dumps({"total_saved": result}, indent=4))


def load_config():
    return None


def connect_db():
    return None


def disconnect_db():
    return None