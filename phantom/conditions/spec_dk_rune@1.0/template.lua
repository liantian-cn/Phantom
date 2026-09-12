--[[
original: ../conditions/spec_dk_rune@1.0/template.lua
uuid: {{uuid}}
摘要：在分配的 Cell 中以数量亮度显示死亡骑士可用符文。
描述：遍历六个符文，统计普通 runeReady；忽略事件的秘密参数。
修改记录：
2026-09-12：新增 spec_dk_rune@1.0 模板。
]]

--[[  namespace initialization  ]]
local addonName, addonTable = ...

--[[  api cache  ]]
local CreateFrame = CreateFrame -- 创建独立事件框架
local GetRuneCooldown = GetRuneCooldown -- 查询每个符文的就绪状态
local insert = table.insert -- 注册延迟初始化
--[[
GetRuneCooldown(runeIndex) 返回 startTime, duration, isRuneReady；允许没有返回值。
runeIndex 是从 1 开始的符文索引，本插件查询 1–6，仅使用普通 isRuneReady。
PlayerScriptDocumentation.lua 未标记秘密返回；官方 RuneFrame.lua 同样对 runeReady 分支。
RUNE_POWER_UPDATE 的 runeIndex、added 负载均可能秘密，本插件不接收或使用负载。
来源：https://warcraft.wiki.gg/wiki/API_GetRuneCooldown
2026-09-12 Wiki 页面访问失败；上述信息依据本地源码，不声称在线核验成功。
E:/Documents/GitHub/wow-ui-source，12.1.0.69587，
revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58；
PlayerScriptDocumentation.lua、UnitDocumentation.lua、Blizzard_UnitFrame/Mainline/RuneFrame.lua。
]]

--[[  variable reference  ]]
local Cell = addonTable.Cell -- 普通灰度 Cell
local UIInitFuncs = addonTable.UIInitFuncs -- 共享背景就绪后创建区域

--[[  logical code  ]]
local runeCell -- 本实例输出区域
local eventFrame = CreateFrame("Frame") -- 本实例独立事件框架

local function RefreshRunes()
    if not runeCell then
        return
    end
    local readyRunes = 0 -- 当前就绪符文数量
    for runeIndex = 1, 6 do
        local _, _, runeReady = GetRuneCooldown(runeIndex)
        if runeReady then
            readyRunes = readyRunes + 1
        end
    end
    local brightness = readyRunes / 255 -- 普通整数可直接转换灰度
    runeCell:setCellRGBA(brightness, brightness, brightness)
end

local function InitializeRunes()
    runeCell = Cell:New({x = {{x1}}, y = 2})
    RefreshRunes()
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
eventFrame:RegisterEvent("RUNE_POWER_UPDATE")
eventFrame:SetScript("OnEvent", RefreshRunes) -- 不接收秘密事件参数
insert(UIInitFuncs, InitializeRunes)
