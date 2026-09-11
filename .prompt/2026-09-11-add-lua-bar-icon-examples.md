# Primary

在第三步解码开始之前，我们要做一些例子，填充lua的区域，正巧这些例子也方便后续开发
在phantom\lua\examples下创建

目前已有5个cell块，现在新建一个valuebar，2个icontile

代码风格参考cell块

### valuebar:技能充能层数

本地变量，大写在前面，回头改造为plugin会替代这些：
技能名称：血液沸腾   -- 其实lua内没用，仅作为注释
技能ID: 50841,50842 一个list
类型: ValueBar  -- 其实lua内没用，仅作为注释
位置X：1    -- 第1个
充能/宽度：2    -- 因为该技能最多有2层充能。
反向填充: false   -- ValueBar的参数


技能充能的整体逻辑

minValue = 0
maxValue = 最大充能 = 宽度
currentValue = 目前充能的层数

技能充能的代码经验

参考 phantom\lua\examples\01_spell_cooldown.lua

使用 C_SpellBook.IsSpellInSpellBook检测是否在技能书，使用第一个检测到的技能。
都检测不到，则为0




关联事件
PLAYER_ENTERING_WORLD
SPELL_UPDATE_CHARGES
SPELL_UPDATE_USES
SPELLS_CHANGED

local GetSpellCharges =  C_Spell.GetSpellCharges

local chargeInfo = GetSpellCharges(chargeBar.spellID)
if chargeInfo then
    chargeBar.bar:SetValue(chargeInfo.currentCharges)
else
    chargeBar.bar:SetValue(0)
end


GetSpellCharges的wiki，加入注释

{{wowapi|t=a}}
Returns a table of info about the charges of a charge-accumulating spell; May return nil if spell is not found or is not charge-based
{{apisig|chargeInfo {{=}} C_Spell.GetSpellCharges(spellIdentifier)}}

==Arguments==
:;spellIdentifier:{{apitype|SpellIdentifier}}

==Returns==
:;chargeInfo:{{apitype|SpellChargeInfo}}
{{:Structure SpellChargeInfo|nocaption=1}}



### icontile:玩家施法技能

本地变量，大写在前面，回头改造为plugin会替代这些：
类型: ValueBar  -- 其实lua内没用，仅作为注释
位置X：1    -- 第1个


技能充能的整体逻辑

玩家正在施法or正在通道技能 > 显示施法图标 > 脚标颜色为COLOR.SPELL_TYPE.PLAYER_SPELL
玩家未在施法和通道技能 > 显示黑色底板 and 脚标为透明 > 等效IconTile:Clear()

local UnitCastingInfo       = UnitCastingInfo
local UnitChannelInfo       = UnitChannelInfo


  -- delayTimeMs is a required NeverSecret sentinel for an active cast, avoiding branches on secret texture or name.
  local _, _, castingTexture, _, _, _, _, _, _, _, castDelayTimeMs = UnitCastingInfo("player")

  if castDelayTimeMs ~= nil then
      icontile:SetIcon(castingTexture)
      icontile:SetBorderColor(COLOR.SPELL_TYPE.PLAYER_SPELL)
      return
  end

  -- isEmpowered is a required NeverSecret sentinel for an active channel, avoiding branches on secret texture or name.
  local _, _, channelTexture, _, _, _, _, _, isEmpowered = UnitChannelInfo("player")

  if isEmpowered ~= nil then
      icontile:SetIcon(channelTexture)
      icontile:SetBorderColor(COLOR.SPELL_TYPE.PLAYER_SPELL)
      return
  end

  icontile:Clear()

关联事件

eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_START", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_STOP", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTED", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED_QUIET", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_DELAYED", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_START", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_STOP", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_UPDATE", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_START", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_STOP", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTIBLE", "player")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_NOT_INTERRUPTIBLE", "player")
PLAYER_ENTERING_WORLD不能漏掉


UnitCastingInfo的Wiki, UnitChannelInfo类似。


{{wowapi|t=a|system=Unit}}
Returns information about the spell currently being cast by the specified unit.
{{apisig|name, displayName, textureID, startTimeMs, endTimeMs, isTradeskill, castID, notInterruptible, castingSpellID, castBarID, delayTimeMs {{=}} UnitCastingInfo(unit)}}

==Arguments==
:;unit:{{apitype|UnitToken}}

==Returns==
:;name:{{apitype|string}} - The name of the spell, or nil if no spell is being cast.
:;displayName:{{apitype|string}} - The name to be displayed.
:;textureID:{{apitype|fileID}} - The texture path associated with the spell icon.
:;startTimeMs:{{apitype|number}} - Specifies when casting began in milliseconds (corresponds to [[API GetTime|GetTime()]]*1000).
:;endTimeMs:{{apitype|number}} - Specifies when casting will end in milliseconds (corresponds to [[API GetTime|GetTime()]]*1000).
:;isTradeskill:{{apitype|boolean|secret=NeverSecret}} - Specifies if the cast is a tradeskill
:;castID:{{apitype|string}} : [[GUID#Cast|GUID]] - The unique identifier for this spell cast, for example <code>Cast-3-3890-1159-21205-8936-00014B7E7F</code>.
:;notInterruptible:{{apitype|boolean?}} - if true, indicates that this cast cannot be interrupted with abilities like [[Kick]] or [[Pummel]]. In default UI those spells have shield frame around their icons on enemy cast bars. Always returns <code>nil</code> in Classic {{bc-inline}}.
:;castingSpellID:{{apitype|number}} - The spell's unique identifier.
:;castBarID:{{apitype|number|secret=NeverSecret}}
:;delayTimeMs:{{apitype|number|secret=NeverSecret}} - Total accrued delay for this spell cast from pushback.

==Details==
* For channeled spells, displayName is "Channeling". So far displayName is observed to be the same as name in any other contexts.
* This function may not return anything when the target is channeling spell post it warm-up period, you should use {{api|UnitChannelInfo}}  in that case. It takes the same arguments and returns similar values specific to channeling spells. Be careful, that although similar, it has different amount of returns and different positions for some returns.
* {{wow-inline}} In Classic, the alternative {{api|CastingInfo}}() is similar to <code>UnitCastingInfo("player")</code>
{| {{apitable}}
{{apirow | Related Events | {{api|t=e|UNIT_SPELLCAST_START}}<br>{{api|t=e|UNIT_SPELLCAST_STOP}} }}
{{apirow | Related API | {{api|CastingInfo}} (Classic)}}
|}



### icontile:目标施法技能

本地变量，大写在前面，回头改造为plugin会替代这些：
类型: ValueBar  -- 其实lua内没用，仅作为注释
位置X：2    -- 第2个

参考 /PhantomProject/src/0209_target_cast_info.lua

相对玩家的更加复杂

目标不存在 -> Clear -> 露出黑色底板
目标施法可否打断 ->         icontile:SetBorderColor(EvaluateColorFromBoolean(
            notInterruptible,
            COLOR.SPELL_TYPE.NOT_INTERRUPTIBLE,
            COLOR.SPELL_TYPE.INTERRUPTIBLE
        ))



注意目标不存在的事件
eventFrame:RegisterEvent("PLAYER_TARGET_CHANGED")
eventFrame:RegisterEvent("UNIT_TARGETABLE_CHANGED") 

PLAYER_ENTERING_WORLD不能漏掉

# Question

**图标位置**

> 玩家、目标图标的“第1个、第2个”如何对应现有 IconTile 坐标？现有构造函数按 x × 8 像素定位，直接传入 1、2 会在内容左侧留下 4 像素空隙。

直接传入 1、2。

**未知角标**

> 目标正在施法，但 notInterruptible 返回普通 nil 时，角标如何显示？

按不可打断着色。

**实施授权**

> Implement the agreed plan after leaving Plan mode?

Implement the plan.

