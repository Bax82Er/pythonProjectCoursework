import pandas as pd
import requests

def get_data_from_excel(date_time):
    # Логика для чтения данных из Excel-файла
    df = pd.read_excel('operations.xls')
    start_date = date_time.replace(day=1)
    end_date = date_time
    mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    print("Data from Excel:", df[mask].head())  # Добавляем печать первых строк для проверки
    return df[mask]

def get_currency_rates():
    # Использование API для получения курсов валют
    response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    data = response.json()
    print("Currency rates:", data['rates'])  # Печать курсов валют
    return data['rates']

def get_stock_prices():
    # Использование API для получения цен на акции
    response = requests.get('https://api.nasdaq.com/api/quote/AAPL/info')
    data = response.json()
    print("Stock prices:", data['stock']['price'])  # Печать цены акции AAPL
    return data['stock']['price']
