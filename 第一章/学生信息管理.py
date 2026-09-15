from storage import save_students
from storage import load_students
from storage import backup_students
from storage import restore_students
from storage import input_score
from storage import export_students
from student_manager import StudentManager
def show_menu():
    print("\n------------学生信息管理系统------------")
    print("1.显示所有学生")
    print("2.查询学生")
    print("3.修改成绩")
    print("4.删除学生")
    print("5.增加学生")
    print("6.成绩统计")
    print("7.查看最高分学生")
    print("8.备份学生数据")
    print("9.恢复备份数据")
    print("10.导出学生数据")
    print("0.退出系统")
def main():
    students = load_students()
    manager = StudentManager(students)
    while True:
        show_menu()
        choice = input("请选择功能")
        if choice == "1":
            manager.show_students()

        elif choice == "2":
            target_name = input("请输入要查询的学生名字：")
            result = manager.find_student(target_name)
            if result is None:
                print("没有查询到这名学生")
            else:
                print(f"学生名字：{result['name']},"
                      f"学生成绩：{result['score']},"
                      f"学生等级：{result['grade']}"
                      )

        elif choice == "3":
            target_name = input("请输入你要修改成绩的学生:")
            target_score = input_score()
            success = manager.update_score(target_name, target_score)
            if success:
                save_students(students)
                print("修改成功")
            else:
                print("没有查找到这个学生")

        elif choice == "4":
            target_name = input("请输入你要删除学生的姓名：")
            success = manager.delete_student(target_name)
            if success:
                save_students(students)
                print("删除成功")
            else:
                print("没有查找到这个学生")

        elif choice == "5":
            name = input("请输入你要添加学生的名字：")
            score = input_score()
            result = manager.add_student(name, score)
            if result == "success":
                save_students(students)
                print("添加成功")
            elif result == "invalid_score":
                print("成绩无效")
            elif result == "invalid_name":
                print("姓名不能为空")
            elif result == "duplicate_student":
                print("姓名重复")

        elif choice == "6":
            manager.show_statistics()


        elif choice == "7":
            results = manager.find_top_students()
            if len(results) == 0:
                print("没有学生数据")
            else:
                print("最高分学生：")
                for student in results:
                    print(
                        f"姓名：{student['name']}，"
                        f"成绩：{student['score']}，"
                        f"等级：{student['grade']}"
                    )

        elif choice == "8":
            backup_students(manager.students)

        elif choice == "9":
            confirm = input("恢复备份会覆盖当前数据，确认恢复吗？(y/n)：")

            if confirm == "y":
                restored_students = restore_students()

                if restored_students is None:
                    print("恢复失败")
                else:
                    students = restored_students
                    manager.students = students
                    save_students(manager.students)
                    print("数据恢复成功")
            else:
                print("已取消恢复")

        elif choice == "10":
            export_students(manager.students)

        elif choice == "0":
            save_students(students)
            print("数据已保存，程序已退出")
            break

        else:
            print("功能编号错误，请重新输入")
if __name__ == "__main__":
    main()