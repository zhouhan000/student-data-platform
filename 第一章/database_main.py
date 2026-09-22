from database import init_db
from database_manager import DatabaseStudentManager
def show_menu():
    print("1.显示学生")
    print("2.添加学生")
    print("3.查询学生")
    print("4.修改学生")
    print("5.删除学生")
    print("0.退出程序")

def main():
    init_db()
    manager = DatabaseStudentManager()

    while True:
        show_menu()
        choice = input("请选择功能：").strip()

        if choice == "1":
            manager.show_students()

        elif choice == "2":
            name = input("请输入学生的姓名：").strip()
            try:
                score = float(input("请输入学生成绩："))
            except ValueError:
                print("成绩必须是数字")
                continue

            result = manager.add_student(name, score)
            print(result)


        elif choice == "3":

            target_name = input("请输入要查询的学生姓名：").strip()

            result = manager.find_student(target_name)

            if result is None:

                print("没有找到该学生")

            else:

                name, score, grade = result

                print(f"姓名：{name}，成绩：{score}，等级：{grade}")

        elif choice == "4":
            target_name = input("请输入要修改的学生姓名：").strip()

            try:
                new_score = float(input("请输入新的成绩："))
            except ValueError:
                print("成绩必须是数字")
                continue

            result = manager.update_score(target_name, new_score)

            if result:
                print("成绩修改成功")
            else:
                print("没有找到该学生，或成绩不符合要求")

        elif choice == "5":
            target_name = input("请输入要删除的学生姓名：").strip()

            result = manager.delete_student(target_name)

            if result:
                print("学生删除成功")
            else:
                print("没有找到该学生")

        elif choice == "0":
            print("程序已退出")
            break

        else:
            print("无效选择，请重新输入")




if __name__ == "__main__":
    main()