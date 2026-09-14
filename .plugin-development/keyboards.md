# 键盘插件开发

## 公共职责

入口为 `phantom/keyboards/<完整标识>/keyboard.py`，导出无参 `Plugin` 类；导入和构造不寻找窗口、不发送按键、不启动线程。核心公开契约位于 `phantom/core/keyboard/`。

- `send(keys: KeyCombination) -> None`：同步完成一组明确按键的按下与释放；错误抛出，不自行重发。
- `close() -> None`：释放插件自身资源，可重复调用。下一次手动运行允许再次调用 send，必要资源由后端重新建立。
- `KeyCombination.keys` 为不可变 `tuple[Key, ...]`，修饰键在前，唯一主键在后。
- 不接受宏文本、条件、rotation、HWND 或公共目标配置；不在插件内解释 WoW 键位字符串。
- 设备编码、按住时长和目标属于后端。内核串行调用 send，停止时等待当前组合释放后再 close，不并行调用同一实例。

## 键位语法

内核在加载 rotation 时解析并校验 `macros.key`，非法键名在任何发送前被拒绝。原字符串仍用于 Lua 绑定和展示。

支持以下主键，标识区分大小写：

- `A`–`Z`、`0`–`9`、`F1`–`F24`、`NUMPAD0`–`NUMPAD9`。
- `NUMPADPLUS`、`NUMPADMINUS`、`NUMPADMULTIPLY`、`NUMPADDIVIDE`、`NUMPADDECIMAL`。
- `UP`、`DOWN`、`LEFT`、`RIGHT`、`HOME`、`END`、`PAGEUP`、`PAGEDOWN`、`INSERT`、`DELETE`。
- `SPACE`、`TAB`、`ENTER`、`ESCAPE`、`BACKSPACE`。
- 标点字面量：逗号、句点、斜杠、分号、单引号、左右方括号、反斜杠、等号、减号、反引号。

主键前可带不重复的 `CTRL-`、`ALT-`、`SHIFT-`，保留声明顺序。减号主键写作 `-`，例如 `CTRL--`。不接受小写、加号分隔、裸修饰键、鼠标按钮或任意未知键名。字符串中反斜杠等字符遵循 TOML 自身转义规则。

## PostMessageW 首版

`liantian_cn.post_message@dev` 每次 send 枚举窗口，要求恰好一个窗口标题精确等于“魔兽世界”。目标在本次组合内保持一致，不查进程名称，不激活窗口，不控制其他插件的目标。零匹配或多匹配抛错。

沿用用户指定的 [keyboard.py](https://raw.githubusercontent.com/liantian-cn/EZWowX2/refs/heads/main/Terminal/terminal/keyboard.py)：以 `WM_KEYDOWN` 依次按下，等待 10 ms，逆序用 `WM_KEYUP` 释放，`lParam` 固定为 0。这是当前游戏接收端参考约定，不宣称适用于所有 Windows 应用；ALT 也沿用此消息路线。

ctypes 声明完整的指针宽度和调用签名，检查 PostMessageW 返回值。中途出错仍尝试释放已成功按下的所有键，保留原始错误与后续释放错误。消息入队不等于目标已经执行，也不验证施法结果。当前后端不自动提权、切换目标或重试失败组合。

Windows 键码依据 [Virtual-Key Codes](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)；消息错误语义依据 [PostMessageW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postmessagew)。平台中立的 Key 不使用 Windows 数值，转换表归本插件所有。

## 验证

验证合法/非法键位、精确版本和加载失败、完整消息顺序、部分失败释放、窗口标题唯一性。Windows 集成仅向测试自行创建的隐藏窗口发送，验证真实消息队列；不要向实际游戏发送测试按键。真实游戏普通键、组合键和闭环另行验收。

新增版本入口必须加入完整 mypy 检查；`plugin.toml` 为作者自述，不参与运行时加载。
