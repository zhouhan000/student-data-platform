import sqlite3
from pathlib import Path

from .grading import get_grade

DB_PATH = Path(__file__).resolve().parent.parent / "students.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

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

def add_student_to_db(name, score, grade):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students (name, score, grade)
        VALUES (?, ?, ?)
        """,
        (name, score, grade)
    )

    student_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return student_id

def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, score, grade FROM students"
    )
    students = cursor.fetchall()
    connection.close()
    return students

def find_student_by_id(student_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, name, score, grade FROM students
        WHERE id = ?
        """,
        (student_id,)
    )
    student = cursor.fetchone()
    connection.close()
    return student

def delete_student_by_id(student_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM students 
        WHERE id = ?
        """,
        (student_id,)
    )
    deleted_count = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted_count > 0

def update_student_grade_by_id(student_id, new_score):
    connection = get_connection()
    cursor = connection.cursor()
    new_grade = get_grade(new_score)
    cursor.execute(
        """
        UPDATE students 
        SET score = ?, grade = ?
        WHERE id = ?
        """,
        (new_score, new_grade, student_id)
    )
    update_count = cursor.rowcount
    connection.commit()
    connection.close()
    return update_count > 0


if __name__ == "__main__":
    init_db()
