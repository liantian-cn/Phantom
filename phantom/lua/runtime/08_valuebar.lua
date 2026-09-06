--[[
original: runtime\08_valuebar.lua
uuid: 99f3155c-0642-41c8-9856-8613628f61ab
runtime_index: 8
摘要：


描述：



修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After                    = C_Timer.After                        -- 指定秒数后执行回调
local insert                   = table.insert                         -- 插入表元素
local CreateFrame              = CreateFrame                          -- 创建框体
local CreateColor              = CreateColor                          -- 创建 RGBA 颜色对象
local UIParent                 = UIParent                             -- 游戏主界面父框体
local CreateColorCurve         = C_CurveUtil.CreateColorCurve         -- 创建颜色曲线对象
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean -- 按布尔值选择对应颜色
local Linear                   = Enum.LuaCurveType.Linear             -- 曲线点之间使用线性插值

--[[  variable reference  ]]

local COLOR                 = addonTable.COLOR                 -- 共享基础颜色，提供单元格黑白配色
local DEBUG                 = addonTable.DEBUG                 -- 共享调试开关（本文件暂未使用）
local FrameLevel            = addonTable.FrameLevel            -- 背景与 Cell 底层框体的层级定义
local UIInitFuncs           = addonTable.UIInitFuncs           -- 共享 UI 初始化函数队列
local SIZE                  = addonTable.SIZE                  -- 共享 Cell 尺寸定义
local ValueBarLength        = addonTable.ValueBarLength        -- Value Bar 区域的共享长度，初值取自共享表
local BackgroundFrameResize = addonTable.BackgroundFrameResize -- 按共享长度数据调整背景尺寸


--[[  logical code  ]]

---@class ValueBar
---@field Frame Frame 单元格框架
---@field StatusBar StatusBar 内部的StatusBar
---@field X integer X坐标
---@field width number 宽度
local ValueBar = {}
ValueBar.__index = ValueBar




---ValueBar 初始化方法（私有）
---@private
---@param x integer X坐标
---@param width number 宽度
---@param index number 序号
---@param reverse boolean 是否反向填充
function ValueBar:_initialize(x, width, index, reverse)
    local parent = addonTable.BackgroundFrame -- 创建时读取共享背景框体作为父框体
    local barName = addonName .. "Bar_" .. x

    --[[
        barFrame:
            每个value bar底部有个frame。是黑色的。
            X从1开始，对于普通人更好理解。但是第0列正好是占位符，所以在 Lua 中不需要额外偏移。
            Y从固定是-2，因为0是通用cell、-1是条件cell
        index
            这里要解决一个问题。
            如果相互挨着的2个bar，在屏幕抗锯齿、渲染机制下，如何做到依然可以分辨。
            那么就在颜色上，稍微做点手脚
            背景色是不是纯黑，而是r=0,g=0,b=index
            状态条的颜色不是纯白，而是r=255,g=255-index,b=255
            细小的颜色差异，在python端可以解码出来。

    ]]

    local barFrame = CreateFrame("Frame", barName, parent)
    local offset_x = x
    local offset_y = -2

    barFrame:SetPoint("TOPLEFT", parent, "TOPLEFT", offset_x * SIZE.CELL, offset_y * SIZE.CELL) -- 以 Cell 边长换算相对背景左上角的位置
    barFrame:SetFrameStrata("TOOLTIP")                                                          -- 使用 TOOLTIP 显示层
    barFrame:SetFrameLevel(FrameLevel.BarFrame)                                                 -- 使用共享 Cell 框体层级
    barFrame:SetSize(width * SIZE.CELL, SIZE.CELL)
    barFrame:Show()

    local bg = barFrame:CreateTexture(nil, "BACKGROUND")
    bg:SetAllPoints()
    bg:SetColorTexture(0, 0, index / 255, 1)


    local bar = CreateFrame("StatusBar", nil, barFrame)
    bar:SetAllPoints()
    bar:SetAllPoints(barFrame)
    bar:SetFrameLevel(FrameLevel.BarFrame)
    bar:SetColorFill(1, (255 - index) / 255, 1, 1)

    if reverse then
        bar:SetReverseFill(true)
    end
    bar:Show()

    self.Frame = barFrame
    self.X = x
    self.width = width
    self.StatusBar = bar
    self:setMinMaxValues(0, 100)
    self:setValue(50)
end

---Bar 构造函数
---@param x integer X坐标
---@param width number 宽度
---@param index number 序号
---@return ValueBar|nil # 返回Bar实例, 如果父框架不存在则返回nil
function ValueBar:New(x, width, index, reverse)
    if reverse and (reverse == true) then
        reverse = true
    else
        reverse = false
    end
    local instance = setmetatable({}, self)
    instance:_initialize(x, width, index, reverse)
    return instance
end

function ValueBar:setMinMaxValues(minValue, maxValue)
    self.StatusBar:SetMinMaxValues(minValue, maxValue)
end

function ValueBar:setValue(currentValue)
    self.StatusBar:SetValue(currentValue)
end
