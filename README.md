# ✈️ Plane Tracker — Анализ воздушного трафика

Проект для отслеживания и анализа воздушных судов в реальном времени с использованием открытых API и хранением данных в PostgreSQL.

## 🚀 Функциональность

  - Сбор данных из двух API:
  - 🌍 [Nominatim](https://nominatim.openstreetmap.org/) — получение географических границ стран
  - ✈️ [OpenSky Network](https://opensky-network.org/) — информация о самолётах
  - Загрузка данных в PostgreSQL через ETL-процесс
  - Аналитика через класс `DBManager`:
  - 📊 Список стран с количеством самолётов
  - 📋 Все воздушные суда
  - 📈 Средняя скорость полёта
  - 🚀 Самолёты со скоростью выше средней (с фильтрацией аномалий)
  - 🔍 Поиск по позывному (например, `RYR`, `DLH`, `BAW`, `AFR`)
  - Интерактивный консольный интерфейс

## 🛠️ Технологии

| Технология | Назначение |
|------------|------------|
| Python 3.14 | Основной язык |
| PostgreSQL | Хранилище данных |
| psycopg2-binary | Драйвер для PostgreSQL |
| requests | Работа с API |
| pytest | Тестирование |
| poetry | Управление зависимостями |
| black, isort, flake8, mypy | Качество кода |

## 📂 Структура проекта

course_project_3/
├── src/
│ ├── db_manager.py # Класс для работы с БД (вся аналитика)
│ ├── etl.py # ETL-процесс (загрузка данных)
│ └── plane_api.py # Работа с API
├── tests/
│ ├── test_db_manager.py
│ └── test_etl.py
├── .env # Переменные окружения (БД)
├── .env.example
├── .gitignore
├── main.py # Точка входа (интерактив)
├── pyproject.toml
├── poetry.lock
└── README.md

## 🐘 База данных

Таблицы создаются автоматически при первом запуске ETL.

### Таблица `countries`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | SERIAL | Первичный ключ |
| `name` | VARCHAR(100) | Название страны |
| `bounding_box` | TEXT | Координаты (bounding box) |
| `last_updated` | TIMESTAMP | Время последнего обновления |

### Таблица `aeroplanes`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | SERIAL | Первичный ключ |
| `icao24` | VARCHAR(10) | Уникальный идентификатор борта |
| `callsign` | VARCHAR(20) | Позывной |
| `origin_country` | VARCHAR(100) | Страна регистрации |
| `velocity` | FLOAT | Скорость (м/с) |
| `baro_altitude` | FLOAT | Высота (м) |
| `country_id` | INTEGER | Внешний ключ к `countries` |

## 🔧 Установка и запуск

```bash
# 1. Клонируем репозиторий
git clone https://github.com/Alexander-Sky/course_project_3.git
cd course_project_3

# 2. Устанавливаем зависимости
poetry install

# 3. Настраиваем БД
# Создайте базу данных в PostgreSQL и заполните .env
cp .env.example .env

# 4. Запускаем ETL (загрузка данных)
poetry run python -c "from src.etl import DataLoader; DataLoader().run_full_etl(['France','Germany','Spain','Italy'])"

# 5. Запускаем интерактивную программу
poetry run python main.py
-----------------------------------------------------------------
## Пример работы

📊 Страны и количество самолётов:
  France: 9444
  Germany: 648
  Spain: 613
  Italy: 599

🏁 Средняя скорость самолётов: 153.19 м/с (551.49 км/ч)

🚀 Самолёты со скоростью выше средней (топ-10):
  738289 | ISR723   | Israel | 462.7 м/с (1666 км/ч)
  46b82c | AEE751   | Greece | 426.7 м/с (1536 км/ч)
  4a3122 | AIZ388   | Romania | 395.2 м/с (1423 км/ч)
 

🔍 ПОИСК ПО ПОЗЫВНОМУ
  Примеры: RYR (Ryanair), DLH (Lufthansa), BAW (British Airways)

Введите ключевое слово: RYR

✈️ Найдено самолётов с позывным, содержащим 'RYR': 506
  4ca4ea | RYR87CX | Ireland | 0.0 м/с
  4ca4f5 | RYR143M | Ireland | 227.7 м/с
  
------------------------------------------------------------------------------------------
##  Тестирование

poetry run pytest
poetry run pytest --cov=src

## Требования

Python 3.14+

PostgreSQL 14+

Poetry

--------------------------------------------------------------------------------------------
## Автор
Alexander Schischkin — студент курса Python-разработчик