--[[
original: runtime\03_rotation_variable.lua
uuid: becdc27d-385d-4d99-b757-50c9bc5ff327
runtime_index: 3
摘要：
    初始化插件启用状态与爆发计时，并提供共享的爆发状态查询。


描述：
    - 默认启用插件，并在本文件加载时将共享爆发截止时间设为当前时间的 60 秒后。
    - 根据共享截止时间查询是否仍处于爆发期，并将剩余秒数限制在 0 至 60 秒之间。
    - 查询时读取 addonTable 中的最新截止时间，使其他文件对爆发时间的修改即时生效。


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]

local addonName, addonTable = ...

--[[  api cache  ]]

local After = C_Timer.After -- 延迟指定秒数执行回调
local GetTime = GetTime -- 获取当前计时值，用于计算爆发截止时间和剩余秒数
local max = math.max -- 取较大值，将爆发剩余秒数下限限制为 0
local min = math.min -- 取较小值，将爆发剩余秒数上限限制为 60
local print = print -- 输出调试或提示信息
local tostring = tostring -- 将值转换为字符串
local GetPhysicalScreenSize = GetPhysicalScreenSize -- 获取屏幕的物理宽度与高度
local GetScreenHeight = GetScreenHeight -- 获取屏幕高度

--[[  variable reference  ]]



--[[  logical code  ]]


addonTable.ENABLE = true -- 是否开启插件


addonTable.BurstTime = GetTime() + 60 -- 初始化共享爆发截止时间，默认从加载时起持续 60 秒
addonTable.InBurst = function() -- 供其他文件查询当前是否处于爆发期
    return addonTable.BurstTime > GetTime() -- 截止时间晚于当前时间时仍处于爆发期
end
addonTable.BurstRemaining = function() -- 供其他文件查询爆发剩余秒数
    return min(60.0, max(0, addonTable.BurstTime - GetTime())) -- 实时读取共享截止时间，将剩余秒数限制在 0 至 60 秒之间
end
