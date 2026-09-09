---
plan: .plan/2026-09-09-delay-slash-commands.md
related_paths:
  - phantom/lua/runtime/03_rotation_variable.lua
  - phantom/lua/general/05_delaying.lua
  - phantom/lua/addonTemplateName.toc
  - .spec/pixel-protocol.md
  - .prompt/2026-09-09-delay-slash-commands.md
---

# 意图 (Intent)

模仿 Burst 加入 Delay 机制，使用 Delaying() 表示是否正在延迟；新增第五个通用状态格，UUID 为 db99c08a-9f97-4ae8-b076-dd2981bf99cc。以 addonName 小写前两位注册命令，提供 disable、enable、toggle、delay [NN]、burst [NN]。

# 约束 (Constraints)

默认不延迟；DelayRemaining 仅限制下限为 0。delay 默认 0.4 秒，burst 默认 15 秒，NN 不限制正负、位数。合法命令静默；空命令、help、未知命令、无效数字或多余参数输出中文帮助且不改状态。命令词忽略大小写并允许首尾空白。沿用现有 Burst 行为和状态 Cell 刷新机制。

Implement the plan.

# 被拒绝的替代方案 (Rejected Alternatives)

None
