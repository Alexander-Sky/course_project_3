from src.db_manager import DBManager

db = DBManager()
db.connect()
db.create_tables()
print("Таблицы созданы успешно!")
db.disconnect()