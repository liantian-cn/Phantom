from pathlib import Path
from typing import Any

import numpy as np
import pytest
from lupa.lua51 import LuaRuntime  # type: ignore[import-untyped]

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
