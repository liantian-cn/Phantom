# target / focus 条件实施与验收清单

## 1. 已确认范围与状态

用户已完成需求确认并授权实施；本清单替代原来的“只盘点、不实施”和暂定参数文字。实施日期：2026-09-18，分支 `develop`。既有未提交／未跟踪工作保留，不提交 Git，不运行游戏入口。

### 16 个目标／焦点条件

| 状态 | 目标插件 | 焦点插件 | 已实现契约 |
| --- | --- | --- | --- |
| [x] | target_is_exists@dev | focus_is_exists@dev | UnitExists，bool，无参数，不存在 False |
| [x] | target_is_alive@dev | focus_is_alive@dev | 存在且非死亡／灵魂，bool，无参数 |
| [x] | target_can_attack@dev | focus_can_attack@dev | 存在且 UnitCanAttack(player, unit)，与 UnitIsEnemy 严格区分 |
| [x] | target_in_combat@dev | focus_in_combat@dev | 存在且 UnitAffectingCombat；不表示正与玩家交战 |
| [x] | target_cast_progress@dev | focus_cast_progress@dev | 已完成 0–100 float，空闲／失败 0.0，无参数 |
| [x] | target_cast_interruptible@dev | focus_cast_interruptible@dev | 有施法／引导且可中断才 True，普通 nil 保守 False，无参数 |
| [x] | target_cast_icon@dev | focus_cast_icon@dev | 一个 IconTile 的 hash str，空槽／解码异常空字符串；单位消失或无施法时清空，无参数 |
| [x] | target_has_dispellable_buff@dev | focus_has_dispellable_buff@dev | 存在且 UnitIsEnemy；必填 dispel_types 布尔映射 |

施法使用 NeverSecret `delayTimeMs` 或 `isEmpowered ~= nil` 哨兵，普通引导 false 有效；进度只使用 Duration `EvaluateElapsedPercent`，图标直接交给纹理消费者，可中断用 `C_CurveUtil.EvaluateColorFromBoolean`。不对秘密值做 Lua 算术、反转或分支。没有新增施法状态插件。

事件下一帧刷新；进度随机错峰 0.1 秒轮询，基础布尔与可中断 1 秒兜底，图标事件刷新；Aura 的日常更新由官方容器管理。没有修改玩家插件。

### 可驱散增益边界

- [x] 固定 `HELPFUL|RAID_PLAYER_DISPELLABLE`，通过 `candidateFilters.includeDispelTypes` 筛选。
- [x] Magic／Poison／Disease／Curse／Stealth／Special／Enrage 七键；值严格 bool，空表和全 false 不匹配。
- [x] `RAID_PLAYER_DISPELLABLE` 表示团队有人能驱散，不保证玩家本人现在能驱散／偷取。
- [x] 保留七键原样，不猜测 Enrage 到空字符串或其他值的映射。
- [ ] Enrage 实际 `dispelName` 键和目标客户端显示：本地证据不足，用户接受标记游戏待验。

## 2. 四个既有减益插件来源过滤

- [x] `target_has_debuff@dev`
- [x] `focus_has_debuff@dev`
- [x] `aura_target_debuff_duration@dev`
- [x] `aura_target_debuff_stacks@dev`

以上固定 `PLAYER|HARMFUL`，不新增 `player_only`；官方 PLAYER 包含玩家、玩家宠物和载具。驱散插件除外。保留既有不可辅助侧分类、多个 ID 的官方首匹配语义，以及时长／层数比例估计，不新增 focus 时长或层数。

## 3. 打断黑名单图标

- [x] 新增 `interrupt_blacklist_icons@dev`，无业务参数，固定共享键 `interrupt_blacklist`。
- [x] 固定十个 IconTile，输出 `list[str]`，过滤空槽、保留槽顺序及重复 hash，全空／异常 `[]`。
- [x] 每份循环只允许声明一次，由 plugin.toml 和示例中文注释说明；不增加核心强制校验，不支持多份独立黑名单。
- [x] 加载期登记一个 panel 编辑入口，按档案保存并回调；初始化主动渲染，默认值仅交由 panel 应用一次。
- [x] 六项默认：468962、1248327、1254669、1258436、1262510、1262526；不覆盖已有列表。
- [x] 配置可超过十项，按 ID 数值升序取前十项固定槽；纹理加载失败留空并清角标、不补位、不删配置、不循环重试、不使用 panel 问号纹理。
- [x] 初始化及配置／档案变化请求数据；`SPELL_DATA_LOAD_RESULT` 成功且仍在配置时下一帧刷新，不再次请求。
- [x] 有效图标黄色 `COLOR.SPELL_TYPE.INTERRUPTIBLE` 角标仅为类别，不表示当前施法状态或打断许可。

## 4. 证据与未完成的游戏验收

### 核验基线

- 只读官方源码：`wow-ui-source@ptr`，commit `a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58`，build **12.1.0.69587**。
- `Interface/AddOns/Blizzard_APIDocumentationGenerated/UnitDocumentation.lua`：单位状态、施法返回值、NeverSecret 哨兵与 `UnitTokenPvPRestrictedForAddOns`。
- 同目录 `CurveUtilDocumentation.lua`、`LuaDurationObjectAPIDocumentation.lua`、`SpellDocumentation.lua`、`SimpleTextureBaseAPIDocumentation.lua`：显示消费者、数据请求和纹理结果。
- `Blizzard_AuraContainer/Blizzard_CustomAuraContainer.lua`、`Blizzard_AuraContainerUtil.lua`：受管 AuraSlot 和 `includeDispelTypes[auraData.dispelName]`。
- `Blizzard_FrameXMLUtil/AuraUtil.lua` 的 `Player` 与 `RaidPlayerDispellable` 注释：宠物／载具来源及团队驱散语义。
- 2026-09-18 获取 Warcraft Wiki 的 UnitExists、UnitIsDeadOrGhost、UnitCanAttack、UnitAffectingCombat、UnitIsEnemy、UnitCastingInfo、UnitChannelInfo、C_Spell.GetSpellTexture、C_Spell.RequestLoadSpellData 页面；链接保留在对应模板。网页可能描述更新版本，不替代指定 build 源码。
- 业务盘点的历史参考仍为只读 `PhantomProject@develop` commit `f693511`：`src/0201–0211`、`src/0301–0311`、`src/0502_target_debuff.lua`、`src/0632_interrupt_blacklist.lua`；不作为 API 可用性证据。

### 验证状态

- [x] 参数正常／边界／缺失／非法输入；真实 Cell、IconTile 解码和失败兜底。
- [x] Lua 5.1 生成编译，目标／焦点切换与清除、单位不存在、死亡、敌对与可攻击分离。
- [x] 普通施法、引导 false 哨兵、空闲、秘密布尔与纹理传递、进度对象缺失、事件下一帧刷新。
- [x] 驱散类型映射和敌人前置；四个玩家来源减益槽的精确过滤字符串。
- [x] 真实 Config/panel/IconTile 模块的默认值、十槽排序、空槽、纹理失败、已有配置、档案切换、迟到加载事件、不循环请求。
- [x] 作者自述、内置条件目录、最小配置示例同步。
- [x] 全量离线回归：1391 passed、5 skipped；5 项符号链接测试因 Windows 权限不足跳过，未重试或变更权限。
- [ ] 实际客户端版本确认、游戏内 Secret Values／PvP 限制／Aura 匹配与渲染验收；本任务没有运行游戏。

类型检查 `scripts/check_types.py` 已通过，沿用精确版本自动发现入口，无需新增硬编码清单。Ruff lint 已通过。P2 修复后仅执行定向验证：224 项测试通过，两个施法图标精确版本入口及测试文件的 mypy、定向 Ruff lint 通过。全库格式检查此前发现 26 个既有 Python 文件混合换行问题，未覆盖这些文件；本次文件另行检查。

最小片段见 `.agents/skills/phantom-plugin-dev/references/target-focus-example.md`，仅声明观察条件。

### P2 历史纠正（2026-09-19，用户最终确认）

此前 P2 以 `SetTexture` 的 false 返回清空目标／焦点图标和角标，并以普通 bool 替身测试；该实现会消费实际客户端的秘密返回布尔，原“未标记秘密返回即可安全判断”的推断错误。用户已明确撤销“设置失败必定同时隐藏角标”的旧要求。

现改为玩家同款 `IconTile:SetIcon` 直接显示路径，不消费 `SetTexture` 返回值；保留单位消失或无施法时清空图标与角标。只读核对的官方源码仍为上列 revision/build，`SimpleTextureBaseAPIDocumentation.lua` 允许秘密参数且声明 success: bool，不能据此保证普通返回值。回归覆盖 target/focus × 普通施法/引导 × true/false/nil 返回，以及空闲／单位消失后的清空和恢复，并静态约束模板使用不消费返回值的显示调用。普通 Lua 不能真实模拟 WoW 秘密布尔，这些离线检查不等于游戏验收。

- [ ] 修复后的目标实际客户端 Secret Values、纹理及角标显示验收；本次不部署游戏、不运行入口。

本次离线验证（2026-09-19）：

- `.venv/Scripts/python -m pytest tests/test_target_focus_conditions.py tests/test_player_conditions.py tests/test_conditions.py -q`：306 passed，包含生成 Lua 5.1 编译与真实 IconTile 消费者回归。
- 同一测试命令追加 `tests/test_generator.py`：338 passed、1 failed。失败项 `test_generated_lua_roundtrip_gcd_and_events` 的旧替身缺少 `Enum.PowerType`，在 `spec_power_runic_power@dev/template.lua` 加载阶段报错，尚未执行本次图标逻辑；保留该验证限制。
- `.venv/Scripts/python scripts/check_types.py`：核心、测试和全部精确版本入口通过。
- `.venv/Scripts/python -m ruff check` 与 `-m ruff format --check`，范围为 `tests/test_target_focus_conditions.py` 及两个施法图标的 `condition.py`：通过。
- `git diff --check`：通过；仅有 Git 的 LF／CRLF 提示。已审阅修复 diff，现有 `rotations/blood-dk.toml` 用户修改保留。

## 5. 排除范围保持

不实现自动匹配施法或自动打断；不修改实际战斗循环，不按插件名修改核心。focus Aura 时长／层数、目标周围计数、party／raid 身份条件、目标／焦点职业职责能量、减益图标名称颜色、切换目标或设置游戏焦点等动作均不纳入。
