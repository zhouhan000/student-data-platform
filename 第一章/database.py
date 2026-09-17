import sqlite3
def get_connection():
    return sqlite3.connect(",tudents.db")
def init_db():
    connection = get_connection()

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

def add_student_to_db(name,score,grade):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO students (name, score, grade)
        VALUES (?, ?, ?)
        """,
        (name, score, grade)
    )
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
#    add_student_to_db("张三",90,"优秀")