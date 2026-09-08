# Primary

按现有构架逻辑，帮我写一个lua文件。

- phantom\lua\下创建一个文件夹，保存这个文件，文件夹名字你来设计。general是否合适
- 创建一个GeneralCell
- index=1 ， x=1,y = 1
- UUID = 0536bd34-e377-4274-a7ae-b80455dd359a
- 这个cell的灰度值体现的是玩家的职业
- classID = select(3, UnitClass("player"))  这个classID就是灰度值，
- r=灰度/255，g=灰度/255，b=灰度/255
- local eventFrame = CreateFrame("Frame") 创建有一个本能独立时间框架。
- PLAYER_ENTERING_WORLD/PLAYER_LOGIN 这些时间要刷新这个cell
- 构造函数在UIInitFuncs，符合缩放。
- 把下面UnitClass的说明写入合适位置的注释
UnitClass
Midnight-Petopia-Logo.pngMists-Logo-Small.pngBc icon.gifWoW Icon update.png	UnitClass
Midnight-Petopia-Logo.pngMists-Logo-Small.pngBc icon.gifWoW Icon update.png	UnitClassBase
Game Types
12.1.5 (69594)	mainline	+ 1.0.0
5.5.4 (68077)	mop classic	+ 1.13.2
2.5.6 (68184)	bcc anniversary	+ 1.13.2
1.15.9 (69109)	classic era	+ 1.13.2
Links
GitHub Octocat.png	GitHub search
Townlong-Yak Globe.png	Globe
Townlong-Yak BAD.png	Townlong Yak
Blizz.gif	Blizzard Docs
Wowprogramming.png	Wowprogramming
System: Unit
Predicates
AllowedWhenUntainted
MayReturnNothing
SecretWhenUnitIdentityRestricted
Main Menu
WoW API
Lua API
Widget API
ScriptObject API
XML schema
FrameXML
Events
CVars
Combat Log
Escape sequences
API changes
HOWTOs
Warcraft Wiki icon stamp.svg Redirect, Google
Discord logo.png WoWUIDev
Returns the class of the unit.

className, classFilename, classId = UnitClass(unit)
Arguments
unit
UnitToken : string
Returns
className
string ConditionalSecret - Localized name, e.g. "Warrior" or "Guerrier".
classFilename
string - Locale-independent name, e.g. "WARRIOR".
classId
number : ClassID
Values
ID	className (enUS)	classFile	Description
1	Warrior	WARRIOR	
2	Paladin	PALADIN	
3	Hunter	HUNTER	
4	Rogue	ROGUE	
5	Priest	PRIEST	
6	Death Knight	DEATHKNIGHT	3.0.2
7	Shaman	SHAMAN	
8	Mage	MAGE	
9	Warlock	WARLOCK	
10	Monk	MONK	5.0.4
11	Druid	DRUID	
12	Demon Hunter	DEMONHUNTER	7.0.3
13	Evoker	EVOKER	10.0.0

- 根据需要，补充必要的.spec信息

# Question

**GeneralCell 与 index 的表达**

> GeneralCell 和 index=1 希望如何表达：使用局部普通 Cell 和文件头序号、通过共享索引表暴露实例，还是新增 GeneralCell 类型？

都不是，generalcell只是在第一行的cell，还是cell。

**UnitClass 注释内容**

> 提供的 UnitClass 页面内容如何写入注释：整理签名、参数、返回值、限制标记和完整 1–13 职业表，去掉图片名、导航和站点链接噪声并标明版本核验差异，还是完整保留所贴原文？

整理技术说明。

**无 classID 时的颜色**

> UnitClass 未返回 classID 时，Cell 应显示代表暂不可用的灰度 0 并在后续指定事件重试、保留原色，还是直接计算并允许 Lua 错误？

显示黑色。

**文件头序号**

> 现有 Cell 构造函数只接收 x、y；你指定的 index=1 是否作为文件头中的通用文件顺序元数据，还是实例属性或仅表示第一列？

文件头 index: 1。

**确认实施**

> 是否按已呈现的完整计划实施玩家职业 Cell、TOC 接入、规范补充、验证与本地原子提交？

Implement the plan.
