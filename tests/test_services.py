import pytest
import logging
from datetime import datetime
from typing import Any, Dict, List

# Предполагается, что ваш модуль называется 'services.py'
from src.services import investment_bank

# Настройка логгера (чтобы не засорять вывод тестов)
logging.basicConfig(level=logging.WARNING)


def test_investment_bank_valid_month():
    """Тестирует функцию investment_bank с корректными данными месяца."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": 1256},
        {"Дата операции": "2023-08-12", "Сумма операции": 1789}
    ]
    result = investment_bank("2023-08", transactions, 50)
    assert result == pytest.approx(5.0, rel=1e-6)


def test_investment_bank_invalid_month_format(caplog):
    """Тестирует функцию investment_bank с некорректным форматом месяца."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": 1256}
    ]
    with caplog.at_level(logging.ERROR):
        result = investment_bank("2023/08", transactions, 50)
    assert result == 0.0
    assert "Неверный формат строки месяца" in caplog.text


def test_investment_bank_transactions_different_month():
    """Тестирует функцию investment_bank с транзакциями за другой месяц."""
    transactions = [
        {"Дата операции": "2023-07-01", "Сумма операции": 1256},
        {"Дата операции": "2023-09-12", "Сумма операции": 1789}
    ]
    result = investment_bank("2023-08", transactions, 50)
    assert result == 0.0


def test_investment_bank_invalid_transaction_date(caplog):
    """Тестирует функцию investment_bank с некорректной датой транзакции."""
    transactions = [
        {"Дата операции": "2023/08/01", "Сумма операции": 1256}
    ]
    with caplog.at_level(logging.WARNING):
        result = investment_bank("2023-08", transactions, 50)
    assert result == 0.0
    assert "Ошибка парсинга даты транзакции" in caplog.text


def test_investment_bank_empty_transactions():
    """Тестирует функцию investment_bank с пустым списком транзакций."""
    transactions: List[Dict[str, Any]] = []
    result = investment_bank("2023-08", transactions, 50)
    assert result == 0.0


def test_investment_bank_rounding_limit():
    """Тестирует функцию investment_bank с разными пределами округления."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": 1256}
    ]
    result_10 = investment_bank("2023-08", transactions, 10)
    assert result_10 == pytest.approx(4.0, rel=1e-6)

    result_100 = investment_bank("2023-08", transactions, 100)
    assert result_100 == pytest.approx(44.0, rel=1e-6)


def test_investment_bank_zero_limit():
    """Тестирует функцию investment_bank с нулевым пределом округления."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": 1256}
    ]
    result = investment_bank("2023-08", transactions, 0)  # Деление на ноль
    assert result == 0.0


# Дополнительный тест для проверки отрицательных сумм операций (полезно!)
def test_investment_bank_negative_amount():
    """Тестирует функцию investment_bank с отрицательной суммой операции."""
    transactions = [
        {"Дата операции": "2023-08-01", "Сумма операции": -1256}
    ]
    result = investment_bank("2023-08", transactions, 50)
    assert result == pytest.approx(6.0, rel=1e-6)
