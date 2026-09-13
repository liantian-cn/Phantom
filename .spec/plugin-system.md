# 插件系统

## 插件标识与解析

插件标识与版本的 Agent 作者约定见 [插件开发手册](../.plugin-development/README.md#版本与变更)。当前标识例如：

- 条件：`liantian_cn.player_health_pct@dev`
- 行为（尚未实现）：`liantian_cn.post_message@dev`
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
- `template.lua` 是该版本条件在游戏内采集和输出数据的模板。

行为插件目录：

```text
phantom/actions/liantian_cn.post_message@dev/
  action.py
```

第一版只规划基于 `ctypes.windll.user32.PostMessageW` 的 `liantian_cn.post_message@dev`。

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
- `CaptureResult` 包含 `image` 和 `status`。图像为独立连续的 RGB `uint8` NumPy 数组，形状 `(height,width,3)`；未定位或底层截图失败时为 `None`。
- 状态固定为 `has_error: bool` 和 `description: str`。有效帧为 `false`、空描述；未定位、多候选、校验失败及底层错误均为 `true`，描述具体原因。
- 尚未启动的空结果为非错误；主动停止不改写最后采集结果。无效区域仍附图，不能作为有效业务输入。
- 主线程取得最新结果的独立快照，不积压历史帧，不共享可被后续截图改写的缓冲区。

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
6. 由 `value()` 调用插件的 `decode_value(cells, value_bars, icon_tiles)` 得到普通 Python 业务值。

## 基类契约

- 基类公开 `raw_value(decoder)`，按冻结的输出描述读取原始区域。
- 基类公开 `value(cells, value_bars, icon_tiles)`，三项均为列表，未使用的类型传空列表，并交给插件实现的 `decode_value(cells, value_bars, icon_tiles)`。
- 每个条件插件必须实现 `decode_value(cells, value_bars, icon_tiles)` 和 `fallback_value()`；任一缺失时，该插件类保持抽象，不能实例化。
- `decode_value(cells, value_bars, icon_tiles)` 抛出任何异常时，`value()` 必须捕获异常并返回 `fallback_value()`。
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

- 行为插件的公共基类接口。
- 行为插件的发现扩展。


## 第 7–10 步条件实现

`phantom/core/condition/` 分别以 contracts.py、base.py、layout.py、template.py 和 registry.py 提供输出契约、生命周期、布局、渲染和精确加载。
通用 Validator 位于 core/validation.py，Decoder 位于 core/condition/decoders.py；核心不含技能参数或冷却业务节点。
每个版本导出 Plugin 类；Registry 只加载精确目录，按标识缓存类，实例不共享。
非法标识、版本缺失、模块或参数错误均附带插件名称；无版本回退和热加载。
output_count 与 value_shape 独立，ValueBar 的 widths 为每条内容宽度，支持单实例多区域。
冻结前验证兜底类型；输入列表数量错误、解码异常或业务类型不符返回已声明兜底。
区域越界由调用层报告，不将整个错误布局伪装为正常业务值。

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

## 截图加载与配置

`phantom/core/capture/` 提供 contracts、worker、imaging 与 registry；`phantom/captures/` 只保存版本插件。
`Registry.create(identifier="liantian_cn.gdi@dev", fps=15)` 返回 CaptureWorker，每次构造独立实例。标识精确匹配、源码限定在版本目录。
配置字段见 [TUI 应用配置](tui.md#应用配置)。非法选择、导入失败或不满足调用接口抛出带标识的 CapturePluginError，入口在进入 UI 前报告并非零退出。
缺省配置采用 GDI；显式配置错误不回退。不提供热切换或热加载。
