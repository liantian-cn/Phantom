---
plan: .plan/2026-09-11-python-capture-foundation.md
related_paths:
  - .gitignore
  - .python-version
  - pyproject.toml
  - requirements.txt
  - requirements-dev.txt
  - phantom/__init__.py
  - phantom/captures/__init__.py
  - phantom/captures/contracts.py
  - phantom/captures/imaging.py
  - phantom/captures/worker.py
  - phantom/captures/gdi@1.0/capture.py
  - phantom/captures/gdi@1.0/demo.py
  - rotations/__init__.py
  - rotations/main.py
  - tests/test_capture.py
  - tests/test_capture_demo.py
  - .spec/architecture.md
  - .spec/development-rules.md
  - .spec/pixel-protocol.md
  - .spec/plugin-system.md
  - .spec/project-overview.md
  - .spec/testing.md
  - todo_list.md
---

# 意图 (Intent)

Python 3.13，使用 pip；python -m rotations.main 是未来 Textual 入口，本次只建立框架。截图插件单独用 demo.py 启动，独立后台线程，捕获整个虚拟桌面。默认 fps=15，标准设置接口支持运行中调用，未来后端可以不生效。

demo 启动 3 秒后 start，再过 5 秒 stop；保存最后结果为 NPY，状态写 result.txt，每次独立目录。状态固定 has_error 布尔值和 description 文本。只保留最新结果，附无效图。角标丢失重定位，色错保留区域。GDI 异常报告后结束本次运行。

# 约束 (Constraints)

只做图像输入和业务流程测试，不做简单字符串或算术测试。定位和中心 2×2 校验采用精确 RGB，多基板视为歧义。未定位也是错误，主动停止保留结果。采用 requirements 文件、pytest、mypy、Ruff。保持 debug=true，但是我现在在工作，没办法玩游戏。就先随便测测吧。

# 被拒绝的替代方案 (Rejected Alternatives)

本次不连接主程序和截图，不实现主程序控制界面；截图运行在后台线程，不使用子进程。demo 不使用交互命令或图形窗口，采用固定时序。默认 FPS 不采用 10 或 30，采用 15 并支持运行中设置。
