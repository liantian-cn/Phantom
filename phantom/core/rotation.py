"""
Summary:
    加载单份 rotation、核验引用并持久化重新分配的条件布局。
Description:
    先校验用户内容和精确版本参数，再冻结输出；布局只是可重建的排错信息。
    TOML Kit 保留注释，仅修改 layout；表达式只解析语法和名称，不执行。
Key Variables:
    Rotation.conditions: 按配置顺序保存的独立条件实例。
    CLASS_IDS: Blizzard 职业 token 对应的亮度 ID。
Change Log:
    2026-09-13: Changed 迁用条件核心与基础校验器。
    2026-09-12: Added 第 7–9 步 rotation 加载与布局回写。
"""

from __future__ import annotations

import ast
import keyword
import os
import re
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import tomlkit
from tomlkit.items import AoT, Table

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Value
from phantom.core.condition.layout import allocate
from phantom.core.condition.registry import Registry
from phantom.core.pixels import PixelDecoder
from phantom.core.validation import Fields, Items, String
from phantom.core.validation import Table as TableValidator

CLASS_IDS = {
    "WARRIOR": 1,
    "PALADIN": 2,
    "HUNTER": 3,
    "ROGUE": 4,
    "PRIEST": 5,
    "DEATHKNIGHT": 6,
    "SHAMAN": 7,
    "MAGE": 8,
    "WARLOCK": 9,
    "MONK": 10,
    "DRUID": 11,
    "DEMONHUNTER": 12,
    "EVOKER": 13,
}


class RotationError(ValueError):
    """用户配置无法转换为可生成的 rotation。"""


def object_table(value: object, name: str) -> dict[str, object]:
    return TableValidator().validate(value, name)


def fields(table: dict[str, object], required: set[str], optional: set[str]) -> None:
    Fields(frozenset(required), frozenset(optional)).validate(table, "rotation")


def string(table: dict[str, object], name: str, *, empty: bool = False) -> str:
    return String(allow_empty=empty).validate(table.get(name), name)


def tables(value: object, name: str) -> list[dict[str, object]]:
    return Items(TableValidator()).validate(value, name)


def validate_addon_name(name: str) -> str:
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name, re.ASCII) is None:
        raise ValueError("插件包名必须匹配 [A-Za-z][A-Za-z0-9_]*")
    return name


def atomic_write(path: Path, content: str | bytes) -> None:
    """写完临时文件后替换单个目标，写入失败不留下截断的 TOML/TOC。"""
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content.encode("utf-8") if isinstance(content, str) else content)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@dataclass(frozen=True)
class Profile:
    title: str
    description: str
    unit_class: str
    unit_class_id: int
    unit_spec: int


@dataclass(frozen=True)
class Macro:
    name: str
    key: str
    bind_key: bool
    macro_text: str | None


@dataclass(frozen=True)
class Rule:
    condition: str
    macro: str
    annotate: str
    expression: ast.Expression | None


@dataclass(frozen=True)
class ConditionEntry:
    title: str
    plugin: str
    instance: Condition


@dataclass(frozen=True)
class Rotation:
    path: Path
    uuid: str
    profile: Profile
    conditions: tuple[ConditionEntry, ...]
    macros: tuple[Macro, ...]
    rules: tuple[Rule, ...]
    board_width: int

    def values(self, decoder: PixelDecoder) -> list[Value]:
        for x, expected in ((1, self.profile.unit_class_id), (2, self.profile.unit_spec)):
            cell = decoder.getCell(x, 1)
            if not cell.is_pure or not bool((cell.inner == expected).all()):
                raise ValueError("截图职业或专精与当前 rotation 不匹配")
        # 先提取全部区域，确保任何越界都不会产生半新半旧的业务快照。
        raw = [entry.instance.raw_value(decoder) for entry in self.conditions]
        return [entry.instance.value(*regions) for entry, regions in zip(self.conditions, raw)]


def parse_profile(value: object) -> Profile:
    table = object_table(value, "profile")
    fields(table, {"title", "description", "unit_class", "unit_spec"}, {"unit_class_id"})
    token = string(table, "unit_class")
    if token not in CLASS_IDS:
        raise ValueError("未知职业 token")
    class_id = table.get("unit_class_id", CLASS_IDS[token])
    if type(class_id) is not int or class_id != CLASS_IDS[token]:
        raise ValueError("unit_class_id 与职业 token 不一致")
    spec = table["unit_spec"]
    if type(spec) is not int or not 1 <= spec <= 4:
        raise ValueError("unit_spec 必须为专精顺序索引 1–4")
    return Profile(
        string(table, "title"), string(table, "description", empty=True), token, class_id, spec
    )


def parse_macros(value: object) -> tuple[Macro, ...]:
    result: list[Macro] = []
    names: set[str] = set()
    for table in tables(value, "macros"):
        fields(table, {"name", "key", "bind_key"}, {"macro_text"})
        name = string(table, "name")
        if name in names or name == "Idle":
            raise ValueError(f"宏名称重复或使用保留名：{name}")
        names.add(name)
        key = string(table, "key")
        parts = key.split("-")
        if (
            not re.fullmatch(r"(?:[A-Z0-9]+-)*[A-Z0-9]+", key)
            or any(part not in ("CTRL", "ALT", "SHIFT") for part in parts[:-1])
            or len(set(parts[:-1])) != len(parts[:-1])
        ):
            raise ValueError(f"键位必须为大写 WoW 格式：{key}")
        bind = table["bind_key"]
        if type(bind) is not bool:
            raise ValueError("bind_key 必须为布尔")
        macro_text = string(table, "macro_text") if bind or "macro_text" in table else None
        result.append(Macro(name, key, bind, macro_text))
    return tuple(result)


def parse_rules(value: object, names: set[str], macro_names: set[str]) -> tuple[Rule, ...]:
    result: list[Rule] = []
    rows = tables(value, "rotation")
    for index, table in enumerate(rows):
        fields(table, {"condition", "macro"}, {"annotate"})
        condition = string(table, "condition", empty=True).strip()
        macro = string(table, "macro")
        annotate = string(table, "annotate", empty=True) if "annotate" in table else ""
        if macro not in macro_names and macro != "Idle":
            raise ValueError(f"循环引用不存在的宏：{macro}")
        expression = None
        if not condition:
            if macro != "Idle" or index != len(rows) - 1:
                raise ValueError("空 condition 仅允许位于末尾显式 Idle")
        else:
            expression = ast.parse(condition, mode="eval")
            references = {node.id for node in ast.walk(expression) if isinstance(node, ast.Name)}
            if references - names:
                raise ValueError(f"表达式引用未知条件：{sorted(references - names)}")
        result.append(Rule(condition, macro, annotate, expression))
    if not result or result[-1].condition or result[-1].macro != "Idle":
        result.append(Rule("", "Idle", "隐含兜底", None))
    return tuple(result)


def load_rotation(path: Path, registry: Registry | None = None) -> Rotation:
    path = path.resolve()
    try:
        source = path.read_bytes().decode("utf-8")
        document = object_table(tomllib.loads(source), "rotation document")
        fields(
            document,
            {"schema_version", "uuid", "profile", "conditions", "macros", "rotation"},
            set(),
        )
        if type(document["schema_version"]) is not int or document["schema_version"] != 1:
            raise ValueError("schema_version 必须为整数 1")
        identifier = string(document, "uuid")
        parsed_uuid = UUID(identifier)
        if str(parsed_uuid) != identifier or parsed_uuid.variant != "specified in RFC 4122":
            raise ValueError("uuid 必须为带连字符的标准 RFC 4122 文本")
        profile = parse_profile(document["profile"])
        macros = parse_macros(document["macros"])
        loader = registry or Registry()
        entries: list[ConditionEntry] = []
        names: set[str] = set()
        for table in tables(document["conditions"], "conditions"):
            fields(table, {"title", "plugin"}, {"plugin_args", "layout"})
            title = string(table, "title")
            if (
                re.fullmatch(r"[A-Za-z\u3400-\u9fff][A-Za-z0-9_\u3400-\u9fff]*", title) is None
                or not title.isidentifier()
                or keyword.iskeyword(title)
                or title in names
            ):
                raise ValueError(f"条件标题非法或重复：{title}")
            names.add(title)
            plugin = string(table, "plugin")
            args = object_table(table.get("plugin_args", {}), f"{title}.plugin_args")
            entries.append(ConditionEntry(title, plugin, loader.create(plugin, args)))
        rules = parse_rules(document["rotation"], names, {macro.name for macro in macros})
        board_width = allocate([entry.instance for entry in entries])
        # 所有用户内容与插件均通过后才回写排错坐标，失败配置不被部分修改。
        editable = tomlkit.parse(source)
        condition_tables = editable["conditions"]
        changed = False
        if entries:
            assert isinstance(condition_tables, AoT)
            for table, entry in zip(condition_tables, entries):
                assert isinstance(table, Table)
                layout = entry.instance.layout()
                if table.get("layout") != layout:
                    table["layout"] = layout
                    changed = True
        if changed:
            if path.read_bytes().decode("utf-8") != source:
                raise ValueError("配置在加载期间被修改，请重新加载")
            atomic_write(path, tomlkit.dumps(editable))
        return Rotation(path, identifier, profile, tuple(entries), macros, rules, board_width)
    except (OSError, ValueError, TypeError, SyntaxError, OverflowError) as error:
        raise RotationError(f"Rotation {path}：{error}") from error
