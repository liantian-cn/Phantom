"""
Summary:
    从启动工作目录读取 Phantom 应用配置，首次运行写入默认文件。
Description:
    配置只在启动时加载，与程序和 rotation 文件的位置无关。
    缺失字段采用默认值；非法配置明确失败，已有文件不被自动改写。
Key Variables:
    AppConfig.path: 启动工作目录中的配置文件绝对路径。
    AppConfig.fps: 截图与界面读取最新快照的频率上限。
Change Log:
    2026-09-12: Added 第 5、6 步的工作目录 TOML 配置。
"""

import math
import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONFIG = """[capture]
fps = 15

[ui]
min_width = 120
min_height = 46
log_max_lines = 1000
"""


class ConfigurationError(ValueError):
    """应用配置无法读取或不满足字段约束。"""


@dataclass(frozen=True)
class AppConfig:
    path: Path
    fps: float = 15
    min_width: int = 120
    min_height: int = 46
    log_max_lines: int = 1000


def _table(document: dict[str, object], name: str) -> dict[str, object]:
    value = document.get(name, {})
    if not isinstance(value, dict):
        raise ConfigurationError(f"[{name}] 必须为 TOML 表")
    return {str(key): item for key, item in value.items()}


def _positive_integer(table: dict[str, object], name: str, default: int) -> int:
    value = table.get(name, default)
    if type(value) is not int or value <= 0:
        raise ConfigurationError(f"ui.{name} 必须为正整数")
    return value


def load_config(working_directory: Path) -> AppConfig:
    path = working_directory.resolve() / "phantom.toml"
    try:
        # 独占创建防止覆盖已有配置，包括存在检查与写入之间出现的新文件。
        try:
            with path.open("x", encoding="utf-8", newline="\n") as config_file:
                config_file.write(DEFAULT_CONFIG)
        except FileExistsError:
            pass
        with path.open("rb") as config_file:
            document = tomllib.load(config_file)
        capture = _table(document, "capture")
        ui = _table(document, "ui")
        fps = capture.get("fps", 15)
        if isinstance(fps, bool) or not isinstance(fps, (int, float)):
            raise ConfigurationError("capture.fps 必须为有限正数")
        fps_number = float(fps)
        if not math.isfinite(fps_number) or fps_number <= 0:
            raise ConfigurationError("capture.fps 必须为有限正数")
        return AppConfig(
            path=path,
            fps=fps_number,
            min_width=_positive_integer(ui, "min_width", 120),
            min_height=_positive_integer(ui, "min_height", 46),
            log_max_lines=_positive_integer(ui, "log_max_lines", 1000),
        )
    except (OSError, ValueError, OverflowError) as error:
        raise ConfigurationError(f"配置文件 {path}：{error}") from error
