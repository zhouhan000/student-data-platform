from database import (
    get_all_students,
    find_student_by_name,
    add_student_to_db,
    update_student_grade,
    delete_student_by_name
)
from storage import get_grade

class DatabaseStudentManager:
    def show_students(self):
        students = get_all_students()

        for name, score, grade in students:
            print(
                f"姓名：{name}，"
                f"成绩：{score}，"
                f"等级：{grade}"
            )
    def add_student(self, name, score):
        if name.strip() == "":
            return "invalid_name"
        name = name.strip()
        if score < 0 or score > 100:
            return "invalid_score"

        if find_student_by_name(name) is not None:
            return "duplicate_student"

        add_student_to_db(name, score, get_grade(score))
        return "success"

    def find_student(self, target_name):
        return find_student_by_name(target_name)

    def update_score(self, target_name, new_score):
        if new_score < 0 or new_score > 100:
            return False

        return update_student_grade(
            target_name,
            new_score,
            get_grade(new_score)
        )

    def delete_student(self, target_name):
        return delete_student_by_name(target_name)