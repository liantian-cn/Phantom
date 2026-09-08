---
plan: .plan/2026-09-08-add-player-specialization-cell.md
related_paths:
  - phantom/lua/general/02_player_specialization.lua
  - phantom/lua/addonTemplateName.toc
  - .spec/pixel-protocol.md
  - .prompt/2026-09-08-add-player-specialization-cell.md
---

# 意图 (Intent)

沿用已满意的职业 Cell 结构，新增 index=2、uuid=154ab0be-9c33-4935-8e57-531eb6bde99e 的玩家专精 Cell，说明注释取自 https://warcraft.wiki.gg/wiki/API:GetSpecialization。

# 约束 (Constraints)

x=2、y=1，沿用灰度与黑色兜底；构造后立即刷新，监听登录、进入世界和两个专精事件，PLAYER_SPECIALIZATION_CHANGED 只注册 player。局部缓存新版接口 C_SpecializationInfo.GetSpecialization，保留 local specializationIndex = GetSpecialization() 写法。沿用已有缩放与文件结构，保留返回索引 5。Implement the plan.

# 被拒绝的替代方案 (Rejected Alternatives)

选择新版接口局部缓存，未采用依赖 loadDeprecationFallbacks 的旧全局接口。
