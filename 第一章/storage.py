import json
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "students.json")
BACKUP_FILE = os.path.join(BASE_DIR, "students_backup.json")
EXPORT_FILE = os.path.join(BASE_DIR, "students.csv")

def save_students(students):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, ensure_ascii=False, indent=4)
            print("保存成功")
    except OSError:
        print("保存失败")

def load_students():
    try:
        with open(DATA_FILE,"r",encoding="utf-8")as file:
            students = json.load(file)
            return students
    except FileNotFoundError:
        print("没有找到数据文件，将创建空空空数据")
        return []

    except json.JSONDecodeError:
        print("数据文件内容损坏，将使用空数据")
        return []

def backup_students(students):
    try:
        with open(BACKUP_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, ensure_ascii=False, indent=4)
        print("数据备份成功")
    except OSError:
        print("数据备份失败")

def restore_students():
    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as file:
            students = json.load(file)
            return students

    except FileNotFoundError:
        print("没有找到备份文件")
        return None

    except json.JSONDecodeError:
        print("备份文件格式错误")
        return None



def input_score(prompt="请输入成绩："):
    while True:
        try:
            score = float(input(prompt))
        except ValueError:
            print("输入错误，请输入数字")
            continue

        if 0 <= score <= 100:
            return score

        print("成绩必须在0到100之间")



def export_students(students):
    try:
        with open(
            EXPORT_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            fieldnames = ["name", "score", "grade"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)

        print("导出成功")

    except OSError:
        print("导出失败")

def get_grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"