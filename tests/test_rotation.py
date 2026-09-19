from pathlib import Path

import pytest
import tomlkit

from phantom.core.rotation import RotationError, load_rotation

FIXTURE = Path(__file__).parent / "fixtures/rotation-validation.toml"


def fixture_copy(tmp_path: Path) -> Path:
    path = tmp_path / "rotation.toml"
    path.write_bytes(FIXTURE.read_bytes())
    return path


def test_memory_layout_idempotent_and_optional_class_id(tmp_path: Path) -> None:
    path = fixture_copy(tmp_path)
    document = tomlkit.parse(path.read_text(encoding="utf-8"))
    del document["profile"]["unit_class_id"]
    path.write_text(tomlkit.dumps(document), encoding="utf-8")
    rotation = load_rotation(path)
    assert rotation.profile.unit_class_id == 6
    assert rotation.board_width == 28
    assert len(rotation.rules) == 3
    assert len(rotation.macros) == 2
    assert rotation.conditions[5].plugin == "spell_gcd@dev"
    assert [e.instance.regions[0].x for e in rotation.conditions] == [1, 2, 3, 1, 4, 5]
    saved = tomlkit.parse(path.read_text(encoding="utf-8"))
    assert "unit_class_id" not in saved["profile"]
    assert "layout" not in path.read_text(encoding="utf-8")
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
        ("player_primary_power@dev", "player_primary_power@2.0"),
        ("player_primary_power@dev", "../player_primary_power@dev"),
        ("max_power = 120", "max_power = -1"),
        ("max_charges = 2", "max_charges = 2.0"),
        ("ignore_gcd = true", 'ignore_gcd = "true"'),
        ('macro_text = "/cast 心脏打击"', ""),
        ('macro_text = "/cast 心脏打击"', 'macro_text = "  "'),
        ('macro_text = "/cast 心脏打击"', "macro_text = false"),
        ("schema_version = 1", "schema_version = 1\nunknown = 42"),
    ],
)
def test_invalid_config_not_rewritten(tmp_path: Path, old: str, new: str) -> None:
    path = fixture_copy(tmp_path)
    source = path.read_text(encoding="utf-8")
    assert old in source
    path.write_text(source.replace(old, new), encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(RotationError):
        load_rotation(path)
    assert path.read_bytes() == before


def test_implicit_idle_not_persisted_and_legacy_layout_preserved(tmp_path: Path) -> None:
    path = fixture_copy(tmp_path)
    source = path.read_text(encoding="utf-8")
    legacy = 'layout = { output_type = "invalid", regions = [{ x = 99, y = -1 }] } # 旧坐标\n'
    source = source.replace('plugin = "player_health_pct@dev"\n', 'plugin = "player_health_pct@dev"\n' + legacy) + "\n# 保留用户注释\n"
    path.write_text(source, encoding="utf-8")
    rotation = load_rotation(path)
    assert rotation.rules[-1].macro == "Idle"
    saved = path.read_text(encoding="utf-8")
    assert "# 保留用户注释" in saved
    assert 'macro = "Idle"' not in saved
    assert legacy in saved
    assert rotation.conditions[0].instance.regions[0].x == 1
    assert 'macro_text = "/cast 心脏打击"' in saved
