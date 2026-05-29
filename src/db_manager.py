"""
Модуль для работы с базой данных PostgreSQL.
"""

import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class DBManager:
    """Класс для управления базой данных."""

    def __init__(self):
        self.conn_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "dbname": os.getenv("DB_NAME", "plane_tracker_db"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD")
        }
        self.conn = None
        self.cur = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
            logger.info("Подключение к БД установлено")
        except Exception as e:
            logger.error(f"Ошибка подключения к БД: {e}")
            raise

    def disconnect(self):
        """Закрывает соединение с базой данных."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("Соединение с БД закрыто")

    def create_tables(self):
        """Создаёт таблицы countries и aeroplanes."""
        # Таблица стран
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                bounding_box TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Таблица самолётов
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS aeroplanes (
                id SERIAL PRIMARY KEY,
                icao24 VARCHAR(10) NOT NULL,
                callsign VARCHAR(20),
                origin_country VARCHAR(100),
                velocity FLOAT,
                baro_altitude FLOAT,
                country_id INTEGER REFERENCES countries(id),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        self.conn.commit()
        logger.info("Таблицы созданы")