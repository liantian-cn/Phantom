# 像素协议

## 画布布局

游戏内输出固定为四行，总高度 20 像素：

| 行 | 内容 | 区域高度 | 排列规则 |
| --- | --- | ---: | --- |
| 1 | 通用 Cell | 4 | 按通用字段声明顺序从左到右紧密排列 |
| 2 | 条件 Cell | 4 | 按条件声明顺序从左到右紧密排列 |
| 3 | Value Bar | 4 | 按条件声明顺序，以含红色分隔的实际占位宽度从左到右紧密排列 |
| 4 | Icon | 8 | 按条件声明顺序从左到右紧密排列 |

每一行独立从左侧起排，不因其他行的区域宽度产生空洞。画布总宽度取四行占用宽度的最大值。

一个条件实例只能选择 `cell`、`value_bar`、`icon` 三种输出类型中的一种，但可以连续占用多个同类区域。区域数量在插件参数通过校验后计算，并在布局完成时冻结；运行中不得改变。

## Cell

- 物理尺寸固定为 4×4。
- Python 读取 NumPy 数组时只信任中间 2×2，即 `cell_pix_array[1:3, 1:3]`。
- `raw_value()` 保留插件需要的 RGB 原始信息；如何把颜色或亮度映射为业务值由插件的版本化编解码契约决定。

边缘像素不参与计算，因为游戏渲染、抗锯齿和缩放可能污染边缘。

## Value Bar

- 高度固定为 4 像素。构造入参 `width` 表示黑白内容宽度，以 Cell 为单位，由插件输出描述决定；内容宽度为 `4 * width` 像素。
- 每条 Bar 的内容左右各保留半个 Cell 的红色分隔，实际占位宽度为 `width + 1` 个 Cell，即 `4 * (width + 1)` 像素。布局与画布行宽计算必须包含分隔占位。
- 构造入参 `x` 表示包含左侧红色分隔的占位起点，相对背景左上角，以 Cell 为单位；黑白内容从 `x + 0.5` 个 Cell 处开始。下一条 Bar 的入参必须为 `next_x = x + width + 1`，不能只累加 `width`。
- `bar_pix_array` 覆盖该 Bar 的完整占位区域，包含两侧红色分隔；只读取中间两行：`inner_pix_array = bar_pix_array[1:3, :]`。
- 只有像素值严格等于 `(255, 255, 255)` 才计为白色，严格等于 `(0, 0, 0)` 才计为黑色；红色分隔及其他颜色均不参与分子或分母。
- 原始值是白色像素占黑色与白色像素总数的百分比，范围为 `0.0` 到 `100.0`；没有黑白像素时返回 `0.0`：

```python
white_mask = np.all(inner_pix_array == (255, 255, 255), axis=2)
black_mask = np.all(inner_pix_array == (0, 0, 0), axis=2)
white_count = int(np.count_nonzero(white_mask))
black_count = int(np.count_nonzero(black_mask))
total_count = white_count + black_count
result = 100.0 * white_count / total_count if total_count > 0 else 0.0
```

该百分比是 `raw_value()`，不是业务值；插件可在 `decode_value()` 中继续缩放或转换。

## Icon

- 每个 Icon 物理尺寸固定为 8×8。
- 只信任中间 6×6，即 `icon_pix_array[1:7, 1:7]`。
- 中间区域全黑时，该槽位的原始值为 `None`。
- 否则先保证数组连续，再以 seed 0 计算 `xxh3_64_hexdigest`，返回 16 位小写字符串。
- 多 Icon 条件的 `raw_value()` 始终返回长度等于 `output_count` 的列表，并用 `None` 保留空槽位。

插件的 `value()` 可以删除空槽、重新组织列表或合并多个区域。业务列表的排序由插件契约定义，核心不附加统一顺序。

## 输出描述

每个条件实例必须分别声明：

- `output_type`：`cell`、`value_bar` 或 `icon`。
- `output_count`：连续占用的同类区域数量。
- `value_type`：`bool`、`int`、`float` 或 `str`。
- `value_shape`：`scalar` 或 `list`。

像素区域数量与业务值形状是两个独立维度。多个区域既可以合成为高精度标量，也可以解码为列表。

## 待定事项

- 第一行通用 Cell 的最终字段及各字段语义；启停、延迟、职业、专精和战斗状态只是候选项。
- 截图数据的 RGB/BGR 等通道顺序归一化位置。
- Cell 的通用颜色约定和各条件的精度分段。
- Value Bar 百分比到具体业务值的编码规则。
