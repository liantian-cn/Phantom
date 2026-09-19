"""用途：仅按冻结的辅助战斗 TXT 显示顺序生成四十份中文循环，并可保存独立来源测试快照。

不读取 CSV、不推断隐藏字段、不加载循环或安装游戏插件。缺失冷却标签按零处理。
示例：.venv/Scripts/python .script/generate_assisted_rotations.py --freeze-source
"""

from __future__ import annotations

import argparse
import hashlib
import json
import keyword
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "WowAssistedCombatReveal/output"
SOURCE_FIXTURE = ROOT / "tests/fixtures/assisted_rotations_source.json"
RULE_PREFIX = "ASSISTED_COMBAT_RULE_TYPE_"

# 专精位置是 GetSpecialization 的索引；不从英文文件排序推断。
CLASSES: dict[str, tuple[str, str, int, dict[str, str]]] = {
    "deathknight": ("死亡骑士", "DEATHKNIGHT", 6, {"blood": "鲜血", "frost": "冰霜", "unholy": "邪恶"}),
    "demonhunter": ("恶魔猎手", "DEMONHUNTER", 12, {"havoc": "浩劫", "vengeance": "复仇", "devourer": "噬灭"}),
    "druid": ("德鲁伊", "DRUID", 11, {"balance": "平衡", "feral": "野性", "guardian": "守护", "restoration": "恢复"}),
    "evoker": ("唤魔师", "EVOKER", 13, {"devastation": "湮灭", "preservation": "恩护", "augmentation": "增辉"}),
    "hunter": ("猎人", "HUNTER", 3, {"beastmastery": "野兽控制", "marksmanship": "射击", "survival": "生存"}),
    "mage": ("法师", "MAGE", 8, {"arcane": "奥术", "fire": "火焰", "frost": "冰霜"}),
    "monk": ("武僧", "MONK", 10, {"brewmaster": "酒仙", "mistweaver": "织雾", "windwalker": "踏风"}),
    "paladin": ("圣骑士", "PALADIN", 2, {"holy": "神圣", "protection": "防护", "retribution": "惩戒"}),
    "priest": ("牧师", "PRIEST", 5, {"discipline": "戒律", "holy": "神圣", "shadow": "暗影"}),
    "rogue": ("潜行者", "ROGUE", 4, {"assassination": "奇袭", "outlaw": "狂徒", "subtlety": "敏锐"}),
    "shaman": ("萨满祭司", "SHAMAN", 7, {"elemental": "元素", "enhancement": "增强", "restoration": "恢复"}),
    "warlock": ("术士", "WARLOCK", 9, {"affliction": "痛苦", "demonology": "恶魔学识", "destruction": "毁灭"}),
    "warrior": ("战士", "WARRIOR", 1, {"arms": "武器", "fury": "狂怒", "protection": "防护"}),
}
DURATIONS = {268877: 10, 257622: 20, 191634: 15, 264571: 12, 335467: 6, 980: 18, 433891: 20}
STACKS = {195181: 12, 51124: 2, 1254252: 8, 203981: 20, 1245577: 15, 359618: 2, 1242974: 25, 1221389: 20, 202090: 4, 325202: 2, 393039: 20, 344179: 10, 264571: 2, 117828: 2}
IGNORED = {"AURA_COUNT_NEAR_PLAYER_GREATER", "AURA_COUNT_NEAR_PLAYER_LESS", "TARGET_COUNT_NEAR_TARGET_GREATER", "TARGET_COUNT_NEAR_TARGET_LESS"}
POWER_NAMES = {
    "RAGE": "怒气",
    "RUNIC_POWER": "符文能量",
    "LUNAR_POWER": "星界能量",
    "INSANITY": "狂乱值",
    "MANA": "法力百分比",
    "ENERGY": "能量",
    "FOCUS": "集中值",
    "SOUL_SHARDS": "灵魂碎片",
    "COMBO_POINTS": "连击点",
    "HOLY_POWER": "神圣能量",
    "CHI": "真气",
    "ESSENCE": "精华",
    "ARCANE_CHARGES": "奥术充能",
}
INTEGER_POWERS = {"COMBO_POINTS", "HOLY_POWER", "CHI", "ESSENCE", "ARCANE_CHARGES"}
POWER_MAX = {("deathknight/blood", "RUNIC_POWER"): 115, ("monk/windwalker", "ENERGY"): 120, ("priest/shadow", "INSANITY"): 150, ("rogue/outlaw", "ENERGY"): 200}
SPELL_TAG = re.compile(r"(?P<name>.+)\[id:(?P<id>\d+)(?:,cd:(?P<cd>\d+(?:\.\d+)?))?\]")
STEP_LINE = re.compile(r"(?P<index>\d+): Spell: (?P<tag>.+)")
RULE_LINE = re.compile(r"\s+(?P<text>.+?)\s+-- ASSISTED_COMBAT_RULE_TYPE_(?P<type>[A-Z_]+)\s*")
QUOTED_TAG = re.compile(r"'(.+?\[id:\d+(?:,cd:\d+(?:\.\d+)?)?\])'")
COMPARISON = re.compile(r"(大于等于|小于等于|大于|小于)\s+(\d+(?:\.\d+)?)")
OPS = {"大于等于": ">=", "小于等于": "<=", "大于": ">", "小于": "<"}


@dataclass(frozen=True)
class Spell:
    name: str
    id: int
    cooldown: float


@dataclass(frozen=True)
class Rule:
    type: str
    text: str
    line: int


@dataclass
class Step:
    index: int
    spell: Spell
    line: int
    rules: list[Rule] = field(default_factory=list)


@dataclass
class Source:
    path: str
    text: str
    steps: list[Step]

    @property
    def spec(self) -> str:
        return self.path.removesuffix(".txt")


def parse_spell(text: str) -> Spell:
    match = SPELL_TAG.fullmatch(text)
    if match is None:
        raise ValueError(f"无效技能标签：{text}")
    return Spell(match["name"], int(match["id"]), float(match["cd"] or 0))


def parse_source(path: str, text: str) -> Source:
    steps: list[Step] = []
    for number, line in enumerate(text.splitlines(), 1):
        if number == 1:
            if not line.strip() or ":" in line:
                raise ValueError(f"{path}:{number}: 缺少专精标题")
            continue
        if not line.strip():
            continue
        step_match = STEP_LINE.fullmatch(line)
        rule_match = RULE_LINE.fullmatch(line)
        try:
            if step_match:
                steps.append(Step(int(step_match["index"]), parse_spell(step_match["tag"]), number))
            elif rule_match and steps:
                steps[-1].rules.append(Rule(rule_match["type"], rule_match["text"], number))
            else:
                raise ValueError(f"无法识别 TXT 行：{line}")
        except ValueError as error:
            raise ValueError(f"{path}:{number}: {error}") from error
    if not steps:
        raise ValueError(f"{path}: 缺少步骤")
    return Source(path, text, steps)


def read_sources(directory: Path) -> list[Source]:
    expected = {f"{unit_class}/{spec}.txt" for unit_class, (_, _, _, specs) in CLASSES.items() for spec in specs}
    actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*.txt")}
    if actual != expected:
        raise ValueError(f"TXT 集合不符：缺少 {sorted(expected - actual)}，多出 {sorted(actual - expected)}")
    return [parse_source(path, (directory / path).read_text(encoding="utf-8-sig")) for path in sorted(expected)]


def rule_spell(rule: Rule) -> Spell:
    match = QUOTED_TAG.search(rule.text)
    if match is None:
        raise ValueError(f"规则没有带 ID 的技能标签：{rule.text}")
    return parse_spell(match[1])


def comparison(rule: Rule, divisor: int = 1) -> tuple[str, int | float]:
    match = COMPARISON.search(rule.text)
    if match is None:
        raise ValueError(f"规则缺少明确比较：{rule.text}")
    value = float(match[2]) / divisor
    return OPS[match[1]], int(value) if value.is_integer() else value


def identifier(text: str) -> str:
    result = "".join(character for character in text if character == "_" or character.isalnum())
    if not result or not result.isidentifier() or keyword.iskeyword(result):
        result = "条件" + result
    if not result.isidentifier():
        raise ValueError(f"不能转换为条件标识符：{text}")
    return result


def width_for(value: int) -> int:
    return min(8, max(1, math.ceil(value / 4)))


class Builder:
    def __init__(self, source: Source) -> None:
        self.source = source
        self.conditions: list[dict[str, Any]] = []
        self.condition_keys: dict[str, str] = {}
        self.titles: set[str] = set()
        self.notes: dict[str, None] = {}
        self.names: dict[str, set[int]] = {}
        for step in source.steps:
            self.names.setdefault(identifier(step.spell.name), set()).add(step.spell.id)
            for rule in step.rules:
                for match in QUOTED_TAG.finditer(rule.text):
                    spell = parse_spell(match[1])
                    self.names.setdefault(identifier(spell.name), set()).add(spell.id)

    def name(self, spell: Spell) -> str:
        if spell.name == "Unknown Spell":
            return f"未知技能{spell.id}"
        name = identifier(spell.name)
        return f"{name}_{spell.id}" if len(self.names[name]) > 1 else name

    def add(self, title: str, plugin: str, args: dict[str, object] | None = None) -> str:
        args = {} if args is None else args
        key = json.dumps([plugin, args], sort_keys=True)
        if key in self.condition_keys:
            return self.condition_keys[key]
        title = identifier(title)
        if title in self.titles:
            raise ValueError(f"不同条件的标题冲突：{title}")
        self.titles.add(title)
        self.condition_keys[key] = title
        self.conditions.append({"title": title, "plugin": plugin + "@dev", "plugin_args": args})
        return title

    def atom(self, title: str, plugin: str, args: dict[str, object], op: str = "==", value: bool | int | float = True) -> str:
        return f"({self.add(title, plugin, args)} {op} {value})"

    def note(self, text: str) -> None:
        self.notes[text] = None

    def map_rule(self, step: Step, rule: Rule) -> str | None:
        kind = rule.type
        if kind in IGNORED:
            return None
        if kind == "AUTOMATION_ONLY":
            return None
        if kind in {"SPELL_LEARNED", "AFFORD_COST", "COOLDOWN_ALLOW_CASTING_SUCCESS", "SPELL_OFF_COOLDOWN", "SPELL_ON_COOLDOWN", "COOLDOWN_REMAINING_GREATER", "COOLDOWN_REMAINING_LESS"}:
            spell = rule_spell(rule)
            name = self.name(spell)
            if kind == "SPELL_LEARNED":
                self.note("天赋条件按技能 ID 查询已知/法术书状态，不解析天赋树。")
                plugin = "talent_known" if "天赋" in rule.text else "spell_known"
                return self.atom(f"已学会{name}", plugin, {"spell_ids": [spell.id]})
            if kind in {"AFFORD_COST", "COOLDOWN_ALLOW_CASTING_SUCCESS"}:
                self.note("资源可支付/成功施放规则映射 spell_usable 的 isUsable；不保证所有实际施放条件。")
                return self.atom(f"{name}可用", "spell_usable", {"spell_ids": [spell.id]})
            op, value = ("==", 0) if kind == "SPELL_OFF_COOLDOWN" else (">", 0) if kind == "SPELL_ON_COOLDOWN" else comparison(rule, 1000)
            return self.atom(f"{name}冷却", "spell_cooldown", {"spell_ids": [spell.id], "ignore_gcd": True}, op, value)
        if kind.startswith("TARGET_DISTANCE_"):
            if kind not in {"TARGET_DISTANCE_LESS", "TARGET_DISTANCE_GREATER"}:
                raise ValueError(f"未知规则 {kind}")
            self.note("距离条件近似为当前步骤技能射程，忽略 TXT 码数；无效技能/无目标/nil 射程也返回 False。")
            return self.atom(f"目标在{self.name(step.spell)}技能范围内", "target_in_range", {"spell_id": step.spell.id}, value=kind.endswith("LESS"))
        if kind == "SPELL_IN_RANGE":
            self.note("技能射程规则使用当前步骤动作 ID 对 target 的射程结果，无效射程返回 False。")
            return self.atom(f"{self.name(step.spell)}对目标在射程内", "spell_in_range", {"spell_id": step.spell.id, "unit_token": "target"})
        if kind in {"TARGET_COUNT_NEAR_PLAYER_GREATER", "TARGET_COUNT_NEAR_PLAYER_LESS"}:
            self.note("玩家周围人数近似为本步骤技能可攻击敌人总数，仅可观察 nameplate1–40；secret/nil 射程漏计，不代表原码数圆内完整人数。")
            op, value = comparison(rule)
            return self.atom(f"{self.name(step.spell)}技能可攻击敌人总数", "player_melee_enemies_count", {"spell_id": step.spell.id, "combat_only": False}, op, value)
        if kind in {"AURA_ON_PLAYER", "AURA_MISSING_PLAYER", "AURA_ON_TARGET", "AURA_MISSING_TARGET"}:
            spell = rule_spell(rule)
            player = kind.endswith("PLAYER")
            self.aura_note(player)
            return self.atom(
                f"{'玩家' if player else '目标'}有{self.name(spell)}{'增益' if player else '减益'}", "player_has_buff" if player else "target_has_debuff", {"buff_ids" if player else "aura_ids": [spell.id]}, value="MISSING" not in kind
            )
        if kind in {"AURA_DURATION_PLAYER", "AURA_DURATION_TARGET", "PLAYER_AURA_APPLICATION_GREATER", "PLAYER_AURA_APPLICATION_LESS", "TARGET_AURA_APPLICATION_GREATER", "TARGET_AURA_APPLICATION_LESS"}:
            spell = rule_spell(rule)
            player = "PLAYER" in kind
            self.aura_note(player)
            duration = kind.startswith("AURA_DURATION")
            suffix = "剩余秒数" if duration else "层数"
            plugin = f"aura_{'player_buff' if player else 'target_debuff'}_{'duration' if duration else 'stacks'}"
            limit = (DURATIONS if duration else STACKS)[spell.id]
            args: dict[str, object] = {"aura_ids": [spell.id]}
            if duration:
                args.update(duration=limit, width=width_for(limit))
                self.note("光环秒数以固定 duration 换算；实际实例时长、延长和天赋变化会产生误差。")
            else:
                args.update(max_value=limit, min_value=0, width=width_for(limit))
                self.note("层数使用固定显示量程；超量程饱和，零填充不能区分无光环与零层。")
                if spell.id == 393039:
                    self.note("皇帝的容电器为 TXT 遗留规则，仍按原 ID 393039 和阈值保留。")
            op, value = comparison(rule, 1000 if duration else 1)
            return self.atom(f"{'玩家' if player else '目标'}{self.name(spell)}{suffix}", plugin, args, op, value)
        if kind in {"SPELL_CHARGES_GREATER", "SPELL_CHARGES_LESS"}:
            op, value = comparison(rule)
            if op != ">=" or value != 2:
                raise ValueError("冻结充能方案仅接受 TXT 的充能 >= 2")
            self.note("充能 max_charges=2 是本批阈值所需显示量程，不宣称技能真实上限为 2。")
            return self.atom(f"{self.name(step.spell)}充能", "spell_charges", {"spell_ids": [step.spell.id], "max_charges": 2, "width": 1}, op, value)
        if kind in {"PLAYER_HEALTH_PCT_GREATER", "PLAYER_HEALTH_PCT_LESS", "HEALTH_PCT_GREATER", "HEALTH_PCT_LESS"}:
            player = kind.startswith("PLAYER")
            op, value = comparison(rule)
            return self.atom("玩家当前血量百分比" if player else "目标当前血量百分比", "player_health_pct" if player else "target_health_pct", {"use_predicted": False}, op, value)
        if kind in {"HAS_PET", "HAS_NO_PET"}:
            self.note("宠物条件只统计存在且存活的 pet 单位，不统计临时召唤物。")
            return self.atom("玩家有存活宠物", "player_has_pet", {}, value=kind == "HAS_PET")
        if kind in {"HOSTILE_TARGET", "FRIENDLY_TARGET"}:
            return self.atom("目标是敌人" if kind == "HOSTILE_TARGET" else "目标可辅助", "target_is_enemy" if kind == "HOSTILE_TARGET" else "target_can_assist", {})
        power, _, direction = kind.rpartition("_")
        if power in POWER_NAMES and direction in {"GREATER", "LESS"}:
            divisor = 100 if power == "INSANITY" else 10 if power in {"RAGE", "RUNIC_POWER", "SOUL_SHARDS", "LUNAR_POWER", "MANA"} else 1
            op, value = comparison(rule, divisor)
            args = {}
            if power == "SOUL_SHARDS":
                fractional = self.source.spec == "warlock/destruction"
                args = {"fractional": fractional}
                if fractional:
                    args["width"] = 25
                self.note("灵魂碎片 TXT 除以 10；毁灭使用 0..50 片段 ValueBar / 10 浮点模式，其他专精保留整数碎片。")
            elif power not in INTEGER_POWERS:
                maximum = POWER_MAX.get((self.source.spec, power), 100)
                args = {"max_power": maximum}
                self.note("资源 max_power 为固定参考，须按天赋调整；临时上限变化会有误差，Cell 量化步长约为 max_power/255。")
                if power == "MANA":
                    self.note("法力特例：TXT 数值除以 10 作为百分比，max_power=100，不作绝对法力值。")
                if (self.source.spec, power) in POWER_MAX:
                    reference = {"deathknight/blood": "鲜血符文能量 115", "monk/windwalker": "踏风能量 120（Ascension）", "priest/shadow": "暗影狂乱值 150（Voidtouched）", "rogue/outlaw": "狂徒能量 200（精力 2 级）"}[self.source.spec]
                    self.note(f"本专精固定资源参考：{reference}。")
            return self.atom(f"玩家{POWER_NAMES[power]}", "spec_power_" + power.lower(), args, op, value)
        raise ValueError(f"未知规则 {kind}")

    def aura_note(self, player: bool) -> None:
        self.note("玩家光环限定 HELPFUL 增益；TXT 的增益/减益合称按现有插件能力映射。" if player else "目标光环限定不可辅助目标的 PLAYER|HARMFUL 减益；PLAYER 包含玩家、宠物和载具，排除其他来源。")

    def build(self) -> tuple[str, str]:
        unit_class, spec = self.source.spec.split("/")
        chinese, token, class_id, specs = CLASSES[unit_class]
        stem = f"{chinese}-{specs[spec]}"
        enabled = self.add("插件启用", "enable")
        macros: dict[str, None] = {}
        rows: list[dict[str, str]] = []
        row_comments: list[list[str]] = []
        for step in self.source.steps:
            atoms = [f"({enabled} == True)"]
            comments = [f"来源 {self.source.path}:{step.line}，步骤 {step.index}，动作 ID {step.spell.id}，TXT 冷却 {step.spell.cooldown:g} 秒。"]
            if step.spell.cooldown >= 60:
                atoms.append(f"({self.add('爆发开启', 'in_burst')} == True)")
            for rule in step.rules:
                try:
                    atom = self.map_rule(step, rule)
                except (ValueError, KeyError) as error:
                    raise ValueError(f"{self.source.path}:{rule.line}: {error}") from error
                if atom is not None:
                    atoms.append(atom)
                else:
                    reason = "仅作来源标记，保留步骤" if rule.type == "AUTOMATION_ONLY" else "按冻结方案仅删除此条件，保留步骤"
                    comments.append(f"来源行 {rule.line}：{rule.type}；{reason}。原文：{rule.text}")
            if not step.rules:
                comments.append("TXT 原无条件步骤，仍在原位置并保留启用/适用爆发门控。")
            macros[step.spell.name] = None
            rows.append({"condition": " and ".join(atoms), "macro": step.spell.name, "annotate": f"来源步骤 {step.index}：{step.spell.name}（ID {step.spell.id}）"})
            row_comments.append(comments)
        lines = [
            "# 此文件由 .script/generate_assisted_rotations.py 按冻结 TXT 显示顺序生成。",
            f"# 唯一规则来源：{self.source.path}；未读取 CSV 或补充隐藏字段。",
            "# 所有叶子条件按 AND 保留顺序；无冷却标签按 0 秒；仅启用与动作冷却 >= 60 秒的爆发门控。",
        ]
        lines.extend("# " + note for note in self.notes)
        lines.extend(
            [
                "schema_version = 1",
                f"uuid = {literal(str(uuid5(NAMESPACE_URL, 'phantom:assisted-txt:' + self.source.spec)))}",
                "",
                "[profile]",
                f"title = {literal(stem)}",
                f"description = {literal(chinese + '一键辅助')}",
                f"unit_class = {literal(token)}",
                f"unit_class_id = {class_id}",
                f"unit_spec = {list(specs).index(spec) + 1}",
            ]
        )
        for condition in self.conditions:
            lines.extend(["", "[[conditions]]", f"title = {literal(condition['title'])}", f"plugin = {literal(condition['plugin'])}"])
            if condition["plugin_args"]:
                lines.append("[conditions.plugin_args]")
                lines.extend(f"{key} = {literal(value)}" for key, value in condition["plugin_args"].items())
        for name in macros:
            lines.extend(["", "[[macros]]", f"name = {literal(name)}", f"macro_text = {literal('/cast ' + name)}"])
        for row, comments in zip(rows, row_comments, strict=True):
            lines.append("")
            lines.extend("# " + comment for comment in comments)
            lines.append("[[rotation]]")
            lines.extend(f"{key} = {literal(value)}" for key, value in row.items())
        lines.extend(["", "[[rotation]]", 'condition = ""', 'macro = "Idle"', 'annotate = "末尾兜底"', ""])
        return stem + ".toml", "\n".join(lines)


def literal(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def freeze_sources(sources: list[Source]) -> None:
    # 独立保存 TXT 原文，而不是由生成 TOML 反推期望；常驻测试不访问外部目录。
    fixture = {
        "format": 1,
        "description": "冻结 TXT 原文，仅作为来源语义与顺序的独立证据；更新必须与源变更一同审阅。",
        "sources": [{"path": source.path, "sha256": hashlib.sha256(source.text.encode("utf-8")).hexdigest(), "text": source.text} for source in sources],
    }
    SOURCE_FIXTURE.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="包含职业/专精.txt 的来源目录")
    parser.add_argument("--destination", type=Path, default=ROOT / "rotations", help="中文 TOML 输出目录")
    parser.add_argument("--freeze-source", action="store_true", help="显式更新仓库内独立来源 fixture")
    args = parser.parse_args()
    sources = read_sources(args.source)
    # 完整解析、映射全部来源后才写文件，未知规则不会留下半批结果。
    outputs = [Builder(source).build() for source in sources]
    counts = Counter(rule.type for source in sources for step in source.steps for rule in step.rules)
    steps = [step for source in sources for step in source.steps]
    summary = {
        "specs": len(sources),
        "steps": len(steps),
        "rules": sum(counts.values()),
        "burst": sum(step.spell.cooldown >= 60 for step in steps),
        "unconditional": sum(not step.rules for step in steps),
        "ignored": sum(counts[kind] for kind in IGNORED),
        "automation_only": counts["AUTOMATION_ONLY"],
    }
    expected = {"specs": 40, "steps": 693, "rules": 3116, "burst": 80, "unconditional": 39, "ignored": 68, "automation_only": 46}
    if summary != expected:
        raise ValueError(f"冻结来源统计不符，停止写入：实际 {summary}；期望 {expected}")
    args.destination.mkdir(parents=True, exist_ok=True)
    for filename, text in outputs:
        (args.destination / filename).write_text(text, encoding="utf-8", newline="\n")
    if args.freeze_source:
        freeze_sources(sources)
    print(json.dumps(summary, ensure_ascii=False))
    for source, (filename, _) in zip(sources, outputs, strict=True):
        print(f"{source.path}:1-{len(source.text.splitlines())} -> {filename} ({len(source.steps)} steps)")


if __name__ == "__main__":
    main()
