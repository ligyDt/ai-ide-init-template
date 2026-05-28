# Cursor 通用研发模板说明

## 模板定位

- 本目录是可独立复制的 Cursor 项目初始化模板，不包含具体产品实现。
- 开始业务实现前，先明确目标用户、问题、输入输出、范围、约束、风险与验收标准。
- 面向人的沟通、说明和代理指令使用中文；代码、命令及固定配置标识可保留英文。

## 协作与质量

- 先检查仓库状态和现有约定，再在任务边界内修改文件。
- 开始任务时优先读取 `AGENTS.md`、`.cursor/project-context.md`、`.cursor/rules.md`、`.cursor/memory.md`、`.cursor/errors.md` 与 `.cursor/rules/*.mdc`。
- 产品规划、体验设计、前端、后端、质量、运维、安全七类职责按需要协作。
- 质量工程与安全架构角色默认先审查并提出通过条件，不主动实施高风险修改。
- 技术栈确定后沿用项目已有工具链；重要架构、接入和运维决策应记录依据。
- 解决可复发问题后更新 `.cursor/errors.md`；确认长期偏好、规则或架构决策后更新 `.cursor/memory.md` 或 `.cursor/rules.md`。

## 能力配置全景

| 层级 | Cursor 承载位置 | 使用规则 |
| --- | --- | --- |
| 认知与上下文层 | `.cursor/project-context.md`、项目 README | 先读取目标、技术栈、领域词表、约束和技术债，再实现。 |
| 角色与人格层 | `.cursor/agents/*.md` | 七类 Agents 按职责协作；质量与安全优先审查。 |
| 工程规范与约束层 | `.cursor/rules/*.mdc`、`.cursor/rules.md` | 约束中文沟通、工程规范、安全边界、外部接入和发布审批。 |
| 自动化执行层 | `.cursor/skills/*`、`.cursor/hooks.json` | 通过 Skills 拆解任务，通过 hooks 拦截凭据和高风险动作。 |
| 安全与合规层 | `.cursor/hooks/guard_secrets.py`、安全规则 | 凭据、隐私、支付、部署、生产访问必须先确认。 |
| 学习与自进化层 | `.cursor/memory.md`、`.cursor/errors.md` | 沉淀偏好、历史决策和错误免疫记录。 |
| 协同与沟通层 | `delivery-orchestration`、Agents 交接 | 明确分工、同步点、交付物和人工介入条件。 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` | 管理 CI/CD、质量、延迟、成本、监控、降级和回滚策略。 |

补充能力 skills：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

## 安全边界

- 禁止将访问令牌、密码、Cookie、私钥、真实连接串、生产标识或真实敏感数据写入受跟踪文件或对话输出。
- 凭据只通过环境变量或已批准的安全存储提供；模板示例只使用占位符。
- 外部服务初始验证仅限已有团队非生产环境中的只读操作。
- 账号授权、外部写入、付费能力、支付、发布、部署、真实数据处理和生产访问，必须在执行前单独获得明确批准。
- Stripe 仅允许测试模式的设计与验证，不执行真实交易。
