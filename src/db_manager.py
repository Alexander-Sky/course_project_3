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

    def get_countries_and_aeroplanes_count(self) -> List[tuple]:
        """
        Получает список всех стран и количество самолётов в их воздушных пространствах.
        """
        self.connect()
        self.cur.execute("""
            SELECT c.name, COUNT(a.id) as planes_count
            FROM countries c
            LEFT JOIN aeroplanes a ON c.id = a.country_id
            GROUP BY c.id, c.name
            ORDER BY planes_count DESC
        """)
        result = self.cur.fetchall()
        self.disconnect()
        return result

    def get_all_aeroplanes(self) -> List[tuple]:
        """
        Получает список всех воздушных судов с информацией о стране.
        """
        self.connect()
        self.cur.execute("""
            SELECT a.icao24, a.callsign, a.origin_country, a.velocity, a.baro_altitude, c.name as country
            FROM aeroplanes a
            JOIN countries c ON a.country_id = c.id
        """)
        result = self.cur.fetchall()
        self.disconnect()
        return result

    def get_avg_speed(self) -> float:
        """
        Получает среднюю скорость по всем самолётам.
        """
        self.connect()
        self.cur.execute("SELECT AVG(velocity) FROM aeroplanes WHERE velocity IS NOT NULL")
        result = self.cur.fetchone()[0]
        self.disconnect()
        return float(result) if result else 0.0

    def get_aeroplanes_with_higher_speed(self) -> List[tuple]:
        """
        Получает список всех самолётов, у которых скорость выше средней.
        """
        avg_speed = self.get_avg_speed()
        self.connect()
        self.cur.execute("""
            SELECT a.icao24, a.callsign, a.origin_country, a.velocity, a.baro_altitude, c.name as country
            FROM aeroplanes a
            JOIN countries c ON a.country_id = c.id
            WHERE a.velocity > %s
            ORDER BY a.velocity DESC
        """, (avg_speed,))
        result = self.cur.fetchall()
        self.disconnect()
        return result

    def get_aeroplanes_with_keyword(self, keyword: str) -> List[tuple]:
        """
        Получает список всех самолётов, в позывном которых содержится переданная строка.
        """
        self.connect()
        self.cur.execute("""
            SELECT a.icao24, a.callsign, a.origin_country, a.velocity, a.baro_altitude, c.name as country
            FROM aeroplanes a
            JOIN countries c ON a.country_id = c.id
            WHERE a.callsign ILIKE %s
        """, (f"%{keyword}%",))
        result = self.cur.fetchall()
        self.disconnect()
        return result