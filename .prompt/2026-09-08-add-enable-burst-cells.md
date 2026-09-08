# Primary

现在我们来设计第三个和第四个通用cell，建立2个文件，uuid是c845da87-d22c-462b-9696-0678101df51b和0db46515-244d-4755-9a77-65b3581d85ef

他们是对phantom\lua\runtime\03_rotation_variable.lua的反应

第三个反应addonTable.ENABLE的状态。

如果addonTable.ENABLE 是 true，那就是白。
如果addonTable.ENABLE 是 false，那就是黑。
使用OnUpdate刷新，使用类似下面的方法，赋予fastTimeElapsed = -random()，从而实现错峰刷新，间隔0.1秒。


local fastTimeElapsed = -random()
eventFrame:HookScript("OnUpdate", function(_, elapsed)
    fastTimeElapsed = fastTimeElapsed + elapsed
    if fastTimeElapsed > 0.1 then
        fastTimeElapsed = fastTimeElapsed - 0.1
        updateCell()
    end
end)


第4个反应addonTable.InBurst的数值。和第三个类似。

# Question

**爆发状态显示**

> 第四个 Cell 是否调用 addonTable.InBurst()，按返回的布尔值显示白／黑，与第三个 Cell 一致，而非通过 BurstRemaining() 编码剩余秒数？

爆发状态黑白。

**首次刷新时机**

> 两个 Cell 构造完成后，是否沿用前两个 Cell 的做法立即刷新一次，再开始随机错峰的 OnUpdate 刷新，还是保持默认黑色并等待各自计时器第一次超过 0.1 秒？

等待错峰首次刷新。

**确认实施**

> 是否按完整计划新增启用状态和爆发状态 Cell、更新 TOC 与像素规范、验证错峰计时及四个 Cell 布局，并归档和本地提交？

Implement the plan.
