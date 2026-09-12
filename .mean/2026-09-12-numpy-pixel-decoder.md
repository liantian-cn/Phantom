---
plan: .plan/2026-09-12-numpy-pixel-decoder.md
related_paths:
  - phantom/core/pixels/__init__.py
  - phantom/core/pixels/_region.py
  - phantom/core/pixels/decoder.py
  - phantom/core/pixels/cell.py
  - phantom/core/pixels/value_bar.py
  - phantom/core/pixels/icon_tile.py
  - phantom/core/pixels/demo01.py
  - tests/test_pixels.py
  - requirements.txt
  - .spec/pixel-protocol.md
  - .spec/architecture.md
  - .spec/development-rules.md
  - .spec/testing.md
  - todo_list.md
---

## 意图 (Intent)

实施第四步 NumPy 像素解析；第三步已完成并测试成功。采用 PixelDecoder，按 Lua 相同入参取得相同区域，创建 Cell、ValueBar、IconTile。计算和定位接口使用只读 property。ValueBar 使用 ratio 返回 0–1、percent 返回百分比。创建定时单次输出 demo，展示指定十个 Cell、一个 ValueBar 和两个 IconTile。Implement the plan.

## 约束 (Constraints)

以用户给出的 Windows Terminal 源码为参考；坐标返回相对基板的物理像素，右下不包含，字符串逗号分隔无空格。区域实例坐标只用于定位，Decoder 负责切分。内部区域分别为 2×2、中间两行、6×6。严格黑白；IconTile 全黑 hash 为 None，保留 _hash_cache。按确认计划完成测试、文档和原子本地提交。

## 被拒绝的替代方案 (Rejected Alternatives)

不采用 ValueBar.value，用户要求肉眼能看出返回值含义。不要 Matrix 名称及参考项目中明确排除的 white_count、remaining、is_green、footnote、title、cell_type 等接口。
