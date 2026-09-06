--[[
original: runtime\07_cell.lua
uuid: 3be6cff3-7f5f-460e-a810-8058d1d27a90
runtime_index: 7
摘要：创建矩阵单元格，并提供 RGB、颜色对象与布尔值着色接口。


描述：
    按指定行列在共享背景框体下创建方形纹理，初始化为不透明黑色并保存坐标。
    第一、二行分别递增本地通用与条件 Cell 计数，再调用依据共享长度调整背景的函数。
    提供颜色更新、布尔值黑白映射及反转、恢复黑色的方法，并通过 addonTable.Cell 公开。


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After                    = C_Timer.After -- 指定秒数后执行回调
local insert                   = table.insert -- 插入表元素
local CreateFrame              = CreateFrame  -- 创建框体
local CreateColor              = CreateColor -- 创建 RGBA 颜色对象
local UIParent                 = UIParent     -- 游戏主界面父框体
local CreateColorCurve         = C_CurveUtil.CreateColorCurve -- 创建颜色曲线对象
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean -- 按布尔值选择对应颜色
local Linear                   = Enum.LuaCurveType.Linear -- 曲线点之间使用线性插值

--[[  variable reference  ]]

local COLOR                 = addonTable.COLOR       -- 共享基础颜色，提供单元格黑白配色
local DEBUG                 = addonTable.DEBUG       -- 共享调试开关（本文件暂未使用）
local FrameLevel            = addonTable.FrameLevel  -- 背景与 Cell 底层框体的层级定义
local UIInitFuncs           = addonTable.UIInitFuncs -- 共享 UI 初始化函数队列
local SIZE                  = addonTable.SIZE        -- 共享 Cell 尺寸定义
local GeneralCellLength     = addonTable.GeneralCellLength -- 通用 Cell 长度的本地计数，初值取自共享表
local ConditionCellLength   = addonTable.ConditionCellLength -- 条件 Cell 长度的本地计数，初值取自共享表
local BackgroundFrameResize = addonTable.BackgroundFrameResize -- 按共享长度数据调整背景尺寸


--[[  logical code  ]]

local WHITE_TEXTURE = "Interface\\Buttons\\WHITE8X8" -- 用于着色的白色基础纹理
local TRUE_COLOR = COLOR.WHITE -- 布尔真值默认显示白色
local FALSE_COLOR = COLOR.BLACK -- 布尔假值默认显示黑色

---@class Cell
---@field Texture Texture 单元格纹理
---@field Frame Frame 单元格框架
---@field X integer X坐标
---@field Y integer Y坐标
local Cell = {} -- 单元格的方法集合
Cell.__index = Cell -- 实例从 Cell 表查找方法


---Cell 初始化方法（私有）
---@private
---@param x integer X坐标
---@param y integer Y坐标
function Cell:_initialize(x, y) -- 按列号和行号创建单元格
    local parent = addonTable.BackgroundFrame -- 创建时读取共享背景框体作为父框体
    local cellName = addonName .. "Cell_" .. x .. "_" .. y -- 按插件名和坐标组合框体名称
    --[[
        cellFrame
        每个cell底部有个frame。是黑色的。
        这里明确下坐标的计算方法。
        X从1开始，对于普通人更好理解。但是第0列正好是占位符，所以在 Lua 中不需要额外偏移。
        Y从1开始，取值1、2。1=通用Cell，2=条件Cell。但是因为现在的布局规划，是从上到下的。且SetPoint的相对坐标从0开始。所以要转换。

    ]]

    local cellFrame = CreateFrame("Frame", cellName, parent) -- 创建单元格承载框体
    local offset_x = x -- 保留第 0 列定位空间，列号直接作为横向偏移
    local offset_y = -(y - 1) -- 将从 1 开始的行号换算为向下的锚点偏移
    cellFrame:SetPoint("TOPLEFT", parent, "TOPLEFT", offset_x * SIZE.CELL, offset_y * SIZE.CELL) -- 以 Cell 边长换算相对背景左上角的位置
    cellFrame:SetFrameStrata("TOOLTIP") -- 使用 TOOLTIP 显示层
    cellFrame:SetFrameLevel(FrameLevel.Cell) -- 使用共享 Cell 框体层级
    cellFrame:SetSize(SIZE.CELL, SIZE.CELL) -- 设置单元格宽高
    cellFrame:Show() -- 显示单元格框体

    if y == 1 then -- 第一行计入通用 Cell
        GeneralCellLength = GeneralCellLength + 1 -- 递增本地通用计数，未写回共享表
    end

    if y == 2 then -- 第二行计入条件 Cell
        ConditionCellLength = ConditionCellLength + 1 -- 递增本地条件计数，未写回共享表
    end

    local cellTexture = cellFrame:CreateTexture(nil, "BACKGROUND") -- 创建单元格底色纹理
    cellTexture:SetAllPoints(cellFrame) -- 让纹理覆盖整个单元格
    cellTexture:SetTexture(WHITE_TEXTURE) -- 使用白色纹理承载后续颜色
    cellTexture:Show() -- 显示单元格纹理

    self.Texture = cellTexture -- 保存用于更新颜色的纹理
    self.Frame = cellFrame -- 保存单元格框体
    self.X = x -- 保存列号
    self.Y = y -- 保存行号

    self:setCell(COLOR.BLACK) -- 将单元格设为黑色
    BackgroundFrameResize() -- 调用背景尺寸更新函数
end

---使用 RGB 分量设置颜色，透明度固定为 1
---@param r number|string|table 红色分量
---@param g number|string|table 绿色分量
---@param b number|string|table 蓝色分量
function Cell:setCellRGBA(r, g, b) -- 按 RGB 分量更新单元格颜色
    self.Texture:SetVertexColor(r, g, b, 1) -- 应用颜色并固定为完全不透明
end

---设置颜色方法
---@param color colorRGBA 要设置的颜色
function Cell:setCell(color) -- 从颜色对象读取分量并更新单元格
    self:setCellRGBA(color:GetRGBA()) -- 传入颜色分量，透明度由 setCellRGBA 固定为 1
end

---Cell 构造函数
---@param options table 构造参数
---@return Cell # 返回初始化后的 Cell 实例
function Cell:New(options) -- 使用 options.x 和 options.y 构造单元格实例
    local instance = setmetatable({}, self) -- 创建共享 Cell 方法的新实例
    instance:_initialize(options.x, options.y) -- 按指定坐标初始化框体和纹理
    return instance -- 返回初始化后的单元格
end

---设置颜色方法, 根据布尔值选择颜色
---@param isTrue boolean 是否为true值
---@param reverse boolean 是否反转颜色选择，默认false
---@return nil
function Cell:setCellBoolean(isTrue, reverse) -- 将布尔值映射为黑白颜色
    if reverse then -- 反转真值与假值的默认配色
        self:setCell(EvaluateColorFromBoolean(isTrue, FALSE_COLOR, TRUE_COLOR)) -- 真值显示黑色，假值显示白色
    else
        self:setCell(EvaluateColorFromBoolean(isTrue, TRUE_COLOR, FALSE_COLOR)) -- 真值显示白色，假值显示黑色
    end
end

---清除颜色方法, 就是恢复默认的黑色
function Cell:clearCell() -- 恢复单元格默认底色
    self:setCell(COLOR.BLACK) -- 将单元格设为黑色
end

addonTable.Cell = Cell -- 向后续模块公开 Cell 构造与颜色操作接口
