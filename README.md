# 学生信息管理系统

一个 Python 学生信息管理练习项目，包含早期命令行版本，以及使用 FastAPI + SQLite 实现的 Web API。
## 功能

- 学生信息增删改查
- JSON 数据持久化
- 数据备份与恢复
- 成绩统计
- 最高分查询
- 学生数据导出
- 输入和文件异常处理
## 项目结构

```text
第一章/
├── 学生信息管理.py    # 主程序与菜单
├── student_manager.py # 学生管理类
└── storage.py         # 数据保存、读取、备份和恢复
```

## 运行方式

```bash
python 第一章/学生信息管理.py
```
## Web API（FastAPI + SQLite）

在项目根目录安装依赖：

```powershell
python -m pip install -r requirements.txt
```

首次运行时，创建数据库表并启动服务：

```powershell
cd 第一章
python -c "from database import init_db; init_db()"
python -m uvicorn api:app --reload
```

启动后访问 http://127.0.0.1:8000/docs，可以在页面中试用接口。

运行自动化测试时，请回到项目根目录执行：

```powershell
python -m pytest tests/test_api.py -v
```