---
plan: .plan/2026-09-05-project-initialization.md
related_paths:
  - AGENTS.md
  - .context/README.md
  - .context/wow-12.1-changes.md
  - .context/secret-values.md
  - .context/aura.md
  - .context/rendering.md
  - .context/events-performance.md
  - .context/security-api.md
  - .spec/README.md
  - .spec/project-overview.md
  - .spec/architecture.md
  - .spec/pixel-protocol.md
  - .spec/plugin-system.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/testing.md
---

## 意图 (Intent)

- 先冻结 Phantom 的架构、协议与 Agent 阅读路径，再开始代码工程。
- `.context` 精编为面向 Phantom 的英文 WoW 12.1 知识；`.spec` 与 `AGENTS.md` 使用中文。
- 初始化四个外部源码目录，供未来只读参考。

## 约束 (Constraints)

- 只在 `develop` 分支工作；本次不创建业务代码或目录骨架，不改根 `README.md`。
- 一份 YAML 对应一份 rotation；条件以唯一 `title` 引用，表达式使用白名单 AST；宏使用安全按钮和运行期覆盖绑定。
- Cell、Status Bar、Icon 只读取可信中间区域；Status Bar 返回中间两行纯白像素的 `0–100` 占比。
- 所有手写 Python 文件强制 Type Hint；业务注释使用中文，代码标识符使用英文。
- 外部源码不进入 Phantom 提交，后续未经明确要求不得写入或更新。

## 被拒绝的替代方案 (Rejected Alternatives)

- 不翻译 `.context`，避免微小技术翻译错误累积。
- 不改根 `README.md`，它保留给未来用户文档；不以旧 Terminal 作为新 UI 设计参考。
- schema v1 不按天赋选择 rotation；不使用稳定英文条件键或数字 `id`，直接以唯一标题引用。
- 不使用 `eval`；不创建持久 WoW 宏槽位或保存键位；覆盖绑定不检查也不提示。
