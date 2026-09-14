--[[
original: ../conditions/liantian_cn.player_has_spell@dev/template.lua
uuid: {{uuid}}
plugin: liantian_cn.player_has_spell@dev
摘要：玩家是否掌握任一候选技能。
描述：
    任一 ID 已知或在法术书中即为真；与 player_has_talent 行为完全相同，事件后延迟 0.25 秒合并刷新。
    参数校验和配对解码见 condition.py；本实例使用冻结坐标，不继承旧项目分类色。
修改记录：
2026-09-15：按已确认计划新增玩家条件插件。
]]

--[[  namespace initialization  ]]
local addonName, addonTable = ...

--[[  api cache  ]]
local CreateFrame = CreateFrame -- 创建本实例事件或显示框架
local insert = table.insert -- 注册 UI 初始化回调
local IsSpellKnown = C_SpellBook.IsSpellKnown -- 查询玩家已知技能
local IsSpellInSpellBook = C_SpellBook.IsSpellInSpellBook -- 查询玩家法术书及覆盖技能
local NewTimer = C_Timer.NewTimer -- 创建可取消的延迟刷新
local ipairs = ipairs -- 遍历配置的候选技能 ID

--[[
用途与签名：known = C_SpellBook.IsSpellKnown(spellID)；inBook = C_SpellBook.IsSpellInSpellBook(spellID)；默认玩家法术书，返回布尔值，后者含覆盖技能。C_Timer.NewTimer(0.25, callback) 返回可取消 timer。
业务限制：任一 ID 已知或在法术书中即为真；与 player_has_talent 行为完全相同，事件后延迟 0.25 秒合并刷新。
核验日期：2026-09-15；本地 E:/Documents/GitHub/wow-ui-source，12.1.0.69587。
源码 revision：a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58。
来源：本地源码 Interface/AddOns/ 下：
    Blizzard_APIDocumentationGenerated/SpellBookDocumentation.lua
旧项目参考：PhantomProject/src/0124_player_hero_talent.lua；revision f6935113e686eb73785b8315c58368093012c959。
Wiki 查询入口（本次未能获取在线说明；以下链接不作为已核验网页证据）：
    https://warcraft.wiki.gg/wiki/API_C_SpellBook.IsSpellKnown
    https://warcraft.wiki.gg/wiki/API_C_SpellBook.IsSpellInSpellBook
    https://warcraft.wiki.gg/wiki/API_C_Timer.NewTimer
]]

--[[  variable reference  ]]
local Cell = addonTable.Cell -- 黑色底板及单元格显示接口
local UIInitFuncs = addonTable.UIInitFuncs -- 共享布局就绪后初始化本实例

--[[  logical code  ]]
local POSITION_X = {{x1}} -- 本实例冻结的横向位置
local POSITION_Y = {{y1}} -- 本实例冻结的 Cell 行
local UNIT_TOKEN = "player" -- 本版本固定玩家单位
local SPELL_IDS = { {{spell_ids}} } -- 任一候选满足即为真
local REFRESH_DELAY_SECONDS = 0.25 -- 合并法术书变化

local cell
local pendingRefreshTimer
local eventFrame = CreateFrame("Frame")

local function update()
    if not cell then return end
    for _, spellID in ipairs(SPELL_IDS) do
        if IsSpellKnown(spellID) or IsSpellInSpellBook(spellID) then
            cell:setCellBoolean(true)
            return
        end
    end
    cell:setCellBoolean(false)
end

local function requestRefresh()
    if pendingRefreshTimer then pendingRefreshTimer:Cancel() end
    pendingRefreshTimer = NewTimer(REFRESH_DELAY_SECONDS, function()
        pendingRefreshTimer = nil
        update()
    end)
end

local function initialize()
    cell = Cell:New({ x = POSITION_X, y = POSITION_Y })
    requestRefresh() -- 初始化之前即使错过世界事件，也会同步法术书
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD") -- 进入世界时同步本实例状态
eventFrame:RegisterEvent("SPELLS_CHANGED")
eventFrame:SetScript("OnEvent", requestRefresh)
insert(UIInitFuncs, initialize)
