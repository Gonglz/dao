# DAO — Shared Engineering Conventions

**Language:** English | [简体中文](README.zh-CN.md)

DAO is the shared engineering control plane for repository conventions and agent development workflows across Gonglz projects. The repository is named `dao`; its default branch is still `main`.

## Documentation

| English (authoritative) | 简体中文 (translation) | Purpose |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | [AGENTS.zh-CN.md](AGENTS.zh-CN.md) | Agent instructions and safety boundaries |
| [docs/PROJECT.md](docs/PROJECT.md) | [docs/PROJECT.zh-CN.md](docs/PROJECT.zh-CN.md) | Shared GitHub/runner/evidence workflow |
| [templates/CHAT_TASK_PROMPT.md](templates/CHAT_TASK_PROMPT.md) | [templates/CHAT_TASK_PROMPT.zh-CN.md](templates/CHAT_TASK_PROMPT.zh-CN.md) | Lightweight task prompt template |
| [templates/STAKEHOLDER_STATUS_BRIEF.md](templates/STAKEHOLDER_STATUS_BRIEF.md) | [templates/STAKEHOLDER_STATUS_BRIEF.zh-CN.md](templates/STAKEHOLDER_STATUS_BRIEF.zh-CN.md) | Optional plain-language project/status reporting prompt |

## Authority and translations

The English versions are the sole normative engineering documents. Chinese versions are maintained translations for readers, not separate specifications. The documentation sync check detects changes to an English source that have not yet been reflected in the corresponding Chinese translation. It does **not** certify the translation's semantic accuracy.

Project-specific architecture, contracts, code, tests, deployment paths, and production permissions remain owned by each project repository. DAO supplies only shared conventions; a successful CI run does not authorize deployment.
