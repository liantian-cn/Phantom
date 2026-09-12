---
plan: .plan/2026-09-12-rotation-toml-docs.md
related_paths:
  - .spec/README.md
  - .spec/architecture.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .spec/configuration.md
  - todo_list.md
---

# 意图 (Intent)
将未来循环配置格式统一改为 TOML，更新 6 份现行文档及完整示例。

# 约束 (Constraints)
保留 schema v1、现有字段和循环语义；历史任务档案保留原文。仅修改文档，隔离已有未提交修改。

# 被拒绝的替代方案 (Rejected Alternatives)
同时规划 YAML 兼容：用户选择统一改为 TOML，不安排 YAML 兼容或迁移。
