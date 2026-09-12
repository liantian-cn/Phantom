from pathlib import Path

import pytest

from phantom.core.configuration import ConfigurationError, load_config


def test_config_uses_launch_directory_and_preserves_existing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    launch = tmp_path / "shortcut-start"
    program = tmp_path / "program"
    launch.mkdir()
    program.mkdir()
    monkeypatch.chdir(launch)
    config = load_config(Path.cwd())
    assert config.path == launch / "phantom.toml"
    assert config.fps == 15
    assert (config.min_width, config.min_height, config.log_max_lines) == (120, 46, 1000)
    assert not (program / "phantom.toml").exists()
    original = b"# keep comment\n[capture]\nfps = 7.5\n[ui]\nmin_width = 132\n"
    config.path.write_bytes(original)
    config = load_config(Path.cwd())
    assert (config.fps, config.min_width, config.min_height) == (7.5, 132, 46)
    assert config.path.read_bytes() == original
    assert Path.cwd() == launch


@pytest.mark.parametrize(
    "content",
    [
        "[capture\nfps = 15",
        "[capture]\nfps = 0",
        "[capture]\nfps = -1",
        "[capture]\nfps = nan",
        "[capture]\nfps = inf",
        "[capture]\nfps = true",
        '[capture]\nfps = "15"',
        "capture = 1",
        "ui = []",
        "[ui]\nmin_width = false",
        "[ui]\nmin_height = 0",
        "[ui]\nlog_max_lines = 3.5",
    ],
)
def test_invalid_config_fails_without_rewriting(tmp_path: Path, content: str) -> None:
    path = tmp_path / "phantom.toml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigurationError, match="phantom.toml"):
        load_config(tmp_path)
    assert path.read_text(encoding="utf-8") == content


def test_unreadable_or_unwritable_config_fails_explicitly(tmp_path: Path) -> None:
    (tmp_path / "phantom.toml").mkdir()
    with pytest.raises(ConfigurationError):
        load_config(tmp_path)
    with pytest.raises(ConfigurationError):
        load_config(tmp_path / "missing-directory")
