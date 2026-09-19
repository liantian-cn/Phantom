"""验证正式示例已显式保存默认参数，离线读取不再改写它。"""

import tomllib
from pathlib import Path

import pytest

from phantom.core.macro_keys import MACRO_KEYS
from phantom.core.rotation import load_rotation

ROTATIONS = Path(__file__).resolve().parents[1] / "rotations"


@pytest.mark.parametrize("source_path", sorted(ROTATIONS.glob("*.toml")), ids=lambda path: path.stem)
def test_formal_rotation_has_no_layout_and_needs_no_default_writeback(tmp_path: Path, source_path: Path) -> None:
    source = source_path.read_bytes()
    document = tomllib.loads(source.decode("utf-8"))
    assert all("layout" not in condition for condition in document["conditions"])
    assert all(set(macro) == {"name", "macro_text"} for macro in document["macros"])
    path = tmp_path / source_path.name
    path.write_bytes(source)
    modified = path.stat().st_mtime_ns

    rotation = load_rotation(path)

    assert len(rotation.conditions) == len(document["conditions"])
    assert any(entry.instance.regions for entry in rotation.conditions)
    assert [macro.key for macro in rotation.macros] == list(MACRO_KEYS[: len(rotation.macros)])
    assert path.read_bytes() == source
    assert path.stat().st_mtime_ns == modified


def test_formal_directory_contains_only_forty_specializations() -> None:
    files = list(ROTATIONS.glob("*.toml"))
    assert len(files) == 40
    assert all(not path.stem.isascii() for path in files)


def test_preserved_observation_fixture_loads_without_writeback(tmp_path: Path) -> None:
    source = (ROTATIONS.parent / "tests/fixtures/condition-observations.toml").read_bytes()
    path = tmp_path / "observations.toml"
    path.write_bytes(source)
    rotation = load_rotation(path)
    assert len(rotation.conditions) > 10
    assert len(rotation.macros) == 4
    assert path.read_bytes() == source
