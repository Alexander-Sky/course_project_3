"""
Модуль для загрузки данных из API в базу данных (ETL).
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict

from src.db_manager import DBManager
from src.plane_api import PlaneAPI

logger = logging.getLogger(__name__)


class DataLoader:
    """Класс для загрузки данных о самолётах в БД."""

    # Список стран для мониторинга (можно менять)
    DEFAULT_COUNTRIES = ["France", "Germany", "Spain", "Italy"]

    def __init__(self):
        self.api = PlaneAPI()
        self.db = DBManager()

    def load_countries(self, countries: List[str]) -> None:
        """
        Загружает список стран в таблицу countries.
        """
        self.db.connect()
        try:
            for country in countries:
                bbox = self.api.get_country_bounds(country)
                self.db.cur.execute(
                    """
                    INSERT INTO countries (name, bounding_box, last_updated)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO UPDATE
                    SET bounding_box = EXCLUDED.bounding_box,
                        last_updated = EXCLUDED.last_updated
                """,
                    (country, str(bbox), datetime.now()),
                )
                logger.info(f"Страна '{country}' добавлена/обновлена")
            self.db.conn.commit()
        except Exception as e:
            logger.error(f"Ошибка при загрузке стран: {e}")
            self.db.conn.rollback()
        finally:
            self.db.disconnect()

    def load_aeroplanes_for_country(self, country: str) -> int:
        """
        Загружает самолёты для указанной страны.
        Возвращает количество загруженных самолётов.
        """
        # Получаем country_id
        self.db.connect()
        self.db.cur.execute("SELECT id FROM countries WHERE name = %s", (country,))
        result = self.db.cur.fetchone()
        if not result:
            logger.error(f"Страна '{country}' не найдена в БД")
            self.db.disconnect()
            return 0
        country_id = result[0]

        # Получаем данные из API
        aeroplanes = self.api.get_aeroplanes_by_country(country)
        if not aeroplanes:
            logger.warning(f"Нет данных о самолётах для страны '{country}'")
            self.db.disconnect()
            return 0

        count = 0
        try:
            for plane in aeroplanes:
                if not plane or len(plane) < 10:
                    continue
                self.db.cur.execute(
                    """
                    INSERT INTO aeroplanes (icao24, callsign, origin_country, velocity, baro_altitude, country_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (
                        plane[0],  # icao24
                        plane[1],  # callsign
                        plane[2],  # origin_country
                        plane[9] if len(plane) > 9 else None,  # velocity
                        plane[7] if len(plane) > 7 else None,  # baro_altitude
                        country_id,
                    ),
                )
                count += 1
            self.db.conn.commit()
            logger.info(f"Загружено {count} самолётов для страны '{country}'")
        except Exception as e:
            logger.error(f"Ошибка при загрузке самолётов для {country}: {e}")
            self.db.conn.rollback()
        finally:
            self.db.disconnect()
        return count

    def load_all_countries_aeroplanes(self, countries: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Загружает самолёты для всех указанных стран.
        Возвращает словарь {страна: количество_самолётов}
        """
        if countries is None:
            countries = self.DEFAULT_COUNTRIES

        results = {}
        for country in countries:
            count = self.load_aeroplanes_for_country(country)
            results[country] = count
        return results

    def run_full_etl(self, countries: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Выполняет полный ETL-процесс:
        1. Загружает страны
        2. Загружает самолёты для всех стран
        """
        if countries is None:
            countries = self.DEFAULT_COUNTRIES

        self.load_countries(countries)
        return self.load_all_countries_aeroplanes(countries)
