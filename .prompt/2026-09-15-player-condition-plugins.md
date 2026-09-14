# 玩家条件插件

## 插件范围
1. **R1**：我要根据指定的 PhantomProject `0104`、`0107–0115`、`0117–0119`、`0121–0127` Lua 文件制作条件插件，只阅读旧项目 Lua，无需阅读旧项目文档。借鉴其秘密值处理、API 和事件处理；着色与命名遵循 Phantom 项目要求。
2. **R2**：我要将插件放在 `phantom/conditions`，统一使用 `liantian_cn.<snake_case>@dev`。包括职责、战斗、自身目标、移动、载具、近战敌人数、选择施法目标、聊天、组队、饰品就绪、治疗石就绪、治疗药水就绪、施法进度、蓄力状态、施法图标、施法目标、大防御、可驱散减益、技能掌握、天赋掌握、伤害吸收、治疗吸收和指定增益，共 23 个插件。

## 行为与刷新
3. **R3**：我要所有插件添加 `PLAYER_ENTERING_WORLD`，保留旧插件已有轮询及间隔：通常为 2 秒，施法进度为 0.1 秒。所有 OnUpdate 使用独立的 `-random()` 错峰并保留累计余量；移动事件通过 `C_Timer.After(0, function() update() end)` 延至下一帧刷新。
4. **R4**：我的载具条件包含坐骑，聊天条件检测任意键盘输入焦点，队伍条件包含团队。近战条件接收用于判断距离的技能 ID。
5. **R5**：我的饰品条件只接受位置 13 或 14。治疗石和治疗药水分别固定使用物品 ID `224464`、`258138`，沿用旧项目冷却及可用性判断，不额外检查背包数量。
6. **R6**：我要把施法信息拆为三个插件。进度通过 `CreateColorCurve()` 和 `DurationObject:EvaluateElapsedPercent()` 表示施法或通道从黑到白的进度，Python 返回 `0–100 float`，空闲为 `0.0`。蓄力状态返回 bool，蓄力属于通道。施法图标使用 IconTile，返回其 hash 字符串。
7. **R7**：我的施法目标返回 `player`、`party1–party4`、`raid1–raid40`；完整保留旧项目成功、停止、失败及每 2 秒清理行为，包括长施法可能提前清空、秘密目标暂时保留旧值的行为。

## 光环、技能与吸收
8. **R8**：我的大防御和指定 buff 条件参考 `phantom/lua/examples/04_player_buff.lua`，使用 AuraContainer、AddAuraSlot 和白色覆盖贴图；至少一个匹配光环存在时显示白色，否则显示黑色。指定 buff 接收一组 buff ID。
9. **R9**：我的可驱散减益条件使用相同的光环显示方式，同时要求玩家可驱散和类型匹配。`dispel_types` 必填，支持 `Magic`、`Poison`、`Disease`、`Curse`、`Stealth`、`Special`、`Enrage` 的布尔映射；遗漏项为 false，允许空表和全 false，表示不匹配任何减益。
10. **R10**：我要将英雄天赋条件改成技能掌握、天赋掌握两个行为完全相同的插件。两者接收非空技能 ID 列表，任意 ID 满足 `IsSpellKnown(spellID) or IsSpellInSpellBook(spellID)` 就返回 true、显示白色。
11. **R11**：我的伤害吸收、治疗吸收条件均接收非负整数阈值 N，允许 0；使用白色 StatusBar，最小值 N、最大值 N+1。吸收量不超过 N 时为黑色，超过 N 时为白色，Python 返回 bool。

## 接口与返回值
12. **R12**：我要参数统一使用 snake_case：`spell_id`、`slot_id`、`spell_ids`、`buff_ids`、`dispel_types`、`threshold`。ID 为正整数，ID 列表非空，饰品位置只接受 13/14，阈值拒绝负数、小数和布尔值。
13. **R13**：我的职责返回 `TANK/HEALER/DAMAGER/NONE`；未知施法目标和空图标返回空字符串。解码失败时，职责返回 `NONE`，布尔返回 `False`，计数与进度返回零，目标与图标返回空字符串。除职责、近战数量、施法进度、图标和目标外，其余插件均返回 bool。

## 实施
14. **R14**：我要实施已确认的计划。
