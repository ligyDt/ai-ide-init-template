# TRAE 通用研发模板说明

## 模板定位

- 本目录是可独立复制的 TRAE 通用研发初始化模板，不包含业务实现。
- 当前模板仅提交已确认能够承载的 `AGENTS.md` 与 `.agents/skills/` 内容；未确认项目文件格式的原生 Agent、MCP、hook 和沙箱设置不在仓库中伪造。
- 开始实现前，先明确目标用户、问题、输入输出、范围、运行约束、风险和验收标准。
- 开始任务时优先读取 `AGENTS.md`、`.agents/project-context.md`、`.agents/rules.md`、`.agents/memory.md` 与 `.agents/errors.md`。
- 所有面向人的沟通和说明使用中文，工具固定标识与代码可保持英文。

## 能力配置全景

| 层级 | TRAE 保守承载位置 | 使用规则 |
| --- | --- | --- |
| 认知与上下文层 | `.agents/project-context.md`、项目 README | 先读取目标、技术栈、领域词表、约束和技术债。 |
| 角色与人格层 | `AGENTS.md` 七类职责协议 | 当前不伪造未确认的项目级 Agent 配置，通过职责协议和 Skills 协作。 |
| 工程规范与约束层 | `.agents/rules.md` | 记录工程规范、禁止清单、依赖与许可证边界。 |
| 自动化执行层 | `.agents/skills/*` | 用 Skills 组织需求、设计、架构、质量、安全、发布和集成接入流程。 |
| 安全与合规层 | `security-risk-review`、安全约束 | 凭据、隐私、支付、部署、生产访问必须先确认。 |
| 学习与自进化层 | `.agents/memory.md`、`.agents/errors.md` | 沉淀偏好、决策、错误免疫和复盘结论。 |
| 协同与沟通层 | `delivery-orchestration` | 明确分工、同步点、交付物和人工介入条件。 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` | 规划 CI/CD、监控、成本、质量、延迟、降级和回滚；运行时配置需在 IDE 内确认。 |

补充能力 skills：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

## 七类职责协作

- 产品规划：使用 `product-intake` 收敛目标、范围、优先级和验收标准。
- 设计体验：使用 `experience-specification` 定义 UI、UX、视觉、交互和可访问性要求。
- 前端工程：在体验规格确定后处理界面实现、状态管理、可访问性和前端测试。
- 后端工程：在接口边界确定后处理 API、数据模型、鉴权、集成和后端测试。
- 质量工程：使用 `quality-gate` 默认以只读方式审查证据、回归风险和门禁结论。
- 运维工程：使用 `release-readiness` 规划环境、非生产验证、监控和回滚。
- 安全架构：使用 `security-risk-review` 默认以只读方式审查凭据、隐私、外部系统、支付和生产风险。

复杂任务使用 `delivery-orchestration` 明确职责顺序、并行工作和交接产物；关键技术选择使用 `architecture-decision`；外部能力接入使用 `integration-onboarding`。

## 安全与外部系统

- 不向仓库、对话或任何配置写入真实令牌、密码、Cookie、私钥、真实连接串、生产标识或敏感用户数据。
- 凭据仅通过 TRAE 授权机制、环境变量或经批准的安全存储提供。
- 默认仅可在已有团队非生产环境中进行只读验证。
- 外部写入、账号授权、付费能力、支付、发布、部署、真实数据处理或生产访问，必须在执行前获得明确批准。
- Stripe 仅限测试模式验证；云部署与监控供应商待实际项目选择后再接入。
