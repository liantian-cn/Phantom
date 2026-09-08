# Primary

很好，我对这个结构满意，新增一个index=2，uuid=154ab0be-9c33-4935-8e57-531eb6bde99e ,显示玩家专精的cell，取值方法 local specializationIndex = GetSpecialization()。关联事件 ACTIVE_PLAYER_SPECIALIZATION_CHANGED， PLAYER_SPECIALIZATION_CHANGED。说明注释取自 https://warcraft.wiki.gg/wiki/API:GetSpecialization

# Question

**编码与布局**

> 是否沿用职业 Cell 的约定，在 x=2、y=1 显示 specializationIndex/255 灰度，无返回值时显示黑色，文件头 index: 2，透明度 1？

沿用灰度与黑色兜底。

**刷新事件**

> 除新增的两个专精事件，是否保留职业 Cell 使用的 PLAYER_LOGIN、PLAYER_ENTERING_WORLD 刷新，并在构造后立即刷新？

四个事件。

**专精 API 引用**

> 是否将新版接口 C_SpecializationInfo.GetSpecialization 缓存为局部 GetSpecialization，保留 local specializationIndex = GetSpecialization() 写法，从而不依赖旧全局接口的 loadDeprecationFallbacks 开关，并在注释中说明新旧关系？

局部缓存新版接口。

**确认实施**

> 是否按完整计划实现玩家专精 Cell、补充 TOC 与像素规范、执行验证并完成工作流归档及本地提交？

Implement the plan.
