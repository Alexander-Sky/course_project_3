from src.db_manager import DBManager

db = DBManager()

print("📊 Страны и количество самолётов:")
for row in db.get_countries_and_aeroplanes_count():
    print(f"  {row[0]}: {row[1]}")

avg_speed = db.get_avg_speed()
print(
    f"\n🏁 Средняя скорость самолётов: {avg_speed:.2f} м/с ({avg_speed * 3.6:.2f} км/ч)"
)

print("\n🚀 Самолёты со скоростью выше средней (топ-10):")
# Фильтрация аномалий происходит внутри метода
for row in db.get_aeroplanes_with_higher_speed()[:10]:
    speed_ms = row[3] if row[3] else 0
    print(
        f"  {row[0]} | {row[1]} | {row[2]} | {speed_ms:.1f} м/с ({speed_ms * 3.6:.0f} км/ч)"
    )

# Подсказка для поиска
print("\n" + "=" * 50)
print("🔍 ПОИСК ПО ПОЗЫВНОМУ")
print("  Примеры позывных: RYR (Ryanair), DLH (Lufthansa), BAW (British Airways)")
print("  Или просто: ACA (Air Canada), SWR (Swiss), THY (Turkish Airlines)")
print("=" * 50)

keyword = input("\nВведите ключевое слово для поиска: ").strip().upper()
if keyword:
    result = db.get_aeroplanes_with_keyword(keyword)
    print(f"\n✈️  Найдено самолётов с позывным, содержащим '{keyword}': {len(result)}")
    for row in result[:20]:
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]:.1f} м/с")
else:
    print("❌ Ключевое слово не введено.")
