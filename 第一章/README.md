# 历史本地数据目录

这里已不是当前程序的源码目录。

- JSON 命令行源码已归档到 `legacy/json_cli/`。
- SQLite 命令行源码已归档到 `legacy/sqlite_cli/`。
- 当前 API 源码位于 `app/`，启动与测试方式见项目根目录 README。

现有 `students.json`、`students_backup.json` 和 `students.db` 等本地数据保留原位置，本次没有移动、合并或清理它们。这些文件通常不提交 Git，其他机器克隆后不一定存在。

当前 API 使用项目根目录的 `students.db`，不是本目录内的数据库。不要直接删除或合并两份数据库；整理数据前请先备份并确认用途。
