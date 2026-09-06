--[[
original: runtime\05_background.lua
uuid: daff1721-dbdd-4c7f-ab23-40701e1e82ab
runtime_index: 5
摘要：
    创建像素矩阵背景与左上、右下两个棋盘格定位标记。

描述：
    将背景初始化函数登记到共享 UI 初始化队列，执行时创建宽 2、高 5 个 Cell 的背景框体。
    调试模式下背景居中并显示蓝色，普通模式下贴齐游戏界面左上角并保持透明。
    在背景的两个对角各放置一个 Cell 大小的双色棋盘格标记，供画面定位使用；
    最后将背景框体写入 addonTable.BackgroundFrame，供后续模块访问。


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After                    = C_Timer.After                      -- 指定秒数后执行回调
local insert                   = table.insert -- 插入表元素
local CreateFrame              = CreateFrame  -- 创建框体
local CreateColor              = CreateColor                        -- 创建 RGBA 颜色对象
local UIParent                 = UIParent     -- 游戏主界面父框体
local CreateColorCurve         = C_CurveUtil.CreateColorCurve       -- 创建颜色曲线对象
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean -- 按布尔值选择对应颜色
local Linear                   = Enum.LuaCurveType.Linear           -- 曲线点之间使用线性插值

--[[  variable reference  ]]


local COLOR       = addonTable.COLOR       -- 共享背景色与定位标记配色
local DEBUG       = addonTable.DEBUG       -- 调试模式决定背景的位置和底色
local FrameLevel  = addonTable.FrameLevel  -- 背景与 Cell 底层框体的层级定义
local UIInitFuncs = addonTable.UIInitFuncs -- 共享 UI 初始化函数队列
local SIZE        = addonTable.SIZE        -- 共享 Cell 尺寸定义

--[[  logical code  ]]

local WHITE_TEXTURE = "Interface\\Buttons\\WHITE8X8" -- 白色纹理资源路径，当前流程未使用

local function InitBackgroundFrame() -- 创建矩阵框架
    --[[
        初始化面板
        逻辑:
        - 以下尺寸都是SIZE.CELL的倍数
        - 初始面板大小仅有高5 宽2
        - 左上角和右下角是定位符。

        DEBUG模式：
        - debug模式下更显眼
    ]]

    local bgFrame = CreateFrame("Frame", addonName .. "BackgroundFrame", UIParent) -- 创建矩阵背景父框体
    if DEBUG then
        bgFrame:SetPoint("CENTER", UIParent, "CENTER", 0, 0) -- 调试时居中便于观察
    else
        bgFrame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0) -- 普通模式固定在界面左上角
    end
    bgFrame:SetSize(SIZE.CELL * 2, SIZE.CELL * 5) -- 初始化为宽 2、高 5 个 Cell
    bgFrame:SetFrameStrata("TOOLTIP") -- 将背景放入 TOOLTIP 显示层
    bgFrame:SetFrameLevel(FrameLevel.Background) -- 使用背景框体层级
    bgFrame:Show()

    local bgTexture = bgFrame:CreateTexture(nil, "BACKGROUND") -- 创建背景底色纹理
    bgTexture:SetAllPoints() -- 铺满背景框体
    if DEBUG then
        bgTexture:SetColorTexture(COLOR.BLUE:GetRGBA()) -- 调试时用蓝色显示背景范围
    else
        bgTexture:SetColorTexture(COLOR.TRANSPARENT:GetRGBA()) -- 普通模式使背景底色透明
    end

    bgTexture:Show()



    local function CreateMaskFrame(mask_idx) -- 按标识创建一个双色棋盘格定位框体
        --[[
        每个标记位：
            整体一个Cell大小，由4个边长为 SIZE.CELL / 2 的方片组成。颜色不同，使用COLOR.MARK.POINT_0和COLOR.MARK.POINT_1
            排列为:
            0 | 1
            -----
            1 | 0

        ]]

        local _frame = CreateFrame("Frame", addonName .. "MaskFrame" .. mask_idx, bgFrame) -- 定位框体随背景移动
        _frame:SetSize(SIZE.CELL, SIZE.CELL) -- 每个定位标记占一个 Cell
        _frame:SetFrameStrata("TOOLTIP")
        _frame:SetFrameLevel(FrameLevel.CellBackground) -- 使用 Cell 底层框体层级
        _frame:Show()

        local cells = {} -- 按行列保存标记的四块纹理
        local cell_size = SIZE.CELL / 2 -- 每块纹理边长为半个 Cell
        local colors = { -- 棋盘格交替使用的两种标记颜色
            COLOR.MARK.POINT_0,
            COLOR.MARK.POINT_1,
        }

        for row = 1, 2 do
            cells[row] = {}
            for col = 1, 2 do
                local _texture = _frame:CreateTexture(nil, "ARTWORK") -- 创建当前行列的标记色块
                _texture:SetSize(cell_size, cell_size)
                _texture:SetPoint(
                    "TOPLEFT", _frame, "TOPLEFT",
                    (col - 1) * cell_size, -(row - 1) * cell_size -- 从左上角向右、向下排列
                )

                local color = colors[(row + col) % 2 + 1] -- 行列和的奇偶决定颜色，形成 0/1、1/0 排列
                _texture:SetColorTexture(color:GetRGBA())

                cells[row][col] = _texture
            end
        end
        return _frame
    end -- CreateMaskFrame

    local top_left_mask = CreateMaskFrame("1") -- 创建左上定位标记
    top_left_mask:SetPoint("TOPLEFT", bgFrame, "TOPLEFT", 0, 0)
    local bottom_right_mask = CreateMaskFrame("1") -- 创建右下定位标记
    bottom_right_mask:SetPoint("BOTTOMRIGHT", bgFrame, "BOTTOMRIGHT", 0, 0)


    addonTable.BackgroundFrame = bgFrame -- 发布背景框体供其他模块引用
end
insert(UIInitFuncs, InitBackgroundFrame) -- 登记初始化函数，由共享 UI 初始化流程执行
