<!-- Source blob SHA: 518c3a3514392a1251e741962c401cdbe31c8bb3 -->
# DAO — 共享工程规范

**语言：** [English](README.md) | 简体中文

DAO 是 Gonglz 各项目共享的工程规范与 Agent 开发工作流控制仓库。仓库名称为 `dao`，默认分支仍为 `main`。

## 文档

| 英文原文（权威版本） | 中文译文 | 用途 |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | [AGENTS.zh-CN.md](AGENTS.zh-CN.md) | Agent 指令与安全边界 |
| [docs/PROJECT.md](docs/PROJECT.md) | [docs/PROJECT.zh-CN.md](docs/PROJECT.zh-CN.md) | GitHub、Runner 与执行证据工作流 |
| [templates/CHAT_TASK_PROMPT.md](templates/CHAT_TASK_PROMPT.md) | [templates/CHAT_TASK_PROMPT.zh-CN.md](templates/CHAT_TASK_PROMPT.zh-CN.md) | 精简的任务提示词模板 |

## 规范效力与翻译维护

**英文文档是唯一具有规范效力的工程文件**。中文文档是为读者维护的翻译，不构成第二套独立的规范。文档同步检查用于发现英文原文已经发生变化但对应中文译文尚未同步的情况；它**不能**证明翻译在语义上完全准确。

各项目自己的架构、契约、代码、测试、部署路径和生产权限仍归各自的项目仓库所有。DAO 只负责共享约定；CI 测试通过不等于获得生产部署授权。
