# Primary

我想开始项目的第2步 Python 工程基础

- 使用pip 管理包
- python 3.13
- 入口为rotations目录。直接python -m rotations.main 执行
- 测试按最佳实践，但是注意，我们只做业务逻辑测试。不做简单的字符串逻辑，测试至少是输入一张图片，解码符合预期这种。不是1+1=2这种。


第2步 屏幕截图基础模块

- 参考文件 C:\Users\liant\Documents\GitHub\EZWowX2\Terminal\terminal\capture

截图模块我的想法：
- 未来是插件化的。
- 一个独立的worker。
- 接受启动和停止2个关键指令。
- 可设置FPS（根据不同插件的实现，可能不生效）
- 目前只做一个gdi截图，参考terminal。（未来会做基于hdmi和dxcam、视频流等等，但都是后话）
- worker的逻辑
  点击开始后。
   - 截取完整的屏幕，寻找定位点。找不到循环这步。
   - 找到定位点后，后续只截取定位内的区域，以解压CPU性能。
   - 把定位店内的区域，转化为RGB顺序的np.ndarray。
   - 验证定位区域是否满足要求。
   - 返回np.ndarray、状态给主进程。
   - 循环，受FPS约束的循环速度，以节约FPS

定位点逻辑：
  - 仅服务插件的非DEBUG模式，插件的debug模式给人看的，不给python读取。
  - 参考phantom\lua\runtime\05_background.lua
  - BackgroundFrame的左上角，右下角，是2个4x4的定位点，内部由 POINT_0和POINT_1两个颜色构成
  -   排列为:
            0 | 1
            -----
            1 | 0
  - 颜色分别为(15 , 25 , 20)和  CreateColor(25, 15, 20)
  - 我过去项目也用的这个方法，参考C:\Users\liant\Documents\GitHub\EZWowX2\Terminal\terminal\capture\find_template_bounds.py 但是颜色和大小可能有变化。


验证定位区域是否满足要求：

  - 参考 phantom\lua\runtime\10_mask.lua
  - 左上角4x4往下，几个4x4的区域分别是cyanFrame magentaFrame yellowFrame flashFrame ，取中心2x2的区域，颜色必须为特定值。flash必须是黑和白。
  - 右下角4x4往上，同理。
  - 此过程验证截图的颜色是对的。

# Question

**入口范围**

> 本次运行 python -m rotations.main 后，用什么方式控制截图启动和停止？

python -m rotations.main是未来启动Textual的构想。按这个设计python框架。 至于截图插件，现在需要在没主体的情况下，单独启动插件。在插件目录有个demo.py实现这个。未来再实现主程序和插件的链接。

**worker 边界**

> 独立 worker 是否要求截图运行在独立子进程？

独立后台线程。

**屏幕范围**

> 首次寻找定位点时，完整屏幕具体截取哪个范围？

整个虚拟桌面。

**demo 行为**

> 插件目录的 demo.py 用什么交互和展示方式？

demo启动后，3秒后start，再过5秒后stop，然后把截取的结果保存。np.ndarray保存成json或者啥都好。状态值保存到result.txt。状态应该有2个。一个has_error，布尔值。 一个描述，文本，为何失败。 后续worker应该都这样设计，会告诉主线程有没有异常。

**失效处理**

> 已锁定区域的定位标记或颜色校验失败后，worker 应怎样处理？

标记丢失重定位，色错保留区域。

**结果交付**

> 主线程消费速度慢或本帧无效时，怎样交付图像与状态？

只保留最新结果，附无效图。

**匹配规则**

> 是否精确匹配 4×4 角标 RGB、校验中心四像素，Flash 必须全黑或全白且不检查跨帧交替，多个合法基板视为歧义？

采用这些严格规则。

**FPS 接口**

> 本次 GDI worker 的默认 FPS 和配置方式采用哪一种？

考虑到有些非gdi的插件，可能无法设计fps。我提前考虑标准化的情况。就是实例化这个worker后，应该有个标准传参接口，传入fps=15（默认值）。未来其他插件worker也有这个接口，可用不可用再说。然后这个接口也支持使用中修改（是否可用不管）。

**工程工具**

> 是否采用 requirements.txt / requirements-dev.txt、pytest、mypy、Ruff，pyproject.toml 保存工程元数据和工具配置？

采用这套工具。

**状态语义**

> 未定位、歧义、校验失败和 GDI 失败均为 has_error=true，有效帧为 false 且描述为空，主动停止保留最后结果，本身不算异常，是否采用？

采用此定义。

**保存内容**

> 是否保存最后结果为 result.npy 和 result.txt，无图时不生成数组文件，每次运行使用独立目录？

保存最后结果为 NPY。

**GDI 失败**

> GDI 调用本身抛错时，是报告异常并结束本次运行，还是持续重试？

报告异常并结束本次运行。

**DEBUG 与验收**

> 针对 Lua 默认 DEBUG=true，本次如何安排非 DEBUG 截图验证？

保持debug=true，但是我现在在工作，没办法玩游戏。就先随便测测吧。

**实施确认**

> 是否实施已提出的完整计划？

Implement the plan.

**中断后继续**

> 是否继续完成已经授权的截图基础实现？

继续
