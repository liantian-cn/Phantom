## Primary

我现在认为 phantom\core\condition\decoders.py是多余的，现在plugin -> decoders -> pixels 多了一层抽象层。看似合理，但其实多余，pixels下cell、value_bar、icontile的各种 方法已经是一次封装了。不需要多层封装。去掉这个文件。所有插件直接访问下cell、value_bar、icontile的各种方法，看起来更直观，更容易理解。

## Question

**颜色校验**

> 删除解码封装后，现有严格灰度／黑白校验及非法颜色兜底如何处理？可以在 decode_value 中直接使用像素属性并保留必要校验和既有行为，或删除额外颜色校验、接受混色均值和非白即 False 等变化，同时保留业务范围校验。

插件内保留校验。

**实施确认**

> 是否授权实施已提出的完整计划：移除条件解码器中间层，迁移 11 个插件，保留颜色校验、业务结果和现有像素接口，同步文档与测试，完成工作流归档和一次本地提交？

Implement the plan.
