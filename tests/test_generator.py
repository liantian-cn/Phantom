from pathlib import Path
from typing import Any

import numpy as np
import pytest
from lupa.lua51 import LuaRuntime  # type: ignore[import-untyped]

from phantom.core.condition.contracts import Region
from phantom.core.condition.registry import Registry
from phantom.core.generator import generate, render
from phantom.core.pixels import PixelDecoder
from phantom.core.rotation import load_rotation

ROOT = Path(__file__).resolve().parents[1]


def copy_rotation(tmp_path: Path) -> Path:
    path = tmp_path / "blood.toml"
    path.write_bytes((ROOT / "rotations/blood-dk.toml").read_bytes())
    return path


def fake_executable(tmp_path: Path) -> Path:
    executable = tmp_path / "_retail_/Wow.exe"
    executable.parent.mkdir()
    executable.touch()
    return executable


def test_generate_real_tree_overwrites_and_retains_stale_files(tmp_path: Path) -> None:
    path = copy_rotation(tmp_path)
    executable = fake_executable(tmp_path)
    result = generate(path, executable, "TestPhantom")
    assert len(result.files) == 23
    stale = result.directory / "old.lua"
    stale.write_text("old", encoding="utf-8")
    toc = result.directory / "TestPhantom.toc"
    toc.write_text("outdated", encoding="utf-8")
    generate(path, executable, "TestPhantom")
    references = [
        line
        for line in toc.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("##")
    ]
    assert len(references) == 16
    assert all((result.directory / name.replace("\\", "/")).is_file() for name in references)
    assert all("examples" not in name and "old.lua" not in name for name in references)
    assert stale.read_text(encoding="utf-8") == "old"
    assert references[-1] == result.rotation.uuid + ".lua"
    for source in (ROOT / "phantom/lua/media").rglob("*"):
        if source.is_file():
            destination = result.directory / source.relative_to(ROOT / "phantom/lua")
            assert destination.read_bytes() == source.read_bytes()
    assert not any("media" in name for name in references)


def test_invalid_generation_does_not_touch_existing_output(tmp_path: Path) -> None:
    path = copy_rotation(tmp_path)
    executable = fake_executable(tmp_path)
    result = generate(path, executable)
    old = {name: (result.directory / name).read_bytes() for name in result.files}
    path.write_text(
        path.read_text(encoding="utf-8").replace("max_power = 120", "max_power = 0"),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        generate(path, executable)
    assert old == {name: (result.directory / name).read_bytes() for name in result.files}
    with pytest.raises(ValueError):
        generate(path, executable, "../Other")


def test_lua51_syntax_for_every_generated_file(tmp_path: Path) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    compile_lua: Any = lua.eval(
        "function(source) local f,err=loadstring(source); assert(f,err); return true end"
    )
    for name, content in render(rotation, "Phantom").items():
        assert "{{" not in content, name
        if name.endswith(".lua"):
            assert compile_lua(content), name


def test_generated_lua_roundtrip_gcd_and_events(tmp_path: Path) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    source = render(rotation, "Phantom")[rotation.uuid + ".lua"]
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state: Any
    addon: Any
    state, addon = lua.execute(
        (ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8")
    )
    execute: Any = lua.eval(
        "function(source, addon) local f=assert(loadstring(source)); f('Phantom', addon) end"
    )
    execute(source, addon)
    state.initialize(state)
    state.update(state)
    assert state.queries[61304] == 1
    assert state.queries[195292] == 1
    pixels = np.zeros((20, rotation.board_width, 3), dtype=np.uint8)
    pixels[:4, 4:8] = 6
    pixels[:4, 8:12] = 1
    for index in range(1, 8):
        pixels[4:8, index * 4 : index * 4 + 4] = round(state.cells[index].brightness)
    pixels[8:12, 4:6] = [255, 0, 0]
    pixels[8:12, 6:10] = 255
    pixels[8:12, 14:16] = [255, 0, 0]
    assert state.bars[1].value == 1
    assert rotation.values(PixelDecoder(pixels)) == [40.0, 3, 1, True, 2.5, 0.0, 40.0, True]
    state.runes = 5
    state.event(state, "RUNE_POWER_UPDATE")
    assert state.cells[2].brightness == 5
    state.power = 1
    state.event(state, "UNIT_DISPLAYPOWER")
    assert state.cells[1].brightness == 255
    state.charges = 2
    state.event(state, "SPELL_UPDATE_CHARGES")
    assert state.bars[1].value == 2
    state.remaining[61304] = None
    state.update(state)
    assert state.cells[4].brightness == 0
    state.remaining[61304] = 0
    state.update(state)
    assert state.cells[4].brightness == 255
    state.known[195292] = False
    state.event(state, "SPELLS_CHANGED")
    state.update(state)
    assert state.cells[5].brightness == 0


@pytest.mark.parametrize(("unit_class", "spec"), [("MAGE", 1), ("DEATHKNIGHT", 2)])
def test_lua_guard_registers_no_conditions(tmp_path: Path, unit_class: str, spec: int) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state: Any
    addon: Any
    state, addon = lua.execute(
        (ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8")
    )
    state["class"] = unit_class
    state.spec = spec
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(render(rotation, "Phantom")[rotation.uuid + ".lua"], addon)
    assert len(addon.UIInitFuncs) == 0
    assert len(state.frames) == 0


@pytest.mark.parametrize(
    ("identifier", "args"),
    [
        ("spec_dk_rune", {}),
        ("player_primary_power", {"max_power": 120}),
        ("player_health_pct", {}),
        ("spell_overlay", {"spell_ids": [50842]}),
        ("spell_usable", {"spell_ids": [49998]}),
        ("spell_gcd", {}),
        ("spell_cooldown", {"spell_ids": [195292], "ignore_gcd": True}),
    ],
)
def test_templates_use_frozen_xy(identifier: str, args: dict[str, object]) -> None:
    plugin = Registry().create(identifier + "@1.0", args)
    # 非默认行揭示模板中隐藏的 y=2；注册器本身不决定布局策略。
    plugin.freeze((Region(7, 1),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute(
        (ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8")
    )
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(plugin.generate_lua("instance"), addon)
    assert len(state.cells) == 0  # 构造仍延迟到 UIInitFuncs。
    state.initialize(state)
    assert (state.cells[7].x, state.cells[7].y) == (7, 1)


@pytest.mark.parametrize("identifier", ["spell_cooldown", "spell_gcd"])
@pytest.mark.parametrize("seconds", [0.0, 2.5, 5.0, 17.5, 30.0, 92.5, 155.0, 265.0, 375.0])
def test_generated_cooldown_curve_roundtrips_all_segments(identifier: str, seconds: float) -> None:
    args: dict[str, object] = (
        {"spell_ids": [195292], "ignore_gcd": True} if identifier == "spell_cooldown" else {}
    )
    plugin = Registry().create(identifier + "@1.0", args)
    plugin.freeze((Region(1, 2),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute(
        (ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8")
    )
    state.remaining[195292 if identifier == "spell_cooldown" else 61304] = seconds
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(plugin.generate_lua("instance"), addon)
    state.initialize(state)
    state.update(state)
    pixels = np.zeros((20, 32, 3), dtype=np.uint8)
    pixels[4:8, 4:8] = round(state.cells[1].brightness)
    # 像素量化在最慢区间每级为 4 秒，误差最多半级。
    assert plugin.value(*plugin.raw_value(PixelDecoder(pixels))) == pytest.approx(seconds, abs=2.0)


def test_charge_template_uses_nondefault_width_and_position() -> None:
    plugin = Registry().create("spell_charges@1.0", {"spell_ids": [50842], "max_charges": 5})
    plugin.freeze((Region(4, width=5),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute(
        (ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8")
    )
    setup: Any = lua.eval("""function(addon, state)
        addon.ValueBar.New = function(self, x, width, reverse)
            assert(reverse == false)
            local bar = {x=x, width=width}
            function bar:setMinMaxValues(low, high) self.low=low; self.high=high end
            function bar:setValue(value) self.value=value end
            state.bars[x]=bar
            return bar
        end
    end""")
    setup(addon, state)
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(plugin.generate_lua("instance"), addon)
    state.initialize(state)
    bar = state.bars[4]
    assert (bar.x, bar.width, bar.low, bar.high, bar.value) == (4, 5, 0, 5, 1)
