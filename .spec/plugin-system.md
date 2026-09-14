# 插件系统

## 插件标识与解析

插件标识与版本的 Agent 作者约定见 [插件开发手册](../.plugin-development/README.md#版本与变更)。当前标识例如：

- 条件：`liantian_cn.player_health_pct@dev`
- 键盘：`liantian_cn.post_message@dev`
- 截图：`liantian_cn.gdi@dev`

解析器以完整标识查找精确目录，不校验作者名、包名或版本格式，不自动改名、降级、升级或回退到相近版本。多个版本可以并存，共享配置继续引用作者已测试的版本。
标识必须是单个安全目录名，禁止绝对路径、目录穿越和 Windows 路径别名；目录及源码、模板不得逃逸各自根目录。文件定位沿用宿主文件系统语义。

## 插件目录

条件插件目录：

```text
phantom/conditions/liantian_cn.player_health_pct@dev/
  condition.py
  template.lua
  plugin.toml
```

- `condition.py` 定义参数校验、输出描述、Lua 模板参数、解码和兜底。
- `template.lua` 是可选的游戏内采集和输出模板；缺失时生成空的实例 `do/end` 块，存在时仍检查模板路径与渲染错误。

键盘插件目录：

```text
phantom/keyboards/liantian_cn.post_message@dev/
  keyboard.py
  plugin.toml
```

首版 `liantian_cn.post_message@dev` 使用显式 ctypes Windows 签名调用 PostMessageW。契约见下方“键盘加载与发送”。

截图插件目录：

```text
phantom/captures/liantian_cn.gdi@dev/
  capture.py
  plugin.toml
```

第一版只规划基于 `ctypes.windll.gdi32` 位图截图的 `liantian_cn.gdi@dev`。

当前 `liantian_cn.gdi@dev` 使用 `ctypes.WinDLL` 声明 Windows 函数签名，完成独立后端与 demo；已通过 core/capture/registry.py 接入精确版本加载，统一导出 Plugin。

## 截图 worker 契约

- worker 提供只读 `is_running: bool`，构造后未运行；初始快照为 `CaptureResult()`。
- worker 实例化接受 `fps=15`，提供 `start()`、`stop()`、`set_fps(fps=15)`、`get_latest_result()`。
- FPS 必须为有限正数，允许运行中修改；GDI 实际应用上限，其他未来后端保留接口但可以不生效。
- 重复 `start()` 不创建重复线程；`stop()` 唤醒等待并等待资源释放，重复停止无副作用。重新启动清除旧结果并重新定位。
- `CaptureResult` 包含 `image`、`status` 和 `sequence`。图像为独立连续的 RGB `uint8` NumPy 数组，形状 `(height,width,3)`；未定位或底层截图失败时为 `None`。
- 状态固定为 `has_error: bool` 和 `description: str`。有效帧为 `false`、空描述；未定位、多候选、校验失败及底层错误均为 `true`，描述具体原因。
- 尚未启动的空结果为非错误；主动停止不改写最后采集结果。无效区域仍附图，不能作为有效业务输入。
- 主线程取得最新结果的独立快照，不积压历史帧，不共享可被后续截图改写的缓冲区。
- `sequence: int | None` 默认 None，表示尚无帧身份；纯解码及独立 demo 可使用无序号结果。持续执行要求有效图像带正整数序号，每次发布递增，重复读取保持原值；内容相同的新截图也递增。公共 worker 计数跨重启延续，初始空结果仍为 None。缺失、非法或倒退序号使执行暂停，不猜测图像是否为新帧。

GDI worker 搜索整个虚拟桌面，包含负坐标显示器，按物理像素坐标截图。定位成功后仅截取完整基板区域。
角标或尺寸失效时下一轮重新全屏搜索；角标有效但校验色错误时保持局部截图。定位与校验规则见像素协议。
搜索和区域截图均受 FPS 上限约束，处理耗时计入周期，不补跑积压帧；停止和 FPS 更新可以唤醒等待。
底层截图异常发布错误并结束本次运行、释放资源，后续可显式重新启动。

独立 `demo/demo.py` 先打印演示内容，等待 3 秒后开始，采集 5 秒后停止，保存最后结果。每次运行在项目根目录的 `demo/demo_results/` 下创建新目录，
有图时保存 `result.npy`（不使用 pickle），始终保存 UTF-8 `result.txt`，内容为两个状态字段的 JSON 对象。
无图时不生成 NPY，不退回保存历史有效帧；结果目录由 Git 忽略。

## 条件实例生命周期

每次在配置中使用条件插件都会创建独立实例。核心维护 `conditions[title] = instance`。实例必须按以下顺序建立：

1. 校验 `plugin_args`。
2. 根据参数计算 `output_type`、`output_count`、`value_type` 和 `value_shape`。
3. 由布局器分配连续区域并冻结位置与数量。
4. 生成本实例对应的 Lua。
5. 运行时从截图区域读取 `raw_value(decoder)`。
6. 由 `value(cells, value_bars, icon_tiles, *, decoder)` 调用同签名的插件 `decode_value`，得到普通 Python 业务值。

不新增区域的插件声明 `output_type="none"`、`output_count=0`，无 widths，冻结后 regions 为空。冻结状态独立记录，零区域也只能冻结一次。Lua 模板是否存在与是否分配区域互相独立；无输出插件仍声明业务类型、形状与兜底。

## 基类契约

- 基类公开 `raw_value(decoder)`，按冻结的输出描述读取原始区域。
- 基类公开 `value(cells, value_bars, icon_tiles, *, decoder)`，前三项均为列表，未使用的类型传空列表，并交给插件实现的同签名 `decode_value`。
- `decoder: PixelDecoder` 为必填关键字参数，所有实例收到本轮 rotation 使用的同一个解码器；插件可按公开坐标接口读取任意有效区域，不得修改帧数据或持有解码器供以后帧使用。
- 每个条件插件必须实现 `decode_value` 和 `fallback_value()`；任一缺失时，该插件类保持抽象，不能实例化。现有 `@dev` 插件统一迁移，不保留旧签名兼容层。
- `decode_value` 中的额外读取或业务解码抛出任何异常时，`value()` 必须捕获异常并返回 `fallback_value()`。
- 插件可以在识别到业务不可用状态时主动返回自己的兜底值。
- `value()` 必须始终返回与声明的 `value_type` 和 `value_shape` 相符的值；核心不使用通用 `None` 业务值。

捕获全部解码异常会隐藏部分插件编程错误，这是用户明确接受的行为。插件仍应通过有效测试发现确定性错误。

兜底规则由插件作者按业务含义定义。例如，冷却信息不可读可以解释为“没有冷却”，目标存在性不可读可以解释为“目标不存在”。作者说明要求见 [条件插件手册](../.plugin-development/conditions.md)。

## 编解码配对

配对协议的作者要求统一见 [条件插件手册](../.plugin-development/conditions.md#配对与说明)；本页下表记录当前八个版本的业务输出。

## 插件作者要求

目录依赖、对象组合、模板头部变量、注释和开发步骤统一维护在 [插件开发手册](../.plugin-development/README.md)。
条件专属文档头见 [条件插件](../.plugin-development/conditions.md#配对与说明)。

## 待定事项

无。新增后端和运行期热切换不属于当前范围。


## 第 7–10 步条件实现

`phantom/core/condition/` 分别以 contracts.py、base.py、layout.py、template.py 和 registry.py 提供输出契约、生命周期、布局、渲染和精确加载。
通用 Validator 位于 core/validation.py；条件插件在 decode_value 中直接读取 core/pixels 的区域对象并完成业务校验与转换，具体作者要求见插件开发手册。核心不含技能参数或冷却业务节点。
每个版本导出 Plugin 类；Registry 只加载精确目录，按标识缓存类，实例不共享。
非法标识、版本缺失、模块或参数错误均附带插件名称；无版本回退和热加载。
output_count 与 value_shape 独立，ValueBar 的 widths 为每条内容宽度，支持单实例多区域。
冻结前验证兜底类型；输入列表数量错误、解码异常或业务类型不符返回已声明兜底。
框架分配区域的越界由调用层报告，不将整个错误布局伪装为正常业务值；插件通过 decoder 主动额外读取的异常在插件解码兜底边界内处理。

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

所有插件独立注册 PLAYER_ENTERING_WORLD。旧插件已有的两秒轮询保留，施法进度使用 0.1 秒；每个实例以 `-random()` 错峰，严格超过间隔时扣除一个间隔，保留余量，每帧最多刷新一次。
移动事件通过 `C_Timer.After(0, callback)` 在后续帧查询；技能/天赋沿用可取消的 0.25 秒延迟刷新。支持单位过滤的旧事件只注册 player。
AuraContainer 在世界事件调用公开的 UpdateAllAuras，平时由官方容器管理更新，不自行轮询或检查 AuraData/可见性。

光环沿用固定 AuraSlot 白色覆盖黑底；指定增益由 includeSpellIDs 筛选，大防御使用 BigDefensive/Normal 排序。
驱散过滤为 `HARMFUL|RAID_PLAYER_DISPELLABLE` 加 includeDispelTypes，同时要求当前玩家可驱散与类型匹配。
吸收量直接传入白色 StatusBar，最小 N、最大 N+1，Lua 不比较秘密吸收量。

施法目标完整保留旧项目按名称匹配、秘密目标暂留旧值、成功/停止/失败清空和每两秒清空行为，因此长施法也可能提前变为空字符串。
三种物品就绪条件使用 enabled、零冷却、usable 且 not noMana，不增加背包数量检查。
技能/天赋只判断 IsSpellKnown 或 IsSpellInSpellBook，不解析天赋树；后者可包含覆盖技能，不保证技能此刻可施放。

## 截图加载与配置

`phantom/core/capture/` 提供 contracts、worker、imaging 与 registry；`phantom/captures/` 只保存版本插件。
`Registry.create(identifier="liantian_cn.gdi@dev", fps=15)` 返回 CaptureWorker，每次构造独立实例。标识精确匹配、源码限定在版本目录。
配置字段见 [TUI 应用配置](tui.md#应用配置)。非法选择、导入失败或不满足调用接口抛出带标识的 CapturePluginError，入口在进入 UI 前报告并非零退出。
缺省配置采用 GDI；显式配置错误不回退。不提供热切换或热加载。

## 键盘加载与发送

`core/keyboard/registry.py` 按 `keyboard.plugin` 加载精确版本，默认 `liantian_cn.post_message@dev`。每次 create 返回独立实例，按实际源码路径隔离模块；目录穿越、逃逸、版本缺失、导入失败或接口错误均抛带标识的 KeyboardPluginError，主入口在进入 UI 前报告。

`send(KeyCombination)` 与 `close()` 是公共接口。内核负责宏和键位字符串解析；后端负责明确按键的设备转换和目标选择，不接收宏、rotation 或公共 HWND。详见[键盘作者契约](../.plugin-development/keyboards.md)。当前不热加载、不回退，不增加第二种真实发送后端。
