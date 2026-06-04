# 官方来源与模板依据

本文件记录 `AI IDE Init Template` 于 2026-06-04 核对的公开官方资料、模板适配结论和未纳入仓库配置的边界。后续新增模板能力时，应同步更新本文件、README、对应初始化指南和离线验证脚本。

## 总原则

- 只把目标工具已确认支持的项目级机制写入对应模板目录。
- 需要用户登录、授权、桌面端设置或运行时确认的能力，只在指南中写人工验收步骤，不提交虚构配置文件。
- WorkBuddy 当前只记录为人工操作清单和产品边界，不新增 `workbuddy/` 模板。
- Cursor Hooks 当前按模板安全扩展和本机验证处理，不写成已有稳定公开官网文件规范。

## Codex

| 模板能力 | 仓库位置 | 官方来源 | 适配结论 |
| --- | --- | --- | --- |
| 项目/全局自定义指令 | `codex/AGENTS.md` | [AGENTS.md 自定义指令](https://developers.openai.com/codex/guides/agents-md) | 已落地项目级 `AGENTS.md`；个人全局指令应放 `~/.codex/AGENTS.md`，不进入模板。 |
| 项目配置、沙箱、审批、MCP | `codex/.codex/config.toml` | [配置参考](https://developers.openai.com/codex/config-reference)、[MCP](https://developers.openai.com/codex/mcp) | 已落地保守项目配置和公开 OpenAI 文档 MCP。 |
| 自定义代理 | `codex/.codex/agents/*.toml` | [Subagents](https://developers.openai.com/codex/subagents) | 已落地七类研发代理，质量和安全代理保持只读。 |
| Skills | `codex/.agents/skills/*` | [Skills](https://developers.openai.com/codex/skills) | 已落地 8 个流程 Skills 和 8 个补充能力 Skills。 |
| Hooks 与 Rules | `codex/.codex/hooks.json`、`codex/.codex/rules/safety.rules` | [Hooks](https://developers.openai.com/codex/hooks)、[Rules](https://developers.openai.com/codex/rules) | 已落地凭据拦截和高风险命令规则；外部写入仍需用户确认。 |

## Cursor

| 模板能力 | 仓库位置 | 官方来源 | 适配结论 |
| --- | --- | --- | --- |
| Project Rules 与 AGENTS.md | `cursor/.cursor/rules/*.mdc`、`cursor/AGENTS.md` | [Rules](https://docs.cursor.com/context/rules) | 已落地 `.cursor/rules/*.mdc` 和项目 `AGENTS.md`。 |
| MCP | `cursor/.cursor/mcp.json` | [MCP](https://docs.cursor.com/context/model-context-protocol) | 已落地公开 OpenAI 文档 MCP；首次加载仍需用户审批。 |
| Subagents 与 Skills | `cursor/.cursor/agents/*`、`cursor/.cursor/skills/*` | [Cursor 2.4 Subagents 与 Skills 发布说明](https://www.cursor.com/changelog/2-4) | 已按项目能力落地，并通过本机 CLI/模板离线检查验证结构。 |
| Hooks | `cursor/.cursor/hooks.json`、`cursor/.cursor/hooks/guard_secrets.py` | 本机验证与模板安全扩展 | 当前不声明为稳定公开官网项目规范；使用前需在 Cursor IDE 内人工确认触发状态。 |

## CodeBuddy

| 模板能力 | 仓库位置 | 官方来源 | 适配结论 |
| --- | --- | --- | --- |
| 项目目录与共享配置 | `codebuddy/.codebuddy/`、`codebuddy/CODEBUDDY.md` | [.codebuddy 目录结构](https://www.codebuddy.cn/docs/cli/codebuddy-dir) | 已落地项目级 `.codebuddy` 能力目录。 |
| Rules | `codebuddy/.codebuddy/rules/*/RULE.mdc` | [Rules](https://www.codebuddy.cn/docs/ide/Rules) | 已落地项目规则，并保持可版本控制。 |
| Slash Commands | `codebuddy/.codebuddy/commands/*.md` | [Slash Commands](https://www.codebuddy.cn/docs/ide/User-guide/Slash-Commands) | 已落地项目级自定义命令。 |
| 模型与 Plan Mode | `codebuddy/.codebuddy/models.json`、`codebuddy/.codebuddy/plans/` | [models.json](https://www.codebuddy.cn/docs/ide/Features/models)、[Plan Mode](https://www.codebuddy.cn/docs/ide/Features/Plan-Mode) | 已落地空模型显示配置和计划落点，不提交真实 API Key。 |
| Subagents、Skills、Hooks | `codebuddy/.codebuddy/agents/*`、`codebuddy/.codebuddy/skills/*`、`codebuddy/.codebuddy/hooks/*` | [Subagents](https://www.codebuddy.cn/docs/ide/Features/Subagents)、[Skills](https://www.codebuddy.cn/docs/ide/Features/Skills)、[Hooks](https://www.codebuddy.cn/docs/ide/Features/Hooks) | 已落地七类 Subagents、16 个 Skills 和安全 Hooks；桌面端加载需人工确认。 |

## WorkBuddy

| 能力 | 仓库处理 | 官方来源 | 适配结论 |
| --- | --- | --- | --- |
| 高效使用技巧 | README 与 CodeBuddy 指南中的人工操作清单 | [高效使用技巧](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Efficient-Tips) | 不作为仓库配置，只用于任务表达、拆分、反馈、备份和自动化边界。 |
| 任务、权限、插件、自动化 | 产品边界说明 | WorkBuddy 官方文档 | 未发现可提交到项目仓库的 WorkBuddy 配置格式，因此不新增 `workbuddy/` 模板。 |

## TRAE

| 模板能力 | 仓库位置 | 官方来源 | 适配结论 |
| --- | --- | --- | --- |
| Skills | `trae/.trae/skills/*`、`trae/.agents/skills/*` | [Skills](https://docs.trae.cn/ide/skills) | 已落地 TRAE 原生工作流 Skill 和通用 Agent Skills。 |
| Rules | `trae/.trae/rules/*` | [Rules](https://docs.trae.cn/ide/rules) | 已落地项目规则，按 alwaysApply、globs、scene 控制范围。 |
| Slash Commands | `trae/.trae/commands/*.md` | [Slash Commands](https://docs.trae.cn/ide/slash-commands) | 已落地高频项目命令。 |
| Spec & Plan | `trae/.trae/specs/`、`trae/.trae/documents/` | [Spec & Plan](https://docs.trae.cn/solo/spec-and-plan) | 仅作为 SOLO 产物落点，不作为 IDE Rules、Commands、MCP 或沙箱配置目录。 |
| MCP 与 Agent | 指南人工配置步骤 | [MCP](https://docs.trae.cn/ide/model-context-protocol)、[Agent](https://docs.trae.cn/ide/agent) | 需要 IDE 内授权和运行时确认，不提交推测性仓库配置。 |
