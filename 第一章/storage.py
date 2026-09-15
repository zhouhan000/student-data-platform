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


def get_grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


def delete_student(students, target_name):
    for student in students:
        if student['name'] == target_name:
            students.remove(student)
            return True
    return False


def find_student(students, target_name):
    for student in students:
        if student['name'] == target_name:
            return student
    return None


def update_score(students, target_name, new_score):
    for student in students:
        if student['name'] == target_name:
            student['score'] = new_score
            student['grade'] = get_grade(new_score)
            return True
    return False


def add_student(students, name, score):
    if name.strip() == "":
        return "invalid_name"
    if score < 0 or score > 100:
        return "invalid_score"
    if find_student(students, name) is not None:
        return "duplicate_student"

    student = {
        "name": name,
        "score": score,
        "grade": get_grade(score)
    }
    students.append(student)
    return "success"


def print_students(students):
    # 遍历并输出所有学生
    for student in students:
        print(f"姓名：{student['name']}，"
              f"成绩{student['score']}，"
              f"等级{student['grade']}")


def find_top_students(students):
    if len(students) == 0:
        return []
    max_score = students[0]['score']
    for student in students:
        if student['score'] > max_score:
            max_score = student['score']
    top_students = []
    for student in students:
        if student['score'] == max_score:
            top_students.append(student)

    return top_students


def show_statistics(students):
    if len(students) == 0:
        print("目前没有学生数据")
        return

    scores = []

    for student in students:
        scores.append(student["score"])

    average = sum(scores) / len(scores)
    passed_count = 0

    for score in scores:
        if score >= 60:
            passed_count += 1

    pass_rate = passed_count / len(scores) * 100

    print(f"学生人数：{len(students)}")
    print(f"平均成绩：{average:.2f}")
    print(f"最高成绩：{max(scores)}")
    print(f"最低成绩：{min(scores)}")
    print(f"及格人数：{passed_count}")
    print(f"及格率：{pass_rate:.2f}%")

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