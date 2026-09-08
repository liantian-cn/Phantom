---
plan: .plan/2026-09-08-add-player-class-cell.md
related_paths:
  - phantom/lua/general/01_player_class.lua
  - phantom/lua/addonTemplateName.toc
  - .spec/architecture.md
  - .spec/pixel-protocol.md
  - .prompt/2026-09-08-add-player-class-cell.md
---

# 意图 (Intent)

按现有构架逻辑新增玩家职业 Cell：index=1，x=1，y=1，UUID=0536bd34-e377-4274-a7ae-b80455dd359a。classID 为 UnitClass("player") 第三个返回值，RGB 均为 classID/255。用户委托目录命名，采用 general/01_player_class.lua，保存第一行通用字段实现。

# 约束 (Constraints)

“generalcell只是在第一行的cell，还是cell。”index 使用文件头 index: 1。独立 eventFrame 监听 PLAYER_LOGIN、PLAYER_ENTERING_WORLD；构造加入 UIInitFuncs，遵循已有缩放，构造完成立即刷新。无 classID 时显示黑色。整理 UnitClass 技术说明及职业表，补充必要的 .spec。Implement the plan.

# 被拒绝的替代方案 (Rejected Alternatives)

用户否定将 GeneralCell 解释为新类型或共享索引表，明确它只是第一行普通 Cell。
