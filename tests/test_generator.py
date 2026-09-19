from dataclasses import replace
from pathlib import Path
from typing import Any
from uuid import uuid4

import numpy as np
import pytest
from lupa.lua51 import LuaRuntime  # type: ignore[import-untyped]

from phantom.core import generator
from phantom.core.condition.contracts import Region
from phantom.core.condition.registry import Registry
from phantom.core.generator import generate, generate_rotations, render, render_rotations
from phantom.core.macro_keys import MACRO_KEYS
from phantom.core.pixels import PixelDecoder
from phantom.core.rotation import Rotation, atomic_write, load_rotation, parse_macros

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("count", [0, 2, 148])
def test_macro_bindings_preserve_text_and_bind_every_macro(tmp_path: Path, count: int) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    text = '/cast [@target] 测试\n/say "quote" \\123\r\t\x00123'
    macros = parse_macros([{"name": f"宏{index}", "macro_text": text + str(index), "key": "ALT-F4", "bind_key": False} for index in range(count)])
    rotation = replace(rotation, conditions=(), macros=macros)
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state: Any = lua.execute("""
        local state = {buttons={}, bindings={}}
        UnitClass = function() return "死亡骑士", "DEATHKNIGHT" end
        C_SpecializationInfo = {GetSpecialization=function() return 1 end}
        CreateFrame = function(kind, name, parent, template)
            assert(kind == "Button" and template == "SecureActionButtonTemplate")
            local frame = {name=name, attributes={}}
            function frame:SetAttribute(key,value) self.attributes[key]=value end
            function frame:RegisterForClicks(down,up)
                assert(down=="AnyDown" and up=="AnyUp")
                self.registered = true
            end
            table.insert(state.buttons, frame)
            return frame
        end
        SetOverrideBindingClick = function(frame, priority, key, name)
            assert(priority and frame.name==name and frame.registered)
            table.insert(state.bindings, {key=key, frame=frame})
        end
        return state
    """)
    source = render(rotation, "TestPhantom")[rotation.uuid + ".lua"]
    execute: Any = lua.eval("function(source) assert(loadstring(source))('TestPhantom', {}) end")
    execute(source)
    assert len(state.buttons) == len(state.bindings) == count
    for index, macro in enumerate(macros, 1):
        assert state.buttons[index].attributes["type"] == "macro"
        assert state.buttons[index].attributes.macrotext == macro.macro_text
        assert state.bindings[index].key == macro.key == MACRO_KEYS[index - 1]
        assert state.buttons[index].name.startswith("TestPhantomButton")
    assert len({state.buttons[index].name for index in range(1, count + 1)}) == count


def copy_rotation(tmp_path: Path) -> Path:
    path = tmp_path / "blood.toml"
    path.write_bytes((ROOT / "tests/fixtures/engine-rotation.toml").read_bytes())
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
    assert len(result.files) == 24
    stale = result.directory / "old.lua"
    stale.write_text("old", encoding="utf-8")
    toc = result.directory / "TestPhantom.toc"
    toc.write_text("outdated", encoding="utf-8")
    generate(path, executable, "TestPhantom")
    references = [line for line in toc.read_text(encoding="utf-8").splitlines() if line and not line.startswith("##")]
    assert len(references) == 17
    assert all((result.directory / name.replace("\\", "/")).is_file() for name in references)
    assert all("examples" not in name and "old.lua" not in name for name in references)
    assert stale.read_text(encoding="utf-8") == "old"
    assert references[-1] == result.rotation.uuid + ".lua"
    for source in (ROOT / "phantom/lua/media").rglob("*"):
        if source.is_file():
            destination = result.directory / source.relative_to(ROOT / "phantom/lua")
            assert destination.read_bytes() == source.read_bytes()
    assert not any("media" in name for name in references)


def rotation_pair(tmp_path: Path) -> tuple[Rotation, Rotation]:
    path = copy_rotation(tmp_path)
    first = load_rotation(path)
    second = load_rotation(path)
    return first, replace(second, uuid=str(uuid4()), profile=replace(second.profile, unit_spec=2))


def test_generate_collection_writes_shared_files_once_and_toc_last(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rotations = rotation_pair(tmp_path)
    executable = fake_executable(tmp_path)
    writes: list[Path] = []

    def record_write(path: Path, content: str | bytes) -> None:
        writes.append(path)
        atomic_write(path, content)

    def reject_load(path: Path) -> Rotation:
        raise AssertionError(f"集合生成不得重读 rotation：{path}")

    monkeypatch.setattr(generator, "atomic_write", record_write)
    monkeypatch.setattr(generator, "load_rotation", reject_load)
    rotations[0].path.unlink()
    result = generate_rotations(rotations, executable, "TestPhantom")
    assert result.rotations is rotations
    assert len(writes) == len(set(writes)) == len(result.files)
    assert writes[-1].name == result.files[-1] == "TestPhantom.toc"
    references = [line.replace("\\", "/") for line in writes[-1].read_text(encoding="utf-8").splitlines() if line and not line.startswith("##")]
    shared = [path.relative_to(generator.LUA_ROOT).as_posix() for directory in ("runtime", "general") for path in sorted((generator.LUA_ROOT / directory).glob("*.lua"))]
    assert references == shared + [rotation.uuid + ".lua" for rotation in rotations]
    for asset in (generator.LUA_ROOT / "media").rglob("*"):
        if asset.is_file():
            name = asset.relative_to(generator.LUA_ROOT).as_posix()
            assert result.files.count(name) == 1
            assert (result.directory / name).read_bytes() == asset.read_bytes()
    for name, source in render_rotations(rotations, "TestPhantom").items():
        assert (result.directory / name).read_text(encoding="utf-8") == source


@pytest.mark.parametrize("conflict", ["group", "uuid"])
def test_collection_rejects_duplicates_before_render_or_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, conflict: str) -> None:
    first, second = rotation_pair(tmp_path)
    second = replace(second, profile=first.profile) if conflict == "group" else replace(second, uuid=first.uuid)
    executable = fake_executable(tmp_path)

    def reject_render(instance_id: str) -> str:
        raise AssertionError("重复集合不应开始渲染")

    monkeypatch.setattr(first.conditions[0].instance, "generate_lua", reject_render)
    message = "重复职业专精" if conflict == "group" else "重复 UUID"
    with pytest.raises(ValueError, match=message):
        render_rotations((first, second), "Phantom")
    with pytest.raises(ValueError, match=message):
        generate_rotations((first, second), executable)
    assert not (executable.parent / "Interface").exists()


def test_collection_rejects_empty_before_write(tmp_path: Path) -> None:
    executable = fake_executable(tmp_path)
    with pytest.raises(ValueError, match="不能为空"):
        render_rotations((), "Phantom")
    with pytest.raises(ValueError, match="不能为空"):
        generate_rotations((), executable)
    assert not (executable.parent / "Interface").exists()


def test_second_rotation_render_failure_preserves_all_existing_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rotations = rotation_pair(tmp_path)
    executable = fake_executable(tmp_path)
    result = generate_rotations((rotations[0],), executable)
    old = {path.relative_to(result.directory): path.read_bytes() for path in result.directory.rglob("*") if path.is_file()}
    rendered: list[str] = []
    generate_first = rotations[0].conditions[0].instance.generate_lua

    def record_first(instance_id: str) -> str:
        rendered.append("first")
        return generate_first(instance_id)

    def fail_second(instance_id: str) -> str:
        rendered.append("second")
        raise ValueError("第二份渲染失败")

    monkeypatch.setattr(rotations[0].conditions[0].instance, "generate_lua", record_first)
    monkeypatch.setattr(rotations[1].conditions[0].instance, "generate_lua", fail_second)
    with pytest.raises(ValueError, match="第二份渲染失败"):
        generate_rotations(rotations, executable)
    assert rendered == ["first", "second"]
    assert old == {path.relative_to(result.directory): path.read_bytes() for path in result.directory.rglob("*") if path.is_file()}
    assert render(rotations[0], "Phantom")[rotations[0].uuid + ".lua"]


def test_single_rotation_wrappers_preserve_results(tmp_path: Path) -> None:
    path = copy_rotation(tmp_path)
    executable = fake_executable(tmp_path)
    single = generate(path, executable, "TestPhantom")
    collection = generate_rotations((single.rotation,), executable, "TestPhantom")
    assert single.directory == collection.directory
    assert single.files == collection.files
    assert collection.rotations[0] is single.rotation
    assert render(single.rotation, "TestPhantom") == render_rotations((single.rotation,), "TestPhantom")


@pytest.mark.parametrize(("unit_class", "spec", "active"), [("DEATHKNIGHT", 1, 0), ("DEATHKNIGHT", 2, 1), ("MAGE", 1, None)])
def test_collection_lua_guards_select_only_matching_rotation(tmp_path: Path, unit_class: str, spec: int, active: int | None) -> None:
    rotations = rotation_pair(tmp_path)
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
    state["class"] = unit_class
    state.spec = spec
    execute: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom', addon) end")
    sources = render_rotations(rotations, "Phantom")
    for index, rotation in enumerate(rotations):
        before = len(state.frames)
        execute(sources[rotation.uuid + ".lua"], addon)
        assert (len(state.frames) > before) == (index == active)


def test_invalid_generation_does_not_touch_existing_output(tmp_path: Path) -> None:
    path = copy_rotation(tmp_path)
    executable = fake_executable(tmp_path)
    result = generate(path, executable)
    old = {name: (result.directory / name).read_bytes() for name in result.files}
    path.write_text(path.read_text(encoding="utf-8").replace("max_power = 120", "max_power = 0"), encoding="utf-8")
    with pytest.raises(ValueError):
        generate(path, executable)
    assert old == {name: (result.directory / name).read_bytes() for name in result.files}
    with pytest.raises(ValueError):
        generate(path, executable, "../Other")


def test_lua51_syntax_for_every_generated_file(tmp_path: Path) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    compile_lua: Any = lua.eval("function(source) local f,err=loadstring(source); assert(f,err); return true end")
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
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
    execute: Any = lua.eval("function(source, addon) local f=assert(loadstring(source)); f('Phantom', addon) end")
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
    assert rotation.values(PixelDecoder(pixels)) == [40.0, 3, 1, True, 2.5, 0.0, 40.0, True, False, False]
    state.runes = 5
    state.event(state, "RUNE_POWER_UPDATE")
    state.flushTimers(state)
    assert state.cells[2].brightness == 5
    state.power = 1
    state.event(state, "UNIT_DISPLAYPOWER")
    state.flushTimers(state)
    assert state.cells[1].brightness == 255
    state.charges = 2
    state.event(state, "SPELL_UPDATE_CHARGES")
    state.flushTimers(state)
    assert state.bars[1].value == 2
    state.remaining[61304] = None
    state.update(state)
    assert state.cells[4].brightness == 0
    state.remaining[61304] = 0
    state.update(state)
    assert state.cells[4].brightness == 255
    state.known[195292] = False
    state.event(state, "SPELLS_CHANGED")
    state.flushTimers(state)
    state.update(state)
    assert state.cells[5].brightness == 0


@pytest.mark.parametrize(("unit_class", "spec"), [("MAGE", 1), ("DEATHKNIGHT", 2)])
def test_lua_guard_registers_no_conditions(tmp_path: Path, unit_class: str, spec: int) -> None:
    rotation = load_rotation(copy_rotation(tmp_path))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state: Any
    addon: Any
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
    state["class"] = unit_class
    state.spec = spec
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(render(rotation, "Phantom")[rotation.uuid + ".lua"], addon)
    assert len(addon.UIInitFuncs) == 0
    assert len(state.frames) == 0


@pytest.mark.parametrize(
    ("identifier", "args"),
    [
        ("spec_power_rune", {}),
        ("player_primary_power", {"max_power": 120}),
        ("player_health_pct", {}),
        ("spell_overlay", {"spell_ids": [50842]}),
        ("spell_usable", {"spell_ids": [49998]}),
        ("spell_gcd", {}),
        ("spell_cooldown", {"spell_ids": [195292], "ignore_gcd": True}),
    ],
)
def test_templates_use_frozen_xy(identifier: str, args: dict[str, object]) -> None:
    plugin = Registry().create(f"{identifier}@dev", args)
    # 非默认行揭示模板中隐藏的 y=2；注册器本身不决定布局策略。
    plugin.freeze((Region(7, 1),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(plugin.generate_lua("instance"), addon)
    assert len(state.cells) == 0  # 构造仍延迟到 UIInitFuncs。
    state.initialize(state)
    assert (state.cells[7].x, state.cells[7].y) == (7, 1)


@pytest.mark.parametrize("identifier", ["spell_cooldown", "spell_gcd"])
@pytest.mark.parametrize("seconds", [0.0, 2.5, 5.0, 17.5, 30.0, 92.5, 155.0, 265.0, 375.0])
def test_generated_cooldown_curve_roundtrips_all_segments(identifier: str, seconds: float) -> None:
    args: dict[str, object] = {"spell_ids": [195292], "ignore_gcd": True} if identifier == "spell_cooldown" else {}
    plugin = Registry().create(f"{identifier}@dev", args)
    plugin.freeze((Region(1, 2),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
    state.remaining[195292 if identifier == "spell_cooldown" else 61304] = seconds
    run: Any = lua.eval("function(source, addon) assert(loadstring(source))('Phantom',addon) end")
    run(plugin.generate_lua("instance"), addon)
    state.initialize(state)
    state.update(state)
    pixels = np.zeros((20, 32, 3), dtype=np.uint8)
    pixels[4:8, 4:8] = round(state.cells[1].brightness)
    # 像素量化在最慢区间每级为 4 秒，误差最多半级。
    decoder = PixelDecoder(pixels)
    assert plugin.value(*plugin.raw_value(decoder), decoder=decoder) == pytest.approx(seconds, abs=2.0)


def test_charge_template_uses_nondefault_width_and_position() -> None:
    plugin = Registry().create("spell_charges@dev", {"spell_ids": [50842], "max_charges": 5, "width": 5})
    plugin.freeze((Region(4, width=5),))
    lua: Any = LuaRuntime(unpack_returned_tuples=True)
    state, addon = lua.execute((ROOT / "tests/lua/conditions_harness.lua").read_text(encoding="utf-8"))
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
