---
plan: .plan/2026-09-09-textual-tui-docs.md
related_paths:
  - .spec/project-overview.md
  - .spec/architecture.md
  - .prompt/2026-09-09-textual-tui-docs.md
---

## 意图 (Intent)

后续不再使用 PySide6，项目 UI 改为 Textual TUI。本次修改项目文档，确定技术选型并补充消息、响应式状态与后台任务的能力说明。

## 约束 (Constraints)

保留 rotation 表格与首列复选框、同职业同专精互斥选择及不同职业或专精可共存的规则；保留不以旧项目 Terminal 为视觉或交互参考的规定。页面、具体通信及调度设计继续待定。本次不添加依赖或 UI 实现，不变更公共 API、配置格式或源码目录。在 develop 将两份规范和三份归档作为一次原子本地提交，不推送，不包含已有无关修改。

Implement the plan.

## 被拒绝的替代方案 (Rejected Alternatives)

不再使用 PySide6。
