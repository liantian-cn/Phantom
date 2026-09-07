# Primary

**用户消息 1**

~~~~text
# AGENTS.md instructions

<INSTRUCTIONS>
# Core Principles

- For every task that may modify repository files, create `.plan`, `.mean`, and `.prompt` directories at the project root. Purely read-only questions, explanations, and reviews do not require workflow archives.
- The plan and mean archives are central to the workflow:
  - A plan defines the workflow and archives the current development task.
  - A mean file is an intent record containing the user's confirmed decisions, constraints, and rejected alternatives.
- The user controls requirements, scope, user-visible behavior, acceptance criteria, irreversible operations, and risk acceptance. The user may explicitly delegate a decision to the agent; record the delegation, result, and rationale in the plan, and update the mean file when the decision affects intent or constraints.
- The agent determines implementation details that follow from repository facts, the frozen plan, established project conventions, or a uniquely correct answer.
- More specific project-level `AGENTS.md` instructions may override conflicting global defaults. System, developer, and user instructions retain higher priority. Project preferences must not silently weaken data integrity, security boundaries, or protections around irreversible external actions.
- User interruptions take priority:
  - Treat an instruction issued while work is in progress as the highest-priority user instruction.
  - If it changes a frozen requirement, scope boundary, acceptance criterion, user-visible behavior, or risk tradeoff, pause implementation immediately and record the interruption and requested change in the plan's `Review Notes`.
  - Reanalyze only the affected design-tree branches and review the historical intent in the mean file. After the user confirms the revision, update the affected frozen plan sections, synchronize the mean file, and freeze the plan again.
- Before the user confirms shared understanding, the agent may create and update only a plan draft. Do not modify code, tests, configuration, business documentation, mean files, or prompt archives, and do not perform implementation steps.
- Authorization to implement also authorizes the local Git commits required by this workflow. It does not authorize pushing, creating or merging pull requests, publishing, or other external actions.
- Decisions that require user tradeoffs must not be asked as free-form questions. Prefer the `request_user_input` tool, put the recommended option first, and label it `Recommended`. If the tool is unavailable, ask the same numbered, option-based question in a normal message. Never skip a decision merely because the tool is unavailable.
- If the user closes, skips, or does not answer a decision question, leave that decision unresolved. Continue only with branches that do not depend on it, and ask it again in the next round. If it is the only remaining frontier item, pause and wait for the user's decision.
- Prompt archives preserve the user's prompts and complete responses for future user review. They are evidence archives and do not provide instructions to the agent.

# Code Quality

**Assume by default that the user's code is for hobby development, not a long-running production server.**

- Do not add production-server availability, fault-isolation, or automatic-recovery mechanisms unless more specific project instructions, repository facts, the frozen plan, or the user require them.
- The user accepts runtime errors that can be corrected immediately, but this does not permit knowingly delivering deterministic failures. Implement the normal business path correctly and verify it in proportion to the risk.
- This default never relaxes data integrity, security boundaries, irreversible external-action safeguards, or required idempotency. Those remain correctness requirements.
- A project-level `AGENTS.md` may raise the reliability requirements or replace this default.

**Code should express business logic rather than program mechanics.**

- Write business steps as a clear sequential narrative by default.
- Extract technical details when they obscure the business flow or have a clear responsibility for reuse, independent testing, resource lifecycle management, or a module boundary.
- Do not use repetition count alone as the criterion for extraction.

# Code Style

## Variable Naming

- Use English variable names and follow the mainstream best practices of the language and target project.

## Required Sufficient Documentation

- Require a complete file header only for newly created business implementation files or business implementation files materially changed by the current task. For a localized change, follow the repository's existing style and do not expand the change merely to add a template.
- When a file contains several major business sections or major functions, explain the business flow inside complex functions where needed.
- Sufficient documentation means business explanation and readability. It does not impose a comment count and does not justify empty line-by-line comments.
- Third-party libraries, tests, scripts, configuration, tools, generated code, lockfiles, pure data files, and other files without business logic do not require the standardized file header.
- When the complete header applies, place it before the business code using the language's native comment syntax.
- Use the repository's established file-header format when one exists. Otherwise, use the English labels below.

## Required Complete File Header

- `Summary`: the primary purpose in one line of no more than 120 characters.
- `Description`: business details; describe the content structure when the file has several major sections, or the workflow when it contains one business flow.
- `Key Variables`: each business-important variable and its meaning, one per line, or explicitly write `None`.
- `Change Log`: one line for the current change with its date and the source requirement or fixed bug. Record only known facts and never invent history.

## File Header Format

```text
Summary:
    (Primary purpose of the file, one line, no more than 120 characters.)
Description:
    (Detailed business explanation. Describe the content structure for multiple major sections,
    or explain the business workflow for a single flow.)
Key Variables:
    (One entry per line: variable name and meaning. Write None when there are no key variables.)
Change Log:
    (One entry per line in the form YYYY-MM-DD: description. Record only known facts and do not
    invent history. Follow an existing project convention for entry prefixes when one exists.)
    YYYY-MM-DD: Added/Changed/Removed/Improved detailed information
```

# Protocols

## Plan Protocol

- A plan draft uses the path `.plan/YYYY-MM-DD-title.md` at the project root.
- Generate `title` from the confirmed goal as a short, stable English kebab-case slug. The corresponding plan, mean, and prompt files must use the same filename.
- Before creating a plan, check the intended plan, mean, and prompt paths. If any same-named archive exists, use `request_user_input` to let the user choose among continuing the same task, providing a new title, or explicitly replacing the existing archive after review. Never reuse, overwrite, or suffix a name automatically.
- Once the goal and filename are settled and the collision check passes, create the plan draft and update it throughout the interview. Write only repository facts and confirmed decisions. Use `Pending` for unresolved content; remove every `Pending` marker before freezing.
- Use English and exactly these sections: `Goal`, `Scope`, `Decisions`, `Implementation Steps`, `Acceptance Criteria`, `Verification`, `Review Notes`, and `Completion`.
- After final confirmation, freeze `Goal`, `Scope`, `Decisions`, `Implementation Steps`, and `Acceptance Criteria`. Do not change them autonomously during implementation. Append audit, verification, and completion metadata only to `Verification`, `Review Notes`, and `Completion`.
- Record the confirmation time, confirmation source, and frozen status in `Review Notes`; do not add a separate status section or YAML structure. Record later refreezes as appended audit entries.
- If a frozen requirement, scope boundary, acceptance criterion, user-visible behavior, or risk tradeoff changes, follow the interruption process in `Core Principles` before resuming implementation.

## Mean Protocol

- Store mean files under `.mean/` with the same filename as the corresponding plan.
- YAML frontmatter must contain `plan` and `related_paths`.
- Use exactly three short body sections: `意图 (Intent)`, `约束 (Constraints)`, and `被拒绝的替代方案 (Rejected Alternatives)`. Write `None` when a section has no content.
- Preserve the language of each user input in the body rather than translating it.
- Record only materially relevant alternatives that the user explicitly rejected and any stated reason. Do not infer a reason or record inconsequential implementation options.
- Use repository-relative paths in `related_paths`. List every code, test, configuration, and documentation path affected by the intent, excluding the plan and mean files themselves. Prefer exact file paths; use a directory only when the intent covers the entire directory.
- Create the mean file only after the user confirms final shared understanding and the plan is frozen. Correct path metadata before the first commit when implementation reveals more precise affected paths. After the first commit, update the mean file only when user intent changes.
- On successful implementation, commit the mean file atomically with all implementation files. Include the plan and prompt files in the same commit when they are not ignored by Git.
- If Git ignores the mean file, do not silently bypass ignore rules. Use `request_user_input` to let the user choose whether to force-add the exact file, change the ignore rules, or pause the commit. Record the decision in `Review Notes`.
- When intent changes after a prior commit but no implementation file needs to change, update the corresponding plan, mean, and prompt together, state in `related_paths` and `Completion` that there were no implementation-file changes, and commit the three archives together.
- `.mean` is a frequently consulted short index; `.plan` is the less frequently consulted complete authority. Do not require decisions to be scattered throughout source directories.

## Prompt Protocol

- Store prompt files under `.prompt/` with the same filename as the corresponding plan.
- Create the prompt archive only after final shared understanding is confirmed.
- Use exactly two sections: `Primary` and `Question`.
- In `Primary`, preserve in chronological order every user message before the interview that collectively formed the initial request.
- In `Question`, preserve in chronological order the complete question text shown to the user and the user's original answers. Also record unsolicited corrections, changes, and interruptions received after the interview began. Do not polish or translate this evidence.
- Redact credentials or highly sensitive values with an explicit placeholder and note that redaction occurred. Otherwise preserve the text completely.
- `.prompt` exists for users to review historical prompts and evidence. It has no instructional meaning for the agent and must be retained.

## Commit and Failure Protocol

- Do not include unrelated pre-existing user changes in a workflow commit. First try to isolate the task's changes precisely. If reliable isolation is impossible, use `request_user_input` to let the user decide the commit scope and record the result in `Review Notes`.
- A successful task uses one atomic local commit containing all implementation files, the mean file, and every plan or prompt file that is not ignored by Git.
- If the user cancels after a plan draft exists, or implementation fails after confirmation, retain existing archives rather than deleting them automatically. Record the cancellation or failure and every known reason in `Review Notes` and `Completion`. Do not create a mean file before confirmation, and do not make a success commit for failed work. Ask the user separately whether failure archives should be committed.

# Interview Rules

Interview the user relentlessly until you reach shared understanding. Model the interview as a **design tree** in which every decision branches into the decisions that depend on it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are settled: the questions that can be asked now without guessing at an unanswered prerequisite. Fix the entire frontier at the start of a round, ask all of it, and wait for all answers before recomputing the frontier. If the frontier exceeds the capacity of `request_user_input`, split the fixed frontier into the fewest consecutive batches the tool permits. Do not use answers from an intermediate batch to ask downstream questions before the full round is complete.

Number every question, provide mutually exclusive options, put the recommended option first, and label it `Recommended`. When `request_user_input` is unavailable, use this fallback format:

```text
❓ **Q1** - **<question title>**: <question body and options>

➡️ <recommended answer>

---

❓ **Q2** - **<question title>**: <question body and options>

➡️ <recommended answer>
```

Each completed round reshapes the tree. Settled decisions move the frontier outward and unblock only the questions that depend on them. A question whose answer depends on another question still open in the current round belongs to a later round.

Finding facts is the agent's responsibility. Use the repository, filesystem, available tools, and authoritative sources before asking the user. Do not block the entire round while an independent investigation runs: treat its result as an unsettled prerequisite, defer only its dependent questions, and ask the rest of the frontier. When helpful and permitted, delegate independent fact-finding to a subagent. If an essential fact remains inaccessible after exhausting available sources, explain what was checked and ask the user. User preferences, goals, and private business context are user-provided inputs rather than discoverable environmental facts.

The decisions belong to the user. If the user explicitly delegates one, follow the delegation rule in `Core Principles`.

The interview is complete only when the frontier is empty and every design-tree branch has been visited. Then present a complete shared-understanding summary and ask the user to choose between `Confirm and authorize implementation (Recommended)` and `Revise`. Do not freeze the plan, create the mean or prompt files, modify implementation files, or begin implementation until the user explicitly confirms.
</INSTRUCTIONS>
~~~~

**用户消息 2**

~~~~text
/init 

以下是我对项目的一些预想，帮我完成一些工作


1. 完善草案稿，书写结构指引，保存到若干文件。
2. 当前环境初始化第三方源码。
3. 整理、压缩、捋顺.context目录的文档，这些文档是魔兽世界插件开发的知识。
4. 整理、压缩、捋顺.spec目录的文档，这些未来是项目的规则。
5. 构建AGENTS.md，指引到上述文件。

上述文件都应该是中文的。
这是极重要的步骤，多思考。




# 以下是草案

## 项目说明

项目名称：Phantom
- 作者：liantian-cn
- repo: git@github.com:liantian-cn/Phantom.git
- 开发分支：develop，只在develop分支上修改。用户会手动冻结特定版本到main分支。
- 这是一个魔兽世界战斗自动化工具，帮助玩家实现最优加血，最高输出。
- 运行平台：windows
- 开发环境：wsl2 + docker容器
- 当前游戏版本12.1


### 大体概念

程序分为python端和lua端。

- 1. python端根据战斗逻辑，生成lua文件。
- 2. lua文件在游戏内的屏幕角落，生成像素点。像素点表示逻辑中条件的值。
- 3. python端捕获屏幕的角落，解析像素。
- 4. 解析结果作为条件的变量，拿回逻辑端，得到战斗逻辑的结果。比如暂停、释放某个技能。
- 5. python端发送技能按键到魔兽世界的窗体。
- 往复循环3-5实现自动化战斗。


## 项目的一些细节。
吸取过去项目的一些经验，本次项目有些特色

### 按需生成像素

不管朋友开发的Shigure ，还是我的旧项目 PhantomProject 和M.I.D.N.I.G.H.T都在游戏内画了比较多的像素。刷新占用大量cpu时间，本项目所用条件生成lua

### 插件能力

合作开发的Shigure的过程中，发现修复一些bug的过程中，改动了逻辑，导致一些现有配置无法使用了。现在把逻辑的条件做成插件。同时可用旧版本。

### 面向AI友好

合作开发的Shigure的过程中，发现虽然是GUI，但是大家还是习惯用ai工具改动循环逻辑。但是AI不擅长修改json。
1. 配置文件改为AI更易懂的yaml格式。
2. 插件的代码注释应该标准化。从而让AI更好的理解。


### 游戏内布局

任何插件生成的lua，有三种模式
cell: 一个4x4大小的像素。根据其亮度值反应数值，精度1/255。
value_bar:高度为4，宽度为4n的条，由于秘密值的原因，有些数值只能这样展现，精度1/2n
icon_tile: 一个8x8大小的图标，无法展示数值，只能获得内部6x6区域的hash

在游戏内
第一行为若干的cell，反应通用信息，占用高度4
第二行为插件生成的cell，占用高度4
第三行为多个value_bar，展通高度4
第四行为icon_tile，高度为8。
意义一共占用20像素的高度。宽度若干。



### UI 

- 前端使用pyside6，和Terminal一致
- 

### 技术细节

- 截图参考 https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/capture/capture_screen.py
- 定位参考 https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/capture/find_template_bounds.py
- 依然使用numpy实现高速处理
- 依然使用xxxhash


### 目录

- main.py               入口文件
- phantom/              python代码的目录
- phantom/ui            前端界面
- phantom/core          核心代码
- phantom/conditions    条件插件目录
- phantom/actions       行为插件目录
- phantom/captures      截图插件
- .context              参考文档
- .spec                 项目规范
- scripts/              脚本
- rotations/            配置文件保存路径

### 插件结构

#### 条件插件结构

条件插件继承自一个类

- health_pct@1.0 目录名
  - condition.py    python代码，包括这个插件入参、生成的lua类型，尺寸。入参包括坐标、参数。
  - template.lua    这个插件生成的lua代码快的模板。python替换其中的标志位，生成游戏内读取的lua


#### 行为插件结构

暂且只做PostMessage一个

- PostMessage@1.0 目录 一个基于   ctypes.windll.user32.PostMessageW的插件你
  - action.py   实现逻辑的文件

#### 截图插件结构

- gdi@1.0   基于 ctypes.windll.gdi32 bitmap截图的插件
 - capture.py 实现逻辑的文件


### 配置格式

配置文件使用对Agent友好的yaml格式

```
uuid: 当前配置的uuid
profile: 
  title: 配置名
  description:描述信息
  unitClass: DEATHKNIGHT  -- 适配职业
  unitSpec:  1 -- 适配的职业专精id
  unitTalnet:     -- 学会那些天赋时，这个配置生效
    - 432459
    - 387786  

conditions：               -- 定义条件
  - id:1    -- 序号
    title: 玩家血量         -- 比如逻辑中要用到玩家血量
    plugin: health_pct@1.0  -- 使用health_pct插件，版本1.0
    plugin_args:
      unitToken: player     -- 插件的参数，unitToken为player

  - id:2    -- 序号
    title: 圣光术冷却时间         -- 比如逻辑中要用到圣光术冷却时间
    plugin: player_spell_cooldown@1.0  -- 使用player_spell_cooldown插件，版本1.0
    plugin_args:
      spell_id: 82326,82325     -- 有2个技能id指向圣光术，这个插件的入参spell_id是list
      ignore_gcd:true           -- 忽略gcd

  - id:3    -- 序号
    title: 目标血量         -- 比如逻辑中要用到玩家血量
    plugin: health_pct@1.0  -- 使用health_pct插件，版本1.0
    plugin_args:
      unitToken: target     -- 插件的参数，unitToken为player

  - id:4    -- 序号
    title: 审判冷却时间        
    plugin: player_spell_cooldown@1.0  -- 使用player_spell_cooldown插件，版本1.0
    plugin_args:
      spell_id: 12345     -- 有2个技能id指向圣光术，这个插件的入参spell_id是list
      ignore_gcd:true           -- 忽略gcd

macro:      -- 游戏里的宏
  - name:对player释放是圣光术        -- 名字，对应action
    macro_text: /cast [@player] 圣光术
    key: ALT+F4           -- 宏绑定的按键，生成lua会在游戏内绑定按键，python端也会发送这个按键。
    bing_key:true        --  是否绑定宏。

  - name:审判        -- 名字，对应action
    macro_text: /cast 审判
    key: E           -- 宏绑定的按键，生成lua会在游戏内绑定按键，python端也会发送这个按键。
    bing_key:false        --  玩家如果现有键位，可以不绑定。此时其实macro_text也没生效。直接发送按键E到游戏。

rotation:  循环开始
  - id:1    -- 序号
  - condition: (玩家血量 < 70) and (圣光术冷却时间 =0 0)
  - macro: 对玩家释放是圣光术

  - id:2    -- 序号
  - condition: (目标血量 > 0) and (审判冷却时间 =0 0)
  - macro: 审判

```









## 开发和测试问题

- 因为程序在windows下运行，开发环境是wsl+docker，所以跳过不必要的测试。
- 避免生硬的pytest，只测试有效的算法逻辑，不进行简单的字符串比较。


## 第三方lua源码。

在当前容器环境内，存在以下源代码，若没有，则git clone

### 魔兽世界官方源码
- 说明：官方UI的源代码，极具参考意义。
- repo:git@github.com:Gethe/wow-ui-source.git
- 分支：`ptr`
- 本地存放目录：`/wow-ui-source`


### PhantomProject

- 说明：个人的测试代码集是，之前测试成功的一些lua代码片段，在秘密值处理上具有参考意义。但是因为在合作开发Shigure的过程中，发现很多问题。所以放弃了继续开发。
- repo:git@github.com:liantian-cn/PhantomProject.git
- 分支：`develop`
- 子目录：'src/'
- 本地存放目录：`/PhantomProject`

### Shigure

- 说明：同僚的项目，构架逻辑不同，但是lua部分有参考意义。
- repo:git@github.com:waynebian01/Shigure.git
- 分支：`main`
- 子目录：'Fuyutsui/'
- 本地存放目录：`/Shigure`


### M.I.D.N.I.G.H.T

- 说明：我过去的项目，其中windows截图和矩阵取值部分有参考意义。
- repo:git@github.com:liantian-cn/M.I.D.N.I.G.H.T.git
- 分支：`12.0`
- 子目录：'Terminal/'
- 本地存放目录：`/midnight`
~~~~

# Question
- **Q1｜交付范围**：只建设文档体系并初始化第三方参考源码，暂不创建代码工程。
- **Q2｜文档结构**：按职责拆分为多份文档，便于 Agent 按需读取。
- **Q3｜原始知识文档**：`.context` 保持英文并精编，避免翻译误差积累。
- **Q4｜知识覆盖范围**：以 Phantom 需求为中心，保留 12.1 API、Secret Values、Aura、像素显示、渲染组件、事件与性能及安全限制等相关知识。
- **Q5｜技术事实处理**：以指定版本的本地源码和版本变更记录交叉核验；无法确认的内容标为“待验证”，不写成强制规则。
- **Q6｜文件语言**：`.spec` 与 `AGENTS.md` 使用中文，`.context` 保持英文，技术标识符保持英文。
- **Q7｜根 README**：保留根 `README.md` 原样，将完整项目说明写入 `.spec/project-overview.md`。
- **Q8｜第三方源码克隆**：按指定分支浅克隆缺失仓库，并将所有第三方源码作为只读参考。
- **Q9｜`.context` 精编方式**：先在项目外备份 42 份原稿，再合并为约 7 份英文专题文档。
- **Q10｜`.spec` 文件集合**：采用八份分层规范文档。
- **Q11｜未确定内容**：显式列为“待定事项”，不得由 Agent 自行补全为规则。
- **Q12｜WoW 版本边界**：面向 12.1 系列；易变事实记录核验信息，并在版本变化时重新核验。
- **Q13｜第三方源码只读约束**：通过规范禁止修改、提交、切分支、拉取或重置，不修改文件权限。
- **Q14｜`AGENTS.md` 职责**：只承担权威顺序和任务路由，不复制规范正文。
- **Q15｜配置字段规范**：字段统一为 `snake_case`，修正拼写，列表使用真正的 YAML 数组；最初选择稳定英文 `key`，后在 Q34 中取消。
- **Q16｜宏与行为关系**：配置必须保留按键与宏文本的对应关系，同时允许 `bind_key: false`，直接使用游戏内已有键位。
- **Q17｜配置版本**：加入 `schema_version: 1`，未来通过显式迁移升级。
- **Q18｜像素协议成熟度**：冻结逻辑协议，将颜色通道、采样、校验和位映射等底层细节列为待定。
- **Q19｜横向布局**：四行分别从左到右紧密排列，画布宽度取各行最大值。
- **Q20｜Lua 生成粒度**：一次生成一个插件包；共享基础模块，并为每份选中的 rotation 生成独立 `<uuid>.lua`。
- **Q21｜插件版本兼容**：使用精确版本，旧版本并存，不自动回退或升级。
- **Q22｜PySide6 UI**：本轮只固定 PySide6 技术，不参考旧 Terminal 界面，具体交互留待后续。
- **Q23｜配置文件边界**：一份 YAML 对应一份 rotation，顶层包含 `schema_version`、`uuid`、`profile`、`conditions`、`macros` 和 `rotation`，删除数字 `id`。
- **Q24｜条件表达式引用**：直接使用唯一的 `conditions[].title` 作为表达式变量名，可用中文或英文。
- **Q25｜循环命中规则**：按 rotation 列表从上到下判断，首个成立项胜出，每轮最多发送一个按键。
- **Q26｜暂停语义**：所谓暂停就是本轮没有动作、不发送按键，不设持久暂停状态。
- **Q27｜天赋匹配**：最初答复为清单中的每个 spell ID 都必须已学会；该设计随后在 Q28 与 Q33 中撤回。
- **Q28｜rotation 激活冲突**：不再按天赋判断；GUI 中同一职业与专精只能勾选一份，选择新项会取消旧项。
- **Q29｜`/reload` 边界**：最初答复专精或天赋变化需 `/reload`；删除天赋判断后，最终只保留专精切换需 `/reload`。
- **Q30｜`bind_key: false`**：`key` 必填，`macro_text` 可省略且不生效；不生成对应的宏绑定 Lua。
- **Q31｜键位冲突风险**：直接覆盖已有动作，不检查也不提示，由配置作者选择冷门键位避让。
- **Q32｜代码注释语言**：使用中文业务注释和标准化头部，代码标识符保持英文。
- **Q33｜`unit_talents` 最终角色**：从 schema v1 删除 `unit_talents`，天赋路由留作未来功能。
- **Q34｜对象标识方式**：不需要额外英文 `key`；rotation 通过条件 `title` 和宏 `name` 引用，宏 `key` 专指物理按键。
- **Q35｜条件标题限制**：标题必须非空且唯一，不含空格、操作符、括号或引号，也不能使用逻辑保留词；后由 Q63 收敛为 Python 标识符规则。
- **Q36｜表达式能力**：支持布尔、整数、浮点数、字符串和列表，以及比较、`and`、`or`、`not`、`in` 等操作。
- **Q37｜激活与重载模型**：Lua 加载时只检查职业和专精，不匹配即提前 `return`；切换专精后需 `/reload`。
- **Q38｜GUI 互斥范围**：采用表格和首列复选框，同一职业与专精勾选新项时取消其他同组合项。
- **Q39｜循环频率**：10 Hz 只是示例，实际频率、节流和配置方式待定。
- **Q40｜按键字符串格式**：采用 WoW 大写连字符格式，如 `ALT-NUMPAD1`、`SHIFT-F8`。
- **Q41｜绑定持久性**：使用不可见的 `SecureActionButtonTemplate` 和 `SetOverrideBindingClick` 建立运行期绑定，不创建宏槽位或持久键位。
- **Q42｜按键分隔符**：最终使用 WoW 连字符格式，Python 端解析同一字符串。
- **Q43｜宏集合字段名**：顶层使用复数 `macros`，每个 rotation 项使用单数 `macro` 引用宏名称。
- **Q44｜`in` 表达式细节**：支持 `in` 与 `not in`；列表元素限整数、浮点数、布尔值或字符串，不允许嵌套与混合类型；优先级为 `not`、比较/成员判断、`and`、`or`。
- **Q45｜UUID 格式**：使用标准带连字符的 UUID 字符串，生成文件名为 `<uuid>.lua`。
- **Q46｜`unit_spec` 含义**：使用 `GetSpecialization()` 返回的专精顺序索引 `1` 至 `4`。
- **Q47｜插件标识命名**：统一为区分大小写的小写 snake_case 精确版本，如 `health_pct@1.0`。
- **Q48｜生成插件包名称**：每次生成时由用户输入目录和 TOC 共用的包名。
- **Q49｜条件插件输出数量**：一个条件只能使用 `cell`、`value_bar` 或 `icon_tile` 中的一种输出类型，但可连续占用多个同类区域，结果可为标量或列表。
- **Q50｜第一行通用 Cell**：保留该行及其通用职责，具体字段暂定为候选项，不在本轮冻结。
- **Q51｜条件类职责**：条件实例保存参数和像素位置、生成 Lua、解码截图；核心维护 `conditions[title] = instance`，表达式读取实例的业务值。
- **Q52｜输出契约声明**：分别声明 `output_type`、`output_count`、`value_type` 和 `value_shape`；多个区域既可合成标量，也可形成列表。
- **Q53｜动态输出尺寸**：插件校验参数后计算并冻结 `output_count`，布局完成后不得改变。
- **Q54｜成员判断类型检查**：预先确认右侧为列表且左侧标量类型与列表元素一致，不做隐式转换。
- **Q55｜不可用值**：每个插件必须定义符合业务语义的兜底值；基类强制要求兜底方法，最终 `value()` 不返回通用 `None`。
- **Q56｜多区域列表顺序**：Icon Tile 的 `raw_value()` 用 `None` 保留空槽，业务 `value()` 的过滤、重排和顺序由插件契约定义。
- **Q57｜插件包名格式**：必须匹配 `[A-Za-z][A-Za-z0-9_]*`，目录名与 `.toc` 文件同名。
- **Q58｜通用 Cell 候选项**：启停、延迟、职业、专精和战斗状态仍只是待定候选，不纳入 v1 固定规则。
- **Q59｜条件基类模板**：基类公开 `raw_value()` 和 `value()`；`value()` 调用插件的 `decode_value(raw)`，插件必须实现 `fallback_value()`。
- **Q60｜Value Bar 原始值单位**：最初选择 `0.0–1.0` 长度比例；后在 Q67 修订为读取中间两行纯白像素占比并返回 `0.0–100.0`。
- **Q61｜Icon Tile 原始空值**：只读取内部 `6×6`；全黑为 `None`，否则返回 16 位小写 `xxh3_64_hexdigest`；多 Icon Tile 原始列表长度固定为 `output_count`。Cell 同理只读取内部 `2×2`。
- **Q62｜兜底触发范围**：`decode_value()` 的任何异常都由基类丢弃并转为插件兜底值，插件也可主动返回兜底值。
- **Q63｜条件标题词法**：采用 Python 标识符兼容规则，可含中文、英文字母、数字和下划线，但不能以数字开头，也不能使用保留词。
- **Q64｜表达式执行器**：在确认性能足够后选择加载时解析、校验一次的白名单 AST；禁止属性访问、下标、函数调用、算术和任意代码执行。
- **Q65｜表达式字面量拼写**：采用 Python 风格的 `True`、`False`、`[]`、字符串引号和数值。
- **Q66｜首次最终确认**：选择修订，未授权按首次共同理解实施。
- **Q67｜修订范围**：未选择预设分类，直接补充两项修订：Value Bar 读取中间两行纯白像素占比；代码风格强制 Type Hint。
- **Q68｜Type Hint 强制范围**：适用于所有手写 Python 文件；函数与方法签名、属性、容器和类型不直观的局部变量必须标注，第三方及生成代码除外。
- **Q69｜修订后最终确认**：确认并授权实施。
