# 内置条件目录

用于筛选已有条件和查阅当前业务契约；确定具体参数、输出和限制时，再读取 `phantom/conditions/<完整标识>/plugin.toml` 与该版本实现。修改现有条件时同步维护对应条目。

## 基础条件

| 插件（统一为 liantian_cn.名称@dev） | 参数 | 输出与解码 | 兜底 |
| --- | --- | --- | --- |
| player_primary_power | 有限正数 max_power | Cell ratio × max_power，float | 0.0 |
| spec_dk_rune | 无 | Cell mean 四舍五入，0–6 int | 0 |
| spell_charges | spell_ids、正整数 max_charges | ValueBar 宽=max_charges，ratio×上限四舍五入 | 0 |
| spell_overlay | spell_ids | Cell 严格黑白 bool | False |
| spell_usable | spell_ids | Cell 严格黑白 bool | False |
| player_health_pct | 无 | Cell percent，预测生命百分比 float | 0.0 |
| spell_cooldown | spell_ids、布尔 ignore_gcd | Cell 分段剩余秒数 float | 375.0 |
| spell_gcd | 无 | Cell 分段剩余秒数 float | 375.0 |

spell_ids 是非空正整数列表，普通法术取首个法术书匹配候选。
spell_gcd 固定 GetSpellCooldownDuration(61304,false)，不查询法术书，不接受技能或 ignore_gcd 参数。
无参插件可省略 plugin_args 或传空表，其他参数一律拒绝。前缀 player_/target_/focus_/spell_/spec_ 仅为建议。
冷却亮度 255/155/105/55/0 对应 0/5/30/155/375 秒，区间内线性反算；黑色同时表示饱和或无 duration。
灰度 Cell 必须纯灰，布尔必须纯黑/白；整数采用非负数四舍五入而非银行家舍入。
能量与血量直接把曲线返回颜色交给渲染，充能直接传秘密 currentCharges；符文仅统计非秘密 runeReady，不读取秘密事件参数。
事件与节流沿用对应模板；GCD 与普通冷却均独立随机错峰、严格超过 0.1 秒轮询。

## 通用状态读取插件

现有 Lua 状态、聊天命令、面板与第一行五个 Cell 保留。以下三个无参数条件插件没有 Lua、不分配新区域，仅在配置声明时实例化；条件标题完全由配置决定，不形成隐式执行门控。

| 插件 | 读取坐标 | 类型 | 非黑白值或解码异常兜底 |
| --- | --- | --- | --- |
| `liantian_cn.enable@dev` | Cell(3, 1) | bool | True |
| `liantian_cn.in_burst@dev` | Cell(4, 1) | bool | False |
| `liantian_cn.delaying@dev` | Cell(5, 1) | bool | False |

兜底后继续求值；enable 与 delay 的上述兜底允许配置规则继续执行动作，这是已确认的业务语义。

## 玩家条件插件（2026-09-15）

以下 23 个插件统一使用 `liantian_cn.<名称>@dev`。每个实例输出一个 scalar：除施法图标使用第四行一个 IconTile 外，其余均占第二行一个 Cell 区域。
AuraContainer 和吸收 StatusBar 是该区域的显示实现，不另分配 ValueBar，不改变核心像素协议。

| 名称 | 必填参数 | Python 返回与业务含义 |
| --- | --- | --- |
| player_role | 无 | str：TANK、HEALER、DAMAGER、NONE |
| player_in_combat | 无 | bool：玩家处于战斗 |
| player_is_player_target | 无 | bool：玩家当前目标是自己 |
| player_is_moving | 无 | bool：玩家正在移动 |
| player_in_vehicle | 无 | bool：玩家处于载具或坐骑状态 |
| player_melee_enemies_count | spell_id | int：nameplate1–40 中可攻击且在指定技能范围内的数量 |
| player_is_targeting_spell | 无 | bool：正在选择法术目标 |
| player_is_chatting | 无 | bool：任意键盘输入焦点存在，包含非聊天输入框 |
| player_in_group | 无 | bool：在队伍或团队中 |
| player_trinket_ready | slot_id | bool：13 或 14 位置的饰品冷却结束且可用 |
| player_healthstone_ready | 无 | bool：固定物品 224464 冷却结束且可用 |
| player_heal_potion_ready | 无 | bool：固定物品 258138 冷却结束且可用 |
| player_cast_progress | 无 | float：施法或通道已进行的百分比，0–100，空闲为 0.0 |
| player_is_empowering | 无 | bool：玩家正在蓄力通道 |
| player_cast_icon | 无 | str：IconTile 内部图像 hash；空槽为空字符串 |
| player_cast_target | 无 | str：player、party1–4、raid1–40；未知为空字符串 |
| player_has_big_defensive | 无 | bool：存在 HELPFUL\|BIG_DEFENSIVE 光环 |
| player_has_dispellable_debuff | dispel_types | bool：存在玩家可驱散且类型匹配的减益 |
| player_has_spell | spell_ids | bool：任一技能已知或在玩家法术书中 |
| player_has_talent | spell_ids | bool：与 player_has_spell 完全相同，按技能 ID 判断 |
| player_damage_absorb | threshold | bool：伤害吸收量严格超过阈值 |
| player_heal_absorb | threshold | bool：治疗吸收量严格超过阈值 |
| player_has_buff | buff_ids | bool：任一指定 HELPFUL 增益存在 |

参数约束：`spell_id` 为正整数；`spell_ids`、`buff_ids` 为非空正整数列表；`slot_id` 只接受 13/14。
`threshold` 为 0–9007199254740990 的整数，保证 Lua 数值中的 N 和 N+1 可精确区分；拒绝布尔值、小数和负数。
`dispel_types` 为必填 bool 映射，键限定 Magic、Poison、Disease、Curse、Stealth、Special、Enrage；未列出为 false，空表和全 false 均不匹配。
所有插件拒绝多余字段，参数名称统一使用 snake_case。

布尔值必须严格全黑/全白，异常兜底 False。职责灰度字节 0/85/170/255 分别表示 NONE/TANK/HEALER/DAMAGER，其他值或秘密职责返回 NONE。
近战计数灰度为 count/40，Python 用非负数四舍五入恢复；秘密或 nil 的距离结果不计数。进度通过黑白颜色曲线求值后直接渲染，Python 读取 Cell.percent。
计数和进度的异常兜底分别为 0、0.0。施法目标编码 0=未知、1=player、2–5=party、6–45=raid，乘 5 后作为灰度字节；非法编码兜底空字符串。
图标直接读取 IconTile.hash，把底层空槽 None 转成空字符串，解码异常同样为空字符串。

本节的玩家 Lua 插件独立注册 PLAYER_ENTERING_WORLD；统一刷新写法见 [条件插件](conditions.md#刷新写法)。支持单位过滤的旧事件只注册 player。
AuraContainer 在世界事件调用公开的 UpdateAllAuras，平时由官方容器管理更新，不自行轮询或检查 AuraData/可见性。

光环沿用固定 AuraSlot 白色覆盖黑底；指定增益由 includeSpellIDs 筛选，大防御使用 BigDefensive/Normal 排序。
驱散过滤为 `HARMFUL|RAID_PLAYER_DISPELLABLE` 加 includeDispelTypes，同时要求当前玩家可驱散与类型匹配。
吸收量直接传入白色 StatusBar，最小 N、最大 N+1，Lua 不比较秘密吸收量。

施法目标完整保留旧项目按名称匹配、秘密目标暂留旧值、成功/停止/失败清空和每秒兜底清空行为，因此长施法也可能提前变为空字符串。
三种物品就绪条件使用 enabled、零冷却、usable 且 not noMana，不增加背包数量检查。
技能/天赋只判断 IsSpellKnown 或 IsSpellInSpellBook，不解析天赋树；后者可包含覆盖技能，不保证技能此刻可施放。
