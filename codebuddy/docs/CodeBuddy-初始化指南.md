# CodeBuddy 通用初始化指南

## 1. 模板目标

本目录提供可复制到任意项目根目录的 CodeBuddy 项目级研发模板。它以中文定义七类职责、八个流程技能、安全审批和公开文档 MCP，仅建立研发协作基础，不创建业务应用，也不连接生产、真实支付或真实用户数据。

本模板采用 CodeBuddy 官方确认的项目机制：`CODEBUDDY.md`、`.codebuddy/settings.json`、`.codebuddy/rules/`、`.codebuddy/commands/`、`.codebuddy/models.json`、`.codebuddy/plans/`、`.codebuddy/agents/`、`.codebuddy/skills/`、Hooks 与项目根级 `.mcp.json`。它不是插件包，因此没有 `.codebuddy-plugin/` 或插件根级组件目录。

## 2. 复制与目录

```text
codebuddy/
├── CODEBUDDY.md
├── .codebuddy/
│   ├── settings.json
│   ├── agents/                  # 七个 Subagents
│   ├── skills/                  # 八个流程 Skills 与八个补充能力 Skills
│   ├── rules/                   # CodeBuddy 原生项目规则
│   ├── commands/                # CodeBuddy 自定义斜杠命令
│   ├── plans/                   # Plan Mode 保存的 Markdown 计划
│   ├── models.json              # 项目级模型显示控制，默认不含真实密钥
│   ├── project-context.md       # 项目上下文、技术栈、领域词表和约束
│   ├── memory.md                # 长期偏好、决策和复盘摘要
│   ├── errors.md                # 错误免疫库
│   ├── rules.md                 # 项目专属工程规则
│   └── hooks/guard_secrets.py
├── .mcp.json                    # 项目 MCP
├── scripts/verify_codebuddy_setup.py
└── docs/CodeBuddy-初始化指南.md
```

复制本目录内容到目标项目根目录即可。个人覆盖项和本地凭据配置放在 `.codebuddy/settings.local.json` 或工具批准的安全存储中，并不得提交版本库。

### 能力配置全景

| 层级 | CodeBuddy 承载位置 |
| --- | --- |
| 认知与上下文层 | `.codebuddy/project-context.md`、`.codebuddy/plans/`、README |
| 角色与人格层 | `.codebuddy/agents/*.md` |
| 工程规范与约束层 | `.codebuddy/rules/*/RULE.mdc`、`.codebuddy/rules.md`、`.codebuddy/settings.json` |
| 自动化执行层 | `.codebuddy/commands/*`、`.codebuddy/skills/*`、settings hooks |
| 安全与合规层 | `.codebuddy/hooks/guard_secrets.py`、`.codebuddy/rules/security-and-access/RULE.mdc` |
| 学习与自进化层 | `.codebuddy/memory.md`、`.codebuddy/errors.md` |
| 协同与沟通层 | Plan Mode、`delivery-orchestration` 与 Subagents 交接协议 |
| 平台与可观测层 | `.codebuddy/models.json`、`release-readiness`、`cicd-integration`、`performance-analysis` |

## 3. 职责与流程

| Subagent | 职责 | 默认边界 |
| --- | --- | --- |
| `product-planner` | 目标、范围与验收 | 不替用户批准外部动作 |
| `experience-designer` | UI、UX、视觉与可访问性 | 写入远端设计前确认 |
| `frontend-engineer` | 前端实现与验证 | 不自行发布 |
| `backend-engineer` | 接口、数据与集成 | 不使用生产凭据 |
| `quality-engineer` | 测试和门禁 | 默认只读 |
| `operations-engineer` | 环境与发布准备 | 默认非生产 |
| `security-architect` | 安全审查 | 默认只读并可阻断 |

八个 Skills 分别为需求收敛、交付编排、体验规格、架构决策、质量门禁、发布准备、安全审查与集成接入。通常按“需求 -> 交付 -> 体验/架构 -> 实施 -> 质量/安全 -> 发布准备”的顺序使用。

补充能力 Skills 包括：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

## 4. Rules、Commands、Plan 与模型配置

`.codebuddy/rules/` 中预置原生项目规则：

| 规则 | 作用 |
| --- | --- |
| `general-workflow/RULE.mdc` | 通用协作、上下文读取、Plan/Craft 模式选择 |
| `security-and-access/RULE.mdc` | 凭据、外部系统、模型密钥、支付、发布、部署和生产访问边界 |
| `frontend-experience/RULE.mdc` | 前端、UI、UX、视觉和可访问性任务约束 |
| `backend-api-data/RULE.mdc` | 后端、API、数据模型、鉴权和外部集成任务约束 |

`.codebuddy/commands/` 中预置项目级斜杠命令：

| 命令 | 场景 |
| --- | --- |
| `/intake` | 将模糊需求整理为目标、范围、约束、风险和验收标准 |
| `/plan-delivery` | 为功能、重构或交付任务生成 Plan Mode 方案和验证清单 |
| `/review-safety` | 对当前变更做安全、质量、凭据和发布风险审查 |
| `/summarize-pr-info` | 汇总当前分支变更，生成中文 PR 描述、验证记录和风险说明 |

Plan Mode 适合复杂功能、架构设计、多文件协同、UI/UX 设计、存量项目改造和复杂任务拆解；完成后的计划自动保存为 Markdown 文件，位于 `.codebuddy/plans/`。快速 Bug 修复、单文件局部调整、代码解释和小范围优化可使用 Craft Mode。

`.codebuddy/models.json` 是项目级模型显示控制文件，优先级高于用户级配置。模板默认只提交空配置，不提交真实 `apiKey`。如需接入自定义模型，请在用户级配置或团队批准的安全存储中配置真实密钥。

## 5. 设置、MCP 与 Hooks

`.codebuddy/settings.json` 使用项目共享配置注册保守权限和安全 hooks：

- 拒绝读取本地环境秘密文件。
- 对发布、部署、镜像推送、集群及基础设施写入类 shell 操作要求人工审批。
- `SessionStart` 注入轻量项目上下文，提示读取模板文件、优先使用 Plan Mode 并遵守安全边界。
- `UserPromptSubmit` 检查用户提示中的明显凭据。
- `PreToolUse` 检查文件写入、shell 和 MCP 外部动作。

项目根级 `.mcp.json` 仅预置公开的 `openaiDeveloperDocs`：`https://developers.openai.com/mcp`。CodeBuddy 首次连接项目作用域 MCP 时可能要求用户审核并批准服务信息，这一步不得绕过。

## 6. 外部集成矩阵

| 能力 | 初始验证方式 | 限制 |
| --- | --- | --- |
| OpenAI 文档 MCP | 公开文档查询 | 模板已声明 |
| GitHub | 非生产仓库只读检查 | PR 写入、推送、release 需确认 |
| 浏览器与设计工具 | 测试页面或设计副本 | 登录及写入需确认 |
| Linear 与文档产物 | 测试项目只读优先 | 创建和编辑需确认 |
| Stripe | 测试模式 | 禁止真实付款与退款 |
| 部署/监控 | 选择供应商后接入 | 不预置生产操作 |

凭据只通过环境变量、OAuth 授权存储或 CodeBuddy 提供的安全机制保存；文档和配置示例不得包含真实值。

## 7. 初始化验证

执行离线检查：

```bash
python3 scripts/verify_codebuddy_setup.py
```

在 CodeBuddy IDE 中进行人工运行时检查：

1. 打开项目并确认 `CODEBUDDY.md`、Rules、Commands、Subagents 与 Skills 可见。
2. 使用 `/skills` 检查八个项目技能。
3. 使用 `/hooks` 审查项目 hook 的事件与命令。
4. 使用 `/rules` 或设置面板检查 `.codebuddy/rules/` 项目规则。
5. 在对话框输入 `/`，确认自定义项目命令可见。
6. 使用 Plan Mode 创建低风险计划，确认完成后计划保存到 `.codebuddy/plans/`。
7. 查看 MCP 配置并仅批准公开文档服务。
8. 以 `${API_KEY}` 测试占位符放行，以虚构令牌测试阻断。

当前模板不以本机桌面应用存在代替运行时加载验证；未实际在 IDE 内执行的步骤应标记为待人工确认。

## 8. 常见问题与升级

- 配置不加载：确认所有内容已复制到项目根目录，检查 JSON 语法并重新打开工作区。
- Hook 不工作：通过 `/hooks` 检查注册状态，并确认 `python3` 可用。
- Rules 不生效：创建或修改规则后新建对话会话；只设置 `alwaysApply: true` 的核心规则会始终加载，其他规则按需加载。
- Commands 不显示：确认命令文件位于 `.codebuddy/commands/`，并在空输入框输入 `/`。
- 模型配置不生效：确认 `.codebuddy/models.json` 是合法 JSON；真实 API Key 不应提交到仓库。
- MCP 被拒绝：复核服务地址及目标权限，只对公开服务或已批准的非生产服务授权。
- 工具升级：重新检查官方 Settings、Skills、Subagents、Hooks 与 MCP 文档，并再次执行离线和人工验收。

## 9. 官方依据

- [.codebuddy 目录结构](https://www.codebuddy.cn/docs/cli/codebuddy-dir)
- [规则](https://www.codebuddy.cn/docs/ide/Rules)
- [内置斜杠指令](https://www.codebuddy.cn/docs/ide/User-guide/Slash-Commands)
- [models.json 配置指南](https://www.codebuddy.cn/docs/ide/Features/models)
- [Plan Mode](https://www.codebuddy.cn/docs/ide/Features/Plan-Mode)
- [Subagents 使用指南](https://www.codebuddy.cn/docs/ide/Features/Subagents)
- [Skills](https://www.codebuddy.cn/docs/ide/Features/Skills)
- [Hook 功能使用文档](https://www.codebuddy.cn/docs/ide/Features/Hooks)
- [根级官方来源矩阵](../../docs/reference/official-sources.md)

本模板于 2026 年 6 月按上述公开资料更新。对于需要本机授权、用户级密钥或生产操作的内容，本模板仅保留安全边界和人工验收步骤，不预置真实访问能力。

## 10. CodeBuddy 与 WorkBuddy 边界

| 产品 | 本仓库当前状态 | 适合配置 | 不混用的内容 |
| --- | --- | --- | --- |
| CodeBuddy IDE | 已提供 `codebuddy/` 项目模板 | `.codebuddy/rules/`、`.codebuddy/commands/`、`.codebuddy/models.json`、`.codebuddy/plans/`、Subagents、Skills、Hooks、项目 MCP | 不把 WorkBuddy 的任务、工作空间、Claw 远程控制或桌面集成配置写进 `.codebuddy/` |
| WorkBuddy | 暂未提供独立模板 | 工作空间、任务管理、产物查看、权限模式、Claw 远程控制、微信/钉钉/企微集成、插件系统 | 不假设 WorkBuddy 复用 `.codebuddy/rules/`、`.codebuddy/commands/`、Subagents、Hooks 或项目 MCP |

当前 `codebuddy/` 目录只面向 CodeBuddy IDE 项目配置。WorkBuddy 是面向通用职场任务的桌面工作台，官方文档重点是工作空间、任务、产物、权限模式、远程控制、插件扩展和自动化；除非后续官方明确给出可提交到项目仓库的 WorkBuddy 配置格式，否则本仓库不新增 `workbuddy/` 模板，也不把 CodeBuddy 的项目配置复制给 WorkBuddy。

### WorkBuddy 人工使用建议

WorkBuddy 的高效使用技巧适合作为操作前检查清单，而不是项目文件：

- 清晰表达任务：说明做什么、已有材料在哪里、输出格式和限制条件是什么。
- 大任务拆小步：一次推进一个目标，每一步先确认方向，再进入下一步。
- 多轮调整：第一轮结果只是起点，不满意时直接指出问题、补充限制、调整角色视角或给出样例。
- 先本地后远程：新流程先在桌面端边看边执行；确认安全后，再考虑微信、QQ、Claw 等远程控制。
- 善用专家与样例：专业任务选择合适专家，风格或格式要求强的任务提供参考样本。
- 分任务管理上下文：不同目标开不同任务；旧会话过长或跑偏时，新建任务并重新给出关键背景。
- 先备份再改文件：处理真实文档、表格、代码或批量文件前，先复制副本或建立可回退版本。
- 自动化只处理稳定任务：定时任务适合重复性高、规则明确、无需实时人工干预的工作；涉及外发、删除、批量改写、远程控制或敏感资料时必须先人工确认。

这些建议可以放入团队使用手册或任务模板中，但不要把它们误写成 `.codebuddy/` 或 `.workbuddy/` 项目配置。

参考来源：[WorkBuddy 高效使用技巧](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Efficient-Tips)。本模板仅引用其任务表达、分步推进、反馈调整、文件备份和自动化边界建议，不把这些建议转换为仓库配置。
