from storage import get_grade
class StudentManager:
    def __init__(self, students):
        self.students = students

    def show_students(self):
        for student in self.students:
            print(
                f"姓名：{student['name']}，"
                f"成绩：{student['score']}，"
                f"等级：{student['grade']}"
            )
    def add_student(self, name, score):
        if name.strip() == "":
            return "invalid_name"

        if score < 0 or score > 100:
            return "invalid_score"

        if self.find_student(name) is not None:
            return "duplicate_student"

        student = {
            "name": name,
            "score": score,
            "grade": get_grade(score)
        }

        self.students.append(student)
        return "success"
    def find_student(self, target_name):
        for student in self.students:
            if student['name'] == target_name:
                return student
        return None

    def update_score(self, target_name, new_score):
        student = self.find_student(target_name)
        if student:
            student['score'] = new_score
            student['grade'] = get_grade(new_score)
            return True
        return False

    def delete_student(self, target_name):
        student = self.find_student(target_name)

        if student is None:
            return False

        self.students.remove(student)
        return True
    def find_top_students(self):
        if len(self.students) == 0:
            return []

        max_score = self.students[0]["score"]

        for student in self.students:
            if student["score"] > max_score:
                max_score = student["score"]

        top_students = []

        for student in self.students:
            if student["score"] == max_score:
                top_students.append(student)

        return top_students
    def show_statistics(self):
        if len(self.students) == 0:
            print("目前没有学生数据")
            return

        scores = []

        for student in self.students:
            scores.append(student["score"])

        average = sum(scores) / len(scores)
        passed_count = 0

        for score in scores:
            if score >= 60:
                passed_count += 1

        pass_rate = passed_count / len(scores) * 100

        print(f"学生人数：{len(self.students)}")
        print(f"平均成绩：{average:.2f}")
        print(f"最高成绩：{max(scores)}")
        print(f"最低成绩：{min(scores)}")
        print(f"及格人数：{passed_count}")
        print(f"及格率：{pass_rate:.2f}%")

if __name__ == "__main__":
    test_students = [
        {"name": "小明", "score": 85, "grade": "良好"}
    ]
    manager = StudentManager(test_students)
    new_student = {
        "name": "小红",
        "score": 92,
        "grade": "优秀"
    }
    manager.show_students()
    print(manager.find_student("小红"))
    print(manager.find_student("不存在"))
    print(manager.update_score("小明", 95))
    manager.show_students()
    print(manager.delete_student("小红"))
    manager.show_students()
    print(manager.delete_student("不存在"))
    print(manager.find_top_students())