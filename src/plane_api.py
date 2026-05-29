"""
Модуль для получения данных о самолётах через API.
"""

import logging
import requests
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class PlaneAPI:
    """Класс для получения данных о самолётах через OpenSky."""

    def __init__(self):
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_bounds(self, country: str) -> List[str]:
        """Получает границы страны через Nominatim API."""
        headers = {"User-Agent": "course-project-3/1.0"}
        params = {"country": country, "format": "json", "limit": 1}

        try:
            response = requests.get(self.openstreetmap_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0].get("boundingbox", [])
        except Exception as e:
            logger.error(f"Ошибка при запросе к Nominatim: {e}")
        return []

    def get_aeroplanes_in_bbox(self, bbox: List[str]) -> List[Dict[str, Any]]:
        """Получает самолёты в заданном bounding box через OpenSky."""
        if len(bbox) != 4:
            logger.warning(f"Некорректный bbox: {bbox}")
            return []

        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3],
        }

        try:
            response = requests.get(self.opensky_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data.get("states", [])
        except Exception as e:
            logger.error(f"Ошибка при запросе к OpenSky: {e}")
            return []

    def get_aeroplanes_by_country(self, country: str) -> List[Dict[str, Any]]:
        """Получает все самолёты над указанной страной."""
        bbox = self.get_country_bounds(country)
        if not bbox:
            logger.error(f"Не удалось получить границы для страны: {country}")
            return []
        return self.get_aeroplanes_in_bbox(bbox)