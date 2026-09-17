# 宏键位语法

## 键位语法

内核在加载 rotation 时解析并校验 `macros.key`，非法键名在任何发送前被拒绝。原字符串仍用于 Lua 绑定和展示。

支持以下主键，标识区分大小写：

- `A`–`Z`、`0`–`9`、`F1`–`F24`、`NUMPAD0`–`NUMPAD9`。
- `NUMPADPLUS`、`NUMPADMINUS`、`NUMPADMULTIPLY`、`NUMPADDIVIDE`、`NUMPADDECIMAL`。
- `UP`、`DOWN`、`LEFT`、`RIGHT`、`HOME`、`END`、`PAGEUP`、`PAGEDOWN`、`INSERT`、`DELETE`。
- `SPACE`、`TAB`、`ENTER`、`ESCAPE`、`BACKSPACE`。
- 标点字面量：逗号、句点、斜杠、分号、单引号、左右方括号、反斜杠、等号、减号、反引号。

主键前可带不重复的 `CTRL-`、`ALT-`、`SHIFT-`，保留声明顺序。减号主键写作 `-`，例如 `CTRL--`。不接受小写、加号分隔、裸修饰键、鼠标按钮或任意未知键名。字符串中反斜杠等字符遵循 TOML 自身转义规则。
