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
- **Q1｜API 本地化**：补齐注释及缺失的 API 本地化声明，保持业务行为不变。
- **Q2｜`original` 路径基准**：以 `phantom/lua` 为基准，保留 `runtime\01_addon.lua` 形式。
- **Q3｜行尾注释密度**：补齐 API 缓存、跨文件引用及有业务含义代码的注释，`end` 等结构行不强制。
- **Q4｜`.mean` 是否被忽略**：用户指出 `.gitignore` 中没有对应规则；复核确认 `.mean` 未被忽略，因此撤回该问题。
- **最终确认**：按上述范围实施。
