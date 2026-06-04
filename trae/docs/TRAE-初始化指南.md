# TRAE 通用初始化指南

## 1. 目标与范围

本模板用于将中文多角色研发流程带入 TRAE 项目，覆盖产品、体验、工程、质量、运维和安全协作。本阶段不提供业务代码、不连接真实服务、不自动发布，也不写入任何凭据。

依据当前可核验的 TRAE 官方能力与本机安装状态，本模板提交 `AGENTS.md`、`.agents/skills/`、`.trae/rules/`、`.trae/commands/`、`.trae/skills/`、`.trae/specs/` 与 `.trae/documents/`。TRAE 官方资料确认了 Skills、Rules、Commands、`AGENTS.md`、Spec/Plan、自定义智能体、MCP 与自定义沙箱等能力；其中项目规则、项目命令、项目技能和 Spec/Plan 文档目录已落到仓库，其余需要运行时授权或本机环境的能力仍通过 IDE 内设置启用，不创建推测性 Agent、MCP、hook 或沙箱配置文件。

## 2. 目录与复制

```text
trae/
├── AGENTS.md
├── .trae/
│   ├── rules/                       # TRAE 原生项目规则，支持全局生效、路径匹配和提交信息场景
│   ├── commands/                    # TRAE 原生项目命令，用于封装高频协作任务
│   ├── skills/
│   │   └── trae-project-workflow/    # TRAE 原生工作流编排 Skill
│   ├── specs/                       # /spec 生成 spec.md、tasks.md、checklist.md 的落点
│   └── documents/                   # /plan 生成 plan.md 的落点
├── .agents/
│   ├── project-context.md       # 项目上下文、技术栈、领域词表和约束
│   ├── memory.md                # 长期偏好、决策和复盘摘要
│   ├── errors.md                # 错误免疫库
│   ├── rules.md                 # 项目专属工程规则
│   └── skills/
│       ├── product-intake/SKILL.md
│       ├── delivery-orchestration/SKILL.md
│       └── ... 共八个流程技能与八个补充能力技能
├── scripts/verify_trae_setup.py
└── docs/TRAE-初始化指南.md
```

将本目录内容复制到目标项目根目录后，在 TRAE 中打开项目，确认 `AGENTS.md`、`.trae/rules/`、`.trae/commands/` 和 `.trae/skills/` 能被识别。若还要复用通用 Agent Skills，请在 TRAE 设置中启用 `.agents` 技能目录；若 `.trae/skills/` 与 `.agents/skills/` 出现重名，TRAE 会优先使用 `.trae/skills/`。

### 能力配置全景

| 层级 | TRAE 模板承载位置 |
| --- | --- |
| 认知与上下文层 | `.agents/project-context.md`、README、`.trae/specs/` |
| 角色与人格层 | `AGENTS.md` 七类职责协议 |
| 工程规范与约束层 | `.trae/rules/*`、`.agents/rules.md` |
| 自动化执行层 | `.trae/commands/*`、`.trae/skills/*`、`.agents/skills/*` |
| 安全与合规层 | `security-risk-review` 与安全约束 |
| 学习与自进化层 | `.agents/memory.md`、`.agents/errors.md` |
| 协同与沟通层 | `delivery-orchestration`、`.trae/specs/`、`.trae/documents/` |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` |

## 3. 角色协作

七类职责由 `AGENTS.md` 和流程技能共同组织，而不是由模板伪造尚未确认的自定义 Agent 配置文件：

| 职责 | 主要用途 | 交付边界 |
| --- | --- | --- |
| 产品规划 | 需求和验收收敛 | 不越权决定外部动作 |
| 设计体验 | UI、UX、视觉与无障碍 | 外部资产写入先确认 |
| 前端工程 | 页面和交互实现 | 不擅自发布 |
| 后端工程 | API、数据与鉴权 | 不接触生产凭据 |
| 质量工程 | 验收和回归审查 | 默认只读 |
| 运维工程 | 非生产准备与回滚 | 生产动作需批准 |
| 安全架构 | 风险和控制要求 | 默认只读并可阻断 |

## 4. Skills 使用

`product-intake` 收敛需求，`delivery-orchestration` 组织交付；界面需求使用 `experience-specification`，关键取舍使用 `architecture-decision`；交付前组合 `quality-gate`、`security-risk-review` 与 `release-readiness`；新增外部能力使用 `integration-onboarding`。

补充能力 skills：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

### TRAE 原生 Rules

`.trae/rules/` 中预置了以下项目规则：

| 文件 | 作用 |
| --- | --- |
| `general-rules.md` | 全局协作、上下文读取、中文输出和 Spec/Plan 使用规则 |
| `security-and-access.md` | 凭据、外部系统、支付、发布、部署和生产访问安全边界 |
| `git-commit-message.md` | 使用 `scene: git_message` 约束 AI 生成提交内容 |
| `frontend/ui-experience.md` | 前端、UI、UX、视觉和可访问性任务规则 |
| `backend/api-data.md` | 后端、API、数据模型、鉴权和外部集成任务规则 |

规则文件使用 Markdown 编写，并通过 `alwaysApply`、`globs` 或 `scene` 控制生效范围。规则较多时可以在 `.trae/rules/` 下继续按前端、后端、测试、运维、安全等目录分类。

### TRAE 原生 Commands

`.trae/commands/` 中预置了高频项目命令：

| 命令 | 场景 |
| --- | --- |
| `/intake` | 将模糊需求整理为目标、范围、约束、风险和验收标准 |
| `/plan-delivery` | 为功能、重构或交付任务生成阶段计划和验证清单 |
| `/review-safety` | 对当前变更做安全、质量、凭据和发布风险审查 |
| `/summarize-pr-info` | 汇总当前分支变更，生成中文 PR 描述、验证记录和风险说明 |

团队可以把常用提示词、固定输出格式和多步骤审查流程继续沉淀为项目命令。命令只封装流程，不保存凭据。

### Spec & Plan 场景

- `/spec`：适合从零搭建系统或模块、大规模重构、多人协作、高稳定性功能和长期维护项目。TRAE 会在 `.trae/specs/<任务名>/` 下生成 `spec.md`、`tasks.md` 和 `checklist.md`，首次生成后需要人工确认或修改。
- `/plan`：适合中小型功能开发和模块级重构。TRAE 会在 `.trae/documents/` 下生成 `plan.md`，确认后按计划执行。
- 若任务涉及外部写入、支付、部署、生产访问或真实数据，必须先完成安全审查，再继续 Spec 或 Plan。

### TRAE IDE 与 TRAE SOLO 边界

| 产品/模式 | 本模板承载配置 | 主要使用场景 | 不混用的内容 |
| --- | --- | --- | --- |
| TRAE IDE | `AGENTS.md`、`.trae/rules/`、`.trae/commands/`、`.trae/skills/`、`.agents/skills/`、IDE 内 MCP/自定义智能体/沙箱设置 | 日常编码、项目规则加载、项目命令、技能调用、非生产集成验证 | 不把 SOLO 生成的 `spec.md`、`tasks.md`、`checklist.md` 或 `plan.md` 当作项目规则文件 |
| TRAE SOLO | `/spec`、`/plan`、`.trae/specs/`、`.trae/documents/` 生成的工作流文档、SOLO Agent 工作流 | 系统级任务规划、中小型计划执行、任务状态和验收清单沉淀 | `.trae/specs/` 与 `.trae/documents/` 是 SOLO 产物落点，不是 IDE Commands、Rules、MCP 或沙箱配置 |

简单判断：需要“规则、命令、技能、工具权限”时看 TRAE IDE 配置；需要“先生成方案、任务列表、验收清单，再确认执行”时使用 TRAE SOLO 的 Spec/Plan。不要手工把 SOLO 文档目录当作可配置能力目录扩展。

## 5. IDE 内接入与安全检查

以下操作需要在 TRAE 当前版本提供的界面内完成，并在具体项目中人工复核：

1. 在 MCP 设置中添加公开 OpenAI 文档服务 `https://developers.openai.com/mcp`，仅用于公开文档查询。
2. 需要 GitHub、设计、浏览器、任务或文档连接时，只选择已有团队非生产资源，先进行只读验证。
3. 需要自定义智能体时，将本模板七类职责文本映射到 IDE 可用 Agent，不赋予超出任务所需的工具权限。
4. 使用自定义沙箱或权限功能限制任意外部写入、部署和生产访问。
5. 在设置中确认 `.agents` 技能目录已启用，以便 TRAE 自动发现 `.agents/skills/`。
6. TRAE 未由本模板注册仓库级 hook，因此使用前仍需人工审查提示和变更中是否含有密钥。

Stripe 仅能在测试模式下评估接入；真实付款、退款、生产发布、真实数据和自动化账号访问均需另行明确确认。

## 6. 验证

离线验证命令：

```bash
python3 scripts/verify_trae_setup.py
```

人工验收清单：

- 在 TRAE 中打开复制后的项目，确认 `AGENTS.md` 与八个 Skills 可用。
- 检查 `.trae/rules/` 中项目规则可见，且 `git-commit-message.md` 能影响 AI 生成提交内容。
- 在对话输入框输入 `/`，确认项目命令和 `/spec`、`/plan` 可见。
- 试运行一个低风险需求，确认 `/plan` 能在 `.trae/documents/` 下生成计划；系统级需求使用 `/spec` 生成文档组后先人工确认。
- 检查公开文档 MCP 是否仅配置了无凭据地址，并按首次授权提示审阅。
- 检查自定义智能体与沙箱设置是否由当前工具版本支持并符合非生产边界。
- 以占位符示例检查文档不会诱导写入真实秘密值。

## 7. 官方依据

- [创建并管理智能体](https://docs.trae.cn/ide/agent)
- [技能（Skill）](https://docs.trae.cn/ide/skills)
- [规则（Rule）](https://docs.trae.cn/ide/rules)
- [命令](https://docs.trae.cn/ide/slash-commands)
- [工作流：Spec & Plan](https://docs.trae.cn/solo/spec-and-plan)
- [MCP 概览](https://docs.trae.cn/ide/model-context-protocol)
- [SOLO Agent](https://docs.trae.cn/ide/solo-coder)
- [根级官方来源矩阵](../../docs/reference/official-sources.md)

本模板于 2026 年 6 月按可获得的 TRAE CN 官方入口与本机应用能力整理。`.trae/specs/` 与 `.trae/documents/` 仅作为 SOLO Spec/Plan 产物落点，不是 IDE Rules、Commands、MCP 或沙箱配置目录。获得明确的仓库级 Agent、MCP、hook 或沙箱配置格式后，可在保持安全边界的前提下继续补充原生配置与运行时验证。
