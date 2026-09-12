# Primary

（目前在windows下，几个根目录下的参考文档不可见，以我给的参考为准）

按todo_list.md实施任务

- 目前第三步已完成，并测试成功，后续更新。
- 现在需要实施第四步[NumPy 像素解析]
- 参考E:\Documents\GitHub\EZWowX2\Terminal\terminal\pixelcalc\matrix.py，我们建立一个Decoder类，但是因为本项目不叫作Matrix，你要另外一个合适名称。需要一个更通用，更范式的名字。
- 包含getCell方法，对应phantom\lua\runtime\07_cell.lua，入参为x和y
- 包含getValueBar方法，对应phantom\lua\runtime\08_value_bar.lua，入参为x和width，reverse不需要
- 包含getIconTile方法，对应phantom\lua\runtime\09_icon_tile.lua，入参为x
- 两个项目参考坐标不同，要求本项目内对齐，即lua和python的入参相同=相同区域。
- 参考E:\Documents\GitHub\EZWowX2\Terminal\terminal\pixelcalc\cell.py，但是本项目要新建cell.py value_bar.py icon_tile.py三个文件。
- cell.py包含一个类Cell
- Cell内置属性self.x、self.y、self.pix_array（完整4x4）,self.inner(内部2x2)
- Cell内置方法，根据self.inner计算，包含：mean decimal  percent is_pure/is_not_pure  color_string is_black is_white
- Cell不需要Terminal项目的white_count/remaining/is_green方法。
- value_bar包含一个类ValueBar
- ValueBar内置属性self.x self.width,self.pix_array（完整bar）,self.inner(内部2行，self.pix_array[1:3, :])
- ValueBar内置方法 value, 为inner区域内， 白色像素数量/(白色像素数量+黑色像素数量)
- 因为本项目的valuebar两侧有红边，所以value计算方法和Terminal项目不同。
- icon_tile.py包含一个类IconTile，借鉴了Terminal项目的BadgeCell
- IconTile内置属性self.xself.pix_array（完整8x8）,self.inner(6x6,pix_array[1:7, 1:7])
- IconTile内置方法，根据self.inner计算, is_black is_pure/is_not_pure  hash
- IconTile不需要Terminal项目的footnote_color_string/footnote/title/cell_type方法。
- IconTile保留_hash_cache，减少hash计算量。
- 如果IconTitle is_black，hash返回 None
- IconTile、ValueBar、Cell包含pos方法，返回左上角定位点的坐标（x,y）。
- IconTile、ValueBar、Cell包含region方法，返回(x1,y,x2,y2)。
- pos_string和region_string返回上述坐标的字符串格式。
- Decoder类负责切分，然后构建并返回IconTile、ValueBar、Cell实例。入参包含的坐标仅为了生成pos和region，并不参与解码、切分、计算。
- 创建demoNN.py(NN为数字编号)测试，目前游戏已启动，可以返回x=1-5,y=1-2，共计10个cell的亮度值。x=1,width=2的valuebar的值，x=1,2的icontile的hash。

# Question

**数值范围**

> ValueBar.value 的返回范围采用 0–1 比例还是 0–100 百分比？

percent返回百分比，帮我想个名字返回0-1，不采用value了。我需要更清晰的方法，肉眼以下看出来返回值的。

**定位坐标**

> pos 与 region 是否使用相对完整基板左上角的物理像素坐标，region 右下边界不包含，字符串使用逗号分隔且无空格？

基板像素坐标。

**调用形式**

> Cell、ValueBar、IconTile 的计算结果及 pos/region 等接口采用只读 property 还是普通方法？Decoder 的 getCell 等仍为方法。

只读 property。

**解码器名称**

> 通用解码器采用哪个名称？代码放在 phantom/core/pixels/，包含 decoder.py 和三个区域文件，并导出四个类。

PixelDecoder。

**演示方式**

> 新增 phantom/core/pixels/demo01.py 如何采集并展示指定的 10 个 Cell、1 个 ValueBar 和 2 个 IconTile？定时方案等待 3 秒、采集 5 秒，停止后输出最后结果，失败明确报错。

定时单次输出。

**比例名称**

> ValueBar 用 percent 返回 0–100，哪个属性名用于返回 0–1？两者无有效黑白像素时均返回 0.0，并取消 value。

ratio。

**实施授权**

> 是否按已呈现的完整 PixelDecoder 计划实施，包括只读快照、输入校验、测试、游戏 demo、文档归档及原子本地提交？

Implement the plan.
