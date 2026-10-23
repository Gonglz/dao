<!-- Source blob SHA: cb1f28e1c6f195672ec237ed3a9686453c4f5106 -->
# 共享工程开发闭环（中文译文）

**状态：Repository Agent Contract v1.3**  
**采用日期：2026-09-18**

[English — 唯一权威规范](PROJECT.md) | **简体中文 — 非独立规范**

## 目的

在不构建复杂编排平台的前提下，为 Gonglz 各仓库统一开发闭环：

```text
Chat
  ↓ 意图／审批
GitHub Ticket / Branch / PR
  ↓
本地或自托管 Runner
  ↓
/var/tmp/<repo>/<run_id>/
  ├── status.json      # 可变的当前状态
  ├── result.json      # 终态证据
  └── raw artifacts    # 原始产物
  ↓
status/result + GitHub 审计
  ↓
Windows 桌面通知
  ↓
仅在需要时由 Chat 复审
```

GitHub 是控制面。Chat 用于操作与决策，不充当项目状态数据库，也不承担长时间执行器的职责。

## 仓库最小结构

每个活跃仓库通常只需要：

```text
AGENTS.md
README.md

docs/
├── PROJECT.md
├── _tmp/        # 需要时保存正在进行的 Ticket 工作空间
└── audits/      # 只有值得长期保留的证据才放这里
```

其他开发文档、索引和子系统文档都是可选项；只有确实需要时才增加。

## 权威来源模型

不能把任务意图与当前实现状态压成同一套权威优先级。

### 任务权威——应该改变什么

1. 当前明确的任务或 Ticket 契约
2. 目标仓库 `AGENTS.md` 的工作流与安全规则
3. 仍在维护的项目／子系统文档

Ticket 定义目标、范围、限制、证据要求和完成标准；它本身不证明所描述的目标状态已经实现。

### 实现权威——当前实际存在什么

1. 当前代码与生效配置
2. 可执行测试与契约
3. 最新的只读运行／生产证据
4. 当前维护的项目文档
5. 历史审计、收尾记录、工作日志、旧计划及聊天记录

曾经通过的审计不证明今天仍然正确；使用旧方案／旧规格前，必须与当前代码、测试及运行证据对账。

项目专用规则保留在项目仓库。本仓库只负责公共约定。

## Agent 工作流

开始工作前：

- 阅读目标仓库的 `AGENTS.md` 和 `docs/PROJECT.md`（如果存在）
- 阅读当前任务／Ticket 契约
- 检查分支、HEAD、工作树以及相关代码实现
- 核查实际运行／生产事实，不做无证据推断

工作过程中：

- 不直接在 `main` 开发
- 一个有边界的任务对应一个短期分支
- 做最小但完整的改动
- 行为发生变化时增加或更新测试
- 迭代时跑定向测试，收尾前跑全部必要 Gate
- 除非明确授权，否则开发与验证不得改动生产环境
- 不向 Git、日志或 Artifact 暴露密钥

完成前：

- 运行要求的 Gate
- 审阅 Diff
- 只在持久事实变化时更新长期文档
- 提供当前仓库实际可产生的证据
- Commit、Push，并更新 PR

## Ticket 工作空间

规范的临时任务路径：

```text
docs/_tmp/TICKET_xxx/
```

典型文件：

```text
PROMPT.md
PLAN.md
CHECKPOINT.md
FINDINGS.md
```

任务收尾时：

- 将长期事实提炼到当前维护的文档或 `docs/audits/`
- 清除过时提示词、重复分析和一次性记录
- 不要因为 Agent 曾生成某份材料就长期保留它

新任务不得再使用旧式单文件路径 `docs/_tmp/TICKET_xxx_PROMPT.md`。

## 运行状态与证据

原始运行数据不应提交到 Git。

共享结构化证据接口是：

```text
/var/tmp/<repo>/<run_id>/
```

`run_id` 格式为：

```text
<UTC timestamp>_<git short sha>
```

例如：`20260908T070500Z_8bcddae`。

任务运行期间可以维护：

```json
{
  "run_id": "...",
  "state": "RUNNING",
  "phase": "...",
  "progress": {"completed": 47, "total": 120},
  "updated_at": "...",
  "needs_user": false,
  "message": "..."
}
```

任务需要人工判断时转为 `WAITING_APPROVAL`；普通任务的继续执行不应依赖用户反复发送“继续”。

任务进入终态时生成：

```json
{
  "run_id": "...",
  "commit": "...",
  "branch": "...",
  "runner": "...",
  "status": "PASS|FAIL|BLOCKED|CANCELLED",
  "gates": {},
  "failures": []
}
```

查询进度读取 `status.json`，查询终态读取 `result.json`，仅在诊断时查看原始日志。

### 异步执行与通知

不需要人工判断的有界任务交由可持续运行的 Runner 执行。Chat 可以启动或检查任务，但任务必须能够在聊天结束后继续存在。

默认仅在有实际价值的状态转换时通知：

- `WAITING_APPROVAL`
- `BLOCKED`
- `PASS`
- `FAIL`

Windows 桌面是默认通知终端。原生 Windows Runner 直接显示通知；WSL、Pi、Jetson 和 macOS 通过私有 Tailscale 通道向 Windows Relay 发送同类事件。GitHub Issue/PR 评论是可选的持久审计记录，不是通知 Gate。

通知送达不替代 `status.json` 或 `result.json`。通知失败应独立呈现，但不能把成功的任务结果改写为失败。

参考实现刻意保持精简：

- `scripts/async_harness.py`：提供 `start`、`set`、`run`、`status`
- `scripts/windows_notify_relay.py`：经认证且绑定 Tailscale 的 Windows 通知中继

应从目标仓库或 Worktree 启动 Harness，使其正确记录 Git 元数据。原生 Windows Runner 直接通知；WSL 视为非 Windows Runner，即使其 `PATH` 中含有 Windows 可执行文件但 WSLInterop 已停用，也仍通过认证的 Relay 发送通知。非 Windows 主机从 `~/.config/gonglz/async-harness.json` 或等价环境变量读取中继配置。配置可以使用 `token` 或 `token_file`；若已能通过私有挂载路径访问 Windows Relay Token，应优先使用 `token_file`。密钥不得进入 Git。

### 实现状态规则

契约只定义接口，不表示所有采用它的仓库已经生成 `result.json` 或上传 Artifact。

只有实际 Runner／Workflow 产生并发布相应证据时，仓库才可以声称已实现结构化证据接口。否则 GitHub Checks 和日志仍是有效依据，但不能谎称已实现。

运行文件由 GitHub Actions Artifacts 保存；Git 仅存储长期有价值、便于人工阅读的审计结论（`docs/audits/`）。

### 保留期限

`/var/tmp/<repo>/<run_id>/` 是可以清理的运行状态。

默认策略：

- 成功运行的证据及 Artifact 按要求发布后，可以删除原始目录
- 失败运行可以暂时保留以供诊断
- 主机上的运行目录必须有保留期限；默认 **7 天**
- 项目可以基于明确的运维需求自行规定例外

不要专门为这个契约开发日志管理服务；尽量使用主机已有的清理机制。

## Git 中应保留什么

应保留：

- 源代码与测试
- 配置模板与迁移文件
- 当前项目文档
- 持久的架构／运维决策
- 有选择地保留的审计或收尾证据

默认不保留：

- pytest、Docker、systemd 日志
- 覆盖率及构建输出
- Trace 和调试转储
- 日常运行生成的截图
- 中间数据集
- 临时 Agent 分析

## 完成契约

跨仓库固定使用以下顶层完成字段：

```text
CODE_OR_DOCS_COMPLETE
REQUIRED_GATES_PASS
EVIDENCE_AVAILABLE
DOCS_CURRENT
WORKTREE_CLEAN
COMMIT_PUSHED
PR_UPDATED
```

项目特定验证应放在该仓库的 Gate／证据模型中，例如：

```json
{
  "gates": {
    "python_tests": "PASS",
    "frontend_build": "PASS"
  }
}
```

不得对项目专用检查重命名顶层字段，也不得创造竞争性的顶层完成字段。

必要项目不满足时，应标记为未完成或阻塞；不适用项目明确说明。

## 角色

不要默认引入复杂的多 Agent 组织；只维持逻辑职责边界：

- **Builder（构建者）**：可以修改代码和文档；不自动获得生产权限。
- **Verifier（验证者）**：独立验证；不应在同一轮审核中直接修复自己正在审查的内容。
- **Operator（操作者）**：仅执行已明确授权的部署和生产变更。

同一个 ChatGPT/Codex 系统可以在不同阶段承担这些角色，但权限边界必须明确。

## 采用方式

已知采用 Repository Agent Contract v1 系列的仓库包括：

- `Gonglz/Quant-v2`
- `Gonglz/obsidian_repo`
- `Gonglz/pi-console`
- `Gonglz/media-ingest`

各仓库必须明确决定是否采用更新版本；DAO 的变化不会自动修改项目的本地规则。`Gonglz/dao` 是当前共享契约版本的初始权威仓库。

## 文档一致性检查

所有具有实质内容的 PR 都必须声明是否影响当前维护的文档。使用共享的 `scripts/check_pr_docs.py` 检查器和仓库的 PR 模板。该检查器只验证文档影响声明，**不能替代**对 API、时间语义或实际行为的可执行契约测试。改变契约政策须经过明确审核，才能合并。历史审计和 Ticket 记录不是当前有效规范。仓库所有权、现有 CI 和发布授权边界保持不变。
