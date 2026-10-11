# 学生管理 API

使用 FastAPI + SQLite 实现的学生管理后端。当前只维护 Web API，早期命令行版本归档在 `legacy/`，不再作为当前运行入口。

## 当前功能

- 创建、查询、更新和删除学生。
- 创建时提交姓名和成绩，更新时只提交成绩。
- 服务端根据成绩计算等级，客户端无需提交等级。
- 成绩范围为 0 到 100；无效请求返回 422，不存在的学生返回 404。
- 自动化测试使用临时数据库，不修改日常使用的数据库。
- 创建学生时去除姓名首尾空白，保留中间空格；处理后的姓名长度为 1～50 个字符，允许同名。

成绩等级：90 分及以上为“优秀”，80 分及以上为“良好”，60 分及以上为“及格”，其余为“不及格”。

成绩统计、JSON 备份恢复和 CSV 导出属于历史命令行功能，目前没有对应的 Web API。


## 项目结构

```text
py_project01/
├── app/
│   ├── __init__.py
│   ├── api.py                 # 请求模型、响应模型与 HTTP 接口
│   ├── database.py            # SQLite 数据操作
│   └── grading.py             # 成绩等级规则
├── tests/
│   └── test_api.py            # API 回归测试
├── legacy/
│   ├── README.md              # 历史版本说明
│   ├── json_cli/              # 早期 JSON 命令行代码及原始说明
│   └── sqlite_cli/            # 早期 SQLite 命令行代码
├── 第一章/                     # 保留历史本地数据，已不是源码入口
├── students.db                # 当前 API 数据库，本地生成且不提交 Git
├── pytest.ini
├── requirements.txt
└── README.md
```

## 环境准备

当前环境使用 Python 3.13。以下命令都在项目根目录执行，不再进入 `第一章`。

没有虚拟环境时先创建；已有 `.venv` 可跳过：

```powershell
python -m venv .venv
```

安装依赖：

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

下面显式使用项目虚拟环境中的 Python，不依赖终端是否已激活虚拟环境。

## 初始化与启动

首次使用或数据库尚未建表时初始化。此命令使用 `CREATE TABLE IF NOT EXISTS`，不会清空现有学生记录：

```powershell
& .\.venv\Scripts\python.exe -c "from app.database import init_db; init_db()"
```

启动开发服务：

```powershell
& .\.venv\Scripts\python.exe -m uvicorn app.api:app --reload --reload-dir app
```

保持终端运行，打开 [接口测试页面](http://127.0.0.1:8000/docs)。按 Ctrl+C 停止服务。

旧的 `uvicorn api:app` 和 `第一章/api.py` 运行配置已不适用，请使用上面的新入口。若旧服务仍占用 8000 端口，先在原终端停止它。

## 接口契约

| 方法 | 路径 | 请求 | 成功响应 |
| --- | --- | --- | --- |
| GET | `/` | 无 | 200，运行状态消息 |
| POST | `/students` | `name`、`score` | 201，完整学生信息 |
| GET | `/students` | 无 | 200，学生列表 |
| GET | `/students/{student_id}` | 路径中的 ID | 200，完整学生信息 |
| PUT | `/students/{student_id}` | `score` | 200，更新成功消息 |
| DELETE | `/students/{student_id}` | 路径中的 ID | 200，删除成功消息 |

创建请求：

```json
{"name": "王五", "score": 95}
```

创建响应包含 `id`、`name`、`score`、`grade`；95 分的等级为“优秀”。ID 由数据库生成，不由客户端指定。

更新请求：

```json
{"score": 75}
```

更新成功返回 `{"message": "学生更新成功"}`；可再次查询确认成绩为 75、等级为“及格”。

不存在的学生返回 404 和 `{"detail": "未找到该学生"}`。

## 运行测试

无需先启动 Uvicorn。测试客户端在进程内调用应用，数据库相关测试会先切换临时数据库路径，再初始化表：

```powershell
& .\.venv\Scripts\python.exe -m pytest -v
```

`pytest.ini` 将测试目录限定为 `tests/`，并把项目根目录加入导入路径，避免手动修改 `sys.path`。

当前测试覆盖创建、查询、合法与非法更新、删除、删除后的 404，以及列表中的学生存在性。测试还覆盖姓名空白、长度边界和同名学生。

测试中可能出现 `StarletteDeprecationWarning`：当前测试客户端仍使用 `httpx`。它是待处理的依赖兼容提醒，不应直接隐藏，也不等于测试失败。

## 数据与历史代码

- 当前 API 始终使用项目根目录的 `students.db`，不随终端工作目录变化。
- `第一章/` 中的旧 SQLite、JSON 和备份数据保留原位置，不会被当前 API 自动使用或合并。
- 数据文件被 Git 忽略；Git 提交不能替代数据备份，不要把它们当作无用代码删除。
- 历史代码的维护状态见 [legacy/README.md](legacy/README.md)，原有版本也可通过 Git 历史查阅。

## 后续待办

后续仍需完善成绩边界用例、数据库约束和异常处理。

已有数据库可能保留早期测试产生的非法成绩，导致查询响应校验失败。应核实日志与记录来源，再决定修正方式，不要直接清空数据库。
