import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.etl import DataLoader

# Создаём загрузчик
loader = DataLoader()

# Запускаем полный ETL-процесс
countries = ["France", "Germany", "Spain", "Italy"]
results = loader.run_full_etl(countries)

print("\n📊 Результаты загрузки:")
for country, count in results.items():
    print(f"  ✈️  {country}: {count} самолётов")

# Проверим, что данные действительно в БД
print("\n📋 Проверка данных в БД...")
loader.db.connect()
loader.db.cur.execute("SELECT COUNT(*) FROM aeroplanes")
total = loader.db.cur.fetchone()[0]
print(f"  Всего записей в таблице aeroplanes: {total}")
loader.db.disconnect()