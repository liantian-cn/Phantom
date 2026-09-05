# Phantom Agent 指引

## 必读入口

任何任务先阅读 [`.spec/README.md`](.spec/README.md)，再按其中的任务路由读取最小相关规范。涉及 WoW 技术事实时，从 [`.context/README.md`](.context/README.md) 进入对应英文专题并核验指定源码。

## 权威顺序

1. 用户当前明确指令与已冻结任务计划。
2. `.spec/` 项目规范。
3. `.context/` 技术背景与核验记录。
4. `/wow-ui-source`、`/PhantomProject`、`/Shigure`、`/midnight` 外部参考源码。

规范中的“待定事项”不是事实或规则，Agent 不得自行补全并实施。

## 全局路由规则

- 只在 `develop` 分支修改 Phantom；用户负责向 `main` 冻结版本。
- `.spec/` 和本文件使用中文；`.context/` 保持英文；技术标识符保持英文。
- 外部参考源码不属于本仓库。未经用户明确要求，不得修改、提交、切换分支、fetch、pull 或 reset。
- 架构、配置、像素、插件、开发与测试的详细规则只维护在相应 `.spec` 专题，本文件不复制其正文。
