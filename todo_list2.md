

WowAssistedCombatReveal条件迁移计划

WowAssistedCombatReveal 

## 任务工作

1. 新字段定义
现有的插件如果满足官方一件辅助的条件字符"ASSISTED_COMBAT_RULE_*"
则在插件的toml配置文件中增加一个字段，用于指定该条件的类型。这个字段是list类型。
这是为便于后续搜索。

2. 添加、维护大量插件

按下述内容，添加维护插件。


### 1. 玩家是否已学习指定技能/天覅

关联：
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_LEARNED

目前，有2个相关插件满足这个要求
phantom\conditions\player_has_spell@dev
phantom\conditions\player_has_talent@dev

但目前看起来，这2个插件的命名不合适，应该改成spell_known 和 talent_known。
使用known不适用learned是因为，C_SpellBook.IsSpellKnown 方法的名字。

这俩插件看似完全一样，是因为游戏内，天赋=被动技能。




### 2. 技能冷却状态及剩余冷却时间

关联：
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_ON_COOLDOWN
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_OFF_COOLDOWN
 - ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_REMAINING_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_REMAINING_LESS


目前，有1个相关插件满足这个要求
- `spell_cooldown@dev`

虽然返回值是秒，只要通过表达式则完全可用。


### 3. 玩家与目标的距离

关联：
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_DISTANCE_LESS
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_DISTANCE_GREATER

需制作插件 `target_in_range`和`focus_in_range`

描述：目标/焦点在距离范围内

说明，实际上目前完全无法实现距离判断，只能判断某个技能是否在施法范围。

参考实现方法：
    local IsSpellInRange        = C_Spell.IsSpellInRange
    local isInRange = IsSpellInRange(spellID, UNIT_TOKEN)
    if isInRange == nil then
        cell:clearCell()
        return
    end
    cell:setCellBoolean(isInRange)
入参：
    - spellID：技能ID
补充：
    先要判断目标/焦点是否存在。兜底为否
参考来源：
    @PhantomProject/src/0206_target_in_ranged.lua
    @PhantomProject/src/0306_focus_in_ranged.lua
    @PhantomProject/src/0301_focus_is_exists.lua
    @PhantomProject/src/0201_target_is_exists.lua

### 4. 目标/焦点是否为敌对单位

关联：
 - ASSISTED_COMBAT_RULE_TYPE_HOSTILE_TARGET

需要制作插件 `target_is_enemy`和`focus_is_enemy`

使用enemy而不是hostile，是因为，游戏内接口是 UnitIsEnemy

入参：无
返回值：布尔值
补充：
    先要判断目标/焦点是否存在。兜底为否
参考
    @PhantomProject/src/0204_target_is_enemy.lua
    @PhantomProject/src/0304_focus_is_enemy.lua



### 5. 目标/焦点是否可辅助

关联：
 - ASSISTED_COMBAT_RULE_TYPE_FRIENDLY_TARGET

需要制作插件 `target_can_assist`和`focus_can_assist`

和`*_is_enemy` 相似，区别是API，使用UnitCanAssist("player",unitToken)


### 6. 目标/焦点生命百分比

关联：
 - ASSISTED_COMBAT_RULE_TYPE_HEALTH_PCT_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_HEALTH_PCT_LESS

需要制作插件 `target_health_pct`和`focus_health_pct`

参考 `player_health_pct`
补充：
    先要判断目标/焦点是否存在。兜底为0


### 7. 玩家指定增益的存在

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_ON_PLAYER
 - ASSISTED_COMBAT_RULE_TYPE_AURA_MISSING_PLAYER

 `player_has_buff` 已经实现

注意：玩家只能过滤buff，具体见Aura的Spellid过滤限制。

### 8. 可辅助目标/焦点指定增益的存在

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_ON_TARGET
 - ASSISTED_COMBAT_RULE_TYPE_AURA_MISSING_TARGET

需要开发插件 `target_has_buff`和`focus_has_buff`

注意：只有可辅助的目标/焦点能过滤buff，具体见Aura的Spellid过滤限制。


### 9. 可辅助目标/焦点指定减益的存在

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_ON_TARGET
 - ASSISTED_COMBAT_RULE_TYPE_AURA_MISSING_TARGET

需要开发插件 `target_has_debuff`和`focus_has_debuff`

注意：只有可敌对的目标/焦点能过滤debuff，具体见Aura的Spellid过滤限制。

### 10. 目标周围指定距离内的目标数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_TARGET_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_TARGET_LESS

目前靠lua无法实现...

### 11. 玩家周围指定距离内的目标数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_PLAYER_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_COUNT_NEAR_PLAYER_LESS

可通过姓名版实现，需要更新插件: `player_melee_enemies_count`

入参：
    - spellid: 一个技能的ID，用于判断玩家是否在施法范围。
    - combatOnly：是否统计在战斗中的单位。** 新增参数**
返回值：目标数量
代码示例

    ```
    local function GetEnemyCountBySpell(spellID, combatOnly)
        local count = 0

        if not C_Spell.DoesSpellExist(spellID) then
            return 0
        end

        for i = 1, 40 do
            local unit = "nameplate" .. i

            if UnitExists(unit)
                and UnitCanAttack("player", unit)
                and not UnitIsDeadOrGhost(unit)
                and (not combatOnly or UnitAffectingCombat(unit))
            then
                if C_Spell.IsSpellInRange(spellID, unit) == true then
                    count = count + 1
                end
            end
        end

        return count
    end
    ```


### 12. 玩家周围指定距离内带有指定增益／减益的目标数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_COUNT_NEAR_PLAYER_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_AURA_COUNT_NEAR_PLAYER_LESS

需要开发插件： `player_range_aura_units_count`

入参：
    - spellID：检测距离的技能ID
    - auraID：增益/减益ID
    - combatOnly：是否统计在战斗中的单位。



代码经验：要判断这个spellID是否是秘密值，然后在初始化阶段就报错。

local function IsAuraSpellNonSecret(spellID)
    return C_Secrets.GetSpellAuraSecrecy(spellID)
        == Enum.SecrecyLevel.NeverSecret
end

demo代码块

-- spellID    : 用于检测距离的技能 ID
-- auraID     : 要检测的 Buff / Debuff ID
-- combatOnly : true = 只统计战斗中的单位
--
-- 返回：
--   count             成功时为敌人数量
--   nil, "AURA_SECRET" 当前 auraID 属于秘密 Aura，无法安全计数

local function CountEnemiesWithAura(spellID, auraID, combatOnly)
    -- 先判断该 Aura 当前是否允许读取。
    -- GetUnitAuraBySpellID 要求传入可访问的 Aura SpellID。
    if C_Secrets.ShouldSpellAuraBeSecret(auraID) then
        return nil, "AURA_SECRET"
    end

    local count = 0

    for i = 1, 40 do
        local unit = "nameplate" .. i

        if UnitExists(unit)
            and UnitCanAttack("player", unit)
            and not UnitIsDeadOrGhost(unit)
            and (not combatOnly or UnitAffectingCombat(unit))
        then
            -- 距离检测：
            -- true  = 在该技能射程内
            -- false = 超出射程
            -- nil   = 该技能无法对这个单位进行射程判断
            local inRange = C_Spell.IsSpellInRange(spellID, unit)

            if inRange ~= nil
                and not issecretvalue(inRange)
                and inRange == true
            then
                local aura =
                    C_UnitAuras.GetUnitAuraBySpellID(unit, auraID)

                -- aura ~= nil 即表示该单位存在这个 Aura。
                -- aura table 本身在这里已经通过
                -- ShouldSpellAuraBeSecret() 做过前置判断。
                if aura ~= nil then
                    count = count + 1
                end
            end
        end
    end

    return count
end


-- 示例
local count, err = CountEnemiesWithAura(
    133,      -- spellID：火球术，用它判断射程
    123456,   -- auraID：要检测的 Buff / Debuff
    true      -- 只统计战斗中的敌人
)

if count then
    print("范围内带指定 Aura 的敌人数量:", count)
elseif err == "AURA_SECRET" then
    print("该 Aura 当前是秘密值，无法计数")
end



### 13. 玩家资源是否足够支付技能消耗

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AFFORD_COST

已有插件：phantom\conditions\spell_usable@dev

因为不可能返回值是true，true，所以spell_usable可以完全替代。





### 14. 玩家指定增益的剩余时间。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_DURATION_PLAYER

需要新开发插件 `aura_player_buff_duration`

这是一个valuebar的插件，返回玩家身上的增益的剩余时间。

入参：
    - auraIDs：list，增益ID，可以多个ID，只显示一个AuraSlot，以应对同名增益，不同天赋不同id的情况。
    - duration：持续时间
返回值
    - 剩余时间：精度0.25秒。持续时间等于valuebar的宽度，因为每个宽度单位是4像素，所以每个像素表示0.25秒。

如何实现valuebar参考 phantom\conditions\spell_charges@dev\template.lua
如何定位特定auraID，参考 phantom\conditions\player_has_buff@dev
如何在AddAuraSlot中绘制bar，参考@PhantomProject /src/0007_aura_slot_container.lua的DurationBar

注意，实际上valuebar只是定位，我们通过AuraContainer的StatusBar方法，绘制了一个新bar在valuebar的位置。


### 15. 目标指定减益的剩余时间

关联：
 - ASSISTED_COMBAT_RULE_TYPE_AURA_DURATION_TARGET

 需要开发插件 `aura_target_debuff_duration`

 参考上面的`aura_player_buff_duration`


## 资源

资源分为两类，一是主要资源，二是次要资源。
主要资源是秘密值，必须转化为亮度，然后乘最大值获得。
次要资源可以直接读取。



| 资源                                    | 12.1 插件读取状态           | 分类/备注                                |
| --------------------------------------- | --------------------------- | ---------------------------------------- |
| **法力 Mana**                           | 🔒 **可成为 Secret Value**   | Primary Resource                         |
| **怒气 Rage**                           | 🔒 **可成为 Secret Value**   | Primary Resource                         |
| **集中值 Focus**                        | 🔒 **可成为 Secret Value**   | Primary Resource                         |
| **能量 Energy**                         | 🔒 **可成为 Secret Value**   | Primary Resource；盗贼/猫德/武僧等       |
| **符文能量 Runic Power**                | 🔒 **可成为 Secret Value**   | DK Primary Resource                      |
| **星界能量 Astral/Lunar Power**         | 🔒 **可成为 Secret Value**   | 未列入 secondary 豁免名单                |
| **漩涡值 Maelstrom**                    | 🔒 **可成为 Secret Value**   | 未列入 UnitPower secondary 豁免名单      |
| **狂乱 Insanity**                       | 🔒 **可成为 Secret Value**   | 暗牧主要战斗资源                         |
| **恶魔之怒 Fury**                       | 🔒 **可成为 Secret Value**   | DH 等主要资源                            |
| **痛苦值 Pain**                         | 🔒 **可成为 Secret Value**   | 主要资源                                 |
| **连击点 Combo Points**                 | ✅ **Non-secret**            | 暴雪明确豁免                             |
| **符文 Runes**                          | ✅ **Non-secret**            | 注意：**符文 ≠ 符文能量**                |
| **灵魂碎片 Soul Shards**                | ✅ **Non-secret**            | 暴雪明确豁免                             |
| **神圣能量 Holy Power**                 | ✅ **Non-secret**            | 暴雪明确豁免                             |
| **真气 Chi**                            | ✅ **Non-secret**            | 暴雪明确豁免                             |
| **奥术充能 Arcane Charges**             | ✅ **Non-secret**            | 暴雪明确豁免                             |
| **精华 Essence**                        | ✅ **Non-secret**            | 唤魔师，暴雪明确豁免                     |
| **醉拳 Stagger**                        | ✅ **玩家自身为 Non-secret** | `UnitStagger()` 后来也被解除 Secret 限制 |
| **最大资源值 `UnitPowerMax("player")`** | ✅ **通常不是 Secret**       | 暴雪后来特意放开了玩家自己的最大资源值   |



### 16. 玩家法力值 

关联：
 - ASSISTED_COMBAT_RULE_TYPE_MANA_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_MANA_LESS

需要新建插件 `spec_power_mana`

法力值在多数职业，都是秘密值，而且目前版本的法力值，都是在固定天赋和职业下的固定值。

- 入参：
    - maxValue：最大法力值

- 参考 phantom\conditions\player_primary_power@dev 使用曲线构造亮度值。
- 不使用 UnitPowerType(UNIT_TOKEN) 而是固定的 Enum.PowerType.Mana。
- python端把亮度 * maxValue，得到法力值。

### 17. 玩家怒气值

关联：
 - ASSISTED_COMBAT_RULE_TYPE_RAGE_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_RAGE_LESS

需要新建插件 `spec_power_rage`

- 入参：
    - maxValue：最大怒气值

-  Enum.PowerType.Rage。
怒气也是主要能量，参考法力值，大概率是秘密值，使用曲线构造亮度，然后计算。


### 18. 玩家集中值

关联：
 - ASSISTED_COMBAT_RULE_TYPE_FOCUS_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_FOCUS_LESS

需要新建插件 `spec_power_focus`

- 入参：
    - maxValue：最大集中值

-  Enum.PowerType.Focus。
集中值也是主要能量，参考法力值，大概率是秘密值，使用曲线构造亮度，然后计算。

### 19. 玩家能量值

关联：
 - ASSISTED_COMBAT_RULE_TYPE_ENERGY_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_ENERGY_LESS

需要新建插件 `spec_power_energy`

- 入参：
    - maxValue：最大能量值

-  Enum.PowerType.Energy。
能量也是主要能量，参考法力值，大概率是秘密值，使用曲线构造亮度，然后计算。

### 20. 玩家连击点值

关联：
 - ASSISTED_COMBAT_RULE_TYPE_COMBO_POINTS_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_COMBO_POINTS_LESS

需要新建插件 `spec_power_combo_points`

连击点不是主要能量，所以不是秘密值，直接使用下面的方式就行。

local power = UnitPower("player", Enum.PowerType.ComboPoints)
local mean = power / 255
cell:setCellRGBA(mean, mean, mean)

返回值，连击点值。整数。

### 21. 死亡骑士玩家符文数量

关联：
 - ASSISTED_COMBAT_RULE_TYPE_RUNES_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_RUNES_LESS

已有符文插件`spec_dk_rune@dev`，改名为`spec_power_rune`

### 22. 玩家符文能量数量

关联：
 - ASSISTED_COMBAT_RULE_TYPE_RUNIC_POWER_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_RUNIC_POWER_LESS

需要新建插件 `spec_power_runic_power`

- 入参：
    - maxValue：最大能量值

-  Enum.PowerType.RunicPower
符文能量也是主要能量，参考法力值，大概率是秘密值，使用曲线构造亮度，然后计算。


### 23. 玩家灵魂碎片数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_SOUL_SHARDS_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_SOUL_SHARDS_LESS

需要新建插件 `spec_power_soul_shards`

- 入参：
    - maxValue：最大灵魂碎片值

参考 spec_power_combo_points ，灵魂碎片不是秘密值。使用 Enum.PowerType.SoulShards



### 24. 玩家星界能量数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_LUNAR_POWER_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_LUNAR_POWER_LESS

需要新建插件 `spec_power_lunar_power`

星界能量是秘密值，参考上述主要能量的实现说明。


### 25. 玩家神圣能量数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_HOLY_POWER_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_HOLY_POWER_LESS

需要新建插件 `spec_power_holy_power`

神圣能量不是秘密值，参考上述连击点的实现说明。


### 26. 玩家漩涡值数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_MAELSTROM_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_MAELSTROM_LESS

需要新建插件 `spec_power_maelstrom`

漩涡值是秘密值，参考上述主要能量的实现说明。


### 27. 玩家真气数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_CHI_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_CHI_LESS

需要新建插件 `spec_power_chi`

真气不是秘密值，参考上述连击点的实现说明。

### 28. 玩家狂乱值数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_INSANITY_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_INSANITY_LESS

需要新建插件 `spec_power_insanity`

狂乱值是秘密值，参考上述主要能量的实现说明。


### 29. 玩家精华数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_ESSENCE_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_ESSENCE_LESS

需要新建插件 `spec_power_essence`

精华不是秘密值，参考上述连击点的实现说明。


### 30. 玩家奥术充能数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_ARCANE_CHARGES_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_ARCANE_CHARGES_LESS

需要新建插件 `spec_power_arcane_charges`

奥术充能不是秘密值，参考上述连击点的实现说明。


### 31. 玩家恶魔之怒数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_FURY_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_FURY_LESS

需要新建插件 `spec_power_fury`

- 入参：
    - maxValue：最大恶魔之怒值

-  Enum.PowerType.Fury。
恶魔之怒是秘密值，参考上述主要能量的实现说明。


### 32. 玩家苦痛值数量。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_PAIN_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_PAIN_LESS

需要新建插件 `spec_power_pain`

- 入参：
    - maxValue：最大苦痛值

-  Enum.PowerType.Pain。
苦痛值是秘密值，参考上述主要能量的实现说明。


### 33. 玩家指定增益的层数。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_PLAYER_AURA_APPLICATION_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_PLAYER_AURA_APPLICATION_LESS

需要新建插件 `aura_player_buff_stacks`

这是一个valuebar的插件，返回玩家身上的增益的层数时间。

入参：
    - auraIDs：list，增益ID，可以多个ID，只显示一个AuraSlot，以应对同名增益，不同天赋不同id的情况。
    - 最大值
    - 最小值
    - 宽度：默认值2
返回值
    - 层数
提供1/（4*宽度）精度。
有些buff的层数很高才有意义，比如最大值30，最小值20，占比50%，则返回25。

如何实现valuebar参考 phantom\conditions\spell_charges@dev\template.lua
如何定位特定auraID，参考 phantom\conditions\player_has_buff@dev
如何在AddAuraSlot中绘制bar，参考@PhantomProject /src/0007_aura_slot_container.lua的ApplicationBar 

注意，实际上valuebar只是定位，我们通过AuraContainer的StatusBar方法，绘制了一个新bar在valuebar的位置。


### 34. 目标指定减益的层数

关联：
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_AURA_APPLICATION_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_TARGET_AURA_APPLICATION_LESS



需要新建插件 `aura_target_debuff_stacks`

和 aura_player_buff_stacks类似 



### 35. 技能是否在射程内。。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_IN_RANGE

新建插件 `spell_in_range`

入参:
    - spell：技能ID
    - unitToken：目标单位
返回值
    - 是否在射程内：boolean

使用定时刷新，1/10秒。判断UnitExists(unitToken)是否存在，若不存在，则返回false。

C_Spell.IsSpellInRange(spellID, unit)

是秘密值，使用EvaluateColorFromBoolean构建颜色。

### 36. 玩家是否有宠物。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_HAS_PET
 - ASSISTED_COMBAT_RULE_TYPE_HAS_NO_PET

新建插件 `player_has_pet`

返回值
    - 是否有宠物：boolean

UnitExists("pet")好像就满足了。



### 37. 技能充能层数

关联：
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_CHARGES_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_SPELL_CHARGES_LESS

已有插件：`spell_charges@dev`
维护说明即可


### 38. 技能可成功施放条件。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_COOLDOWN_ALLOW_CASTING_SUCCESS

已有插件 "spell_usable"
维护说明即可

### 39. 玩家生命值百分比。

关联：
 - ASSISTED_COMBAT_RULE_TYPE_PLAYER_HEALTH_PCT_GREATER
 - ASSISTED_COMBAT_RULE_TYPE_PLAYER_HEALTH_PCT_LESS

已有插件：`player_health_pct@dev`
维护说明即可












## Aura的Spellid过滤限制。

```lua
local canAssist = UnitCanAssist("player", unitToken, true, true)
```

AuraContainer 的 `includeSpellIDs / excludeSpellIDs` 大致规则：

```lua
if filter == "HELPFUL" then
    allowed = canAssist
elseif filter == "HARMFUL" then
    allowed = not canAssist
end
```

也就是：

```text
友方/可辅助单位：
HELPFUL + spellID ✅
HARMFUL + spellID ❌

不可辅助单位：
HELPFUL + spellID ❌
HARMFUL + spellID ✅
```

注意：

```lua
UnitCanAssist("player", unitToken)
```

默认等价于：

```lua
UnitCanAssist("player", unitToken, false, false)
```

而 Blizzard AuraContainer 用：

```lua
UnitCanAssist("player", unitToken, true, true)
```

目的是让“免疫 / 暂时不可交互”的友方仍然稳定归类为可辅助侧。

另外，`includeSpellIDs` 不能替代 `HELPFUL/HARMFUL`：

```lua
"HELPFUL|HARMFUL" -- ❌ 不是 OR
```

所以一个 Slot 不能直接做到“同一 spellID，不管 Buff 还是 Debuff 都匹配”。
