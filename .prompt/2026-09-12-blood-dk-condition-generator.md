# 目标与范围

- **R1**：我要用给定血 DK 示例完成第 7–9 步，初步实现第 10 步，通过实际生成目录验证，不进入游戏，不实现表达式执行、宏绑定或发键。
- **R2**：我要使用职业 DEATHKNIGHT、职业 ID 6、专精索引 1。职业 ID 可省略并推导，填写时必须一致。
- **R3**：我要保留 UUID `550e8400-e29b-41d4-a716-446655440000`、标题“血DK循环”、描述“测试使用。”、四个宏和优先级；修正宏引用为“死神的抚摩”，重复能量溢出规则只保留一条，修正 TOML 注释语法。该游戏名称无需写入规范。

# 插件与数据

- **R4**：我要实现 player_primary_power、spec_dk_rune、spell_charges、spell_overlay、spell_cooldown、player_health_pct、spell_usable 的 @1.0。能量采用 Cell ratio×max_power（本例 120），符文采用 GetRuneCooldown 遍历六个符文并以数量/255 输出灰度，忽略 RUNE_POWER_UPDATE 秘密参数。充能采用 ValueBar ratio×max_charges（本例 2），宽度由上限决定。符文和充能四舍五入为整数。血量返回 0–100 百分比，可用性和高亮返回布尔，冷却使用示例的非线性反算。其他实现参考原有 Lua 示例；能量使用 UnitPowerPercent 颜色曲线和 UNIT_POWER_UPDATE、UNIT_DISPLAYPOWER 玩家事件。
- **R5**：公共冷却改用独立的 spell_gcd@1.0，没有入参，固定查询 61304，固定 ignoreGCD=false，不检查玩家是否学会该技能。普通 spell_cooldown 保留法术书筛选。
- **R6**：每个插件由 Python 类和 Lua 模板组成，负责生成 Lua、声明输出类型与占位，并统一接收 Cell、ValueBar、IconTile 列表解码；一次实例能够产生多个同类区域。我接受保留生命周期并更新解码入参。
- **R7**：能量、符文、充能和血量不可用时返回零，布尔返回 False，冷却返回 375 秒；截图失败或职业专精不匹配时 UI 清空为 —。
- **R8**：程序按条件顺序分类分配位置，每次加载和生成都重新计算；不一致时保存新坐标，保留其他内容和注释。TOML 中的位置只供排错。
- **R9**：每个循环都有隐含 Idle。Idle 不需要宏定义；空条件仅允许位于末尾显式 Idle，没有时在内存中补足。
- **R10**：插件名建议采用 player_、target_、focus_、spell_、spec_ 前缀，不强制。

# 血 DK 示例

- **R11**：八个条件按顺序为符文能量（max_power=120）、符文数量（无参数）、血沸充能（spell_ids=[50841,50842], max_charges=2）、血沸高亮（spell_ids=[50841,50842]）、公共冷却（spell_gcd，无参数）、死神的抚摩冷却（spell_ids=[195292], ignore_gcd=true）、玩家血量百分比（无参数）、灵界打击可用（spell_ids=[49998]）。
- **R12**：四个宏均 bind_key=true：灵界打击 `/cast [@target] 灵界打击` 对应 CTRL-NUMPAD1，血液沸腾 `/cast 血液沸腾` 对应 CTRL-NUMPAD2，死神的抚摩 `/cast 死神的抚摩` 对应 CTRL-NUMPAD3，心脏打击 `/cast 心脏打击` 对应 CTRL-NUMPAD4。顺序规则为血量低于50且灵界打击可用且能量至少40时灵界打击；高亮且充能至少1时血液沸腾；抚摩冷却为0时死神的抚摩；灵界打击可用且能量至少100时灵界打击；符文至少1时心脏打击；最后 Idle。

# 界面与生成

- **R13**：我要在应用配置中指定单份 rotation、Wow.exe 路径和包名，通过现有 TUI 按钮生成，并在循环条件页显示条件名称、插件名称、返回值。生成时重读 rotation，采集期间禁用生成。
- **R14**：输出位置从 `E:\World of Warcraft\_retail_\Wow.exe` 的父目录拼接 Interface\AddOns 得到；插件名默认 Phantom，可通过配置修改。
- **R15**：重复生成直接覆盖同名产物，TOC 只引用本次生成的 Lua，其他旧文件保留。保留源码 examples 文件，但移除 TOC 引用。

# 工程约束

- **R16**：我要把现有 Cell.decimal→ratio 修改及对应测试、规范同步纳入本次提交，历史 plan/prompt 修改保持独立。
- **R17**：Windows 下使用 `E:\Documents\GitHub\wow-ui-source` 作为只读参考，同时更新路径说明。

- **R18**：生成包出现 FontString:SetFont 找不到 `media/UiFont.ttf` 的错误，调用来自 runtime/06_panel.lua；我要修复生成时遗漏共享运行时资源的问题。
