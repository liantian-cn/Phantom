# Phantom 项目 Skills 整理需求

## 技能与归属

1. **R1**：我要将 Phantom 的项目指引和相关文档整理为可复用的 skills。
2. **R2**：至少包含 phantom-code-dev（项目代码开发）、phantom-plugin-dev（插件开发）、phantom-rotation-dev（循环开发）；额外需要由 Agent 判断并补充。
3. **R3**：我要将 skills 放在项目 .agents/skills/，随项目管理。

## 文档与职责

4. **R4**：我要将相关文档迁入 references，精简重复内容、分离历史记录、保留有效约束和核验来源，并移除旧入口、修复当前引用。
5. **R5**：循环 skill 负责 TOML 配置、条件组合、宏键位和战斗优先级；需要新插件或引擎修改时由相应开发 skill 负责。
6. **R6**：我要大幅简化项目根 AGENTS.md，通过按需读取降低未来提示词占用。

## 实施

7. **R7**：我批准实施已提出的完整计划，包括补充 phantom-wow-api、迁移验证和一个原子本地提交，不推送。
