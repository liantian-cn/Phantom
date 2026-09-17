# 辅助战斗条件候选插件清单

## 范围与使用方式

- 来源：只读参考 `C:\Users\liantian\.local\share\opencode\repos\github.com\liantian-cn\WowAssistedCombatReveal@main\ConditionTypeMap.csv`。
- 收录 Type 0–69 共 70 条，包括 `Active=N`；仅排除 Type 70 `ASSISTED_COMBAT_RULE_TYPE_AUTOMATION_ONLY`。下表完整枚举、Active 和条件简介沿用 CSV；Active 不表示 Phantom 实现状态。
- 按候选插件合并同类上下限、存在／缺失条件；每条 Type 仅归属一节。候选名采用 `snake_case@dev`，不代表实现授权，各节实现说明留待补充。
- 同名或相关现有插件仅作关联，不标记完成，也不承诺覆盖对应官方条件；枚举名为主要依据，CSV 描述差异单独注明。
- 保留 CSV 的比较含义：距离及普通目标计数的 GREATER 为严格大于，其他条目按各自简介，不统一改成大于等于。
- 资源按类别独立命名。相关现有 `player_primary_power@dev` 仅返回当前主要资源，不等同于各类指定资源插件。

## 1. `player_has_spell@dev`

简介：玩家是否已学习指定技能。

关联：同名现有插件仅检查技能已知／玩家法术书，不解析天赋树。枚举为 SPELL_LEARNED，CSV 则描述为“点出天赋”，两者差异保留待确认。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 0 | ASSISTED_COMBAT_RULE_TYPE_SPELL_LEARNED | Y | 若已点出天赋 {spell} |

### 实现说明


## 2. `spell_cooldown@dev`

简介：技能冷却状态及剩余冷却时间。

关联：同名现有插件返回剩余秒数；CSV 剩余冷却阈值为毫秒，不能直接视为相同契约。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 1 | ASSISTED_COMBAT_RULE_TYPE_SPELL_ON_COOLDOWN | Y | 若技能 {arg1} 正在冷却 |
| 2 | ASSISTED_COMBAT_RULE_TYPE_SPELL_OFF_COOLDOWN | Y | 若技能 {spell} 不在冷却中 |
| 65 | ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_REMAINING_GREATER | Y | 若技能 {arg1} 的剩余冷却大于等于 {arg2} 毫秒 |
| 66 | ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_REMAINING_LESS | Y | 若技能 {arg1} 的剩余冷却小于等于 {arg2} 毫秒 |

### 实现说明


## 3. `target_distance@dev`

简介：玩家与目标的距离。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 3 | ASSISTED_COMBAT_RULE_TYPE_TARGET_DISTANCE_LESS | Y | 若目标距离小于等于 {arg1} 码 |
| 4 | ASSISTED_COMBAT_RULE_TYPE_TARGET_DISTANCE_GREATER | Y | 若目标距离大于 {arg1} 码 |

### 实现说明


## 4. `target_is_hostile@dev`

简介：目标是否为敌对单位。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 5 | ASSISTED_COMBAT_RULE_TYPE_HOSTILE_TARGET | Y | 若目标是敌对单位 |

### 实现说明


## 5. `target_is_friendly@dev`

简介：目标是否为友方单位。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 6 | ASSISTED_COMBAT_RULE_TYPE_FRIENDLY_TARGET | N | 若目标是友方单位 |

### 实现说明


## 6. `target_health_pct@dev`

简介：目标生命值百分比。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 7 | ASSISTED_COMBAT_RULE_TYPE_HEALTH_PCT_GREATER | N | 若目标生命值大于等于 {arg1}% |
| 8 | ASSISTED_COMBAT_RULE_TYPE_HEALTH_PCT_LESS | Y | 若目标生命值小于等于 {arg1}% |

### 实现说明


## 7. `player_has_aura@dev`

简介：玩家指定增益／减益的存在与缺失。

关联：现有 `player_has_buff@dev` 仅检查 HELPFUL 增益，不等于通用 aura 条件。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 9 | ASSISTED_COMBAT_RULE_TYPE_AURA_ON_PLAYER | Y | 若玩家拥有增益/减益 {arg1} |
| 16 | ASSISTED_COMBAT_RULE_TYPE_AURA_MISSING_PLAYER | Y | 若玩家没有增益/减益 {arg1} |

### 实现说明


## 8. `target_has_aura@dev`

简介：目标指定增益／减益的存在与缺失。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 10 | ASSISTED_COMBAT_RULE_TYPE_AURA_ON_TARGET | Y | 若目标拥有增益/减益 {arg1} |
| 15 | ASSISTED_COMBAT_RULE_TYPE_AURA_MISSING_TARGET | Y | 若目标没有增益/减益 {arg1} |

### 实现说明


## 9. `target_nearby_units_count@dev`

简介：目标周围指定距离内的目标数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 11 | ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_TARGET_GREATER | Y | 若目标周围 {arg2} 码内的目标数量大于 {arg1} 个 |
| 49 | ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_TARGET_LESS | Y | 若目标周围 {arg2} 码内的目标数量小于等于 {arg1} 个 |

### 实现说明


## 10. `player_nearby_units_count@dev`

简介：玩家周围指定距离内的目标数量。

关联：现有 `player_melee_enemies_count@dev` 按指定技能范围统计可攻击姓名板单位，仅为相关插件。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 12 | ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_PLAYER_GREATER | Y | 若玩家周围 {arg2} 码内的目标数量大于 {arg1} 个 |
| 50 | ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_PLAYER_LESS | Y | 若玩家周围 {arg2} 码内的目标数量小于等于 {arg1} 个 |

### 实现说明


## 11. `player_nearby_aura_units_count@dev`

简介：玩家周围指定距离内带有指定增益／减益的目标数量。

备注：Type 13 的 CSV 描述包含参数，但 Value1、Value2、Value3 全为 UNUSED，此差异留待补充。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 13 | ASSISTED_COMBAT_RULE_TYPE_AURA_COUNT_NEAR_PLAYER_GREATER | N | 若玩家周围 {arg2} 码内带有增益/减益 {arg3} 的目标数量大于等于 {arg1} 个 |
| 51 | ASSISTED_COMBAT_RULE_TYPE_AURA_COUNT_NEAR_PLAYER_LESS | Y | 若玩家周围 {arg2} 码内带有增益/减益 {arg3} 的目标数量小于等于 {arg1} 个 |

### 实现说明


## 12. `spell_afford_cost@dev`

简介：玩家资源是否足够支付技能消耗。

关联：现有 `spell_usable@dev` 不等于资源足够，也不等于成功施放。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 14 | ASSISTED_COMBAT_RULE_TYPE_AFFORD_COST | Y | 若玩家有足够资源施放技能 {spell} |

### 实现说明


## 13. `player_aura_duration@dev`

简介：玩家指定增益／减益的剩余时间。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 17 | ASSISTED_COMBAT_RULE_TYPE_AURA_DURATION_PLAYER | Y | 若玩家身上的增益/减益 {arg1} 剩余时间小于等于 {arg2} 毫秒 |

### 实现说明


## 14. `target_aura_duration@dev`

简介：目标指定增益／减益的剩余时间。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 18 | ASSISTED_COMBAT_RULE_TYPE_AURA_DURATION_TARGET | Y | 若目标身上的增益/减益 {arg1} 剩余时间小于等于 {arg2} 毫秒 |

### 实现说明


## 15. `player_mana@dev`

简介：玩家法力数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 19 | ASSISTED_COMBAT_RULE_TYPE_MANA_GREATER | N | 若玩家法力大于等于 {arg1} |
| 20 | ASSISTED_COMBAT_RULE_TYPE_MANA_LESS | Y | 若玩家法力小于等于 {arg1} |

### 实现说明


## 16. `player_rage@dev`

简介：玩家怒气数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 21 | ASSISTED_COMBAT_RULE_TYPE_RAGE_GREATER | Y | 若玩家怒气大于等于 {arg1} |
| 22 | ASSISTED_COMBAT_RULE_TYPE_RAGE_LESS | N | 若玩家怒气小于等于 {arg1} |

### 实现说明


## 17. `player_focus@dev`

简介：玩家集中值数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 23 | ASSISTED_COMBAT_RULE_TYPE_FOCUS_GREATER | Y | 若玩家集中值大于等于 {arg1} |
| 24 | ASSISTED_COMBAT_RULE_TYPE_FOCUS_LESS | N | 若玩家集中值小于等于 {arg1} |

### 实现说明


## 18. `player_energy@dev`

简介：玩家能量数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 25 | ASSISTED_COMBAT_RULE_TYPE_ENERGY_GREATER | Y | 若玩家能量大于等于 {arg1} |
| 26 | ASSISTED_COMBAT_RULE_TYPE_ENERGY_LESS | N | 若玩家能量小于等于 {arg1} |

### 实现说明


## 19. `player_combo_points@dev`

简介：玩家连击点数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 27 | ASSISTED_COMBAT_RULE_TYPE_COMBO_POINTS_GREATER | Y | 若玩家连击点大于等于 {arg1} |
| 28 | ASSISTED_COMBAT_RULE_TYPE_COMBO_POINTS_LESS | Y | 若玩家连击点小于等于 {arg1} |

### 实现说明


## 20. `spec_dk_rune@dev`

简介：死亡骑士玩家符文数量。

关联：已有同名符文插件，仅记录关联，覆盖情况待确认。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 29 | ASSISTED_COMBAT_RULE_TYPE_RUNES_GREATER | Y | 若玩家符文大于等于 {arg1} |
| 30 | ASSISTED_COMBAT_RULE_TYPE_RUNES_LESS | N | 若玩家符文小于等于 {arg1} |

### 实现说明


## 21. `player_runic_power@dev`

简介：玩家符文能量数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 31 | ASSISTED_COMBAT_RULE_TYPE_RUNIC_POWER_GREATER | Y | 若玩家符文能量大于等于 {arg1} |
| 32 | ASSISTED_COMBAT_RULE_TYPE_RUNIC_POWER_LESS | Y | 若玩家符文能量小于等于 {arg1} |

### 实现说明


## 22. `player_soul_shards@dev`

简介：玩家灵魂碎片数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 33 | ASSISTED_COMBAT_RULE_TYPE_SOUL_SHARDS_GREATER | Y | 若玩家灵魂碎片大于等于 {arg1} |
| 34 | ASSISTED_COMBAT_RULE_TYPE_SOUL_SHARDS_LESS | Y | 若玩家灵魂碎片小于等于 {arg1} |

### 实现说明


## 23. `player_lunar_power@dev`

简介：玩家星界能量数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 35 | ASSISTED_COMBAT_RULE_TYPE_LUNAR_POWER_GREATER | Y | 若玩家星界能量大于等于 {arg1} |
| 36 | ASSISTED_COMBAT_RULE_TYPE_LUNAR_POWER_LESS | N | 若玩家星界能量小于等于 {arg1} |

### 实现说明


## 24. `player_holy_power@dev`

简介：玩家神圣能量数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 37 | ASSISTED_COMBAT_RULE_TYPE_HOLY_POWER_GREATER | Y | 若玩家神圣能量大于等于 {arg1} |
| 38 | ASSISTED_COMBAT_RULE_TYPE_HOLY_POWER_LESS | Y | 若玩家神圣能量小于等于 {arg1} |

### 实现说明


## 25. `player_maelstrom@dev`

简介：玩家漩涡值数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 39 | ASSISTED_COMBAT_RULE_TYPE_MAELSTROM_GREATER | N | 若玩家漩涡值大于等于 {arg1} |
| 40 | ASSISTED_COMBAT_RULE_TYPE_MAELSTROM_LESS | N | 若玩家漩涡值小于等于 {arg1} |

### 实现说明


## 26. `player_chi@dev`

简介：玩家真气数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 41 | ASSISTED_COMBAT_RULE_TYPE_CHI_GREATER | N | 若玩家真气大于等于 {arg1} |
| 42 | ASSISTED_COMBAT_RULE_TYPE_CHI_LESS | Y | 若玩家真气小于等于 {arg1} |

### 实现说明


## 27. `player_insanity@dev`

简介：玩家狂乱值数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 43 | ASSISTED_COMBAT_RULE_TYPE_INSANITY_GREATER | Y | 若玩家狂乱值大于等于 {arg1} |
| 44 | ASSISTED_COMBAT_RULE_TYPE_INSANITY_LESS | N | 若玩家狂乱值小于等于 {arg1} |

### 实现说明


## 28. `player_essence@dev`

简介：玩家精华数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 45 | ASSISTED_COMBAT_RULE_TYPE_ESSENCE_GREATER | Y | 若玩家精华大于等于 {arg1} |
| 46 | ASSISTED_COMBAT_RULE_TYPE_ESSENCE_LESS | N | 若玩家精华小于等于 {arg1} |

### 实现说明


## 29. `player_arcane_charges@dev`

简介：玩家奥术充能数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 47 | ASSISTED_COMBAT_RULE_TYPE_ARCANE_CHARGES_GREATER | Y | 若玩家奥术充能大于等于 {arg1} |
| 48 | ASSISTED_COMBAT_RULE_TYPE_ARCANE_CHARGES_LESS | Y | 若玩家奥术充能小于等于 {arg1} |

### 实现说明


## 30. `target_aura_stacks@dev`

简介：目标指定增益／减益的层数。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 52 | ASSISTED_COMBAT_RULE_TYPE_TARGET_AURA_APPLICATION_GREATER | Y | 若目标身上增益/减益 {arg1} 的层数大于等于 {arg2} |
| 53 | ASSISTED_COMBAT_RULE_TYPE_TARGET_AURA_APPLICATION_LESS | Y | 若目标身上增益/减益 {arg1} 的层数小于等于 {arg2} |

### 实现说明


## 31. `player_aura_stacks@dev`

简介：玩家指定增益／减益的层数。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 54 | ASSISTED_COMBAT_RULE_TYPE_PLAYER_AURA_APPLICATION_GREATER | Y | 若玩家身上增益/减益 {arg1} 的层数大于等于 {arg2} |
| 55 | ASSISTED_COMBAT_RULE_TYPE_PLAYER_AURA_APPLICATION_LESS | Y | 若玩家身上增益/减益 {arg1} 的层数小于等于 {arg2} |

### 实现说明


## 32. `spell_in_range@dev`

简介：技能是否在射程内。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 56 | ASSISTED_COMBAT_RULE_TYPE_SPELL_IN_RANGE | Y | 若技能 {spell} 在射程内 |

### 实现说明


## 33. `player_has_pet@dev`

简介：玩家宠物的存在与缺失。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 57 | ASSISTED_COMBAT_RULE_TYPE_HAS_PET | Y | 若玩家有宠物 |
| 58 | ASSISTED_COMBAT_RULE_TYPE_HAS_NO_PET | Y | 若玩家没有宠物 |

### 实现说明


## 34. `player_fury@dev`

简介：玩家恶魔之怒数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 59 | ASSISTED_COMBAT_RULE_TYPE_FURY_GREATER | N | 若玩家恶魔之怒大于等于 {arg1} |
| 60 | ASSISTED_COMBAT_RULE_TYPE_FURY_LESS | N | 若玩家恶魔之怒小于等于 {arg1} |

### 实现说明


## 35. `player_pain@dev`

简介：玩家苦痛值数量。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 61 | ASSISTED_COMBAT_RULE_TYPE_PAIN_GREATER | N | 若玩家苦痛值大于等于 {arg1} |
| 62 | ASSISTED_COMBAT_RULE_TYPE_PAIN_LESS | N | 若玩家苦痛值小于等于 {arg1} |

### 实现说明


## 36. `spell_charges@dev`

简介：技能充能层数。

关联：已有同名充能插件，仅记录关联，覆盖情况待确认。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 63 | ASSISTED_COMBAT_RULE_TYPE_SPELL_CHARGES_GREATER | Y | 若技能 {spell} 的充能层数大于等于 {arg1} |
| 64 | ASSISTED_COMBAT_RULE_TYPE_SPELL_CHARGES_LESS | N | 若技能 {spell} 的充能层数小于等于 {arg1} |

### 实现说明


## 37. `spell_can_cast@dev`

简介：技能可成功施放条件的候选分类。

备注：按 COOLDOWN_ALLOW_CASTING_SUCCESS 字面暂命名，具体语义待补充。相关现有 `spell_usable@dev` 不保证成功施放或资源足够。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 67 | ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_ALLOW_CASTING_SUCCESS | Y | 若技能 {spell} 可以成功施放 |

### 实现说明


## 38. `player_health_pct@dev`

简介：玩家生命值百分比。

关联：同名现有插件返回预测生命百分比，与 CSV 生命值百分比不能直接视为相同语义。

| Type | 完整官方枚举 | Active | CSV 条件简介 |
| --- | --- | --- | --- |
| 68 | ASSISTED_COMBAT_RULE_TYPE_PLAYER_HEALTH_PCT_GREATER | Y | 若玩家生命值大于等于 {arg1}% |
| 69 | ASSISTED_COMBAT_RULE_TYPE_PLAYER_HEALTH_PCT_LESS | Y | 若玩家生命值小于等于 {arg1}% |

### 实现说明
