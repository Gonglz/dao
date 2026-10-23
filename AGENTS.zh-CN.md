<!-- Source blob SHA: 928c544e9292935047fe533a801d2ea438f7404c -->
# Agent 指令（中文译文）

**Repository Agent Contract：** v1.3

[English — 唯一权威规范](AGENTS.md) | **简体中文 — 非独立规范**

本仓库是 Gonglz 各仓库共享的工程约定控制面。

## 阅读顺序

1. `AGENTS.md`
2. `docs/PROJECT.md`
3. 当前任务、分支和 PR 状态
4. 如果需要核实跨仓库事实，再检查受影响仓库的证据

## 权威来源模型

不要把“任务想改变什么”和“当前实际实现是什么”合并成同一份优先级列表。

### 任务权威——应该改变什么

1. 当前明确的任务或 Ticket 契约
2. 目标仓库 `AGENTS.md` 的安全及工作流规则
3. 仍在维护的项目／子系统文档

### 实现权威——目前实际存在什么

1. 当前仓库代码与生效的配置
2. 可执行测试与契约
3. 新鲜的运行证据
4. 当前维护的项目文档
5. 历史审计、收尾报告、旧计划及聊天记录

DAO 只拥有共享工作流和证据约定。每个项目仓库自行拥有架构、代码、测试、生产路径和项目专用规则。

## 变更规则

- 除无法避免的仓库初始化外，不直接在 `main` 上开发。
- 实质性变更使用短期分支和 PR。
- 保持 DAO 仓库精简，不在此复制项目专用文档。
- 没有明确需求，不增加 Agent、Schema、自动化或流程层级。
- 区分开发、验证和生产操作。
- CI 通过绝不意味着取得部署许可。
- 不向 Git 提交密钥或原始运行日志。

## 自主执行

任务具备确定目标、安全执行边界和可验证完成条件时，不应仅仅为了继续执行而反复要求用户发送提示。

- 自主完成普通实施与验证步骤。
- 把确定性的长时间任务放在可持久运行的本地或自托管 Runner 上，而不是依赖聊天会话持续存在。
- 只在需要用户判断、授权、凭据、破坏性操作、待定政策／架构决策或存在真实阻塞时暂停。
- 不要无限重试；应明确报告重复发生或无法恢复的失败。
- 使用下文的结构化执行状态，使后续会话无需依赖聊天记录即可恢复进度。

## Ticket 工作空间

临时任务工作空间的规范路径为：

```text
docs/_tmp/TICKET_xxx/
```

典型文件：`PROMPT.md`、`PLAN.md`、`CHECKPOINT.md`、`FINDINGS.md`。

任务收尾时，只将持久知识整理进当前维护的文档或 `docs/audits/`；清理一次性提示词、重复分析和自动生成的日志。

## 结构化证据接口

Repository Agent Contract v1.3 定义了结构化执行／证据接口，但**只有 Runner 或工作流实际产生相应文件时**，项目才能声称已实现。

实际接入后，Git 之外的运行产物放在：

```text
/var/tmp/<repo>/<run_id>/
```

其中：

```text
run_id = <UTC timestamp>_<git short sha>
```

执行期间可以维护可变的 `status.json`，至少包含：

- `run_id`
- `state`：`PENDING|RUNNING|WAITING_APPROVAL|BLOCKED|PASS|FAIL|CANCELLED`
- `phase`
- `progress`
- `updated_at`
- `needs_user`
- `message`

`status.json` 是当前运行状态，而非永久验收证据。用户询问“现在进行到哪一步”时，优先读取它。

执行进入终态时，生成至少包含以下字段的 `result.json`：

- `run_id`
- `commit`
- `branch`
- `runner`
- `status`
- `gates`
- `failures`

对执行中的任务优先读取 `status.json`；已完成任务以 `result.json` 为终态证据。只有诊断需要时才展开原始日志。原始证据可作为 GitHub Actions Artifact 上传；提交进 Git 的应当是长期有价值的审计结论。

通知只是输出渠道，不是事实来源。默认通知终端是用户的 Windows 桌面：Windows 原生 Runner 直接通知；WSL、Pi、Jetson 和 macOS 通过私有 Tailscale 路径中继。GitHub 可以同时保留审计记录，但通知是否送达不是执行状态的权威依据。`status.json`／`result.json` 仍是权威状态。

在仓库真正接入该接口以前，GitHub Checks 和日志仍然是有效证据，不得声称已产生 `result.json` 或完成 Artifact 发布。

## 完成契约

下列顶层完成字段必须保持完全一致；项目特定 Gate 应写入证据负载，而不是改名或另造顶层字段。

```text
CODE_OR_DOCS_COMPLETE
REQUIRED_GATES_PASS
EVIDENCE_AVAILABLE
DOCS_CURRENT
WORKTREE_CLEAN
COMMIT_PUSHED
PR_UPDATED
```

必要项目未满足时，必须报告未完成或阻塞，而不是 `PASS`。不适用的项目应明确标注。

## 文档一致性检查

所有具有实质内容的 PR 都必须声明是否影响当前维护的文档。使用共享的 `scripts/check_pr_docs.py` 检查器和仓库的 PR 模板。该检查器只验证文档影响声明，**不能替代**对 API、时间语义或实际行为的可执行契约测试。改变契约政策须经过明确审核，才能合并。历史审计和 Ticket 记录不是当前有效规范。仓库所有权、现有 CI 和发布授权边界保持不变。
