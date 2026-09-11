# 插件系统

## 插件标识与解析

插件标识由小写 `snake_case` 名称、字符 `@` 和精确版本组成，例如：

- 条件：`health_pct@1.0`
- 行为：`post_message@1.0`
- 截图：`gdi@1.0`

标识区分大小写。解析器必须查找精确目录；不得自动降级、升级或回退到相近版本。多个版本可以并存，共享配置继续引用作者已测试的版本。

## 插件目录

条件插件目录：

```text
phantom/conditions/health_pct@1.0/
  condition.py
  template.lua
```

- `condition.py` 定义参数校验、输出描述、Lua 模板参数、解码和兜底。
- `template.lua` 是该版本条件在游戏内采集和输出数据的模板。

行为插件目录：

```text
phantom/actions/post_message@1.0/
  action.py
```

第一版只规划基于 `ctypes.windll.user32.PostMessageW` 的 `post_message@1.0`。

截图插件目录：

```text
phantom/captures/gdi@1.0/
  capture.py
```

第一版只规划基于 `ctypes.windll.gdi32` 位图截图的 `gdi@1.0`。

当前 `gdi@1.0` 使用 `ctypes.WinDLL` 声明 Windows 函数签名，完成独立后端与 demo；通用插件发现和版本解析尚未实现。

## 截图 worker 契约

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

独立 demo 等待 3 秒后开始，采集 5 秒后停止，保存最后结果。每次运行在插件的 `demo_results/` 下创建新目录，
有图时保存 `result.npy`（不使用 pickle），始终保存 UTF-8 `result.txt`，内容为两个状态字段的 JSON 对象。
无图时不生成 NPY，不退回保存历史有效帧；结果目录由 Git 忽略。

## 条件实例生命周期

每次在配置中使用条件插件都会创建独立实例。核心维护 `conditions[title] = instance`。实例必须按以下顺序建立：

1. 校验 `plugin_args`。
2. 根据参数计算 `output_type`、`output_count`、`value_type` 和 `value_shape`。
3. 由布局器分配连续区域并冻结位置与数量。
4. 生成本实例对应的 Lua。
5. 运行时从截图区域读取 `raw_value()`。
6. 由 `value()` 调用插件的 `decode_value(raw)` 得到普通 Python 业务值。

## 基类契约

- 基类公开 `raw_value()`，按冻结的输出描述读取原始区域。
- 基类公开 `value()`，并把原始值交给插件实现的 `decode_value(raw)`。
- 每个条件插件必须实现 `decode_value(raw)` 和 `fallback_value()`；任一缺失时，该插件类保持抽象，不能实例化。
- `decode_value(raw)` 抛出任何异常时，`value()` 必须捕获异常并返回 `fallback_value()`。
- 插件可以在识别到业务不可用状态时主动返回自己的兜底值。
- `value()` 必须始终返回与声明的 `value_type` 和 `value_shape` 相符的值；核心不使用通用 `None` 业务值。

捕获全部解码异常会隐藏部分插件编程错误，这是用户明确接受的行为。插件仍应通过有效测试发现确定性错误。

兜底规则由插件作者按业务含义定义。例如，冷却信息不可读可以解释为“没有冷却”，目标存在性不可读可以解释为“目标不存在”。每个插件都必须把自己的选择写入文档。

## 编解码配对

Lua 编码与 Python 解码属于同一插件版本的配对契约。任何缩放、精度分段、空值表示、多个区域合并或列表过滤都必须两端一致，并随插件版本记录。一个已确认的合法场景是用不同 Cell 亮度区间表示不同精度范围。

## 条件插件文档头

每个条件插件除项目级 Python 文件头外，还必须明确记录：

- 用途和业务语义。
- `plugin_args` 的字段、类型和约束。
- 输出类型、数量、业务类型、形状和物理尺寸。
- 使用的 WoW API 与核验来源。
- Secret Value 风险与安全处理边界。
- 解码算法与兜底规则。
- 插件版本变化。

代码标识符使用英文，业务注释使用中文。所有手写 Python 文件的 Type Hint 要求见 [development-rules.md](development-rules.md)。

## 待定事项

- 各首批条件插件的完整清单、参数与编解码公式。
- 行为插件的公共基类接口。
- 插件发现、缓存和冲突报错的具体实现。
