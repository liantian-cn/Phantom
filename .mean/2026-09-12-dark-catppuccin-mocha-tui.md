---
plan: .plan/2026-09-12-dark-catppuccin-mocha-tui.md
related_paths:
  - phantom/ui/theme.py
  - phantom/ui/app.tcss
  - phantom/ui/app.py
  - tests/test_ui.py
  - .context/catppuccin-latte.md
  - .context/catppuccin-mocha.md
  - .context/README.md
  - .spec/tui.md
  - .spec/architecture.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .prompt/2026-09-12-dark-catppuccin-mocha-tui.md
---

## 意图 (Intent)

目前UI风格是浅色的，既没有跟随系统，也和catppuccin-Latte不搭配。帮我改成深色的，并修改对应的spec和context文件。

## 约束 (Constraints)

使用 catppuccin/palette 1.8.0 的 Catppuccin Mocha 官方色值，原样转写，不得改写、近似或替换。界面固定深色，不检测系统或终端主题，不新增配置项与切换快捷键。保留原有语义映射：Base 背景、Mantle 容器、Text 正文、Blue 选中与强调、开 Green、关 Peach。主题名、调色板常量与 CSS 变量统一改为 Mocha 命名。Latte context 文件由 Mocha 文件替换，历史保留在 git。同步 `.spec/tui.md`、`.spec/architecture.md`、`.spec/project-overview.md`、`.spec/testing.md` 与 `.context/README.md`，并完成自动化检查与一次 develop 上的原子本地提交。

## 被拒绝的替代方案 (Rejected Alternatives)

不使用 Catppuccin Macchiato 或 Frappé。不通过 COLORFGBG／TEXTUAL_THEME 环境变量或 OSC 11 查询跟随系统深浅色，也不增加手动切换入口。不保留 Latte 与 Mocha 两份 context 文档，也不在本次修改中调整布局、交互、应用配置 schema 或 Lua 侧配色。
