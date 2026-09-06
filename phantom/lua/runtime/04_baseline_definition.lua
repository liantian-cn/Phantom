--[[
original: runtime\04_baseline_definition.lua
uuid: d9cf2e29-674c-4ad5-828a-d61d47fbed0d
runtime_index: 4
摘要：



描述：
    -


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local CreateColor = CreateColor
local insert      = table.insert -- 插入表元素

--[[  variable reference  ]]

local DEBUG            = addonTable.DEBUG
local GetUIScaleFactor = addonTable.GetUIScaleFactor
local scale            = addonTable.SCALE
local UIInitFuncs      = addonTable.UIInitFuncs


--[[  logical code  ]]

addonTable.COLOR = {
    AURA_TYPE = {                                                           -- 光环
        MAGIC = CreateColor(60 / 255, 100 / 255, 220 / 255, 1),             -- 魔法
        CURSE = CreateColor(100 / 255, 0, 120 / 255, 1),                    -- 诅咒
        DISEASE = CreateColor(160 / 255, 120 / 255, 60 / 255, 1),           -- 疾病
        POISON = CreateColor(154 / 255, 205 / 255, 50 / 255, 1),            -- 中毒
        ENRAGE = CreateColor(230 / 255, 120 / 255, 20 / 255, 1),            -- 激怒
        BLEED = CreateColor(80 / 255, 0, 20 / 255, 1),                      -- 流血
        DEBUFF_ON_FRIENDLY = CreateColor(255 / 255, 60 / 255, 60 / 255, 1), -- 在友方身上的减益,不属于上述状态
        BUFF_ON_FRIENDLY = CreateColor(80 / 255, 220 / 255, 120 / 255, 1),  -- 在友方身上的增益,不属于上述状态
        DEBUFF_ON_ENEMY = CreateColor(105 / 255, 105 / 255, 210 / 255, 1),  -- 在敌方身上的减益,不属于上述状态
    },
    SPELL_TYPE = {
        PLAYER_SPELL = CreateColor(64 / 255, 158 / 255, 210 / 255, 1),     -- 友方施法
        INTERRUPTIBLE = CreateColor(255 / 255, 255 / 255, 60 / 255, 1),    -- 可打断
        NOT_INTERRUPTIBLE = CreateColor(200 / 255, 0, 0, 1),               -- 不可打断
    },
    NONE = CreateColor(0, 0, 0, 0),                                        -- 无
    RED = CreateColor(255 / 255, 0, 0, 1),                                 -- 红色
    GREEN = CreateColor(0, 255 / 255, 0, 1),                               -- 绿色
    BLUE = CreateColor(0, 0, 255 / 255, 1),                                -- 蓝色
    BLACK = CreateColor(0, 0, 0, 1),                                       -- 黑色
    WHITE = CreateColor(1, 1, 1, 1),                                       -- 白色
    TRANSPARENT = CreateColor(0, 0, 0, 0),                                 -- 透明
    PANEL = {                                                              -- 面板的UI配色
        Black           = CreateColor(0 / 255, 0 / 255, 0 / 255, 1),       -- 纯黑
        WindowBg        = CreateColor(30 / 255, 30 / 255, 30 / 255, 1),    -- 窗口背景色
        WindowText      = CreateColor(0 / 255, 0 / 255, 0 / 255, 1),       -- 窗口文字色（备用）
        WindowBorder    = CreateColor(83 / 255, 88 / 255, 91 / 255, 1),    -- 窗口边框色
        Base            = CreateColor(255 / 255, 255 / 255, 255 / 255, 1), -- 基础白
        ButtonBorder    = CreateColor(52 / 255, 52 / 255, 52 / 255, 1),    -- 按钮边框色
        ButtonHighlight = CreateColor(86 / 255, 86 / 255, 86 / 255, 1),    -- 按钮悬停高亮
        ButtonMouseUp   = CreateColor(43 / 255, 43 / 255, 43 / 255, 1),    -- 按钮正常底色
        ButtonMouseDown = CreateColor(37 / 255, 37 / 255, 37 / 255, 1),    -- 按钮按下底色
        SliderLeft      = CreateColor(73 / 255, 179 / 255, 234 / 255, 1),  -- 滑块已填充色
        SliderRight     = CreateColor(159 / 255, 159 / 255, 159 / 255, 1), -- 滑块未填充色
        RowHover        = CreateColor(50 / 255, 50 / 255, 50 / 255, 1),    -- 行悬停色
        Text            = CreateColor(230 / 255, 230 / 255, 230 / 255, 1), -- 文本颜色
        DropdownBg      = CreateColor(34 / 255, 34 / 255, 34 / 255, 1),    -- 下拉列表背景色
    }
}

--[[
标记位颜色
debug模式下明显，肉眼可辩别
非debug模式下，不明显，但是冷门，方便识别

]]
if DEBUG then
    addonTable.COLOR.MARK = {
        POINT_0 = CreateColor(0, 255 / 255, 0, 1),
        POINT_1 = CreateColor(255 / 255, 0, 0, 1),
    }
else
    addonTable.COLOR.MARK = {
        POINT_0 = CreateColor(15 / 255, 25 / 255, 20 / 255, 1), -- 接近黑色
        POINT_1 = CreateColor(25 / 255, 15 / 255, 20 / 255, 1), -- 接近黑色
    }
end

--[[
框架层级，合理设置层级，确保显示正确。
- 基础为9500
]]


addonTable.FrameLevel = {
    Background = 9500,     -- 底板为9000
    CellBackground = 9510, -- 每个Cell的底板是9510。status_bat和Icon的底板同样
}


--[[
尺寸表，尺寸在游戏启动后下一帧立即计算
]]
addonTable.SIZE = {}                                              -- 尺寸表
local function InitializeSize()                                   -- 初始化尺寸
    local SIZE = addonTable.SIZE
    SIZE.CELL = GetUIScaleFactor(scale * 4)                       -- Cell尺寸
    SIZE.PANEL = {                                                -- 游戏内设置面板尺寸
        MainFrame = {                                             -- 主框体尺寸
            Width = GetUIScaleFactor(400),                        -- 主框体宽度
            Height = GetUIScaleFactor(16) + GetUIScaleFactor(36), -- 主框体单行高度
            Border = GetUIScaleFactor(1),                         -- 主框体边框
            Spacing = GetUIScaleFactor(8),                        -- 内边距/间距
        },                                                        -- MainFrame 结束
        BUTTON = {                                                -- 按钮尺寸
            Width = GetUIScaleFactor(110),                        -- 按钮宽度
            Height = GetUIScaleFactor(36),                        -- 按钮高度
            Border = GetUIScaleFactor(2),                         -- 按钮边框
            IconBorder = GetUIScaleFactor(8),                     -- 图标边框
        },                                                        -- BUTTON 结束
        SETTING_LINE = {                                          -- 设置行尺寸
            Height = GetUIScaleFactor(36),                        -- 行高
            Spacing = GetUIScaleFactor(8),                        -- 行间距
            TitleWidth = GetUIScaleFactor(172),                   -- 标题宽度
            WidgetWidth = GetUIScaleFactor(204),                  -- 控件宽度
            SliderBarHeight = GetUIScaleFactor(6),                -- 滑块条高度
            SliderSquareHeight = GetUIScaleFactor(16),            -- 滑块方块高度
            SliderValueWidth = GetUIScaleFactor(48),              -- 滑块数值区宽度
        }                                                         -- SETTING_LINE 结束
    }
end
insert(UIInitFuncs, InitializeSize)
