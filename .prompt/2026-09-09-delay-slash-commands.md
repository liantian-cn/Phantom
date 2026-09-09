# Primary

帮我修改：phantom\lua\runtime\03_rotation_variable.lua

1. 模仿Burst，加入一套Delay机制

代表延迟/暂停之意。

我觉得唯一的区别是 `InBurst`体现是否在爆发中很生动。Delaying则在是否延迟中更加生动，你觉得到呢？


2. 加入命令行机制

插件名称是addonName

那么就是addonName的小写前两位作为命令

比如插件叫Apple时，使用/ap command
当插件叫Bear时，使用/be command


command 用法如下

disable , 关闭，修改addonTable.ENABLE状态
enable , 开启，修改addonTable.ENABLE状态
toggle , 切换 开启/关闭

delay , addonTable.DelayTime =  GetTime() + 0.4 延迟0.4秒
delay NN,  addonTable.DelayTime =  GetTime() + NN 延迟N秒

burst , addonTable.BurstTime = GetTime() + 15  爆发15秒
burst NN , addonTable.BurstTime =  GetTime() + NN 爆发NN秒

注意上述NN不限制正负，位数。 可实现 99999=永远  -1=关闭的效果。

3. 在phantom\lua\general下新建第5个通用状态展现lua，用以显示delay的状态，使用uuid db99c08a-9f97-4ae8-b076-dd2981bf99cc

# Question

**Delay 初始状态**

> Delay 加载时默认是否启动？现有 Burst 默认启动 60 秒。

默认不延迟。

**Delay 剩余时间**

> 采用 Delaying() 查询状态，同时新增 DelayRemaining() 时，剩余秒数如何返回？

仅限制下限为 0。

**命令反馈**

> 空命令、未知命令、无效数字或多余参数如何处理？

输出帮助信息。

**帮助输出**

> 你说的“输出帮助信息”，是否指空命令、help、未知命令、无效数字或多余参数都输出中文帮助且不改状态，而合法命令静默执行？命令词统一忽略大小写并允许首尾空白。

是，合法命令静默。

**实施授权**

> 是否实施已呈现的完整计划？

Implement the plan.
