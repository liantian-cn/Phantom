--[[
original: runtime\05_background.lua
uuid: daff1721-dbdd-4c7f-ab23-40701e1e82ab
runtime_index: 5
摘要：



描述：
    -


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After                    = C_Timer.After
local insert                   = table.insert -- 插入表元素
local CreateFrame              = CreateFrame  -- 创建框体
local CreateColor              = CreateColor
local UIParent                 = UIParent     -- 游戏主界面父框体
local CreateColorCurve         = C_CurveUtil.CreateColorCurve
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean
local Linear                   = Enum.LuaCurveType.Linear

--[[  variable reference  ]]


local COLOR       = addonTable.COLOR
local DEBUG       = addonTable.DEBUG
local FrameLevel  = addonTable.FrameLevel
local UIInitFuncs = addonTable.UIInitFuncs
local SIZE        = addonTable.SIZE

--[[  logical code  ]]

local WHITE_TEXTURE = "Interface\\Buttons\\WHITE8X8"

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

    local bgFrame = CreateFrame("Frame", addonName .. "BackgroundFrame", UIParent)
    if DEBUG then
        bgFrame:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
    else
        bgFrame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)
    end
    bgFrame:SetSize(SIZE.CELL * 2, SIZE.CELL * 5)
    bgFrame:SetFrameStrata("TOOLTIP")
    bgFrame:SetFrameLevel(FrameLevel.Background)
    bgFrame:Show()

    local bgTexture = bgFrame:CreateTexture(nil, "BACKGROUND")
    bgTexture:SetAllPoints()
    if DEBUG then
        bgTexture:SetColorTexture(COLOR.BLUE:GetRGBA())
    else
        bgTexture:SetColorTexture(COLOR.TRANSPARENT:GetRGBA())
    end

    bgTexture:Show()



    local function CreateMaskFrame(mask_idx)
        --[[
        每个标记位：
            整体一个Cell大小，由4个1/2 * CELL.SIZE大小的片组成。颜色不同，使用COLOR.MARK.POINT_0和COLOR.MARK.POINT_1
            排列为:
            0 | 1
            -----
            1 | 0

        ]]

        local _frame = CreateFrame("Frame", addonName .. "MaskFrame" .. mask_idx, bgFrame)
        _frame:SetSize(SIZE.CELL, SIZE.CELL)
        _frame:SetFrameStrata("TOOLTIP")
        _frame:SetFrameLevel(FrameLevel.CellBackground)
        _frame:Show()

        local cells = {}
        local cell_size = SIZE.CELL / 2
        local colors = {
            COLOR.MARK.POINT_0,
            COLOR.MARK.POINT_1,
        }

        for row = 1, 2 do
            cells[row] = {}
            for col = 1, 2 do
                local _texture = _frame:CreateTexture(nil, "ARTWORK")
                _texture:SetSize(cell_size, cell_size)
                _texture:SetPoint(
                    "TOPLEFT", _frame, "TOPLEFT",
                    (col - 1) * cell_size, -(row - 1) * cell_size
                )

                local color = colors[(row + col) % 2 + 1]
                _texture:SetColorTexture(color:GetRGBA())

                cells[row][col] = _texture
            end
        end
        return _frame
    end -- CreateMaskFrame

    local top_left_mask = CreateMaskFrame("1")
    top_left_mask:SetPoint("TOPLEFT", bgFrame, "TOPLEFT", 0, 0)
    local bottom_right_mask = CreateMaskFrame("1")
    bottom_right_mask:SetPoint("BOTTOMRIGHT", bgFrame, "BOTTOMRIGHT", 0, 0)


    addonTable.BackgroundFrame = bgFrame
end
insert(UIInitFuncs, InitBackgroundFrame)
