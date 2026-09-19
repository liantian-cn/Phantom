"""验证正式示例已显式保存默认参数，离线读取不再改写它。"""

import tomllib
from pathlib import Path

from phantom.core.rotation import load_rotation


def test_blood_example_has_no_layout_and_needs_no_default_writeback(tmp_path: Path) -> None:
    source = (Path(__file__).resolve().parents[1] / "rotations/blood-dk.toml").read_bytes()
    document = tomllib.loads(source.decode("utf-8"))
    assert all("layout" not in condition for condition in document["conditions"])
    path = tmp_path / "blood-dk.toml"
    path.write_bytes(source)
    modified = path.stat().st_mtime_ns

    rotation = load_rotation(path)

    assert len(rotation.conditions) == len(document["conditions"])
    assert any(entry.instance.regions for entry in rotation.conditions)
    assert path.read_bytes() == source
    assert path.stat().st_mtime_ns == modified
