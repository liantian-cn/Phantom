# Primary

~~~~text
这个项目，有些基础的lua，就是让条件插件得以运行的基础lua。放置在什么目录好呢？帮我设计。新建目录。
~~~~

# Question

~~~~text
❓ **Q1 — 目录命名**：共享基础 Lua 放在哪里？

1. **`phantom/lua/runtime/`（Recommended）**：表示供生成插件使用的游戏内共享运行时源码，职责最明确。
2. **`phantom/lua/base/`**：更贴近“基础 Lua”的说法，但 `base` 的长期职责容易变模糊。
3. **`phantom/lua/templates/`**：强调生成素材，但容易与条件插件的 `template.lua` 混淆。

➡️ 推荐选择：**1**

---

❓ **Q2 — 规范同步**：是否同时更新 `.spec/architecture.md`？

1. **更新架构规范（Recommended）**：把新目录及其职责写入预定源码结构，同时保留“最终 Lua 文件拆分”这一待定事项。
2. **只创建目录**：暂不形成规范约束，目录用途只能从本次归档理解。

➡️ 推荐选择：**1**
~~~~

~~~~text
都按推荐来。
~~~~

~~~~text
最终共享理解：

- 新建 `phantom/lua/runtime/`
- 使用空的 `phantom/lua/runtime/.gitkeep` 占位
- 更新 `.spec/architecture.md`：
  - 将 `phantom/lua/runtime/` 加入预定源码结构
  - 明确它保存生成器使用、并进入生成后 WoW 插件的共享 Lua 运行时源码
  - 明确它不保存条件专属模板；条件模板仍位于 `phantom/conditions/<name>@<version>/template.lua`
- 保留“共享基础模块最终拆成哪些 Lua 文件”为待定事项
- 不新增 Lua、Python、具体插件或生成产物
- 不纳入现有 `.gitignore`、`LICENSE`、`README.md` 修改
- 验证后创建一个原子本地提交，不推送

❓ **Q3 — 最终确认**

1. **确认并授权实施（Recommended）**
2. **修改计划**

➡️ 推荐选择：**1**
~~~~

~~~~text
1
~~~~
