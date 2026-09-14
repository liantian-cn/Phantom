---
plan: .plan/2026-09-14-keyboard-rotation-runtime.md
related_paths:
  - .context/security-api.md
  - .plugin-development/README.md
  - .plugin-development/captures.md
  - .plugin-development/keyboards.md
  - .prompt/2026-09-14-keyboard-rotation-runtime.md
  - .spec/README.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/plugin-system.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .spec/tui.md
  - phantom.toml
  - phantom/core/capture/contracts.py
  - phantom/core/capture/worker.py
  - phantom/core/configuration.py
  - phantom/core/generator.py
  - phantom/core/keyboard/__init__.py
  - phantom/core/keyboard/contracts.py
  - phantom/core/keyboard/registry.py
  - phantom/core/rotation.py
  - phantom/core/runtime.py
  - phantom/keyboards/liantian_cn.post_message@dev/keyboard.py
  - phantom/keyboards/liantian_cn.post_message@dev/plugin.toml
  - phantom/main.py
  - phantom/ui/app.py
  - pyproject.toml
  - rotations/blood-dk.toml
  - scripts/check_types.py
  - tests/lua/conditions_harness.lua
  - tests/test_capture.py
  - tests/test_expression.py
  - tests/test_generator.py
  - tests/test_keyboard.py
  - tests/test_rotation.py
  - tests/test_runtime.py
  - tests/test_ui.py
  - todo_list.md
---

## 意图 (Intent)

帮我完成todo_list的第14-16步。采用 keyboards；直接插件化；实现并离线验收，真实游戏闭环保留待验。Implement the plan.

phantom内核决定发送什么按键；插件只负责发送按键，不负责解释宏。不同插件，不同的目标；驱动模拟没有目标。PostMessageW 内部写死标题精确匹配“魔兽世界”。按用户提供的 keyboard.py 与 Macro.lua 标准示例实现。

新帧驱动；现有启动即运行。插件启用、爆发开启、正在延迟放进表达式，采用中文名称，示例增加未启用或正在延迟时匹配 Idle 的规则。Sleep Pass未来作为Idle的别名，都是跳过当前循环一次。首版支持常用键盘键。

## 约束 (Constraints)

当前没有测试环境；实现并离线验收，不能宣称真实游戏通过。找不到目标、发送失败、执行异常暂停并手动重启。只在 develop 实施并按工作流本地提交。

## 被拒绝的替代方案 (Rejected Alternatives)

用户明确纠正公共层统一确定目标窗口的方案：不同插件目标不同，驱动模拟没有目标。用户纠正按键发送前附加全局启用/延迟门控的方案：由 rotation 表达式匹配宏决定发送。Sleep/Pass 不作为可省略 key 的普通宏，而是未来的 Idle 别名。
