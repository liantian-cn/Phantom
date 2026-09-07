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

**问题轮次 1**

~~~~text
已完成只读盘点，并建立计划草案：[2026-09-05-project-initialization.md](/workspaces/phantom-5796e240/.plan/2026-09-05-project-initialization.md)。

第一轮需要确定范围、信息架构及资料保留策略。请按 `Q1-1、Q2-1……` 的格式选择。

❓ **Q1 - 交付范围**：本次初始化做到哪一层？

1. **仅完成文档体系与第三方源码初始化（推荐）**：不创建 Python/Lua 代码、空业务目录或依赖配置。
2. 文档、第三方源码，加上草案中列出的空目录骨架。
3. 文档、第三方源码，并创建可运行的 Python/Lua 初始工程。

➡️ 推荐答案：**Q1-1**。先冻结架构和规则，再开始代码工程。

---

❓ **Q2 - 文档结构**：草案应如何拆分？

1. **分层拆分（推荐）**：根 `README.md` 作为项目入口；`.spec/` 分别保存架构、像素协议、插件协议、配置格式、开发测试规则；`.context/` 只保存 WoW 知识；`AGENTS.md` 负责路由。
2. 将项目设计集中在一份大型设计文档中，其他文件只做索引。
3. 尽量保持现有三份 `.spec` 文件，只补充少量内容。

➡️ 推荐答案：**Q2-1**。不同规则的变更频率与阅读场景不同，拆分后更适合 Agent 按需读取。

---

❓ **Q3 - 原始知识文档**：现有 `.context/` 有 42 份、约 1.53 万行，多数是英文通用资料。如何处理？

1. **中文精编替换并留仓库外备份（推荐）**：先将现有内容压缩备份到项目目录之外，再用少量中文专题文档替换，并保留来源及版本索引。
2. 保留全部英文原文，另加中文摘要；将“全部中文”理解为仅要求新增文件为中文。
3. 全量翻译现有 42 份资料，尽量保持原有细节和文件结构。

➡️ 推荐答案：**Q3-1**。这最符合“整理、压缩、捋顺”和中文化要求，同时避免未跟踪原稿不可恢复。

---

❓ **Q4 - 知识覆盖范围**：精编后的 `.context/` 应保留多宽的知识面？

1. **以 Phantom 需求为中心（推荐）**：重点保留 12.1 API、Secret Values、Aura、像素显示、Frame/Texture/StatusBar、事件与性能、安全限制；通用 UI 美化教程只留必要摘要。
2. 保留完整的通用 WoW 插件开发手册，包括皮肤、设置面板、滚动容器等暂时无关主题。
3. 只保留 Secret Values 与 Aura，删除其他知识。

➡️ 推荐答案：**Q4-1**。

---

❓ **Q5 - 技术事实处理**：现有资料包含 PTR 周报、AI 指南和可能过时的结论，应如何整理？

1. **校验后收录（推荐）**：以指定版本的本地源码和版本变更记录交叉验证；无法确认的内容明确标成“待验证”，不写成强制规则。
2. 只做语言和结构编辑，默认保留所有现有技术结论。
3. 删除所有不能直接从当前 `/wow-ui-source` 证明的内容。

➡️ 推荐答案：**Q5-1**。兼顾可靠性和变更记录的价值。

---

❓ **Q6 - 文件命名语言**：“上述文件都应该是中文”是否包括文件名和技术标识符？

1. **中文正文、英文文件名与技术标识符（推荐）**：例如 `.spec/pixel-protocol.md`，正文全部中文；类名、字段名、API 名保持英文。
2. 正文和普通文档文件名都使用中文；仅 `README.md`、`AGENTS.md` 等约定文件保留英文名。
3. 尽可能连配置字段和插件标识符也中文化。

➡️ 推荐答案：**Q6-1**。ASCII 路径更适合跨 Windows、WSL、Git 与 Agent 工具链协作。

---

❓ **Q7 - 根 README**：当前 `README.md` 只有标题和版本说明，其未提交差异只是换行符变化。是否纳入本次改写？

1. **纳入并改为中文项目入口（推荐）**：介绍目标、工作流、平台、文档导航和当前阶段。
2. 保留根 README 原样，将完整说明放入 `.spec/project-overview.md`。
3. 根 README 和独立项目说明都写完整内容。

➡️ 推荐答案：**Q7-1**。避免两个完整入口逐渐产生冲突。

---

❓ **Q8 - 第三方源码克隆方式**：三个缺失仓库如何初始化？

1. **浅克隆指定分支（推荐）**：使用 SSH、`--branch`、`--single-branch`、`--depth 1`；保留现有 `/wow-ui-source` 原样。
2. 完整克隆指定分支及其历史；保留现有 `/wow-ui-source` 原样。
3. 完整克隆，并尝试同步 `/wow-ui-source` 到远端 `ptr`。

➡️ 推荐答案：**Q8-1**。这些仓库用于源码参考，不需要历史；现有 `/wow-ui-source` 的额外本地提交属于用户档案，不能重置。
~~~~

**用户回答 1**

~~~~text
Q1-1。先冻结架构和规则，再开始代码工程。
Q2-1。不同规则的变更频率与阅读场景不同，拆分后更适合 Agent 按需读取。
Q3: 都不选 .context目录直接保留英文，精编就行。我怕翻译产生错误，小错误积累也是大错误
Q4-1: 以 Phantom 需求为中心（推荐）：重点保留 12.1 API、Secret Values、Aura、像素显示、Frame/Texture/StatusBar、事件与性能、安全限制；
Q5-1:校验后收录（推荐）：以指定版本的本地源码和版本变更记录交叉验证；无法确认的内容明确标成“待验证”，不写成强制规则。
Q6：既然Q3决定，那么.context这些第三方经验/资料，就保持英文。
Q7-2： 保留根 README 原样，将完整说明放入 .spec/project-overview.md。readme.md最终是给用户看的。
Q8 浅克隆指定分支，注意这些第三方源码未来不需要写入。
~~~~

**问题轮次 2**

~~~~text
第二轮聚焦文档落盘形态和权威边界。请继续按 `Q9-1、Q10-1……` 回复。

❓ **Q9 - `.context` 精编方式**：英文资料具体如何压缩？

1. **合并为少量专题文件（推荐）**：先把现有 42 份原稿打包到项目目录之外，再替换为约 7 份英文专题文档。
2. 保持现有 42 个路径，逐份删减和校正。
3. 保留全部原文不动，另加约 7 份英文摘要。

建议专题：入口索引、12.1 变更、Secret Values、Aura、渲染组件、事件与性能、安全与 API 查询。

➡️ 推荐答案：**Q9-1**。信息最集中，同时仓库外备份可以防止未跟踪原稿丢失。

---

❓ **Q10 - `.spec` 文件集合**：是否采用下面的规范结构？

1. **八份分层规范（推荐）**：
   - `README.md`：规范入口、权威顺序、按任务阅读路径
   - `project-overview.md`：项目定位、目标、平台、边界
   - `architecture.md`：Python/Lua 数据回路、模块与目录
   - `pixel-protocol.md`：四行布局和三种输出模式
   - `plugin-system.md`：条件、行为、截图插件契约与版本兼容
   - `configuration.md`：YAML 数据结构与示例
   - `development-rules.md`：代码风格、API 查询、第三方源码规则
   - `testing.md`：WSL/Windows 测试边界与有效测试原则
2. 合并为四份：总览、架构、协议、开发规则。
3. 由我根据内容密度自行决定最终拆分，并在计划中记录理由。

➡️ 推荐答案：**Q10-1**。

---

❓ **Q11 - 未确定内容**：草案中存在尚未定义的协议细节和 UI 空项，规范如何表达？

1. **显式列为“待定事项”（推荐）**：只把已确认内容写成规则；Agent 不得把待定项当成事实或自行扩展。
2. 暂时从规范中完全省略，等开发时再补。
3. 授权我为所有待定项选择合理默认值并直接冻结。

➡️ 推荐答案：**Q11-1**。这样既保存设计边界，也不会让猜测变成规则。

---

❓ **Q12 - WoW 版本边界**：知识与规范面向哪个兼容范围？

1. **面向 12.1 系列（推荐）**：易变事实记录核验日期和源码修订；未来小版本变动时重新核验。
2. 只面向当前 12.1.0 / Build 69587，不承诺后续 12.1.x。
3. 同时覆盖 12.0 和 12.1，并保留版本分支说明。

➡️ 推荐答案：**Q12-1**。

---

❓ **Q13 - 第三方源码只读约束**：“未来不需要写入”如何落实？

1. **规则约束（推荐）**：在规范和 `AGENTS.md` 中禁止修改、提交、切分支、拉取或重置；只有用户明确要求更新时才可写入。不修改文件权限。
2. 除规则约束外，对仓库执行递归只读权限设置。
3. 只说明它们是参考资料，不设置明确禁止行为。

➡️ 推荐答案：**Q13-1**。不会妨碍工具读取，也避免权限变化影响 Git。

---

❓ **Q14 - `AGENTS.md` 的职责**：它应包含多少规则正文？

1. **任务路由为主（推荐）**：声明权威顺序、强制阅读入口、按任务指向对应 `.spec` / `.context` 文件，只保留少量不可遗漏的总规则。
2. 在 `AGENTS.md` 中重复所有核心规范，使其可以独立阅读。
3. 只列文件链接，不写权威顺序或读取条件。

➡️ 推荐答案：**Q14-1**。避免 `AGENTS.md` 与规范副本逐渐不一致。
~~~~

**用户回答 2**

~~~~text
Q9-1 合并为少量专题文件（推荐）：先把现有 42 份原稿打包到项目目录之外，再替换为约 7 份英文专题文档。
Q10-1 八份分层规范（推荐）
Q11-1 显式列为“待定事项”（推荐）：只把已确认内容写成规则；Agent 不得把待定项当成事实或自行扩展。
Q12-1 面向 12.1 系列（推荐）：易变事实记录核验日期和源码修订；未来小版本变动时重新核验。
Q13-1  规则约束
Q14-1 Agents.md只是路由。
~~~~

**问题轮次 3**

~~~~text
第三轮确定未来实现必须遵守的核心契约。请按 `Q15-1、Q16-1……` 回复。

❓ **Q15 - 配置字段规范**：草案中的拼写、命名和引用方式如何定稿？

1. **现在统一修正（推荐）**：字段统一为 `snake_case`；修正 `unitTalnet`、`bing_key` 等拼写；列表使用真正的 YAML 数组；配置对象同时具有稳定英文 `key` 和可修改的中文 `title`。草案不视为旧版兼容契约。
2. 原样保留草案字段，避免偏离最初设计。
3. 新旧字段都接受，并在规范中定义别名。

➡️ 推荐答案：**Q15-1**。目前没有已发布配置，正是清理格式的最佳时点。

---

❓ **Q16 - 宏与行为插件关系**：二者如何分工？

1. **宏是配置数据，行为插件负责执行（推荐）**：`macros` 定义宏文本、按键及是否绑定；循环通过稳定 `key` 选择宏；`post_message@1.0` 将对应按键发送给游戏窗口。
2. 取消独立 `macros`，每个可执行项都定义成行为插件实例。
3. 暂不确定，只保留草案原文。

➡️ 推荐答案：**Q16-1**。这与“目前只有 PostMessage 行为插件”的设想最一致，也能把游戏宏定义和 Windows 输入实现分开。

---

❓ **Q17 - 配置版本**：是否从第一版开始声明配置格式版本？

1. **加入 `schema_version: 1`（推荐）**：未来升级由显式迁移处理，不靠猜测字段形状。
2. 暂时不加版本，等第一次破坏性变更时再补。
3. 直接使用项目版本号作为配置格式版本。

➡️ 推荐答案：**Q17-1**。

---

❓ **Q18 - 像素协议成熟度**：本次是否要冻结尚未给出的底层编码细节？

1. **冻结逻辑协议，隔离底层待定项（推荐）**：确认四行布局、三种输出类型、尺寸和用途；颜色通道、采样算法、校验、哈希位映射等留在“待定事项”。
2. 本次必须把所有底层编码细节一并决定并冻结。
3. 像素协议整份都只作为草案，不形成任何规则。

➡️ 推荐答案：**Q18-1**。现有输入足以确定架构，但不足以安全推导每一位的含义。

---

❓ **Q19 - 横向布局**：四行中的元素如何排列？

1. **每行独立、从左到右确定性紧密排列（推荐）**：通用 Cell、条件 Cell、Value Bar、Icon Tile 分别按各自声明顺序排列；总画布宽度取四行最大宽度。
2. 四行共享统一列网格，不同类型必须纵向对齐。
3. 本次只固定行高和总高度，横向布局列为待定。

➡️ 推荐答案：**Q19-1**。

---

❓ **Q20 - Lua 生成粒度**：“按需生成”具体指什么？

1. **每份 rotation 配置生成一个独立插件包（推荐）**：只组合该配置引用的条件模板、通用渲染代码和所需宏绑定。
2. 生成一个包含全部条件插件的通用 WoW 插件，运行时选择配置。
3. 每个条件实例生成独立 Lua 文件，由游戏内代码动态组合。

➡️ 推荐答案：**Q20-1**。

---

❓ **Q21 - 插件版本兼容**：`health_pct@1.0` 这类版本如何解析？

1. **精确版本并存（推荐）**：配置必须写完整插件标识；运行时只加载完全匹配的目录；旧版本可以长期并存；不自动回退、不自动升级。
2. 使用兼容版本回退，例如找不到 `1.1` 时可尝试同一主版本的其他版本。
3. 目录只保留最新版本，旧配置通过迁移脚本升级。

➡️ 推荐答案：**Q21-1**。

---

❓ **Q22 - PySide6 UI**：本轮文档对尚未描述的 UI 做到什么程度？

1. **只固定技术和参考边界（推荐）**：确认使用 PySide6、参考旧 Terminal；页面、交互和视觉设计全部列为后续 UI 任务。
2. 要求未来 UI 尽量一比一复刻旧 Terminal。
3. 本次继续访谈并完整定义 UI 页面和交互。

➡️ 推荐答案：**Q22-1**。当前任务先冻结架构与规则，UI 需求尚不足以形成可靠规范。
~~~~

**用户回答 3**

~~~~text
Q15-1 字段统一为 snake_case；修正 unitTalnet、bing_key 等拼写；列表使用真正的 YAML 数组；配置对象同时具有稳定英文 key 和可修改的中文 title。草案不视为旧版兼容契约。
Q16-1 这里解释下，lua有创造宏，然后绑定k的能力，也就是给某个按键组合绑定某个宏。自动化工具都是这么做的。所以必须存在一个按键宏文本的对应关系。但是本项目允许不绑定宏，就是选一个不需要绑定的按键。游锡内已有的按键。
Q17-1 加入 schema_version: 1（推荐）：未来升级由显式迁移处理，不靠猜测字段形状。
Q18-1 冻结逻辑协议，隔离底层待定项（推荐）
Q19-1 每行独立、从左到右确定性紧密排列（推荐）：通用 Cell、条件 Cell、Value Bar、Icon Tile 分别按各自声明顺序排列；总画布宽度取四行最大宽度。
Q20 - Lua 生成粒度：“按需生成”具体指什么？
    - 我设想是这样的。生成一个插件。
    - 插件的基础模块是通用的。
    - 不同的 rotation 生成不同的lua文件。 lua文件名是 rotation 的uuid。因为没份 rotation 都限制了unitClass、unitSpec、unitTalnet。所以如果不匹配。就return。没加载后续部分。
    - 如果2个rotation拥有相同的unitClass、unitSpec、unitTalnet组合，那么需要生成插件前，勾选好。
    - 生成插件前，勾选rotation列表，一次性生成包含多个rotation的插件。
    - 基础模块部分会要求天赋变更后reload。
Q21-1 - 插件版本兼容：health_pct@1.0 这类版本如何解析？精确版本。因为做好后分享给别人，作者本身就测试了。不存在版本不存在的情况。
Q22 - PySide6 UI：本轮文档对尚未描述的 UI 做到什么程度？
    - 只固定技术和参考边界（推荐）：确认使用 PySide6。
    - 界面并未打算参考Terminal
~~~~

**问题轮次 4**

~~~~text
本地 12.1 源码确认了宏创建、键位保存和绑定相关机制仍存在，但没有提供完整的全局 API 契约文档；因此规范会记录业务意图，并把具体调用时机与受保护状态标为实现前复核项。

第四轮确定 rotation 配置与运行语义。

❓ **Q23 - 配置文件边界**：一份 YAML 表示什么？

1. **一份 YAML 对应一份 rotation（推荐）**：顶层包含 `schema_version`、`uuid`、`profile`、`conditions`、`macros`、`rotation`；删除数字 `id`，使用唯一 `key` 引用，列表顺序就是布局或执行顺序。
2. 一份 YAML 对应一份 rotation，但同时保留数字 `id` 和英文 `key`。
3. 一份 YAML 可以包含多份 rotation。

➡️ 推荐答案：**Q23-1**。

---

❓ **Q24 - 条件表达式**：rotation 如何引用条件？

1. **使用稳定 `key` 的小型表达式语言（推荐）**：例如 `player_health_pct < 70 and holy_light_cooldown == 0`；仅支持比较、`and`、`or`、`not` 和括号，由专用解析器处理，禁止直接 `eval`。
2. 像草案一样直接用中文 `title` 作为变量名。
3. 不使用表达式字符串，改成嵌套 YAML 逻辑树。

➡️ 推荐答案：**Q24-1**。兼顾可读性、AI 编辑体验和稳定引用。

---

❓ **Q25 - 循环命中规则**：一次循环有多个条件成立时如何执行？

1. **按列表从上到下，首个成立项胜出（推荐）**：每轮最多发送一个按键；没有命中则不执行动作。
2. 执行本轮所有成立项。
3. 增加显式数字 `priority`，按优先级执行首个成立项。

➡️ 推荐答案：**Q25-1**。列表本身已经清楚表达优先级。

---

❓ **Q26 - 暂停语义**：项目说明提到循环结果可能是“暂停”，它属于哪一层？

1. **Python 核心运行状态（推荐）**：暂停后不再发送按键；它不是 rotation 中的宏或特殊动作。暂停期间是否继续截图和刷新 UI 留待运行时设计。
2. 在 rotation 中定义特殊的 `pause` 动作。
3. 本次完全不定义暂停，将其列为待定概念。

➡️ 推荐答案：**Q26-1**。

---

❓ **Q27 - 天赋匹配**：`unit_talents` 列表如何判断生效？

1. **全部包含匹配（推荐）**：角色必须学会配置列出的所有天赋；允许角色拥有额外天赋；空列表表示不限制天赋。
2. 精确集合匹配：角色天赋必须与列表完全相同。
3. 任一包含匹配：学会列表中任意一个天赋即可。

➡️ 推荐答案：**Q27-1**。

---

❓ **Q28 - rotation 激活冲突**：勾选的多份 rotation 具有相同职业、专精和天赋条件时怎么办？

1. **生成前拒绝冲突（推荐）**：界面要求用户在冲突组中只保留一份；不生成可能同时激活的插件。
2. 允许生成，按勾选顺序只激活第一份。
3. 允许多份同时加载和运行。

➡️ 推荐答案：**Q28-1**。

---

❓ **Q29 - `/reload` 边界**：哪些角色配置变化要求重新加载插件？

1. **专精或天赋变化都要求 `/reload`（推荐）**：rotation 文件只在插件加载时判断激活条件，不做运行时热切换。
2. 仅天赋变化要求 `/reload`，专精变化可自动切换。
3. 专精和天赋都支持运行时自动切换。

➡️ 推荐答案：**Q29-1**。与 rotation 文件的加载早退模型一致。

---

❓ **Q30 - `bind_key: false` 时的宏文本**：未绑定宏的条目如何定义？

1. **`key` 必填，`macro_text` 可选且不生效（推荐）**：`title` 描述该按键用途；Python 直接发送玩家已有游戏键位。
2. `key` 和 `macro_text` 仍都必填，但 Lua 忽略宏文本。
3. 不允许省略绑定；每个 rotation 动作都必须由插件创建宏。

➡️ 推荐答案：**Q30-1**。

---

❓ **Q31 - 键位冲突风险**：`bind_key: true` 可能覆盖玩家已有绑定，如何处理？

1. **配置即显式授权，但必须可见（推荐）**：生成前检查所选配置内部的重复按键；插件绑定时记录清晰结果。是否能可靠读取游戏已有绑定，留给实现前 API 核验。
2. 只有确认游戏内按键当前未绑定时才允许绑定，否则拒绝。
3. 直接覆盖，不检查也不提示。

➡️ 推荐答案：**Q31-1**。

---

❓ **Q32 - 未来代码注释语言**：插件注释标准使用什么语言？

1. **中文业务注释与标准化头部（推荐）**：代码标识符保持英文；插件头部说明用途、参数、输出类型与尺寸、WoW API 来源、Secret Value 风险和版本变更。
2. 所有代码注释和头部都用英文。
3. 不规定注释语言，只规定必填信息。

➡️ 推荐答案：**Q32-1**。与项目中文规范一致，同时不影响英文代码生态。
~~~~

**用户回答 4**

~~~~text
Q23-1 - 配置文件边界：一份 YAML 表示什么？

一份 YAML 对应一份 rotation（推荐）：顶层包含 schema_version、uuid、profile、conditions、macros、rotation；删除数字 id，使用唯一



Q24-2 - 条件表达式：rotation 如何引用条件？

- 像草案一样直接用中文 title 作为变量名。这样最好读
- conditions的title就是做这个作用的，title会是唯一的。
- 相反，player_health_pct这样的名字没有地方定义。

应该说存在一个字典 

conditions[title]  = 条件类(参数，位置)
比如
conditions["玩家血量"]  = HealthPct({"unitToken":"player"},x=cell坐标)



Q25-1 - 循环命中规则：一次循环有多个条件成立时如何执行？

按列表从上到下，首个成立项胜出（推荐）：每轮最多发送一个按键；没有命中则不执行动作。




Q26 - 暂停语义：项目说明提到循环结果可能是“暂停”，它属于哪一层？

假设循环每秒执行10次，暂停就是那次没动作，不向游戏发送按键。比如没人掉血，怪不存在等等。


Q27 - 天赋匹配：unit_talents 列表如何判断生效？

后续我会写lua实现，就是清单里的每个spellid，玩家都会的意思
注：魔兽世界里，天赋=被动技能。可以使用检测技能是否学会来判断。

Q28 - rotation 激活冲突：勾选的多份 rotation 具有相同职业、专精和天赋条件时怎么办？

在勾选的gui界面上，每个职业，每个专精，只能勾选一个。
我收回之前的设计，不再判断天赋。其实这样足够了。每个职业，每个专精，只能勾选一个。勾选一个，另一个就取消勾选，在ui层面实现就行。


Q29 - /reload 边界：哪些角色配置变化要求重新加载插件？

专精或天赋变化都要求 /reload（推荐）
这个现在不实现，很容易后续做。

Q30 - bind_key: false 时的宏文本：未绑定宏的条目如何定义？

key 必填，macro_text 可选且不生效（推荐）：title 描述该按键用途；Python 直接发送玩家已有游戏键位。

因为哪怕macro_text填了，也不能覆盖玩家原本的键位。如果选择了bind_key=false，就不会生成这项的key + macro text的绑定lua代码。

 Q31-3 - 键位冲突风险：bind_key: true 可能覆盖玩家已有绑定，如何处理？
  直接覆盖，不检查也不提示。
  一半来说，配置开发人员会使用一些冷门按键。就比如 https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/rotation/PriestDiscipline.py 


Q32-1 - 未来代码注释语言：插件注释标准使用什么语言？

中文业务注释与标准化头部（推荐）：代码标识符保持英文；插件头部说明用途、参数、输出类型与尺寸、WoW API 来源、Secret Value 风险和版本变更。
~~~~

**问题轮次 5**

~~~~text
已核对你给出的旧 rotation：它确实大量使用 `ALT-NUMPAD1`、`SHIFT-F8`、`SHIFT-,` 等冷门组合键，支持你所说的配置作者主动避让常用键位的设计判断。

第五轮用于消除天赋修订和中文标题引用带来的歧义。

❓ **Q33 - `unit_talents` 最终角色**：你在 Q28 撤回了按天赋判断的设计，配置格式应如何调整？

1. **从 schema v1 删除 `unit_talents`（推荐）**：rotation 只按 `unit_class` 与 `unit_spec` 激活；天赋路由作为未来待定功能。
2. 保留 `unit_talents` 作为说明性元数据，但不参与 Lua 激活判断。
3. 保留并参与 Lua 判断：列出的每个法术都必须已学会；只是 GUI 仍限制每个职业/专精只能选择一份。

➡️ 推荐答案：**Q33-1**。这最直接地落实“现在不再判断天赋”。

---

❓ **Q34 - 对象标识方式**：Q24 改为中文标题引用后，还需要英文 `key` 吗？

1. **条件和宏都只用唯一中文 `title`（推荐）**：不再设置英文 `key`；条件字典、宏字典和 rotation 引用都以标题为键。
2. 条件只用中文 `title`，宏仍保留英文 `key`。
3. 条件和宏仍同时包含英文 `key` 与中文 `title`，但表达式显示中文标题。

➡️ 推荐答案：**Q34-1**。这与“title 就是为字典引用而存在”的说明一致。

---

❓ **Q35 - 条件标题限制**：直接把标题写进表达式时，如何避免解析歧义？

1. **保留自然中文标题并限制语法字符（推荐）**：标题必须非空且唯一，可以包含中文、英文、数字和普通空格，但不能包含比较符、括号、引号，也不能等于 `and`、`or`、`not`；解析器按已注册标题精确识别。
2. 标题必须是无空格、无标点的连续文字。
3. 引用时加定界符，例如 `[玩家血量] < 70`，标题本身不受限制。

➡️ 推荐答案：**Q35-1**。保留草案的自然可读形式，同时给解析器明确边界。

---

❓ **Q36 - 表达式能力**：第一版条件语言支持哪些值和操作？

1. **比较与布尔组合（推荐）**：支持数字、布尔值、带引号字符串；支持 `<`、`<=`、`>`、`>=`、`==`、`!=`、`and`、`or`、`not` 和括号；不支持算术、函数调用或任意 Python。
2. 只支持数字比较与布尔组合。
3. 支持完整 Python 表达式。

➡️ 推荐答案：**Q36-1**。

---

❓ **Q37 - 激活和重载模型**：若删除天赋判断，rotation Lua 如何激活？

1. **加载时只检查职业和专精（推荐）**：不匹配即提前 `return`；切换专精后需要 `/reload`；未来若重新加入天赋判断，再扩展重载规则。
2. 加载时检查职业和专精，但专精切换可立即热切换。
3. Lua 不检查职业和专精，完全信任生成界面的选择。

➡️ 推荐答案：**Q37-1**。

---

❓ **Q38 - GUI 互斥范围**：每个职业/专精只能勾选一份，具体行为是？

1. **组合互斥（推荐）**：同一 `unit_class + unit_spec` 组合只能选择一份；选择新项时自动取消该组合的旧项；其他职业或专精不受影响。
2. 每个职业只能选择一份，不区分专精。
3. 允许重复选择，但生成时只取最后一份。

➡️ 推荐答案：**Q38-1**。

---

❓ **Q39 - 循环频率**：“每秒执行 10 次”是要求还是举例？

1. **只是举例（推荐）**：本轮只定义循环语义，实际频率、节流和配置方式列为待定。
2. 固定为 10 Hz。
3. 默认 10 Hz，但允许配置覆盖。

➡️ 推荐答案：**Q39-1**。

---

❓ **Q40 - 按键字符串格式**：配置采用哪种写法？

1. **采用 WoW 风格连字符（推荐）**：例如 `ALT-NUMPAD1`、`SHIFT-F8`；Python 端负责映射为 Windows 输入。
2. 采用加号，例如 `ALT+NUMPAD1`、`SHIFT+F8`。
3. 两种格式都接受并在加载时标准化。

➡️ 推荐答案：**Q40-1**。与你给出的旧项目实际键位表一致。

---

❓ **Q41 - 绑定持久性**：`bind_key: true` 创建的绑定应保存到哪里？

1. **保存到玩家当前使用的 WoW 键位集合（推荐）**：生成 Lua 使用当前账号级或角色级集合，不擅自切换集合；绑定持续到玩家再次修改。
2. 只做插件生命周期内的临时覆盖，退出或禁用插件后消失。
3. 本轮只记录“需要绑定”，具体持久性列为待定并等待实现前验证。

➡️ 推荐答案：**Q41-1**。这与自动化配置一次生成、长期使用的模式更一致。
~~~~

**用户回答 5**

~~~~text
Q33-1 - unit_talents 最终角色：你在 Q28 撤回了按天赋判断的设计，配置格式应如何调整？

从 schema v1 删除 unit_talents（推荐）：rotation 只按 unit_class 与 unit_spec 激活；天赋路由作为未来待定功




Q34 - 对象标识方式：Q24 改为中文标题引用后，还需要英文 key 吗？

我觉得你的理解有误

以下文的rotation1号为例。
rotation.1.condition里的条件是中文，正好对应到conditions的title。
rotation.1.macro的中文，正好对应到macro的name。

这里的部分，只是字符串，循环是用户写的，爱用英文就英文，愿意中文就中文，只要对上了就行。

macro的key是键盘的物理按键，肯定是英文的，还必须是加号分割的大写。

rotation:  循环开始
  - id:1    -- 序号
  - condition: (玩家血量 < 70) and (圣光术冷却时间 =0 0)
  - macro: 对玩家释放是圣光术


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


macro:      -- 游戏里的宏
  - name:对玩家释放是圣光术        -- 名字，对应action
    macro_text: /cast [@player] 圣光术
    key: ALT+F4           -- 宏绑定的按键，生成lua会在游戏内绑定按键，python端也会发送这个按键。
    bing_key:true        --  是否绑定宏。


  ———

Q35-1 - 条件标题限制：直接把标题写进表达式时，如何避免解析歧义？

保留自然中文标题并限制语法字符（推荐）：标题必须非空且唯一，可以包含中文、英文、数字，也不能包括空格。不能包含比较符、括号、引号，也不能等于 and、or、not；解析器按已注册标题精确识别，



  ———

Q36 - 表达式能力：第一版条件语言支持哪些值和操作？

值可能是布尔，浮点、证书，字符串。
那就要 <、<=、>、>=、==、!=、and、or、not 、还需要补上in。  某个图标的hash in [一组图标的哈希,]
   

Q37-1 - 激活和重载模型：若删除天赋判断，rotation Lua 如何激活？

加载时只检查职业和专精（推荐）：不匹配即提前 return；切换专精后需要 /reload；未来若重新加入天赋判断，再扩展重载规则。


Q38 - GUI 互斥范围：每个职业/专精只能勾选一份，具体行为是？

UI界面做个表格，第一列是多选框。勾选某一个相同专精的，会取消勾选其他相同专精的。

  ———

Q39-1 - 循环频率：“每秒执行 10 次”是要求还是举例？

只是举例（推荐）：本轮只定义循环语义，实际频率、节流和配置方式列为待定。



Q40-1- 按键字符串格式：配置采用哪种写法？

采用 WoW 风格连字符（推荐）：例如 ALT-NUMPAD1、SHIFT-F8；Python 端负责映射为 Windows 输入。




Q41-1 - 绑定持久性：bind_key: true 创建的绑定应保存到哪里？

参考我写过的代码 https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/DejaVu/DejaVu_DeathKnight/Blood/Macro.lua

使用下面的lua代码，wow的SecureActionButtonTemplate会帮按键绑定到一个看不见的按钮上。这个按钮关联了macrotext。所有战斗自动化脚本都是这么工作的。

local buttonName = addonName .. "Button" .. macro.title
local frame = CreateFrame("Button", buttonName, UIParent, "SecureActionButtonTemplate")
frame:SetAttribute("type", "macro")
frame:SetAttribute("macrotext", macro.text)
frame:RegisterForClicks("AnyDown", "AnyUp")
SetOverrideBindingClick(frame, true, macro.key, buttonName)
print("RegMacro[" .. macro.title .. "] > " .. macro.key .. " > " .. macro.text)
~~~~

**问题轮次 6**

~~~~text
第六轮主要解决字段名和格式中最后几处冲突。

❓ **Q42 - 按键分隔符**：你先强调“必须用加号分割”，随后又选择了连字符；最终以哪个为准？

1. **YAML 使用大写加号格式，生成时转换（推荐）**：配置写 `ALT+NUMPAD1`；Lua 生成器转换为 WoW 所需的 `ALT-NUMPAD1`；Python 行为插件也从同一格式映射 Windows 输入。
2. YAML 直接使用 WoW 连字符格式，例如 `ALT-NUMPAD1`，Python 端解析同一字符串。
3. 加号和连字符都接受，加载后统一规范化。

➡️ 推荐答案：**Q42-1**。既满足你对配置格式的明确要求，也兼容已验证的 WoW Lua 写法。

---

❓ **Q43 - 宏集合字段名**：顶层使用单数还是复数？

1. **顶层使用 `macros`（推荐）**：因为它是列表；每个循环项仍写 `macro: 宏名称`。
2. 顶层沿用草案的 `macro`。
3. 顶层改名为 `key_bindings`。

➡️ 推荐答案：**Q43-1**。

---

❓ **Q44 - `in` 表达式细节**：成员判断如何定义？

1. **同时支持 `in` 与 `not in`（推荐）**：右侧是由整数、浮点数、布尔值或字符串组成的 YAML 风格列表字面量；禁止嵌套列表和混合类型。优先级为 `not` → 比较/成员判断 → `and` → `or`。
2. 只支持 `in`，不支持 `not in`；其他限制相同。
3. 本次只记录需要 `in`，具体语法全部待定。

➡️ 推荐答案：**Q44-1**。

---

❓ **Q45 - UUID 格式**：rotation 的 UUID 如何约束？

1. **标准 UUID 字符串（推荐）**：使用带连字符的 RFC 4122 文本；生成文件名固定为 `<uuid>.lua`。
2. 接受任意由用户填写的唯一字符串。
3. 使用递增数字代替 UUID。

➡️ 推荐答案：**Q45-1**。

---

❓ **Q46 - `unit_spec` 含义**：草案写“专精 ID”，但示例值和旧 Lua 使用的是 `GetSpecialization()` 返回的顺序索引。

1. **使用专精顺序索引（推荐）**：即 `GetSpecialization()` 的 `1`、`2`、`3`、`4`。
2. 使用全局 specialization ID，例如 `GetSpecializationInfo()` 返回的专精编号。
3. 同时记录索引和全局 ID。

➡️ 推荐答案：**Q46-1**。与你现有 Lua 的 `currentSpec ~= 1` 判断一致。

---

❓ **Q47 - 插件标识命名**：三个插件族的目录名如何统一？

1. **小写 snake_case，区分大小写（推荐）**：例如 `health_pct@1.0`、`post_message@1.0`、`gdi@1.0`。
2. 保留行为插件的类名式写法 `PostMessage@1.0`，其他插件小写。
3. 使用 kebab-case，例如 `health-pct@1.0`。

➡️ 推荐答案：**Q47-1**。

---

❓ **Q48 - 生成插件包名称**：本次是否确定 WoW 插件目录和 TOC 名称？

1. **暂列为待定（推荐）**：本轮只冻结“共享基础模块 + UUID rotation 文件”的结构，具体包名在生成器任务中决定。
2. 固定为 `PhantomGenerated`。
3. 每次生成时由用户输入包名。

➡️ 推荐答案：**Q48-1**。

---

❓ **Q49 - 条件插件输出数量**：一个条件实例可以占用多少输出区域？

1. **一个实例声明一个连续输出区域（推荐）**：插件元数据声明 `cell`、`value_bar` 或 `icon_tile` 之一及其尺寸；生成器据此分配位置。通用 Cell 由基础模块负责，不属于条件实例。
2. 一个条件实例可以声明多个不同类型的输出区域。
3. 本次不定义条件实例与输出区域的数量关系。

➡️ 推荐答案：**Q49-1**。

---

❓ **Q50 - 第一行通用 Cell**：当前尚未给出其具体字段，本轮如何处理？

1. **保留第一行和职责，字段清单列为待定（推荐）**：后续核心运行协议任务再定义。
2. 本轮继续访谈并确定所有通用 Cell。
3. 删除“通用 Cell”概念，所有 Cell 都由条件插件生成。

➡️ 推荐答案：**Q50-1**。保持四行架构，同时不凭空发明字段。
~~~~

**用户回答 6**

~~~~text
Q42 - 按键分隔符：你先强调“必须用加号分割”，随后又选择了连字符；最终以哪个为准？

 YAML 直接使用 WoW 连字符格式，例如 ALT-NUMPAD1，Python 端解析同一字符串。



Q43 - 宏集合字段名：顶层使用单数还是复数？

顶层使用 macros（推荐）：因为它是列表；每个循环项仍写 macro: 宏名称。



Q44 - in 表达式细节：成员判断如何定义？

同时支持 in 与 not in（推荐）：右侧是由整数、浮点数、布尔值或字符串组成的 YAML 风格列表字面量；禁止嵌套列表和混合类型。优先级为 not → 比较/成员判断 → and → or。

这里我要说下，每个条件，都会做成一个python的类。每次条件的使用，说白了都是这个类的实例化，python类有足够的能力做这些不是么。



Q45 - UUID 格式：rotation 的 UUID 如何约束？

标准 UUID 字符串（推荐）：使用带连字符的 RFC 4122 文本；生成文件名固定为 <uuid>.lua。


Q46 - unit_spec 含义：草案写“专精 ID”，但示例值和旧 Lua 使用的是 GetSpecialization() 返回的顺序索引。

使用专精顺序索引（推荐）：即 GetSpecialization() 的 1、2、3、4。


Q47 - 插件标识命名：三个插件族的目录名如何统一？

小写 snake_case，区分大小写（推荐）：例如 health_pct@1.0、post_message@1.0、gdi@1.0。



Q48 - 生成插件包名称：本次是否确定 WoW 插件目录和 TOC 名称？

每次生成时由用户输入包名。


Q49 - 条件插件输出数量：一个条件实例可以占用多少输出区域？

一个条件只能是cell、value_bar、icon_tile之一。
但是一个条件可以占用多个cell、value_bar，icon_tile。

比如有个条件是 敌人施法图标 那就是1个icon_tile，返回值是这个icon_tile的xxh3_64_hexdigest，比如'ef46db3751d8e999'
还有个条件是"敌人施法打断黑名单“，占用10个icon_tile，返回值是一个0-10长度的list  ，比如["ef46db3751d8e999","ef46db3333d32199"]
那我可以用 敌人施法图标 in 敌人施法打断黑名单这样的判断。

同样的，每个条件都可能返回的是list。虽然我还没想到其他用途。

Q50 - 第一行通用 Cell：当前尚未给出其具体字段，本轮如何处理？

保留第一行和职责，字段清单列为待定（推荐）：后续核心运行协议任务再定义。

我暂时只想到了，脚本启停状态、延迟状态、职业、专精、是否在战斗等通用选项。还没想到其他的。
~~~~

**问题轮次 7**

~~~~text
第七轮将条件插件的“像素输出”和“Python 值”分开定义，避免把多像素误认为一定返回列表。

❓ **Q51 - 条件类职责**：条件实例如何参与循环？

1. **条件类负责完整转换（推荐）**：每个实例保存参数与像素位置、生成自己的 Lua、从截图区域解码出普通 Python 值；核心维护 `conditions[title] = instance`，表达式读取 `instance.value`。
2. 条件实例通过实现 `__lt__`、`__contains__` 等 Python 魔术方法直接参与运算。
3. 把实例字典直接传给 Python `eval`。

➡️ 推荐答案：**Q51-1**。条件插件可以充分使用 Python 能力，同时表达式执行仍有清晰、安全的边界。

---

❓ **Q52 - 输出契约声明**：如何描述“多个像素区域”和“标量或列表”？

1. **分别声明四项（推荐）**：
   - `output_type`：`cell` / `value_bar` / `icon_tile`
   - `output_count`：连续占用的同类区域数量
   - `value_type`：`bool` / `int` / `float` / `str`
   - `value_shape`：`scalar` / `list`

   多个区域既可以合成一个高精度标量，也可以解码成列表，具体由插件实现。
2. `output_count = 1` 固定返回标量，大于 1 固定返回列表。
3. 不声明值类型和形状，完全依靠运行时结果。

➡️ 推荐答案：**Q52-1**。像素数量和业务值形状本来就是两个独立维度。

---

❓ **Q53 - 动态输出尺寸**：`output_count` 在哪里确定？

1. **实例化后计算并冻结（推荐）**：插件先校验 `plugin_args`，再根据参数生成本实例的输出描述；布局完成后数量不可改变。
2. 每个插件版本写死一个固定数量，参数不能影响数量。
3. 运行过程中允许数量随战斗状态变化。

➡️ 推荐答案：**Q53-1**。既能支持“最多十个图标”，也保证屏幕布局稳定。

---

❓ **Q54 - 成员判断类型检查**：例如“施法图标 in 黑名单”如何验证？

1. **按插件声明预先检查（推荐）**：`in` / `not in` 的右侧必须声明为列表，左侧标量类型必须与列表元素类型一致；不做字符串或数字的隐式转换。
2. 不预先检查，完全采用 Python 运行时行为。
3. 自动在字符串、整数和浮点数之间转换。

➡️ 推荐答案：**Q54-1**。

---

❓ **Q55 - 不可用值**：像素缺失、Cell 被清除或条件暂时不可读时返回什么？

1. **支持 `null` / Python `None`（推荐）**：插件可声明结果允许为空；DSL 支持 `== null` 和 `!= null`；其他比较及成员判断遇到空值均视为不成立，不抛出循环错误。
2. 每个插件自行选择 `false`、`0`、空字符串或空列表作为默认值。
3. 遇到不可用值立即终止整个循环。

➡️ 推荐答案：**Q55-1**。不会把“不可用”错误解释成合法的零值。

---

❓ **Q56 - 多区域列表顺序**：十个 Icon Tile 如何形成长度 0–10 的列表？

1. **按屏幕区域从左到右（推荐）**：依次解码已占用槽位，空槽位不加入结果；列表顺序与非空区域顺序一致。
2. 始终返回固定长度列表，空槽位写 `null`。
3. 由每个插件自行定义，核心不规定顺序。

➡️ 推荐答案：**Q56-1**。

---

❓ **Q57 - 用户输入的插件包名**：允许什么格式？

1. **安全 ASCII 标识符（推荐）**：必须匹配 `[A-Za-z][A-Za-z0-9_]*`；目录名和 `.toc` 文件同名，展示标题以后可另行设置。
2. 允许中文、空格和常见标点，只禁止路径分隔符。
3. 本次不限制，生成时原样使用。

➡️ 推荐答案：**Q57-1**。

---

❓ **Q58 - 通用 Cell 候选项**：启停、延迟、职业、专精、战斗状态是否现在成为 v1 规则？

1. **仍作为待定候选（推荐）**：第一行和通用职责已冻结，但具体 Cell 直到数据方向和控制方式明确后再决定。
2. 将这五项全部固定为 v1 通用 Cell。
3. 只固定职业、专精和战斗状态；启停、延迟待定。

➡️ 推荐答案：**Q58-1**。目前尚不清楚“启停”和“延迟”是 Lua→Python 状态还是 Python 本地控制。
~~~~

**用户回答 7**

~~~~text
Q51 - 条件类职责：条件实例如何参与循环？

条件类负责完整转换（推荐）：每个实例保存参数与像素位置、生成自己的 Lua、从截图区域解码出普通 Python 值；核心维护 conditions[title] = instance，表达式读取 instance.value。


Q52 - 输出契约声明：如何描述“多个像素区域”和“标量或列表”？

  1. 分别声明四项（推荐）：
      - output_type：cell / value_bar / icon_tile
      - output_count：连续占用的同类区域数量
      - value_type：bool / int / float / str
      - value_shape：scalar / list

     多个区域既可以合成一个高精度标量，也可以解码成列表，具体由插件实现。



Q53 - 动态输出尺寸：output_count 在哪里确定？

实例化后计算并冻结（推荐）：插件先校验 plugin_args，再根据参数生成本实例的输出描述；布局完成后数量不可改变。

Q54 - 成员判断类型检查：例如“施法图标 in 黑名单”如何验证？

按插件声明预先检查（推荐）：in / not in 的右侧必须声明为列表，左侧标量类型必须与列表元素类型一致；不做字符串或数字的隐式转换。


Q55 - 不可用值：像素缺失、Cell 被清除或条件暂时不可读时返回什么？

每个插件自行选择 false、0、空字符串或空列表作为默认值。
每个插件设计时，要设计好兜底规则。
插件对象至少有raw_value和value共2个python方法。raw_value返回cell的r、g、b。 value_bar的长度百分比。 icon_tile的hash。
但是value 就不一样了，是包含计算，并且一定要给一个返回值的。
比如冷却时间异常，那就返回没冷却。
目标存在异常，那就返回不存在。
value还有计算只能，比如把冷却时间进行缩放。亮度0-100是0.1秒精度。100-120是1秒精度等等（lua端也要对应实现）

我的想法是，基类强制设置好一个兜底方法。制作插件时不覆盖这个方法不行。


Q56 - 多区域列表顺序：十个 Icon Tile 如何形成长度 0–10 的列表？

对于icon_tile来说，哪里全黑就是没有图标。
如果是raw_value，用None占位list
但如果是value，应该是排除掉的。
所以应该是 由每个插件自行定义，核心不规定顺序

Q57 - 用户输入的插件包名：允许什么格式？

安全 ASCII 标识符（推荐）：必须匹配 [A-Za-z][A-Za-z0-9_]*；目录名和 .toc 文件同名，展示标题以后可另行设置。

Q58 - 通用 Cell 候选项：启停、延迟、职业、专精、战斗状态是否现在成为 v1 规则？

仍作为待定候选（推荐）：第一行和通用职责已冻结，但具体 Cell 直到数据方向和控制方式明确后再决定。
~~~~

**问题轮次 8**

~~~~text
第八轮只剩条件基类与表达式执行边界；这些决定完成后，我预计可以给出完整的共同理解摘要。

❓ **Q59 - 条件基类模板**：`raw_value`、`value` 和兜底如何组织？

1. **基类控制固定流程（推荐）**：
   - 基类公开 `raw_value()`，按输出描述读取原始区域；
   - 基类公开 `value()`，调用插件实现的 `decode_value(raw)`；
   - 原始值不可用时调用插件必须实现的抽象方法 `fallback_value()`；
   - 插件缺少解码或兜底实现时无法实例化。
2. 每个插件自行覆盖 `raw_value()`、`value()`、`fallback_value()`，基类只检查方法存在。
3. 插件只实现 `value()`，所有读取和兜底都放在该方法里。

➡️ 推荐答案：**Q59-1**。既满足对象对外至少提供 `raw_value` 和 `value`，又能强制每个插件认真定义兜底。

---

❓ **Q60 - Value Bar 原始值单位**：`raw_value()` 返回什么？

1. **返回 `0.0–1.0` 的长度比例（推荐）**：业务百分比或非线性数值由 `decode_value()` 转换。
2. 返回 `0–100` 的百分数。
3. 返回实际填充像素数和总宽度组成的元组。

➡️ 推荐答案：**Q60-1**。原始层保持归一化比例，更适合不同宽度的 Value Bar。

---

❓ **Q61 - Icon Tile 原始空值**：是否固定以下行为？

1. **固定（推荐）**：只检查内部 `6×6` 区域；全黑则该槽位为 `None`，否则返回 16 位小写 `xxh3_64_hexdigest`；多 Icon Tile 的 `raw_value()` 始终返回长度等于 `output_count` 的列表。
2. 整个 `8×8` 全黑才视为空；其他规则相同。
3. 是否为空完全由各插件定义。

➡️ 推荐答案：**Q61-1**。与最初“内部 6×6 区域”的协议一致。

---

❓ **Q62 - 兜底触发范围**：哪些异常应转为插件兜底值？

1. **只处理声明过的不可用原始状态（推荐）**：例如空 Cell、空 Icon Tile、超出有效范围；代码错误、类型错误和未预期异常仍抛出，避免悄悄隐藏插件缺陷。
2. `value()` 中出现任何异常都返回兜底值。
3. 由每个插件自行决定捕获哪些异常。

➡️ 推荐答案：**Q62-1**。

---

❓ **Q63 - 条件标题词法**：为了让中文标题可直接进入表达式，是否采用 Python 标识符兼容规则？

1. **采用（推荐）**：标题必须以中文字符或英文字母开头，后续可含中文、英文字母、数字或下划线；不得使用空格、操作符或保留词。
2. 允许数字开头，未来编写完全自定义的分词器处理。
3. 保持现有规则，不进一步限制开头字符。

➡️ 推荐答案：**Q63-1**。

---

❓ **Q64 - 表达式执行器**：如何利用 Python 能力但避免任意代码执行？

1. **白名单 AST 求值（推荐）**：使用 Python 表达式语法解析，但只允许已确认的比较、布尔、成员、标量和列表节点；标题解析为 `conditions[title].value()`；禁止属性访问、下标、函数调用和算术。
2. 使用 `eval`，仅清空 globals 并注入条件字典。
3. 从零实现独立分词器和语法解析器。

➡️ 推荐答案：**Q64-1**。

---

❓ **Q65 - 表达式字面量拼写**：布尔和空列表采用哪套语法？

1. **Python 风格（推荐）**：`True`、`False`、`[]`、字符串引号和数值；与白名单 AST 一致。
2. YAML 风格：`true`、`false`、`[]`。
3. 两种布尔拼写都接受。

➡️ 推荐答案：**Q65-1**。减少额外语法转换和大小写歧义。
~~~~

**用户回答 8**

~~~~text
Q59 - 条件基类模板：raw_value、value 和兜底如何组织？

- 基类公开 raw_value()，按输出描述读取原始区域；
- 基类公开 value()，调用插件实现的 decode_value(raw)；
- 原始值不可用时调用插件必须实现的抽象方法 fallback_value()；
- 插件缺少解码或兜底实现时无法实例化。




Q60 - Value Bar 原始值单位：raw_value() 返回什么？

返回 0.0–1.0 的长度比例（推荐）



Q61 - Icon Tile 原始空值：是否固定以下行为？

固定（推荐）：只检查内部 6×6 区域；全黑则该槽位为 None，否则返回 16 位小写 xxh3_64_hexdigest；多 Icon Tile 的 raw_value() 始终返回长度等于 output_count 的列表。

这里要补充Terminal时代的经验

因为游戏内的抗锯齿，渲染等因素。

cell有4x4，但是只计算中间2x2区域的，当读取为np.ndarray后，使用array[1:3, 1:3]获取。
所以icon_tile只能信任中间的6x6，用array[1:7, 1:7]

https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/pixelcalc/cell.py


Q62 - 兜底触发范围：哪些异常应转为插件兜底值？

1. python说的try decode_value报错就都丢。
2. 用户可能在写decode_value的时候，会考虑直接返回兜底值。


Q63 - 条件标题词法：为了让中文标题可直接进入表达式，是否采用 Python 标识符兼容规则？

采用：标题必须以中文字符或英文字母开头，后续可含中文、英文字母、数字或下划线；不得使用空格、操作符或保留词。


Q64 - 表达式执行器：如何利用 Python 能力但避免任意代码执行？

  1. 白名单 AST 求值（推荐）：使用 Python 表达式语法解析，但只允许已确认的比较、布尔、成员、标量和列表节点；标题解析为
     conditions[title].value()；禁止属性访问、下标、函数调用和算术。

  2. 使用 eval，仅清空 globals 并注入条件字典。
  3. 从零实现独立分词器和语法解析器。

  方案1速度怎么样。告诉我我再回答。

  假设每秒循环10次，每次30个条件，每秒300次AST求值，应该在现代计算机没啥压力对吧。


Q65 - 表达式字面量拼写：布尔和空列表采用哪套语法？

Python 风格（推荐）：True、False、[]、字符串引号和数值；与白名单 AST 一致。
~~~~

**Q64 性能答复与复问**

~~~~text
结论：方案 1 的性能完全足够。代表性微基准中，30 条预解析表达式每轮约 29.9 微秒；10 Hz 下约占 0.03% 单核时间。真正的主要成本会是截图和 NumPy 图像处理。

❓ **Q64 - 表达式执行器**：现在请选择最终方案。

1. **白名单 AST 求值（推荐）**：加载配置时只解析、校验一次；循环中读取 `conditions[title].value()` 并执行已验证节点。
2. 使用受限 `eval`。
3. 从零编写解析器。

➡️ 推荐答案：**Q64-1**。它兼顾速度、可维护性和安全边界。
~~~~

**用户回答 Q64**

~~~~text
1
~~~~

**首次共同理解确认问题**

~~~~text
完整共同理解如下，计划草案见 [2026-09-05-project-initialization.md](/workspaces/phantom-5796e240/.plan/2026-09-05-project-initialization.md)。

### 本次范围

- 只建设文档体系并初始化第三方参考源码。
- 不创建 Python/Lua 工程、业务代码、依赖配置或空目录骨架。
- 根 `README.md` 保持原样，完整项目说明写入 `.spec/project-overview.md`。
- `.spec/` 和 `AGENTS.md` 使用中文；`.context/` 保持英文，避免技术翻译误差。
- 不触碰或提交用户现有的 `.gitignore`、`LICENSE`、`README.md` 改动。

### 文档体系

`.spec/` 固定为八份中文文档：

- `README.md`
- `project-overview.md`
- `architecture.md`
- `pixel-protocol.md`
- `plugin-system.md`
- `configuration.md`
- `development-rules.md`
- `testing.md`

`.context/` 的 42 份原稿先在项目目录外打包备份，然后合并成约七份英文专题资料，覆盖：

- 入口与事实源
- WoW 12.1 API 变化
- Secret Values
- Aura
- 渲染组件
- 事件与性能
- 安全限制和 API 查询

只保留与 Phantom 有关的知识。技术结论要与本地源码和版本变更记录交叉核验；无法确认的内容标记为待验证，不升级成项目规则。

根 `AGENTS.md` 使用中文，只承担权威顺序、强制入口和按任务路由，不复制规范正文。

### 项目架构

- Python 根据用户勾选的多份 rotation 生成一个 WoW 插件包。
- 插件包名称由用户输入，必须匹配 `[A-Za-z][A-Za-z0-9_]*`。
- 插件包含共享基础模块，以及每份 rotation 对应的 `<uuid>.lua`。
- UUID 使用标准带连字符格式。
- 每份 Lua 在加载时检查职业和专精，不匹配便提前 `return`。
- `unit_spec` 使用 `GetSpecialization()` 返回的顺序索引。
- schema v1 删除 `unit_talents`；天赋路由留给未来。
- 切换专精后需要 `/reload`，暂不支持热切换。
- PySide6 是当前唯一 UI 技术决定，不参考旧 Terminal 的界面。

生成界面采用列表表格，第一列是复选框。同一 `unit_class + unit_spec` 只能选一份 rotation；选择新项会取消同组合的旧项。

### YAML 配置

一份 YAML 对应一份 rotation，顶层为：

- `schema_version`
- `uuid`
- `profile`
- `conditions`
- `macros`
- `rotation`

字段统一使用 `snake_case`，修正草案中的拼写错误；列表使用真实 YAML 数组；删除数字 `id`。

`conditions[].title` 是条件字典的唯一键，可以使用中文或英文。`rotation[].condition` 直接通过标题引用条件。

`macros[].name` 是宏的唯一名称，`rotation[].macro` 通过该名称引用。`macros[].key` 则是物理按键组合，采用大写 WoW 连字符格式，例如 `ALT-NUMPAD1`。

### 条件表达式

- 条件标题必须符合 Python 标识符规则，可以包含中文、英文字母、数字和下划线，但不能以数字开头。
- 支持整数、浮点数、布尔值、字符串和列表。
- 支持 `<`、`<=`、`>`、`>=`、`==`、`!=`、`and`、`or`、`not`、`in`、`not in` 和括号。
- 支持一个条件的标量结果判断是否位于另一条件的列表结果中。
- 使用加载时解析一次的白名单 AST；禁止属性访问、下标、函数调用、算术和任意 Python 执行。
- 每轮按 rotation 列表从上到下判断，首个成立项胜出，每轮最多发送一个按键。
- 没有条件命中就是该轮不执行动作，不存在持久“暂停状态”。
- 循环频率暂不确定，10 Hz 只是示例。

### 条件插件

插件标识使用区分大小写的小写 snake_case 精确版本，例如 `health_pct@1.0`。旧版本并存，不自动升级或回退。

每个条件实例：

- 只能使用 `cell`、`value_bar`、`icon_tile` 中的一种输出模式；
- 可以连续占用多个同类区域；
- 在参数验证后计算并冻结 `output_count`；
- 分别声明 `output_type`、`output_count`、`value_type`、`value_shape`；
- 多个区域既可组合成标量，也可形成列表。

基类公开：

- `raw_value()`：读取原始像素事实；
- `value()`：调用插件的 `decode_value(raw)`；
- `fallback_value()`：插件必须实现的兜底方法。

`decode_value()` 抛出的任何异常都由基类丢弃并转为插件兜底值；插件也可以主动返回兜底值。最终 `value()` 必须返回符合声明类型和形状的业务值，不返回通用 `None`。

这项设计意味着插件错误可能被兜底隐藏；这是本轮确认采用的取舍。

### 像素协议

固定四行、总高 20 像素：

1. 通用 Cell：高 4
2. 条件 Cell：高 4
3. Value Bar：高 4
4. Icon Tile：高 8

各行独立从左向右紧密排列，画布宽度取四行最大宽度。

- Cell 为 `4×4`，只信任 `array[1:3, 1:3]`。
- Value Bar 高 4、宽 `4n`，原始值为 `0.0–1.0` 的长度比例。
- Icon Tile 为 `8×8`，只信任 `array[1:7, 1:7]`。
- Icon Tile 内部 `6×6` 全黑时原始值为 `None`；否则返回 16 位小写 `xxh3_64_hexdigest`。
- 多 Icon Tile 的原始列表长度固定为 `output_count`，空槽保留 `None`。
- 业务 `value()` 可以过滤、重排或转换结果，顺序由插件契约定义。

具体通用 Cell、Cell/Value Bar 编码和截图通道顺序留给后续协议任务。

### 宏与按键

当 `bind_key: true`：

- Lua 创建不可见的 `SecureActionButtonTemplate`；
- 设置 `type = "macro"` 和 `macrotext`；
- 使用 `SetOverrideBindingClick` 建立高优先级运行期绑定；
- 不创建 WoW 宏槽位，也不改写玩家持久键位；
- 若该按键已有动作，直接覆盖，不检查、不提示。

当 `bind_key: false`：

- `key` 必填；
- `macro_text` 可省略，即使填写也不生效；
- 不生成安全按钮或绑定 Lua；
- Python 直接发送玩家已有游戏键位。

### 第三方源码

- 保留 `/wow-ui-source` 原样，不重置其本地档案提交。
- 浅克隆：
  - `/PhantomProject`：`develop`
  - `/Shigure`：`main`
  - `/midnight`：`12.0`
- 使用 SSH、指定分支、单分支、深度 1。
- 四个仓库均作为外部只读资料，不加入 Phantom Git。
- 未经用户明确要求，未来 Agent 不得修改、提交、切分支、拉取、重置或更新它们。

### 提交与验证

实施完成后：

- 校验文档链接、语言边界、规范导航、源码分支和目录状态。
- 保留仓库外的原始 `.context` 备份，并记录具体路径。
- 只提交 `AGENTS.md`、整理后的 `.context`、`.spec` 以及 plan/mean/prompt 档案。
- 创建一个原子本地提交，不推送。
- 排除用户现有的 `.gitignore`、`LICENSE`、根 `README.md` 改动。

❓ **Q66 - 最终确认**

1. **Confirm and authorize implementation（推荐）**
2. **Revise**

➡️ 推荐答案：**Q66-1**。
~~~~

**用户回答 Q66**

~~~~text
2
~~~~

**修订范围问题**

~~~~text
❓ **Q67 - 修订范围**：先重新打开哪一部分？

1. **核心设计（推荐）**：配置格式、表达式、rotation、插件、宏或像素协议。
2. **文档体系**：`.context`、`.spec`、语言、拆分方式或 `AGENTS.md`。
3. **执行流程**：第三方源码、备份、验证、Git 提交或本次交付范围。
4. **多个部分**：依次重新检查全部相关分支。

➡️ 请先选择 `Q67-1`、`Q67-2`、`Q67-3` 或 `Q67-4`。
~~~~

**用户主动修订**

~~~~text
补充1

参考 https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/pixelcalc/matrix.py

速度value_bar的时候，是读取其中中间2行的白色占比。

inner_pix_array: np.ndarray = bar_pix_array[1:3, :]
white_mask = np.all(inner_pix_array == (255, 255, 255), axis=2)
white_count: int = int(np.count_nonzero(white_mask))
total_count: int = int(inner_pix_array.shape[0] * inner_pix_array.shape[1])
return 100.0 * white_count / total_count if total_count > 0 else 0.0


补充2

代码风格强制TypeHint
~~~~

**Type Hint 范围问题**

~~~~text
Value Bar 修订已核验并写入计划：读取 `bar_pix_array[1:3, :]`，精确统计 `(255, 255, 255)`，`raw_value()` 返回 `0.0–100.0`。

❓ **Q68 - Type Hint 强制范围**

1. **所有手写 Python 文件（推荐）**：函数和方法的参数、返回值、类属性、实例属性、容器，以及类型不直观的局部变量必须标注；显而易见的简单局部变量和循环变量不强制；第三方代码与生成代码除外。
2. 每一个 Python 变量都必须显式标注，包括简单局部变量和循环变量。
3. 只强制公共接口的参数与返回值。

➡️ 推荐答案：**Q68-1**。保持严格可检查，同时避免类型标注淹没业务流程。
~~~~

**用户回答 Q68**

~~~~text
所有手写 Python 文件
~~~~

**修订后共同理解确认问题**

~~~~text
修订后的共同理解如下，计划仍是未冻结草案：[project-initialization.md](/workspaces/phantom-5796e240/.plan/2026-09-05-project-initialization.md)。

### 本次交付

- 只建设文档体系并初始化参考源码，不创建业务代码或工程骨架。
- 根 `README.md` 保持原样，完整项目说明写入 `.spec/project-overview.md`。
- `.spec/`、`AGENTS.md` 使用中文；`.context/` 保持英文，避免翻译误差。
- 不触碰或提交现有 `.gitignore`、`LICENSE`、`README.md` 用户改动。

### 文档体系

`.spec/` 固定包含八份中文规范：

- `README.md`
- `project-overview.md`
- `architecture.md`
- `pixel-protocol.md`
- `plugin-system.md`
- `configuration.md`
- `development-rules.md`
- `testing.md`

现有 42 份 `.context` 原稿先备份到项目目录外，再精编成约七份英文专题：入口与来源、12.1 变化、Secret Values、Aura、渲染组件、事件与性能、安全与 API 查询。

`.context` 只保留与 Phantom 有关的知识。技术结论与指定源码和变更记录交叉核验；无法确认的内容标为待验证。

`AGENTS.md` 只负责权威顺序和任务路由，不复制规范正文。

### 生成模型

- 一次选择多份 rotation，生成一个 WoW 插件包。
- 包名由用户输入，必须匹配 `[A-Za-z][A-Za-z0-9_]*`。
- 包内包含共享基础模块，以及每份 rotation 对应的 `<uuid>.lua`。
- UUID 使用标准带连字符格式。
- rotation Lua 加载时检查职业和专精，不匹配立即 `return`。
- `unit_spec` 是 `GetSpecialization()` 返回的顺序索引。
- schema v1 删除 `unit_talents`；切换专精后需要 `/reload`。
- GUI 使用表格和首列复选框，同一职业与专精组合只能选一份。
- UI 只确定使用 PySide6，不参考旧 Terminal 界面。

### YAML 与循环

一份 YAML 对应一份 rotation，顶层字段为：

- `schema_version`
- `uuid`
- `profile`
- `conditions`
- `macros`
- `rotation`

字段统一使用 `snake_case`，列表使用真正的 YAML 数组，删除数字 `id`。

- `conditions[].title` 是唯一条件名称，供表达式直接引用。
- `macros[].name` 是唯一宏名称，供 `rotation[].macro` 引用。
- `macros[].key` 是大写、连字符分隔的 WoW 按键，例如 `ALT-NUMPAD1`。
- rotation 从上到下判断，首个成立项胜出；每轮最多发送一个按键。
- 没有命中表示该轮不执行动作，不存在持久暂停状态。
- 循环频率暂不确定，10 Hz 只是例子。

### 表达式

- 条件标题遵循 Python 标识符规则，可以使用中文、英文、数字和下划线，但不能以数字开头。
- 支持整数、浮点数、布尔、字符串和列表。
- 支持比较、`and`、`or`、`not`、`in`、`not in` 和括号。
- 可以判断一个条件的标量结果是否属于另一条件返回的列表。
- 使用加载时解析一次的白名单 AST。
- 运行时读取 `conditions[title].value()`。
- 禁止属性访问、下标、函数调用、算术和任意 Python 执行。
- 预解析 AST 的 30 条代表性表达式在本环境约需 29.9 微秒/轮，10 Hz 下开销可忽略。

### 条件插件

插件标识使用区分大小写的小写 snake_case 精确版本，例如 `health_pct@1.0`。不同版本并存，不自动回退或升级。

每个条件实例：

- 只使用 `cell`、`value_bar`、`icon_tile` 中的一种类型；
- 可以连续占用多个同类区域；
- 参数校验后计算并冻结输出数量；
- 声明 `output_type`、`output_count`、`value_type`、`value_shape`；
- 多个区域可以合成标量，也可以形成列表。

基类公开 `raw_value()` 和 `value()`。基类的 `value()` 调用插件实现的 `decode_value(raw)`；插件必须实现 `fallback_value()`。

`decode_value()` 未自行处理的任何异常都会被基类丢弃并转换成兜底值。最终业务值不得为通用 `None`。这个选择可能隐藏插件编程错误，但已作为当前设计接受。

### 像素读取

四行布局总高 20 像素，各行独立从左向右紧密排列：

1. 通用 Cell，高 4
2. 条件 Cell，高 4
3. Value Bar，高 4
4. Icon Tile，高 8

具体规则：

- `4×4` Cell 只读取 `array[1:3, 1:3]`。
- `8×8` Icon Tile 只读取 `array[1:7, 1:7]`。
- Icon Tile 内部 `6×6` 全黑时原始值为 `None`；否则计算带 seed 0 的 16 位小写 `xxh3_64_hexdigest`。
- 多 Icon Tile 的原始列表固定为 `output_count` 长度，空槽保留 `None`；业务值可由插件过滤或重排。
- Value Bar 读取 `bar_pix_array[1:3, :]`，精确统计纯白 `(255, 255, 255)` 像素，返回 `0.0–100.0` 的白色占比。这一修订来自并符合参考实现 [matrix.py](https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/pixelcalc/matrix.py)。
- Cell/Icon Tile 中间区域与哈希方式符合参考实现 [cell.py](https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/Terminal/terminal/pixelcalc/cell.py)。

通用 Cell 字段、Cell/Value Bar 编码和截图通道规范留给后续任务。

### 宏绑定

当 `bind_key: true`：

- 创建不可见 `SecureActionButtonTemplate`；
- 设置 `type = "macro"` 和 `macrotext`；
- 使用 `SetOverrideBindingClick` 建立高优先级运行期覆盖；
- 不创建 WoW 宏槽位，不改写玩家的持久键位；
- 已有动作会被直接覆盖，不检查、不提示。

该行为依据用户提供的 [Macro.lua](https://github.com/liantian-cn/M.I.D.N.I.G.H.T/blob/12.0/DejaVu/DejaVu_DeathKnight/Blood/Macro.lua)。

当 `bind_key: false`：

- `key` 必填；
- `macro_text` 可省略，即使填写也不生效；
- 不生成安全按钮或覆盖绑定；
- Python 直接发送玩家已有游戏键位。

### 开发规则

- 所有手写 Python 文件强制使用 Type Hint。
- 函数和方法参数、返回值、类与实例属性、容器及类型不直观的局部变量必须标注。
- 简单且类型显然的局部变量、循环变量不强制。
- 第三方代码和生成代码除外。
- 标识符使用英文，业务注释使用中文。
- 条件插件头部必须说明参数、输出、尺寸、API 来源、Secret Value 风险、兜底和版本变化。
- Windows 专属流程只测试真正有价值的算法逻辑，不编写生硬的字符串比较测试。

### 外部源码与提交

- `/wow-ui-source` 保持原样。
- 缺失仓库使用 SSH、指定分支、单分支、深度 1 克隆到：
  - `/PhantomProject`：`develop`
  - `/Shigure`：`main`
  - `/midnight`：`12.0`
- 四个外部仓库后续均视为只读，未经用户明确要求不得更新或修改。
- 完成后验证文档链接、语言边界、源码分支和目录状态。
- 创建一个原子本地提交，不推送。
- 提交仅包含 `AGENTS.md`、`.context`、`.spec` 和 plan/mean/prompt 档案。

❓ **Q69 - 修订后最终确认**

1. **Confirm and authorize implementation（推荐）**
2. **Revise**

➡️ 推荐答案：**Q69-1**。
~~~~

**用户最终回答**

~~~~text
Confirm
~~~~
