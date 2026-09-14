## Primary

帮我整改项目

通用cell中，除了职业和专精，影响rotation加载。其他仅在rotation内部使用。
但是现有的delay、爆发、enable开关，可lua框架深度绑定，不方便独立使用。
那我想这么设计：
- 插件的python代码部分，可以访问当前帧的PixelDecoder实例，从而访问任意cell、valuebar、icontile，只是需要指定坐标。
- 插件允许没有lua代码，生成空代码块
上述操作，给插件更高的开发自由度。
同时  delay、爆发、enable 三个通用Cell，则做成插件，按需加载。
- 插件可按需加载，并且可能是不同名字，不再限于 "插件启用": "爆发开启":  "正在延迟" 这三个固定名字。而是配置中写什么就是什么。
妥否？

## Question

**迁移边界**

> delay、爆发、enable 做成插件后，游戏端现有状态与第一行三个 Cell 如何处理？

保留 Lua，读取插件化。

**插件接口**

> 开放当前帧 PixelDecoder 时，如何调整现有插件解码接口？

保留区域列表，增加 decoder。

**配置迁移**

> 已有 rotation 使用三个内置名称但未声明条件插件时，如何处理？

要求显式声明。

**异常行为**

> 三个状态插件读到非黑白值时，应如何处理？目前内置读取会让该帧决策失败。

兜底，但是 enable=True burst=False delay=False。

**页面展示**

> TUI 的通用条件页是否继续展示五个固定 Cell 的原始值？配置加载的三个状态插件会另外出现在循环条件页，使用配置中的名称。

只展示职业和专精。

**Implementation confirmation**

> Confirm the proposed Condition Frame Access and Optional Lua plan through the native Plan-to-implementation flow.

Implement the plan.
