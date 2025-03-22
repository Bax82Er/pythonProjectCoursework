import json
from datetime import datetime
from unittest.mock import patch

import pytest

# Assuming your module is named 'your_module'
from src.views import home_view, get_greeting


# Mocking the utils functions to isolate the home_view function
@pytest.fixture
def mock_utils():
    with (
        patch("src.views.get_data_from_excel") as mock_get_data_from_excel,  # Изменено
        patch("src.views.get_currency_rates") as mock_get_currency_rates,  # Изменено
        patch("src.views.get_stock_prices") as mock_get_stock_prices,  # Изменено
        patch("src.views.get_cards_data") as mock_get_cards_data,  # Изменено
        patch("src.views.get_top_transactions") as mock_get_top_transactions,  # Изменено
    ):
        yield (
            mock_get_data_from_excel,
            mock_get_currency_rates,
            mock_get_stock_prices,
            mock_get_cards_data,
            mock_get_top_transactions,
        )


def test_home_view(mock_utils):
    (
        mock_get_data_from_excel,
        mock_get_currency_rates,
        mock_get_stock_prices,
        mock_get_cards_data,
        mock_get_top_transactions,
    ) = mock_utils

    # Mock the return values of the utils functions
    mock_get_data_from_excel.return_value = {"some": "excel data"}
    mock_get_currency_rates.return_value = {"USD": 75.0, "EUR": 85.0}
    mock_get_stock_prices.return_value = {"AAPL": 150.0, "GOOG": 2500.0}
    mock_get_cards_data.return_value = [{"card": "card data"}]
    mock_get_top_transactions.return_value = [{"transaction": "transaction data"}]

    # Call the home_view function with a sample date and time
    date_time_str = "2024-01-01 10:00:00"
    result = home_view(None, date_time_str)  # Pass None for request as it's not used.

    # Assert that the result is a JSON string
    assert isinstance(result, str)
    try:
        result_json = json.loads(result)
    except json.JSONDecodeError:
        pytest.fail("The result is not a valid JSON string.")

    # Assert that the JSON string contains the expected data
    assert "greeting" in result_json
    assert "cards" in result_json
    assert "top_transactions" in result_json
    assert "currency_rates" in result_json
    assert "stock_prices" in result_json

    # Assert that the greeting is correct for the given time
    assert result_json["greeting"] == "Доброе утро"
    assert result_json["cards"] == [{"card": "card data"}]
    assert result_json["top_transactions"] == [{"transaction": "transaction data"}]
    assert result_json["currency_rates"] == {"USD": 75.0, "EUR": 85.0}
    assert result_json["stock_prices"] == {"AAPL": 150.0, "GOOG": 2500.0}


@pytest.mark.parametrize(
    "date_time_str, expected_greeting",
    [
        ("2024-01-01 08:00:00", "Доброе утро"),
        ("2024-01-01 14:00:00", "Добрый день"),
        ("2024-01-01 20:00:00", "Добрый вечер"),
        ("2024-01-01 02:00:00", "Доброй ночи"),
    ],
)
def test_get_greeting(date_time_str, expected_greeting):
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(date_time)
    assert greeting == expected_greeting
