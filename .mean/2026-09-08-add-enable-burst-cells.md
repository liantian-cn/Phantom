---
plan: .plan/2026-09-08-add-enable-burst-cells.md
related_paths:
  - phantom/lua/general/03_enable.lua
  - phantom/lua/general/04_in_burst.lua
  - phantom/lua/addonTemplateName.toc
  - .spec/pixel-protocol.md
  - .prompt/2026-09-08-add-enable-burst-cells.md
---

# 意图 (Intent)

第三个通用 Cell 反映 addonTable.ENABLE，第四个调用 addonTable.InBurst() 反映爆发状态；true 白色、false 黑色。UUID 分别为 c845da87-d22c-462b-9696-0678101df51b 和 0db46515-244d-4755-9a77-65b3581d85ef。

# 约束 (Constraints)

分别位于 (3,1)、(4,1)，沿用普通 Cell、UIInitFuncs 和已有缩放。两个独立 OnUpdate 各自使用 fastTimeElapsed = -random()，累加 elapsed，严格 > 0.1 时减去 0.1 并刷新一次。等待错峰首次刷新，构造后保持黑色。ENABLE 不控制爆发 Cell 输出。Implement the plan.

# 被拒绝的替代方案 (Rejected Alternatives)

用户选择等待错峰首次刷新，未采用构造后立即刷新；选择爆发状态黑白，未采用剩余秒数灰度。
