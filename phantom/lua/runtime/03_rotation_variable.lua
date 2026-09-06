--[[
original: runtime\03_rotation_variable.lua
uuid: becdc27d-385d-4d99-b757-50c9bc5ff327
runtime_index: 3
摘要：



描述：
    -


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

--[[  variable reference  ]]



--[[  logical code  ]]


addonTable.ENABLE = true -- 是否开启插件


addonTable.BurstTime = GetTime() + 60
addonTable.InBurst = function()
    return addonTable.BurstTime > GetTime()
end
addonTable.BurstRemaining = function()
    return min(60.0, max(0, addonTable.BurstTime - GetTime()))
end
