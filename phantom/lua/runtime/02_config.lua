--[[
original: runtime\02_config.lua
uuid: 623444a0-7dad-4fe6-8554-21d6753c6773
runtime_index: 2
摘要：第2个加载的lua，为插件提供config/profile和对应的逻辑。



描述：
    - 第2个加载的lua，为插件提供config/profile和对应的逻辑。


修改记录：
2026-09-06：liantian-cn初始化创建。

]]


--[[  namespace initialization  ]]
local addonName, addonTable = ...

--[[  api cache  ]]
local insert = table.insert
local setmetatable = setmetatable

--[[  variable reference  ]]



--[[  logical code  ]]

_G[addonName .. "Settings"] = _G[addonName .. "Settings"] or {}

local addonSettings = _G[addonName .. "Settings"]

addonSettings.profiles = addonSettings.profiles or {}
addonSettings.profiles["default"] = addonSettings.profiles["default"] or {}
addonSettings.current_profile = addonSettings.current_profile or "default"


local all_configs = {}
local Profile = {}

-- 获取当前profile名称
function Profile.current_profile()
    return addonSettings.current_profile
end

-- 切换profile（不存在则创建, 所有值恢复默认）
function Profile.switch_profile(name)
    -- 如果profile不存在, 创建一个空表
    if not addonSettings.profiles[name] then
        addonSettings.profiles[name] = {}
    end

    -- 切换当前profile
    addonSettings.current_profile = name

    -- 通知所有config回调
    for configIndex = 1, #all_configs do
        local config = all_configs[configIndex]
        config:_notify()
    end
end

-- 内部函数: 注册config对象
function Profile._register_config(config)
    insert(all_configs, config)
end

-- 获取当前profile的数据表（内部使用）
function Profile._get_current_data()
    return addonSettings.profiles[addonSettings.current_profile]
end

-- 缓存所有config对象, 相同key返回同一对象
local config_cache = {}

-- Config对象
local ConfigObj = {}
ConfigObj.__index = ConfigObj

-- 创建新的config对象
function ConfigObj:new(key)
    local obj = {
        key = key,
        default_value = nil,
        callbacks = {}
    }
    setmetatable(obj, self)
    return obj
end

-- 设置默认值
function ConfigObj:set_default(value)
    self.default_value = value
end

-- 获取当前值（优先从profile读取, 没有则返回默认值）
function ConfigObj:get_value()
    local data = Profile._get_current_data()
    if data[self.key] ~= nil then
        return data[self.key]
    end
    return self.default_value
end

-- 设置值（写入当前profile, 触发回调）
function ConfigObj:set_value(value)
    local data = Profile._get_current_data()
    data[self.key] = value
    self:_notify()
end

-- 注册回调函数（值改变或profile切换时触发）
function ConfigObj:register_callback(func)
    insert(self.callbacks, func)
end

-- 内部: 触发所有回调
function ConfigObj:_notify()
    local value = self:get_value()
    for callbackIndex = 1, #self.callbacks do
        local callback = self.callbacks[callbackIndex]
        callback(value)
    end
end

-- 工厂函数: 获取或创建config对象
local function Config(key)
    if not config_cache[key] then
        config_cache[key] = ConfigObj:new(key)
        Profile._register_config(config_cache[key])
    end
    return config_cache[key]
end

addonTable.Config = Config
addonTable.ConfigRows = {}
