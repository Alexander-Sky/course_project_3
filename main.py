from src.db_manager import DBManager

db = DBManager()

print("📊 Страны и количество самолётов:")
for row in db.get_countries_and_aeroplanes_count():
    print(f"  {row[0]}: {row[1]}")

print(f"\n🏁 Средняя скорость самолётов: {db.get_avg_speed():.2f} м/с")

print("\n🚀 Самолёты со скоростью выше средней (топ-5):")
for row in db.get_aeroplanes_with_higher_speed()[:5]:
    print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]:.1f} м/с")

keyword = input("\n🔍 Введите ключевое слово для поиска по позывному: ")
result = db.get_aeroplanes_with_keyword(keyword)
print(f"Найдено самолётов: {len(result)}")