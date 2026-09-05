---
plan: .plan/2026-09-05-add-lua-foundation-directory.md
related_paths:
  - .spec/architecture.md
  - phantom/lua/runtime/.gitkeep
---

# 意图 (Intent)

- 为让条件插件运行的共享基础 Lua 设计并新建目录。
- 使用 `phantom/lua/runtime/`，并同步更新架构规范。

# 约束 (Constraints)

- 本次只创建空目录占位和更新目录职责规范，不编写 Lua 或 Python 代码。
- 条件专属 Lua 模板继续属于对应的版本化条件插件目录。
- 共享基础模块的最终 Lua 文件拆分保持待定。

# 被拒绝的替代方案 (Rejected Alternatives)

- 不采用 `phantom/lua/base/`，因为 `base` 的长期职责较模糊。
- 不采用 `phantom/lua/templates/`，因为容易与条件插件的 `template.lua` 混淆。
- 不选择只创建目录而不更新架构规范。
