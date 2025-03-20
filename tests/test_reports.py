import pandas as pd
import numpy as np
import pytest
from src.reports import spending_by_category, food_spending_report  # Замените your_module

@pytest.fixture
def transactions_df():
    data = {'date': ['2023-07-01', '2023-07-15', '2023-08-15', '2023-09-01', '2023-10-01', '2023-10-15'],
            'category': ['Food', 'Transportation', 'Food', 'Entertainment', 'Food', 'Transportation'],
            'amount': [50.0, 30.0, 60.0, 40.0, 70.0, 35.0]}
    return pd.DataFrame(data)


def test_spending_by_category(transactions_df):
    category = 'Food'
    date = '2023-10-31'
    report = spending_by_category(transactions_df, category, date)

    assert isinstance(report, dict)
    assert report['category'] == category
    assert report['start_date'] == (pd.to_datetime(date).date() - pd.Timedelta(days=90)).strftime('%Y-%m-%d')
    assert report['end_date'] == date
    assert isinstance(report['total_spending'], float)

    assert report['total_spending'] == 130.0  # Исправленная проверка


def test_food_spending_report(transactions_df):
    report = food_spending_report(transactions_df)

    assert isinstance(report, dict)
    assert report['category'] == "Food"
    assert report['total_spending'] == 130.0  # Исправленная проверка

def test_empty_transactions(transactions_df):
    empty_df = pd.DataFrame(columns = transactions_df.columns)
    report = food_spending_report(empty_df)

    assert isinstance(report, dict)
    assert report['category'] == "Food"
    assert report['total_spending'] == 0.0  # Corrected assertion
