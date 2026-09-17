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

def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, score, grade FROM students"
    )
    students = cursor.fetchall()
    connection.close()
    return students

def find_student_by_name(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT name, score, grade FROM students
        WHERE name = ?
        """,
        (name,)
    )
    student = cursor.fetchone()
    connection.close()
    return student

def delete_student_by_name(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM students 
        WHERE name = ?
        """,
        (name,)
    )
    deleted_count = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted_count>0

def update_student_grade(name,new_score,new_grade):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE students 
        SET score = ?, grade = ?
        WHERE name = ?
        """,
        (new_score,new_grade,name)
    )
    update_count = cursor.rowcount
    connection.commit()
    connection.close()
    return update_count>0


if __name__ == '__main__':
    init_db()
