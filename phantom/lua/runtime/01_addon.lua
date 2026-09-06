--[[
original: runtime\01_addon.lua
uuid: 20d63786-5c32-4c07-8c5f-c8f0420844a8
runtime_index: 1
摘要：定义插件默认业务配置、公共日志函数与基础运行参数。



描述：
    - 第一个加载的lua，为插件的底层构架。


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After = C_Timer.After
local GetTime = GetTime
local max = math.max
local min = math.min
local print = print
local tostring = tostring
local GetPhysicalScreenSize = GetPhysicalScreenSize
local GetScreenHeight = GetScreenHeight

--[[  logical code  ]]

addonTable.DEBUG = true             -- 是否开启调试模式
addonTable.VERSION = "12.1.0.68209" -- 插件版本

addonTable.logging = function(msg)
    print("|cFFFFBB66[" .. addonName .. "]|r" .. tostring(msg))
end

addonTable.debug = function(msg)
    if addonTable.DEBUG then
        print("|cFFFFBB66[" .. addonName .. "]|r" .. tostring(msg))
    end
end


-- 缩放
if addonTable.DEBUG then
    addonTable.SCALE = 8
else
    addonTable.SCALE = 1
end

--[[  UI设计
为了游戏内的组件高度匹配真实屏幕像素高度。我们需要做2件事
1. 缩放：魔兽世界的默认UI环境是一个假设768高度的画布，内部API创造的宽高都是基于这个画布的，所以这里使用 GetUIScaleFactor 函数实现。
2. 延迟调整，必须在游戏内第二帧创造UI，因为加载过程中存在一次缩放的绘制。在第二帧稳定后，绘图。

]]

addonTable.GetUIScaleFactor = function(pixelValue)
    local physicalHeight = select(2, GetPhysicalScreenSize())
    local UI_scale = UIParent:GetScale()
    return pixelValue * 768 / physicalHeight / UI_scale
end


addonTable.UIInitFuncs = {} -- UI初始化函数表

After(0, function()
    for _, func in ipairs(addonTable.UIInitFuncs) do
        func()
    end
end)



SetCVar("useUiScale", 0)
SetCVar("secretChallengeModeRestrictionsForced", 1)
SetCVar("secretCombatRestrictionsForced", 1)
SetCVar("secretEncounterRestrictionsForced", 1)
SetCVar("secretMapRestrictionsForced", 1)
SetCVar("secretPvPMatchRestrictionsForced", 1)
SetCVar("secretAuraDataRestrictionsForced", 1)
SetCVar("scriptErrors", 1);
SetCVar("doNotFlashLowHealthWarning", 1);
SetCVar("lossOfControl", 0);
SetCVar("cameraIndirectVisibility", 1);
SetCVar("cameraIndirectOffset", 10);
SetCVar("targetNearestDistance", 5)
SetCVar("cameraDistanceMaxZoomFactor", 2.6)
SetCVar("CameraReduceUnexpectedMovement", 1)
SetCVar("synchronizeSettings", 1)
SetCVar("synchronizeConfig", 1)
SetCVar("synchronizeBindings", 1)
SetCVar("synchronizeMacros", 1)
SetCVar("LowLatencyMode", 0)      --低延迟模式 0:关闭 1:内置 2:NVIDIA Reflex 3:NVIDIA Reflex + Boost 4:Intel XeLL
SetCVar("ffxAntiAliasingMode", 0) --基于图像的技术 0:无 1:FXAA低 2:FXAA高 3:CMAA 4:CMAA2
SetCVar("MSAAQuality", 0)         --多重采样技术 0:无 1:色彩 2x / 景深 2x 2:色彩 4x / 景深 4x 3:色彩 8x / 景深 8x
SetCVar("Contrast", 50)           --对比度 minValue, maxValue, step = 0, 100, 1
SetCVar("Brightness", 50)         --亮度 minValue, maxValue, step = 0, 100, 1
SetCVar("Gamma", 1)               --伽马值 minValue, maxValue, step = .3, 2.8, .1
