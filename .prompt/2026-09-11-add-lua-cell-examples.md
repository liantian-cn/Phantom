## Primary

```text
在第三步解码开始之前，我们要做一些例子，填充lua的区域，正巧这些例子也方便后续开发
在phantom\lua\下新建examples目录

代码风格类似phantom\lua\general下的文件，uuid用占位符{{uuid}}替换，

## 新建5个cell块

---设置颜色方法
---@param color colorRGBA 要设置的颜色
function Cell:setCell(color) -- 从颜色对象读取分量并更新单元格
    self:setCellRGBA(color:GetRGBA()) -- 传入颜色分量，透明度由 setCellRGBA 固定为 1
end


### 第一个块，技能冷却块

本地变量，大写在前面，回头改造为plugin会替代这些：
技能名称：黑暗命令   -- 其实lua内没用，仅作为注释
技能ID: 56221,56222  -- 一个list
类型: RotationsCell  -- 其实lua内没用，仅作为注释
位置Y：2    -- 第二行，RotationsCell对应的行。
位置X：1    -- 第一个
忽略GCD:   true -- 是否忽略GCD，未来改造成插件的入参。


技能冷却块的整体逻辑

白色 -> 冷却好
黑色 -> 冷却不好 or 不会
多个技能ID，是因为某些技能在不同天赋下ID不同。


技能冷却块的代码经验

用下面的方法，创建一个非线性的色彩曲线，实现技能冷却缩短时候

local C0 = CreateColor(255/255, 255/255, 255/255, 1),                                                   
local C1 = CreateColor(155 / 255, 155 / 255, 155 / 255, 1)                        
local C2 = CreateColor(105 / 255, 105 / 255, 105 / 255, 1)
local C3 = CreateColor(55 / 255, 55 / 255, 55 / 255, 1)
local C4 = CreateColor(0 / 255, 0 / 255, 0 / 255, 1)

local CreateColorCurve              = C_CurveUtil.CreateColorCurve
local remainingCurve = CreateColorCurve()
remainingCurve:SetType(Enum.LuaCurveType.Linear)
remainingCurve:AddPoint(0.0, C0)
remainingCurve:AddPoint(5.0, C1)
remainingCurve:AddPoint(30.0, C2)
remainingCurve:AddPoint(155.0, C3)
remainingCurve:AddPoint(375.0, C4)



IsSpellInSpellBook = C_SpellBook.IsSpellInSpellBook  

GetSpellCooldownDuration = C_Spell.GetSpellCooldownDuration

使用 IsSpellInSpellBook(spellID) 检测技能是否学会。如果学会，就用下一个技能。 IsSpellInSpellBook的返回值不是秘密值。



使用 EvaluateRemainingDuration 获得冷却事件
local remaining = GetSpellCooldownDuration(spellID,ignoreGCD)
local result = remaining:EvaluateRemainingDuration(remainingCurve)
result返回值是CreateColor对象。


技能冷却块的刷新机制

冷却时间不能绑定机制，只能OnUpdate，然后0.1秒间隔刷新，初始时间
local fastTimeElapsed = -random()

因为设计判断技能是否会，再绑定SPELLS_CHANGED

技能冷却块的的wiki注释，理解后写入注释

{{wowapi|t=a}}
Returns a duration object describing the active cooldown duration for a spell.
{{apisig|duration {{=}} C_Spell.GetSpellCooldownDuration(spellIdentifier [, ignoreGCD])}}

==Arguments==
:;spellIdentifier:{{apitype|SpellIdentifier}}
:;ignoreGCD:{{apitype|boolean?|default=false}}

==Returns==
:;duration:{{apitype|LuaDurationObject}}

==Patch changes==
* {{Patch 12.0.5|note=Added <code>ignoreGCD</code> argument.}}



{{widgetmethod}}
Calculates the remaining duration in seconds and evaluates it against a supplied curve.
{{apisig|result {{=}} DurationObject:EvaluateRemainingDuration(curve [, modifier])}}

==Arguments==
:;curve:{{apitype|LuaCurveObjectBase}}
:;modifier:{{apitype|Enum.DurationTimeModifier?|default=RealTime}}
{{:Enum.DurationTimeModifier|nocaption=1}}

==Returns==
:;result:{{apitype|LuaCurveEvaluatedResult|secret=SecretWhenCurveSecret}} - If no curve is specified, a floating point percentage value. Else, the result of evaluating the curve with the percentage as the input.

==Patch changes==
* {{Patch 12.0.0|note=Added.}}


### 第2个块，技能高亮块

本地变量，大写在前面，回头改造为plugin会替代这些：
技能名称：枯萎凋零   -- 其实lua内没用，仅作为注释
技能ID: 43264,43265  -- 一个list
类型: RotationsCell  -- 其实lua内没用，仅作为注释
位置Y：2    -- 第二行，RotationsCell对应的行。
位置X：2    -- 第2个



技能高亮块的整体逻辑

白色 -> 高亮
黑色 -> 没高亮 or 都不会
多个技能ID，是因为某些技能在不同天赋下ID不同。



local EvaluateColorFromBoolean      = C_CurveUtil.EvaluateColorFromBoolean
负责将秘密布尔值转化为颜色

local IsSpellOverlayed              = C_SpellActivationOverlay.IsSpellOverlayed
技能是否高亮，返回秘密布尔值

local isOverlayed = IsSpellOverlayed(spellID),
local color = EvaluateColorFromBoolean(isOverlayed, COLOR.WHITE, COLOR.BLACK)
isOverlayed 返回值是CreateColor对象

技能高亮块的刷新机制。

SPELL_ACTIVATION_OVERLAY_GLOW_SHOW
SPELL_ACTIVATION_OVERLAY_GLOW_HIDE

因为设计判断技能是否会，再绑定SPELLS_CHANGED

技能高亮块的wiki 


{{wowapi|t=a|namespace=C_SpellActivationOverlay|system=SpellActivationOverlay}}
Returns true if the specified spell currently has a proc / spell activation alert (glowing border).
{{apisig|isSpellOverlayed {{=}} C_SpellActivationOverlay.IsSpellOverlayed(spellID)}}

==Arguments==
:;spellID:{{apitype|number}}

==Returns==
:;isSpellOverlayed:{{apitype|boolean}}





### 第3个块，技能可用块

本地变量，大写在前面，回头改造为plugin会替代这些：
技能名称：灵界打击   -- 其实lua内没用，仅作为注释
技能ID: 50000,49998  -- 一个list
类型: RotationsCell  -- 其实lua内没用，仅作为注释
位置Y：2    -- 第二行，RotationsCell对应的行。
位置X：3    -- 第3个



技能可用块的整体逻辑

白色 -> 可用
黑色 -> 都不可用 or 都不会
多个技能ID，是因为某些技能在不同天赋下ID不同。

isUsable, insufficientPower = C_Spell.IsSpellUsable(spellIdentifier)

返回颜色的逻辑

local isUsable, insufficientPower = C_Spell.IsSpellUsable(spellID)
local color = EvaluateColorFromBoolean(isUsable, COLOR.WHITE, COLOR.BLACK)


技能可用块的刷新机制。


和冷却一样，只能用OnUpdate刷新。

因为设计判断技能是否会，再绑定SPELLS_CHANGED

技能可用块wiki

{{wowapi|t=a|namespace=C_Spell|system=Spell}}
Returns whether the spell is currently castable.
{{apisig|isUsable, insufficientPower {{=}} C_Spell.IsSpellUsable(spellIdentifier)}}

==Arguments==
:;spellIdentifier:{{apitype|SpellIdentifier}} - Spell ID, name, name(subtext), or link

==Returns==
:;isUsable:{{apitype|boolean}} - True if the spell is usable, false otherwise
:;insufficientPower:{{apitype|boolean}} - True if spell is specifically unusable due to insufficient power (i.e. MANA, RAGE, etc)

==Details==
* A spell might be unusable for a variety of reasons, such as:
:* The player hasn't learned the spell.
:* The player lacks required mana or reagents.
:* Reactive conditions haven't been met.

==Patch changes==
* {{Patch 11.0.0|note=Added, replacement for {{api|IsUsableSpell}}.}}


### 第4个块，玩家存在某个增益

本地变量，大写在前面，回头改造为plugin会替代这些：
技能名称：枯萎凋零   -- 其实lua内没用，仅作为注释
技能ID: 188298,188290  -- 一个list
类型: RotationsCell  -- 其实lua内没用，仅作为注释
位置Y：2    -- 第二行，RotationsCell对应的行。
位置X：4    -- 第4个

玩家存在某个增益的整体逻辑

CELL染黑，作为底板

白色 -> 存在增益
黑色 -> 露出底板，代表没有对应的增益
完全利用 AuraContainer实现，不需要刷新机制

local FrameLevel            = addonTable.FrameLevel            -- 数值条分隔底板、内容背景与填充层的层级定义

local container = CreateFrame("AuraContainer", nil, parent, "CustomAuraContainerTemplate")

local AURA_BORDER_FULL_TEXTURE = "Interface\\AddOns\\" .. addonName .. "\\media\\aura\\aura_border_full.tga" --一个覆盖满的贴图

cell.Frame现在是container父级

local function CreateSpellIDMap(spellIDs)
    local includeSpellIDs = {}

    for _, spellID in ipairs(spellIDs) do
        includeSpellIDs[spellID] = true
    end

    return includeSpellIDs
end

local function InitializeAuraButton(auraButton, container, parent)
    auraButton:SetSize(SIZE.CELL, SIZE.CELL)
    auraButton:SetPoint("TOPLEFT", container, "TOPLEFT")
    auraButton:SetFrameLevel(FrameLevel.AuraButton)

    auraButton.ActiveOverlay = auraButton:CreateTexture(nil, "OVERLAY")
    auraButton.ActiveOverlay:SetAllPoints(auraButton)
    auraButton.ActiveOverlay:SetTexture(AURA_BORDER_FULL_TEXTURE)
    auraButton.ActiveOverlay:SetVertexColor(COLOR.WHITE:getRGBA())
end


container:SetPoint(
    "TOPLEFT",
    cell.Frame,
    "TOPLEFT",
    SIZE.CELL,
    SIZE.CELL
)
container:SetSize(size.CELL, size.CELL)
-- 这里有其他填满的方式更好。我忘了。


container:SetFrameLevel(FrameLevel.AuraContainer)

container:SetUnit("player")

container:AddAuraSlot("{{uuid}}", "HELPFUL", {
    candidateFilters = {
        includeSpellIDs = CreateSpellIDMap(技能ID组成的table),
    },
    initializeFrame = function(frame)
        InitializeAuraButton(frame, size, container, parent)
    end,
})



### 第5个块，玩家血量

本地变量，大写在前面，回头改造为plugin会替代这些：
类型: RotationsCell  -- 其实lua内没用，仅作为注释
位置Y：2    -- 第二行，RotationsCell对应的行。
位置X：5    -- 第5个
usePredicted -- 怎么翻译，默认true



技能可用块的整体逻辑

白色 -> 满血
黑色 -> 没血
多个技能ID，是因为某些技能在不同天赋下ID不同。

local UnitHealthPercent     = UnitHealthPercent  -- 输入

返回颜色的逻辑
local healthCurve = CreateColorCurve()
healthCurve:SetType(Linear)
healthCurve:AddPoint(0.0, COLOR.BLACK)
healthCurve:AddPoint(1.0, COLOR.WHITE)
local color = UnitHealthPercent("player", usePredicted , cell.zeroToOneCurve)



事件注册

eventFrame:RegisterUnitEvent("UNIT_HEALTH", "player")
eventFrame:RegisterUnitEvent("UNIT_MAXHEALTH", "player")

```

## Question

**技能选择**

> 前三个示例如何处理多个技能 ID？“如果学会，就用下一个技能”是否指未学会才继续查找？是按顺序选择首个已学会 ID、任意技能满足，还是最后一个已学会 ID？

首个已学会 ID。

**冷却颜色**

> 冷却块采用给定灰度曲线，还是冷却完成白色、仍在冷却或未学会黑色的两态行为？给定曲线在 0 秒为白色，5/30/155/375 秒分别为 155/105/55/0 灰度，中间分段线性过渡，未学会黑色。

采用给定灰度曲线。

**加载方式**

> 五个独立示例是否加入 TOC，在 general 后按顺序加载并直接填充第二行第 1–5 列，还是仅保存源码供手动接入？

加入 TOC。

**冷却空值**

> 选中的技能通过 IsSpellInSpellBook 检查，但 GetSpellCooldownDuration 没有返回 duration 对象时，冷却块应显示黑色并在下次 0.1 秒刷新重新查询，还是将其视为已就绪并显示白色？

黑色。

**实施授权**

> 是否按已确认的五个 Lua Cell 示例计划实施？

Implement the plan.
