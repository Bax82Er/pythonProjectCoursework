import pytest
import pandas as pd
from unittest.mock import patch
import requests
from requests.exceptions import RequestException
from datetime import datetime

# Предполагается, что ваш модуль называется 'utils.py'
from src.utils import get_data_from_excel, get_currency_rates, get_stock_prices


@pytest.fixture
def mock_excel_data():
    """Фикстура для создания примера DataFrame Excel для тестирования."""
    data = {'Дата операции': [pd.to_datetime('2024-05-01'), pd.to_datetime('2024-05-15'), pd.to_datetime('2024-06-01')],
            'Сумма': [100, 200, 150],
            'Описание': ['Transaction 1', 'Transaction 2', 'Transaction 3']}
    return pd.DataFrame(data)


def test_get_data_from_excel(mock_excel_data, monkeypatch):
    """Тестирует функцию get_data_from_excel."""
    # Мокируем pd.read_excel, чтобы он возвращал моковый DataFrame
    monkeypatch.setattr(pd, "read_excel", lambda x: mock_excel_data)

    # Тестируем с конкретной датой
    date_time = datetime(2024, 5, 20)
    result = get_data_from_excel(date_time)

    # Утверждаем, что результат является DataFrame
    assert isinstance(result, pd.DataFrame)

    # Утверждаем, что результат отфильтрован правильно
    expected_rows = 2  # Ожидаемое количество строк для мая 2024
    assert len(result) == expected_rows

    # Утверждаем, что данные в первой строке такие, как мы ожидаем
    assert result['Сумма'].iloc[0] == 100
    assert result['Описание'].iloc[0] == 'Transaction 1'


def test_get_currency_rates(monkeypatch):
    """Тестирует функцию get_currency_rates."""
    # Мокируем функцию requests.get
    mock_response = {
        "rates": {"EUR": 0.85, "GBP": 0.75},
        "base": "USD",
        "date": "2024-06-07"
    }

    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

            def raise_for_status(self):
                if self.status_code != 200:
                    raise RequestException("Request failed")

        return MockResponse(mock_response, 200)  # Успешный ответ

    monkeypatch.setattr(requests, "get", mock_get)

    # Вызываем функцию
    rates = get_currency_rates()

    # Утверждаем, что результат является словарем
    assert isinstance(rates, dict)

    # Утверждаем, что курсы валют верны
    assert rates['EUR'] == 0.85
    assert rates['GBP'] == 0.75

    def test_get_stock_prices(monkeypatch):
        """Тестирует функцию get_stock_prices."""
        # Мокируем функцию requests.get
        mock_response = {
            "stock": {"price": 160.00},
            "other": "some other data"
        }

        def mock_get(*args, **kwargs):
            class MockResponse:
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code

                def json(self):
                    return self.json_data

                def raise_for_status(self):
                    if self.status_code != 200:
                        raise RequestException("Request failed")

            return MockResponse(mock_response, 200)  # Успешный ответ

        monkeypatch.setattr(requests, "get", mock_get)

        # Вызываем функцию
        price = get_stock_prices()

        # Утверждаем, что результат является float
        assert isinstance(price, float)

        # Утверждаем, что цена верна
        assert price == 160.00

    def test_get_currency_rates_request_exception(monkeypatch):
        """Тестирует функцию get_currency_rates, когда происходит исключение RequestException."""

        def mock_get(*args, **kwargs):
            raise RequestException("Request failed")

        monkeypatch.setattr(requests, "get", mock_get)

        # Вызываем функцию и утверждаем, что она вызывает RequestException
        with pytest.raises(RequestException) as excinfo:
            get_currency_rates()
        assert "Request failed" in str(excinfo.value)  # Проверяем сообщение об исключении

    def test_get_stock_prices_request_exception(monkeypatch):
        """Тестирует функцию get_stock_prices, когда происходит исключение RequestException."""

        def mock_get(*args, **kwargs):
            raise RequestException("Request failed")

        monkeypatch.setattr(requests, "get", mock_get)

        # Вызываем функцию и утверждаем, что она вызывает RequestException
        with pytest.raises(RequestException) as excinfo:
            get_stock_prices()
        assert "Request failed" in str(excinfo.value)  # Проверяем сообщение об исключении