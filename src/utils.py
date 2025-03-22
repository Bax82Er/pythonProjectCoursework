import pandas as pd
import requests


def get_data_from_excel(date_time):
    """
    Получение данных из Excel-файла за определенный период.

    Аргумент:
        date_time (datetime): Дата, используемая для фильтрации данных.

    Возвращаемое значение:
        DataFrame: Фильтрованная таблица данных из Excel-файла.
    """
    df = pd.read_excel('operations.xls')
    start_date = date_time.replace(day=1)
    end_date = date_time
    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    print("Data from Excel:", df[mask].head())
    return df[mask]


def get_currency_rates():
    """
    Получение актуальных курсов валют через API.

    Возвращаемое значение:
        dict: Словарь с курсами валют относительно базовой валюты USD.
    """
    response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    data = response.json()
    print("Currency rates:", data['rates'])
    return data['rates']


def get_stock_prices():
    """
    Получение текущих цен на акции через API Nasdaq.

    Возвращаемое значение:
        float: Текущая цена акций Apple (AAPL).
    """
    response = requests.get('https://api.nasdaq.com/api/quote/AAPL/info')
    data = response.json()
    print("Stock prices:", data['stock']['price'])
    return data['stock']['price']
