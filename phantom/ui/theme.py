"""
Summary:
    用户提供的 Catppuccin Mocha 色值与 Phantom 的 Textual 深色主题配置。
Description:
    集中定义 Mocha 全套官方色值，并据此注册界面唯一使用的深色主题。
    主题通过 mocha-* 变量提供给样式表，语义固定为 Base 背景、Mantle 容器、
    Text 正文、Blue 选中与强调。
Key Variables:
    MOCHA: Catppuccin Mocha 官方色值，键为色名。
    PHANTOM_THEME: 注册到 Textual 的 Phantom 深色主题。
Change Log:
    2026-09-12: Changed 界面配色由 Catppuccin Latte 改为 Catppuccin Mocha 深色。
"""

from textual.theme import Theme

MOCHA: dict[str, str] = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext_1": "#bac2de",
    "subtext_0": "#a6adc8",
    "overlay_2": "#9399b2",
    "overlay_1": "#7f849c",
    "overlay_0": "#6c7086",
    "surface_2": "#585b70",
    "surface_1": "#45475a",
    "surface_0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}

PHANTOM_THEME = Theme(
    name="phantom-mocha",
    primary=MOCHA["blue"],
    secondary=MOCHA["mauve"],
    accent=MOCHA["blue"],
    warning=MOCHA["peach"],
    error=MOCHA["red"],
    success=MOCHA["green"],
    foreground=MOCHA["text"],
    background=MOCHA["base"],
    surface=MOCHA["mantle"],
    panel=MOCHA["mantle"],
    dark=True,
    variables={
        **{f"mocha-{name.replace('_', '-')}": color for name, color in MOCHA.items()},
        "text": MOCHA["text"],
        "text-muted": MOCHA["subtext_1"],
        "text-disabled": MOCHA["overlay_1"],
        "block-cursor-background": MOCHA["blue"],
        "block-cursor-foreground": MOCHA["base"],
    },
)
