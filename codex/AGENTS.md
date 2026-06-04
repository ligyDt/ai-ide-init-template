# 工作区说明

## 仓库定位

- 项目名称为 `AI IDE Init Template`。
- 本仓库是可复制的 Codex 多角色研发初始化模板，不包含具体产品或应用实现。
- 本文件是项目级 `AGENTS.md`，用于定义随仓库复制的长期协作、安全和验证约束；个人跨仓库偏好应放在用户自己的 `~/.codex/AGENTS.md`，临时全局覆盖放在 `~/.codex/AGENTS.override.md`，不要提交到本仓库。
- 开始实现业务代码前，先明确产品目标、目标用户、输入与输出、范围边界、运行约束和验收标准。
- 涉及第三方平台、外部数据、支付、自动化账号访问或部署时，先确定允许的环境、权限边界、成本与合规要求。

## 协作约定

- 编辑前检查仓库状态，将变更限制在当前任务范围内。
- 开始任务时优先读取 `AGENTS.md`、`.codex/project-context.md`、`.codex/rules.md`、`.codex/memory.md` 与 `.codex/errors.md`，区分已确认事实、历史决策和待确认事项。
- 技术栈确定后，优先遵循项目已有命令、目录组织和工程约定。
- 实现后运行项目已定义的相关检查；尚未定义工具链时，不为满足形式要求而随意引入依赖。
- 对重要架构、集成、安全或运维决定形成可追溯记录。
- 解决可复发问题后，将根因、修复方式和预防措施追加到 `.codex/errors.md`；确认长期偏好或决策后，更新 `.codex/memory.md` 或 `.codex/rules.md`。
- 面向用户的沟通、说明文档和代理指令使用中文；命令、代码标识符与标准配置键可保留英文。

## 能力配置全景

本模板按 8 大层组织 Codex 的项目能力，不把未确认的业务信息写死在模板中：

| 层级 | 项目承载位置 | 使用规则 |
| --- | --- | --- |
| 认知与上下文层 | `.codex/project-context.md`、`README.md` | 先读取项目目标、技术栈、领域词表、约束和已知技术债，再进入实现。 |
| 角色与人格层 | `.codex/agents/*.toml` | 七类代理覆盖产品、体验、前端、后端、质量、运维、安全；质量与安全默认只读审查。 |
| 工程规范与约束层 | `.codex/rules.md`、`.codex/rules/safety.rules` | 记录命名、格式、测试、提交、ADR、依赖和禁止清单；高风险命令由规则拦截或审批。 |
| 自动化执行层 | `.agents/skills/*`、hooks、rules | 复杂任务先拆解，执行后验证；失败重试不超过当前任务合理边界。 |
| 安全与合规层 | `.codex/hooks/guard_secrets.py`、`security-risk-review` | 凭据、隐私、支付、外部写入、部署和生产访问必须先审查并确认。 |
| 学习与自进化层 | `.codex/memory.md`、`.codex/errors.md` | 沉淀偏好、决策、错误免疫和可复用规则，不记录敏感信息。 |
| 协同与沟通层 | `delivery-orchestration`、代理交接物 | 多代理任务先声明分工、同步点、交付物和人工介入条件。 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` | 规划成本、Token、延迟、质量、CI/CD、监控、降级和回滚，不默认连接生产平台。 |

除 8 个通用交付流程外，模板还提供 8 个补充能力 skill：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

## 安全与数据

- 不得将访问令牌、密码、Cookie、私钥、真实连接串、生产资源标识或用户敏感信息写入跟踪文件、对话输出、钩子、skill 或 MCP 配置。
- 凭据仅通过环境变量或已授权的本地安全存储提供；只有在明确选定集成后才添加已脱敏的 `.env.example`。
- 默认只允许使用已有团队非生产环境进行集成验证，优先执行只读检查。
- 执行外部写入、账号授权、服务开通、付费能力、支付交易、真实数据处理、发布、部署或生产访问前，必须取得用户明确确认。

## 角色协作

- 产品规划负责收敛目标、范围和验收标准；需求未稳定前不进入实现。
- 设计体验负责用户流程、交互、视觉和可访问性；工程实现应尊重已确认的体验规格。
- 前端与后端工程负责在确认边界内实现并验证接口契约。
- 质量工程与安全架构默认以只读审查为主，输出问题、风险和通过条件。
- 运维工程仅在环境与授权边界明确后处理发布准备、监控与回滚方案。
