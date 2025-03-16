from datetime import datetime
import json
import requests
from utils import get_data_from_excel, get_currency_rates, get_stock_prices

def home_view(request, date_time_str):
    # Преобразуем строку с датой и временем в объект datetime
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Получаем данные из Excel-файла
    data = get_data_from_excel(date_time)

    # Получаем курсы валют
    currency_rates = get_currency_rates()

    # Получаем цены на акции
    stock_prices = get_stock_prices()

    # Формируем JSON-ответ
    response = {
        "greeting": get_greeting(date_time),
        "cards": get_cards_data(data),
        "top_transactions": get_top_transactions(data),
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response)

def get_greeting(date_time):
    hour = date_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_cards_data(data):
    # Логика для получения данных по картам
    pass

def get_top_transactions(data):
    # Логика для получения топ-5 транзакций
    pass
