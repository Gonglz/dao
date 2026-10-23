<!-- Source blob SHA: 5067ba0d18111bdaab9c1f905b6c3070afd3fcde -->
# Chat 任务提示词（中文译文）

[English — 唯一权威模板](CHAT_TASK_PROMPT.md) | **简体中文 — 参考译文**

这是 ChatGPT/Codex 启动仓库开发任务时使用的精简入口模板。

提示词只应传递**本次新增的任务意图**。仓库状态属于 GitHub，不属于聊天记录。

## Level 0 —— 讨论

正常交流即可。对于问答、架构讨论、审核、优先级判断和探索，无需套用模板。

例如：

```text
Quant-v2 现在还缺什么？
这个架构有没有问题？
下一步做什么？
```

## Level 1 —— 普通开发任务

适用于绝大多数代码／文档开发任务：

```text
Repository: Gonglz/<repo>

Goal:
<希望完成什么>

Scope:
<主要子系统／功能／边界>

Constraints:
- 先阅读 AGENTS.md 和 docs/PROJECT.md。
- 以当前任务作为任务权威来源。
- 以当前代码、测试、生效配置和最新运行证据作为实现权威来源。
- 未明确授权时不得修改生产环境。
- 使用短期分支和 PR。
- 使用仓库已有的验证工作流，修复失败并迭代直至适用的 Gate 通过。

Expected result:
<任务完成时应达到的状态>
```

只需加入新的或任务专用的限制。如果仓库已保存项目状态、架构、Runner 配置、测试命令或历史背景，就不要把它们重新复制到聊天中。

## Level 2 —— 仓库 Ticket 任务

适用于大型、跨会话、高风险、生产、迁移或多设备协作任务。

聊天提示词仍应保持简短：

```text
Repository: Gonglz/<repo>
Task: TICKET_<id>

权威任务规格：
docs/_tmp/TICKET_<id>/PROMPT.md

先阅读 AGENTS.md 和 docs/PROJECT.md。
严格执行 Ticket，以最新实现／运行证据验证事实，而不是仅依赖聊天历史；更新分支和 PR，直到适用的 Gate 通过。
```

详细目标、范围、排除项、安全限制、验收 Gate、生产授权、证据要求和任务收尾说明保留在 Ticket 工作空间，不在聊天中重复。

## 简明原则

```text
Chat = 新增意图
Repository = 当前项目状态
Ticket = 详细任务契约
GitHub Actions / runtime evidence = 执行状态
```

不要在 Chat 和 GitHub 中维持两份同时具有权威效力的任务规格。
