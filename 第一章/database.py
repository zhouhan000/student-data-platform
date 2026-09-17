import sqlite3

connection = sqlite3.connect("students.db")
print("数据库连接成功")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score REAL NOT NULL,
        grade TEXT NOT NULL
    )
""")
connection.commit()
connection.close()