from pathlib import Path

import pytest
import tomlkit

from phantom.core.rotation import RotationError, load_rotation

EXAMPLE = Path(__file__).resolve().parents[1] / "rotations/blood-dk.toml"


def example_copy(tmp_path: Path) -> Path:
    path = tmp_path / "blood.toml"
    path.write_bytes(EXAMPLE.read_bytes())
    return path


def test_example_layout_idempotent_and_optional_class_id(tmp_path: Path) -> None:
    path = example_copy(tmp_path)
    document = tomlkit.parse(path.read_text(encoding="utf-8"))
    del document["profile"]["unit_class_id"]
    path.write_text(tomlkit.dumps(document), encoding="utf-8")
    rotation = load_rotation(path)
    assert rotation.profile.unit_class_id == 6
    assert rotation.board_width == 36
    assert len(rotation.rules) == 7
    assert len(rotation.macros) == 4
    assert rotation.conditions[4].plugin == "liantian_cn.spell_gcd@dev"
    assert [e.instance.regions[0].x for e in rotation.conditions if e.instance.regions] == [1, 2, 1, 3, 4, 5, 6, 7]
    old = path.read_bytes()
    modified = path.stat().st_mtime_ns
    load_rotation(path)
    assert path.read_bytes() == old
    assert path.stat().st_mtime_ns == modified


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("schema_version = 1", "schema_version = true"),
        ("schema_version = 1", "schema_version = 2"),
        ("550e8400-e29b-41d4-a716-446655440000", "not-a-uuid"),
        ("unit_class_id = 6", "unit_class_id = 1"),
        ("unit_spec = 1", "unit_spec = 5"),
        ('unit_class = "DEATHKNIGHT"', 'unit_class = "deathknight"'),
        ('title = "符文数量"', 'title = "符文能量"'),
        ('title = "符文数量"', 'title = "and"'),
        ('name = "心脏打击"', 'name = "灵界打击"'),
        ('name = "心脏打击"', 'name = "Idle"'),
        ('macro = "心脏打击"', 'macro = "未知宏"'),
        ('condition = "符文数量>=1"', 'condition = "未知条件>=1"'),
        ('condition = "符文数量>=1"', 'condition = "("'),
        ('condition = "符文数量>=1"', 'condition = ""'),
        ("liantian_cn.player_primary_power@dev", "player_primary_power@2.0"),
        ("liantian_cn.player_primary_power@dev", "../liantian_cn.player_primary_power@dev"),
        ("max_power = 120", "max_power = -1"),
        ("max_charges = 2", "max_charges = 2.0"),
        ("ignore_gcd = true", 'ignore_gcd = "true"'),
        ('key = "CTRL-NUMPAD1"', 'key = "ctrl-numpad1"'),
        ('key = "CTRL-NUMPAD1"', 'key = "CTRL-CTRL-NUMPAD1"'),
        ("bind_key = true", "bind_key = 1"),
        ("schema_version = 1", "schema_version = 1\nunknown = 42"),
    ],
)
def test_invalid_config_not_rewritten(tmp_path: Path, old: str, new: str) -> None:
    path = example_copy(tmp_path)
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(RotationError):
        load_rotation(path)
    assert path.read_bytes() == before


def test_implicit_idle_not_persisted_and_layout_repaired(tmp_path: Path) -> None:
    path = example_copy(tmp_path)
    source = path.read_text(encoding="utf-8")
    source = source[: source.rindex("[[rotation]]")]
    source = source.replace("x = 7", "x = 99") + "\n# 保留用户注释\n"
    path.write_text(source, encoding="utf-8")
    rotation = load_rotation(path)
    assert rotation.rules[-1].macro == "Idle"
    saved = path.read_text(encoding="utf-8")
    assert "# 保留用户注释" in saved
    assert saved.count('macro = "Idle"') == 1  # 显式启用/延迟规则保留；兜底不回写。
    assert "x = 99" not in saved
    assert 'macro_text = "/cast 死神的抚摩"' in saved
