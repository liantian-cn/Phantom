# 截图插件开发

## 入口与职责

版本目录内 `capture.py` 必须导出 `Plugin` 类；可用 `Plugin = GDIWorker` 这样的别名公开具体类。
构造接受 `fps=15`，不得在构造或模块导入时启动线程、占用桌面采集资源；加载器会在进入 UI 前检查签名、未启动状态和初始结果。

返回实例遵循 [截图 worker 契约](../.spec/plugin-system.md#截图-worker-契约)，包括只读 `is_running`、`start()`、`stop()`、`set_fps(fps=15)` 和 `get_latest_result()`。
方法名相同不等于业务契约满足，仍需生命周期和图像测试。

可组合 `phantom.core.capture.worker.ThreadCaptureWorker`：版本内后端实现 `CaptureBackend` 的 `desktop_bounds()`、`capture(bounds)`、`close()`，公共 worker 负责定位、校验、FPS、最新结果与停止。
后端在采集线程内创建及关闭；释放资源后恢复该线程的 DPI 上下文。不要复制公共线程或定位算法到插件。

## 配置接入

应用通过 `capture.plugin` 选择精确版本，省略时默认 `gdi@1.0`；加载入口为 `phantom.core.capture.registry.Registry.create(identifier, fps=...)`。
现有配置只读，修改后重启程序生效。不存在的版本或损坏插件明确失败，不换用 GDI。
独立 demo 显式指定 GDI 并使用同一注册器，不读取应用配置。

## Python 说明与验收

文件头及关键步骤应解释平台限制、坐标系、通道转换、缓冲区所有权、资源申请释放和失败结果。
GDI 尤其应说明负坐标虚拟桌面、位图选择/恢复、自顶向下读取、BGRA 到 RGB 转换。

使用合成图像验证定位和裁剪，使用真实 worker 验证启停、重启、错误和最新结果所有权。
注册器测试覆盖默认/显式精确版本、缺失文件、导入错误、非 Plugin 类与接口不完整；Windows smoke 单独验证真实后端调用。
本阶段不要求新增第二种真实后端，也不引入运行期切换。
