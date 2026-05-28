# CodeBuddy 通用研发模板说明

## 定位

- 本目录是可独立复制的 CodeBuddy 项目初始化模板，不包含具体业务代码。
- 实现任何功能前，明确产品目标、目标用户、输入输出、范围边界、运行约束、风险和验收标准。
- 面向人的沟通、文档及 Agent 指令使用中文；命令和固定配置标识可保留英文。

## 七类职责

- `product-planner`：目标、范围、优先级、需求和验收标准。
- `experience-designer`：UI、UX、视觉、信息架构、可访问性与体验验收。
- `frontend-engineer`：前端实现、组件质量、状态交互与测试。
- `backend-engineer`：接口、数据、服务集成、鉴权和测试。
- `quality-engineer`：默认只读审查测试覆盖、回归风险和门禁结论。
- `operations-engineer`：环境、流水线、非生产验证、监控和回滚准备。
- `security-architect`：默认只读审查隐私、凭据、支付、外部访问和生产风险。

## 工作与安全约定

- 优先沿用项目已有技术栈、命令和目录习惯，修改前检查仓库状态。
- 开始任务时优先读取 `CODEBUDDY.md`、`.codebuddy/project-context.md`、`.codebuddy/rules.md`、`.codebuddy/memory.md` 与 `.codebuddy/errors.md`。
- 重要架构、第三方集成、安全或运维决定应形成可复核记录。
- 解决可复发问题后更新 `.codebuddy/errors.md`；确认长期偏好、规则或架构决策后更新 `.codebuddy/memory.md` 或 `.codebuddy/rules.md`。
- 禁止将真实令牌、密码、Cookie、私钥、连接串、生产资源标识或敏感用户数据写入仓库、对话或 MCP 配置。
- 外部服务验证默认限定于已有团队非生产环境中的只读操作。
- 外部写入、账号授权、支付、付费开通、发布、部署、真实数据处理或生产访问必须执行前获得用户明确批准。
- Stripe 仅可用于测试模式接入说明与验证，不进行真实交易。

## 能力配置全景

| 层级 | CodeBuddy 承载位置 | 使用规则 |
| --- | --- | --- |
| 认知与上下文层 | `.codebuddy/project-context.md`、项目 README | 先读取目标、技术栈、领域词表、约束和技术债。 |
| 角色与人格层 | `.codebuddy/agents/*.md` | 七类 Subagents 分工协作；质量与安全默认审查优先。 |
| 工程规范与约束层 | `.codebuddy/rules.md`、`.codebuddy/settings.json` | 约束命令权限、规则沉淀、工程规范和高风险审批。 |
| 自动化执行层 | `.codebuddy/skills/*`、settings hooks | 通过 Skills 执行流程，通过 hooks 拦截凭据和危险动作。 |
| 安全与合规层 | `.codebuddy/hooks/guard_secrets.py` | 凭据、隐私、支付、部署、生产访问执行前确认。 |
| 学习与自进化层 | `.codebuddy/memory.md`、`.codebuddy/errors.md` | 记录偏好、决策、错误免疫和复盘结论。 |
| 协同与沟通层 | `delivery-orchestration`、Subagents 交接 | 明确分工、同步点、交付物和人工介入条件。 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` | 规划 CI/CD、监控、成本、质量、延迟、降级和回滚。 |

补充能力 skills：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。
