--[[
original: ../conditions/liantian_cn.player_is_targeting_spell@dev/template.lua
uuid: {{uuid}}
plugin: liantian_cn.player_is_targeting_spell@dev
摘要：玩家是否正在选择施法目标。
描述：
    布尔值直接用黑白编码。
    参数校验和配对解码见 condition.py；本实例使用冻结坐标，不继承旧项目分类色。
修改记录：
2026-09-15：按已确认计划新增玩家条件插件。
]]

--[[  namespace initialization  ]]
local addonName, addonTable = ...

--[[  api cache  ]]
local CreateFrame = CreateFrame -- 创建本实例事件或显示框架
local insert = table.insert -- 注册 UI 初始化回调
local SpellIsTargeting = SpellIsTargeting -- 查询法术目标选择状态
local random = math.random -- 为本实例轮询生成随机错峰

--[[
用途与签名：result = SpellIsTargeting()；返回是否处于法术目标选择状态。
业务限制：布尔值直接用黑白编码。
核验日期：2026-09-15；本地 E:/Documents/GitHub/wow-ui-source，12.1.0.69587。
源码 revision：a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58。
来源：本地源码 Interface/AddOns/ 下：
    Blizzard_FrameXML/SecureTemplates.lua
旧项目参考：PhantomProject/src/0112_player_is_targeting_spell.lua；revision f6935113e686eb73785b8315c58368093012c959。
Wiki 查询入口（本次未能获取在线说明；以下链接不作为已核验网页证据）：
    https://warcraft.wiki.gg/wiki/API_SpellIsTargeting
]]

--[[  variable reference  ]]
local Cell = addonTable.Cell -- 黑色底板及单元格显示接口
local UIInitFuncs = addonTable.UIInitFuncs -- 共享布局就绪后初始化本实例

--[[  logical code  ]]
local POSITION_X = {{x1}} -- 本实例冻结的横向位置
local POSITION_Y = {{y1}} -- 本实例冻结的 Cell 行
local UNIT_TOKEN = "player" -- 本版本固定玩家单位
local REFRESH_SECONDS = 2 -- 保留旧插件兜底间隔

local cell
local eventFrame = CreateFrame("Frame")

local function update()
    if not cell then return end -- UI 初始化之前不访问显示对象
    cell:setCellBoolean(SpellIsTargeting())
end

local function initialize()
    cell = Cell:New({ x = POSITION_X, y = POSITION_Y }) -- 黑底等待事件或错峰首次刷新
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD") -- 进入世界时同步本实例状态
eventFrame:RegisterEvent("CURRENT_SPELL_CAST_CHANGED")
eventFrame:SetScript("OnEvent", update)

local fastTimeElapsed = -random() -- 每个实例独立错峰，不修改全局随机种子
eventFrame:SetScript("OnUpdate", function(_, elapsed)
    fastTimeElapsed = fastTimeElapsed + elapsed
    if fastTimeElapsed > REFRESH_SECONDS then
        fastTimeElapsed = fastTimeElapsed - REFRESH_SECONDS -- 保留余量，每帧最多刷新一次
        update()
    end
end)

insert(UIInitFuncs, initialize)
