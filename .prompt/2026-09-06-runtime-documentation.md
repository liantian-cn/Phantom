# Primary

**User**

我古法手工变成，写了下面的文件。

phantom\lua\runtime\01_addon.lua
phantom\lua\runtime\02_config.lua
phantom\lua\runtime\03_rotation_variable.lua
phantom\lua\runtime\04_baseline_definition.lua
phantom\lua\runtime\05_background.lua
phantom\lua\runtime\06_panel.lua

现在帮我完成以下任务

1. 维护项目规则
2. 补全我缺失的行尾注释、摘要、描述
3. 本次不增加修改记录。
4. 文件较大，每个文件独立subagent去执行，节约上下文。






我做了很好的例子。每个文件，分为文件头、 namespace initialization、api cache、 variable reference、logical code几个部分。

### 文件头

必须包含original、uuid、摘要、描述、修改记录几个部分

original、uuid是未来发布改名你用的。
- original为文件的相对路径。
- uuid只要不重就行

摘要：已计划描述
描述：详细描述文件的功能
修改记录：未来的每次修订记录，只有在逻辑增加修改时写，修复bug，增减注释不写。

### namespace initialization

固定只有 local addonName, addonTable = ...


### namespace initialization

文件内所有用到的wow官方API，lua的API，在此本地化声明，提高性能。
要有行尾注释，表明这个API的用途。

### variable reference 

插件内部，多个文件间的引用，在此本地化声明。
要有行尾注释，表明这个API的用途。

### logical code 

代码部分

# Question

**Assistant — Q1**

Q1：本次是否同时补齐缺失的 API 本地化声明？

- 补齐注释及缺失的 API 本地化，保持业务行为不变（Recommended）
- 本次仅改注释与项目规则，API 本地化留待后续

**Assistant — Q2**

Q2：文件头 original 的相对路径以哪个目录为基准？

- 以 phantom/lua 为基准，保留现有 runtime\01_addon.lua 格式（Recommended）
- 以仓库根目录为基准，使用 phantom/lua/runtime/01_addon.lua 格式

**Assistant — Q3**

Q3：行尾注释补全到什么程度？

- API 缓存、跨文件引用及有业务含义的代码补齐注释，end 等结构行不强制（Recommended）
- 按面板现有密度，每个非空代码行都加注释，包括 end 等结构行

**Assistant — Q4**

Q4：工作流要求将 mean 文件与本次改动原子提交，但 .gitignore 忽略了 .mean，如何处理？提交会精确隔离你已有的修改。

- 仅强制加入本次对应的 mean 文件，保留现有忽略规则（Recommended）
- 修改忽略规则，使工作流归档可正常提交
- 暂停本地提交，完成修改并保留归档

**User**

Q1-Q3 按推荐来 . Q4我检查了.gitignore 没看到啊，在第几行

**Assistant — final shared-understanding confirmation**

你看得对，**`.gitignore` 没有这三项，没有对应行号**。我把上一条命令末尾的目录列表误读成了文件内容，抱歉。`git check-ignore` 也确认它们未被忽略，Q4 撤回。

最终范围：

- 更新 `.spec/development-rules.md`，记录你指定的文件头、五段结构及修改记录规则。
- 六个文件分别由独立 subagent 处理。
- 补齐摘要、描述，以及 API 缓存、跨文件引用和有业务含义代码的行尾注释。
- 补齐缺失的 API 本地化，保持业务行为不变。
- `original` 保留相对 `phantom/lua` 的现有格式；保留唯一 UUID 和现有修改记录，本次不新增记录。
- 验证后精确隔离本次改动，与归档一起做本地提交。

是否确认以上范围并授权实施，还是需要调整？

这次最终确认是你提供的 `AGENTS.md` 工作流明确要求的；目前只更新了计划草稿。

**User**

实施
