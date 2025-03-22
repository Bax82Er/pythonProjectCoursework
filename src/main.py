"""
Модуль запуска, объединяющий все функциональные возможности проекта.
"""

import logging
from datetime import datetime

from src.services import load_config, connect_db, disconnect_db


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_data(db_connection, param):
    pass


def generate_reports(processed_data, param):
    pass


def main():
    """Основная точка входа в программу."""
    config = load_config()  # Загрузка конфигурационных данных
    db_connection = connect_db(config["db_url"])  # Подключение к базе данных

    try:
        # Выполнение основной логики
        processed_data = process_data(db_connection, config["input_path"])
        reports = generate_reports(processed_data, config["output_dir"])


        # Логируем успешное выполнение
        logging.info("Программа выполнена успешно!")
    finally:
        disconnect_db(db_connection)  # Отключение от базы данных

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    logging.info(f"Время выполнения программы: {execution_time.total_seconds()} секунд")
    