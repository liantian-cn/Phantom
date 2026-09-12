"""
Summary:
    Flexoki 官方色值与 Phantom 的 Textual 深色主题配置。
Description:
    集中定义 Flexoki 深色方案使用的官方色值，并据此注册界面唯一使用的深色主题。
    主题通过 flexoki-* 变量提供给样式表，语义固定为 black 背景、base-950 容器、
    paper 正文、blue-400 选中与强调。
Key Variables:
    FLEXOKI: Flexoki 官方色值，键为 Phantom 使用的颜色角色名。
    PHANTOM_THEME: 注册到 Textual 的 Phantom 深色主题。
Change Log:
    2026-09-12: Changed 界面配色由 Catppuccin Mocha 改为 Flexoki 深色（纯黑底）。
"""

from textual.theme import Theme

FLEXOKI: dict[str, str] = {
    "base": "#100f0f",
    "mantle": "#1c1b1a",
    "crust": "#282726",
    "surface_0": "#343331",
    "surface_1": "#403e3c",
    "overlay_0": "#575653",
    "overlay_1": "#6f6e69",
    "subtext_0": "#878580",
    "subtext_1": "#b7b5ac",
    "text": "#fffcf0",
    "blue": "#4385be",
    "green": "#879a39",
    "orange": "#da702c",
    "red": "#d14d41",
    "yellow": "#d0a215",
    "cyan": "#3aa99f",
    "purple": "#8b7ec8",
    "magenta": "#ce5d97",
}

PHANTOM_THEME = Theme(
    name="phantom-flexoki",
    primary=FLEXOKI["blue"],
    secondary=FLEXOKI["purple"],
    accent=FLEXOKI["blue"],
    warning=FLEXOKI["orange"],
    error=FLEXOKI["red"],
    success=FLEXOKI["green"],
    foreground=FLEXOKI["text"],
    background=FLEXOKI["base"],
    surface=FLEXOKI["mantle"],
    panel=FLEXOKI["mantle"],
    dark=True,
    variables={
        **{f"flexoki-{name.replace('_', '-')}": color for name, color in FLEXOKI.items()},
        "text": FLEXOKI["text"],
        "text-muted": FLEXOKI["subtext_1"],
        "text-disabled": FLEXOKI["overlay_1"],
        "block-cursor-background": FLEXOKI["blue"],
        "block-cursor-foreground": FLEXOKI["base"],
    },
)
