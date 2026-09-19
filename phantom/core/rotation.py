"""
Summary:
    加载单份 rotation、核验引用并补写缺失的条件插件默认参数。
Description:
    先校验用户内容和精确版本参数，再冻结内存布局；旧 layout 兼容保留但不使用或更新。
    TOML Kit 按键补写默认值并保留用户显式配置；表达式加载时完成白名单及类型校验。
Key Variables:
    Rotation.conditions: 按配置顺序保存的独立条件实例。
    CLASS_IDS: Blizzard 职业 token 对应的亮度 ID。
Change Log:
    2026-09-19: Changed 按宏声明顺序分配固定快捷键，忽略旧键位字段并统一要求宏文本。
    2026-09-19: Changed 停止布局回写，全部校验成功后递归补齐插件声明的默认参数。
    2026-09-14: Changed 仅以配置条件求值，向插件传递当前帧解码器。
    2026-09-14: Changed 冻结解析后的按键组合，支持内置通用布尔表达式变量。
    2026-09-13: Changed 加载时校验表达式类型并提供单帧优先级试运行。
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
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID

import tomlkit
from tomlkit.container import OutOfOrderTableProxy
from tomlkit.items import AoT, InlineTable, Table

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Output, Value
from phantom.core.condition.layout import allocate
from phantom.core.condition.registry import Registry
from phantom.core.expression import evaluate, parse_expression
from phantom.core.keyboard.contracts import KeyCombination, parse_key
from phantom.core.macro_keys import MACRO_KEYS
from phantom.core.pixels import PixelDecoder
from phantom.core.validation import Fields, Items, String
from phantom.core.validation import Table as TableValidator

CLASS_IDS = {"WARRIOR": 1, "PALADIN": 2, "HUNTER": 3, "ROGUE": 4, "PRIEST": 5, "DEATHKNIGHT": 6, "SHAMAN": 7, "MAGE": 8, "WARLOCK": 9, "MONK": 10, "DRUID": 11, "DEMONHUNTER": 12, "EVOKER": 13}


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


def fill_config_defaults(table: Table | InlineTable | OutOfOrderTableProxy, defaults: Mapping[str, object]) -> bool:
    """只补缺失键，原位修改 TOML 节点以保留显式值、键顺序和注释。"""
    changed = False
    for key, default in defaults.items():
        if key not in table:
            # 新默认值先按行内值转换，避免点分键下的嵌套表或表数组生成脱离父级的表头。
            inline = tomlkit.inline_table()
            inline[key] = default
            table[key] = inline[key]
            changed = True
        else:
            current = table[key]
            if isinstance(current, (Table, InlineTable, OutOfOrderTableProxy)) and isinstance(default, Mapping):
                changed = fill_config_defaults(current, default) or changed
    return changed


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
    macro_text: str
    keys: KeyCombination = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "keys", parse_key(self.key))


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
class Decision:
    values: tuple[Value, ...]
    rule_index: int
    rule: Rule
    macro: Macro | None


@dataclass(frozen=True)
class Rotation:
    path: Path
    uuid: str
    profile: Profile
    conditions: tuple[ConditionEntry, ...]
    macros: tuple[Macro, ...]
    rules: tuple[Rule, ...]
    board_width: int

    def decide(self, values: list[Value]) -> Decision:
        if len(values) != len(self.conditions) or any(not entry.instance.output.accepts(value) for entry, value in zip(self.conditions, values)):
            raise ValueError("决策条件值与声明不匹配")
        snapshot = {entry.title: value.copy() if isinstance(value, list) else value for entry, value in zip(self.conditions, values)}
        for index, rule in enumerate(self.rules, 1):
            if rule.expression is None or evaluate(rule.expression, snapshot):
                macro = next((item for item in self.macros if item.name == rule.macro), None)
                return Decision(tuple(snapshot[entry.title] for entry in self.conditions), index, rule, macro)
        raise ValueError("rotation 缺少 Idle 兜底")

    def trial(self, decoder: PixelDecoder) -> Decision:
        """同一帧解码与求值；发送由运行器负责。"""
        return self.decide(self.values(decoder))

    def values(self, decoder: PixelDecoder) -> list[Value]:
        for x, expected in ((1, self.profile.unit_class_id), (2, self.profile.unit_spec)):
            cell = decoder.getCell(x, 1)
            if not cell.is_pure or not bool((cell.inner == expected).all()):
                raise ValueError("截图职业或专精与当前 rotation 不匹配")
        # 先提取全部区域，确保任何越界都不会产生半新半旧的业务快照。
        raw = [entry.instance.raw_value(decoder) for entry in self.conditions]
        return [entry.instance.value(*regions, decoder=decoder) for entry, regions in zip(self.conditions, raw)]


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
    return Profile(string(table, "title"), string(table, "description", empty=True), token, class_id, spec)


def parse_macros(value: object) -> tuple[Macro, ...]:
    result: list[Macro] = []
    names: set[str] = set()
    rows = tables(value, "macros")
    if len(rows) > len(MACRO_KEYS):
        raise ValueError(f"宏数量 {len(rows)} 超过快捷键容量 {len(MACRO_KEYS)}")
    for index, table in enumerate(rows):
        # 旧键位字段只允许残留，不读取其值，也不参与分配或校验。
        fields(table, {"name", "macro_text"}, {"key", "bind_key"})
        name = string(table, "name")
        if name in names or name == "Idle":
            raise ValueError(f"宏名称重复或使用保留名：{name}")
        names.add(name)
        result.append(Macro(name, MACRO_KEYS[index], string(table, "macro_text")))
    return tuple(result)


def parse_rules(value: object, outputs: dict[str, Output], macro_names: set[str]) -> tuple[Rule, ...]:
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
            try:
                expression = parse_expression(condition, outputs)
            except (ValueError, SyntaxError) as error:
                raise ValueError(f"rotation[{index + 1}] {condition!r}：{error}") from error
        result.append(Rule(condition, macro, annotate, expression))
    if not result or result[-1].condition or result[-1].macro != "Idle":
        result.append(Rule("", "Idle", "隐含兜底", None))
    return tuple(result)


def load_rotation(path: Path, registry: Registry | None = None) -> Rotation:
    path = path.resolve()
    try:
        source = path.read_bytes().decode("utf-8")
        document = object_table(tomllib.loads(source), "rotation document")
        fields(document, {"schema_version", "uuid", "profile", "conditions", "macros", "rotation"}, set())
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
            if re.fullmatch(r"[A-Za-z\u3400-\u9fff][A-Za-z0-9_\u3400-\u9fff]*", title) is None or not title.isidentifier() or keyword.iskeyword(title) or title in names:
                raise ValueError(f"条件标题非法或重复：{title}")
            names.add(title)
            plugin = string(table, "plugin")
            args = object_table(table.get("plugin_args", {}), f"{title}.plugin_args")
            entries.append(ConditionEntry(title, plugin, loader.create(plugin, args)))
        rules = parse_rules(document["rotation"], {entry.title: entry.instance.output for entry in entries}, {macro.name for macro in macros})
        board_width = allocate([entry.instance for entry in entries])
        # 先由插件检查必填字段和显式值；全部校验及布局成功后才补写默认值。
        editable = tomlkit.parse(source)
        condition_tables = editable["conditions"]
        changed = False
        if entries:
            assert isinstance(condition_tables, AoT)
            for table, entry in zip(condition_tables, entries):
                assert isinstance(table, Table)
                defaults = entry.instance.config_defaults
                if not defaults:
                    continue
                if "plugin_args" not in table:
                    table["plugin_args"] = tomlkit.table()
                arguments = table["plugin_args"]
                assert isinstance(arguments, (Table, InlineTable, OutOfOrderTableProxy))
                changed = fill_config_defaults(arguments, defaults) or changed
        if changed:
            if path.read_bytes().decode("utf-8") != source:
                raise ValueError("配置在加载期间被修改，请重新加载")
            content = tomlkit.dumps(editable)
            # TOML Kit 新节点默认使用 LF；纯 CRLF 文件延续原风格，混合换行不全量规整。
            if "\r\n" in source and "\n" not in source.replace("\r\n", ""):
                content = content.replace("\r\n", "\n").replace("\n", "\r\n")
            atomic_write(path, content)
        return Rotation(path, identifier, profile, tuple(entries), macros, rules, board_width)
    except (OSError, ValueError, TypeError, SyntaxError, OverflowError) as error:
        raise RotationError(f"Rotation {path}：{error}") from error
