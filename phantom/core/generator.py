"""
Summary:
    将单份 rotation 生成到零售 WoW 的 AddOns 目录。
Description:
    先验证并生成完整内容，再覆盖同名文件，最后发布只引用本次文件的 TOC。
    包含共享 media 资源并保留未引用的旧文件；UUID Lua 用职业专精守卫隔离条件实例。
Key Variables:
    GenerationResult.directory: 本次插件输出目录。
Change Log:
    2026-09-14: Changed 生成 bind_key 宏安全按钮，按 Lua 5.1 规则转义文本。
    2026-09-12: Added 第 10 步离线生成链路。
    2026-09-12: Fixed 生成包漏掉面板字体与图标边框资源。
"""

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid5

from phantom.core.rotation import Rotation, atomic_write, load_rotation, validate_addon_name

LUA_ROOT = Path(__file__).resolve().parents[1] / "lua"


@dataclass(frozen=True)
class GenerationResult:
    directory: Path
    rotation: Rotation
    files: tuple[str, ...]


def render(rotation: Rotation, addon_name: str) -> dict[str, str]:
    validate_addon_name(addon_name)
    files: dict[str, str] = {}
    for directory in ("runtime", "general"):
        for path in sorted((LUA_ROOT / directory).glob("*.lua")):
            files[path.relative_to(LUA_ROOT).as_posix()] = path.read_text(encoding="utf-8")
    # 配置中的文本不会作为 Lua 代码插入；token 已经过职业白名单校验。
    source = (
        "local addonName, addonTable = ...\n"
        f'if select(2, UnitClass("player")) ~= "{rotation.profile.unit_class}" '
        f"or C_SpecializationInfo.GetSpecialization() ~= {rotation.profile.unit_spec} then\n"
        "    return\nend\n\n"
    )
    for index, entry in enumerate(rotation.conditions):
        instance_id = str(uuid5(UUID(rotation.uuid), str(index)))
        source += "do\n" + entry.instance.generate_lua(instance_id) + "\nend\n\n"
    for index, macro in enumerate(rotation.macros):
        if not macro.bind_key:
            continue
        # 名称不包含用户文本；宏文本只作为字符串传给安全按钮。
        button = addon_name + "Button" + UUID(rotation.uuid).hex + str(index)
        source += (
            "do\n"
            f"    local buttonName = {lua_string(button)}\n"
            '    local frame = CreateFrame("Button", buttonName, UIParent, "SecureActionButtonTemplate")\n'
            '    frame:SetAttribute("type", "macro")\n'
            f'    frame:SetAttribute("macrotext", {lua_string(macro.macro_text or "")})\n'
            '    frame:RegisterForClicks("AnyDown", "AnyUp")\n'
            f"    SetOverrideBindingClick(frame, true, {lua_string(macro.key)}, buttonName)\n"
            "end\n\n"
        )
    files[f"{rotation.uuid}.lua"] = source
    template = (LUA_ROOT / "addonTemplateName.toc").read_text(encoding="utf-8")
    metadata = [
        line.replace("addonTemplateName", addon_name)
        for line in template.splitlines()
        if line.startswith("##")
    ]
    toc = "\n".join(metadata) + "\n\n" + "\n".join(name.replace("/", "\\") for name in files) + "\n"
    files[f"{addon_name}.toc"] = toc
    return files


def lua_string(value: str) -> str:
    """Lua 5.1 字符串转义；三位十进制转义避免与后继数字粘连。"""
    escaped = "".join(
        "\\\\"
        if character == "\\"
        else '\\"'
        if character == '"'
        else f"\\{ord(character):03d}"
        if ord(character) < 32 or ord(character) == 127
        else character
        for character in value
    )
    return '"' + escaped + '"'


def generate(
    rotation_path: Path, executable: Path, addon_name: str = "Phantom"
) -> GenerationResult:
    validate_addon_name(addon_name)
    executable = executable.resolve()
    if (
        executable.name.casefold() != "wow.exe"
        or executable.parent.name.casefold() != "_retail_"
        or not executable.is_file()
    ):
        raise ValueError("wow.executable 必须指向实际存在的 _retail_/Wow.exe")
    rotation = load_rotation(rotation_path)
    sources = render(rotation, addon_name)
    toc_name = f"{addon_name}.toc"
    toc = sources.pop(toc_name)
    files = {name: source.encode("utf-8") for name, source in sources.items()}
    # 共享运行时通过路径读取字体/纹理；这些二进制资源不能作为 Lua 加入 TOC。
    for asset in sorted((LUA_ROOT / "media").rglob("*")):
        if asset.is_file():
            files[asset.relative_to(LUA_ROOT).as_posix()] = asset.read_bytes()
    for required in ("media/UiFont.ttf", "media/aura/aura_border_32_4px.tga"):
        if required not in files:
            raise ValueError(f"共享运行时资源缺失：{required}")
    files[toc_name] = toc.encode("utf-8")
    directory = executable.parent / "Interface" / "AddOns" / addon_name
    directory.mkdir(parents=True, exist_ok=True)
    # 检查全部目标后再写；不跟随现有目录或文件链接覆盖到插件目录之外。
    for name in files:
        target = directory / name
        if not target.resolve().is_relative_to(directory.resolve()) or target.is_symlink():
            raise ValueError(f"生成目标超出插件目录：{target}")
        if target.exists() and not target.is_file():
            raise ValueError(f"生成目标不是文件：{target}")
    for name, content in files.items():
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(target, content)
    return GenerationResult(directory, rotation, tuple(files))
