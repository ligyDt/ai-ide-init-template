# AI IDE Init Template 中文初始化指南

## 1. 模板目标

`AI IDE Init Template` 提供一套可复制到新项目的 Codex 研发基线，用于在业务实现开始前建立统一的协作、安全和验证方式。

本模板提供：

- 项目级 Codex 沙箱、审批、MCP、应用安全默认值和多代理设置。
- 产品、设计体验、前端、后端、质量、运维和安全七类项目代理。
- 从需求收敛到发布准备的八个跨角色流程 skill。
- 凭据防泄漏钩子、危险动作规则和离线验收脚本。
- 对研发工具、测试支付与未来部署监控扩展的接入方法。

本模板不提供：

- 具体产品需求、业务实现、框架脚手架或部署供应商选择。
- 生产资源、真实数据、真实支付或外部服务写入授权。
- 任何账号密码、令牌、Cookie、密钥或真实资源标识。

## 2. 使用前提

### 2.1 环境要求

- 安装可读取项目级 `.codex/` 配置、项目级代理和 `.agents/skills/` 的 Codex 客户端。
- 将新项目标记为可信后，Codex 才会加载项目级配置、钩子和规则。
- 复制模板后，从新项目根目录启动 Codex，以便发现根目录中的代理与 skills。
- Python 3.11 或更高版本可用于运行内置离线验证脚本，其中使用标准库 `tomllib`。

本模板于 `2026-05-28` 使用 `codex-cli 0.129.0` 进行初始化验证。升级 Codex 后应重新执行第 9 节的检查。

### 2.2 复制到新项目

当前仓库将模板资产集中保存在 `codex/` 目录中。使用本模板时，将 `codex/` 内的内容作为目标项目的模板根目录；若直接在本仓库内验证或维护模板，请先进入 `codex/` 目录启动 Codex 或运行命令。

复制下列模板资产，不复制本地日志、临时文件或任何凭据：

```text
AGENTS.md
.codex/
  config.toml
  agents/
  hooks.json
  hooks/
  rules/
.agents/
  skills/
scripts/
  verify_codex_setup.py
docs/
  Codex-初始化指南.md
```

复制后执行：

```bash
python3 scripts/verify_codex_setup.py
codex mcp get openaiDeveloperDocs
```

在本仓库内维护模板时，对应命令为：

```bash
cd codex
python3 scripts/verify_codex_setup.py
codex mcp get openaiDeveloperDocs
```

若新项目选择了技术栈或外部集成，再添加对应工程文件和脱敏的环境变量示例文件。

## 3. 配置基线

### 3.1 默认安全边界

项目级 `.codex/config.toml` 使用以下原则：

- `sandbox_mode = "workspace-write"`：Codex 可在工作区内完成受控修改。
- `approval_policy = "on-request"`：超出安全边界的动作交由用户决定。
- 沙箱网络默认关闭：业务尚未选择外部目标前，不默认放开任意网络访问。
- 应用连接器默认禁用破坏性动作和开放网络动作；在明确任务中再逐项启用。
- `openaiDeveloperDocs` 为唯一预先声明的实际 MCP，用于查询官方 Codex 与 OpenAI 文档。
- 多代理并发上限为七，嵌套深度为一，避免无界拆分或重复外部动作。

### 3.2 配置文件责任

| 文件或目录 | 作用 | 是否可包含凭据 |
| --- | --- | --- |
| `AGENTS.md` | 对整个项目生效的长期协作与安全约束 | 不可 |
| `.codex/config.toml` | 项目级沙箱、能力、应用与 MCP 默认配置 | 不可 |
| `.codex/agents/*.toml` | 可派发的角色代理行为与安全边界 | 不可 |
| `.codex/hooks.json` | 生命周期钩子触发配置 | 不可 |
| `.codex/hooks/` | 本地安全检查脚本 | 不可 |
| `.codex/rules/` | 高风险命令审批或阻断策略 | 不可 |
| `.codex/project-context.md` | 项目上下文、技术栈、领域词表、约束和技术债模板 | 不可 |
| `.codex/memory.md` | 长期偏好、已确认决策、已否定方案和复盘摘要 | 不可 |
| `.codex/errors.md` | 可复发问题的根因、解决方案和预防措施 | 不可 |
| `.codex/rules.md` | 项目专属工程规则、禁止清单、依赖和许可证边界 | 不可 |
| `.agents/skills/` | 可复用的流程能力、补充能力与界面元数据 | 不可 |

### 3.3 能力配置全景

| 层级 | Codex 文件 | 说明 |
| --- | --- | --- |
| 认知与上下文层 | `.codex/project-context.md` | 记录项目基本信息、技术栈、架构、领域词表、约束和技术债。 |
| 角色与人格层 | `.codex/agents/*.toml` | 七类自定义代理覆盖产品、体验、工程、质量、运维和安全。 |
| 工程规范与约束层 | `.codex/rules.md`、`.codex/rules/safety.rules` | 记录工程规范、禁止清单、ADR、依赖和危险命令规则。 |
| 自动化执行层 | `.agents/skills/*`、hooks、rules | 通过流程 skill、hook 和命令规则组织可验证执行。 |
| 安全与合规层 | `.codex/hooks/guard_secrets.py`、`security-risk-review` | 拦截凭据和高风险动作，审查隐私、支付、部署和生产访问。 |
| 学习与自进化层 | `.codex/memory.md`、`.codex/errors.md` | 沉淀偏好、决策、错误免疫和复盘结论。 |
| 协同与沟通层 | `delivery-orchestration`、代理交接物 | 明确多代理分工、同步点、合并方式和人工介入条件。 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` | 管理 CI/CD、成本、Token、延迟、质量、监控、降级和回滚。 |

## 4. 七个角色代理

项目代理位于 `.codex/agents/`。代理继承父会话模型和已批准能力；模板不固定模型或服务等级。

| 代理 | 适用时机 | 核心交付物 | 默认限制 |
| --- | --- | --- | --- |
| `product-planner` | 想法进入项目或范围变更时 | 需求基线、验收标准、决策缺口 | 不执行外部授权或生产动作 |
| `experience-designer` | 用户流程、界面或视觉需要定义时 | 体验规格、状态说明、可访问性验收项 | 外部设计资产写入需确认 |
| `frontend-engineer` | 界面与交互实现阶段 | 前端代码、组件验证结果 | 不擅自发布或接入账号服务 |
| `backend-engineer` | API、数据或第三方服务实现阶段 | 接口、数据流、失败处理和测试 | 不访问未授权外部系统 |
| `quality-engineer` | 规划覆盖、验收或发布审查时 | 测试矩阵、缺陷、门禁结论 | `read-only` |
| `operations-engineer` | 发布准备、监控和回滚设计时 | 环境方案、运行手册、非生产验证 | 发布与资源变更需批准 |
| `security-architect` | 涉及数据、账号、支付或外部动作时 | 风险清单、控制要求、阻断结论 | `read-only` |

### 4.1 建议协作顺序

1. 由 `product-planner` 通过 `$product-intake` 明确需求基线。
2. 由 `delivery-orchestration` 决定本次实际需要的角色与交接顺序。
3. 存在界面时由 `experience-designer` 先形成体验规格。
4. 工程代理按确认的接口和体验边界实施工作。
5. 高风险集成在实施前由 `security-architect` 审查。
6. `quality-engineer` 给出验证覆盖与门禁结论。
7. 需要进入环境验证时，由 `operations-engineer` 准备发布、观测与回滚措施。

## 5. 八个流程 Skills

Skills 位于 `.agents/skills/`，可由用户显式调用，也可在匹配任务时被 Codex 选用。

| Skill | 作用 | 示例提示语 |
| --- | --- | --- |
| `$product-intake` | 将新方向收敛为需求基线 | `使用 $product-intake 整理这个功能想法。` |
| `$delivery-orchestration` | 编排角色、阶段与交接物 | `使用 $delivery-orchestration 拆解本次交付。` |
| `$experience-specification` | 建立流程、界面和可访问性规格 | `使用 $experience-specification 定义用户流程。` |
| `$architecture-decision` | 记录技术选型、接口和数据流决定 | `使用 $architecture-decision 比较两个方案。` |
| `$quality-gate` | 制定验证覆盖并给出质量门禁 | `使用 $quality-gate 评估是否具备交付条件。` |
| `$release-readiness` | 准备环境验证、观测与回滚 | `使用 $release-readiness 规划非生产发布验证。` |
| `$security-risk-review` | 审查敏感数据与高风险动作 | `使用 $security-risk-review 审查第三方接入。` |
| `$integration-onboarding` | 安全接入 MCP、插件或连接器 | `使用 $integration-onboarding 接入研发工具。` |

### 5.1 八个补充能力 Skills

| Skill | 用途 |
| --- | --- |
| `$prompt-template-library` | 沉淀标准化提示模板。 |
| `$test-generation` | 生成 TDD、单测、集成、边界和回归验证方案。 |
| `$performance-analysis` | 定位性能热点并规划可回滚优化。 |
| `$internationalization-support` | 规划多语言、时区、格式化和本地化验收。 |
| `$documentation-generation` | 生成 README、API、架构、运维和交接文档。 |
| `$dependency-vulnerability-scan` | 审查依赖漏洞、许可证和供应链风险。 |
| `$cicd-integration` | 设计 CI/CD、质量门禁、发布审批和回滚路径。 |
| `$monorepo-awareness` | 分析单仓多包边界、影响范围和最小验证集合。 |

### 5.2 组合方式

- 新产品能力：`$product-intake` -> `$delivery-orchestration` -> 需要的专业流程。
- 新外部服务：`$integration-onboarding` -> `$security-risk-review` -> `$architecture-decision`。
- 用户界面交付：`$experience-specification` -> 工程实施 -> `$quality-gate`。
- 环境交付：`$security-risk-review` -> `$release-readiness` -> 经批准后的非生产验证。

### 5.3 新增业务专属 Skill

后续项目需要专属流程时：

1. 将其创建在当前项目的 `.agents/skills/<skill-name>/` 下。
2. 使用小写连字符命名，并在 `SKILL.md` 前置元数据中清晰写明触发场景。
3. 在 `agents/openai.yaml` 中填写中文界面名称、中文简介和包含 `$skill-name` 的默认提示语。
4. 仅声明真实需要且已经确认存在的工具依赖。
5. 执行 skill 校验和本项目离线验证后再交付。

## 6. MCP、插件与连接器矩阵

模板预先连接的 MCP 只有无需账号凭据的官方文档服务。下表中的其余能力属于兼容接入范围，是否可用取决于当前 Codex 主机上已安装的插件和用户授权。

| 能力 | 用途 | 建议使用角色 | 是否需要授权 | 初始验证边界 |
| --- | --- | --- | --- | --- |
| `openaiDeveloperDocs` | Codex 与 OpenAI 官方文档核实 | 全部角色 | 否 | 可查询公开文档 |
| GitHub | 仓库、Issue、PR、CI 协作 | 工程、质量、运维 | 通常需要 | 已有非生产或测试仓库优先只读 |
| Browser | 本地页面查看与交互验证 | 前端、质量、设计体验 | 本地通常不需要 | 本地目标或明确允许页面 |
| Chrome | 使用用户现有登录态的网页检查 | 设计体验、质量 | 可能需要 | 已授权非生产页面只读优先 |
| Figma | 设计稿、组件与视觉交付 | 设计体验、前端 | 通常需要 | 非生产文件，写入前确认 |
| Canva | 品牌与视觉内容产物 | 设计体验、产品 | 通常需要 | 非生产设计，写入前确认 |
| Linear | 需求和任务管理 | 产品、质量 | 通常需要 | 只读核对或批准后的测试项目 |
| Documents | 文档产物 | 产品、运维、安全 | 视目标而定 | 本地生成或批准后的测试文档 |
| Presentations | 汇报与评审材料 | 产品、设计体验 | 视目标而定 | 本地生成或批准后的测试文件 |
| Spreadsheets | 结构化分析与验收记录 | 产品、质量 | 视目标而定 | 本地生成或批准后的测试表格 |
| Stripe | 支付设计与测试集成指导 | 后端、安全、质量 | 通常需要 | 仅测试模式，不进行真实交易 |
| 部署与监控供应商 | 发布、日志、指标和告警 | 运维、安全 | 待选择 | 选择供应商及非生产环境后再接入 |

### 6.1 接入流程

1. 使用 `$integration-onboarding` 明确能力、账号归属、目标环境、读写范围与验证标准。
2. 只配置官方或已审查的 MCP、插件或连接器。
3. 凭据留在平台授权存储或环境变量中，例如 `API_KEY=${API_KEY}`；不粘贴实际值到仓库或对话。
4. 首次验证优先采用既有团队非生产环境中的只读查询。
5. 远程创建、修改、推送、发布、部署、支付、服务开通或权限变更必须单独确认。
6. 使用 `scripts/verify_codex_setup.py` 记录“模板支持”“本机能力可见”“授权需验证”三类状态，而不是假设已成功登录。

## 7. 安全、钩子与规则

### 7.1 凭据管理

- 不跟踪 `.env`、密钥文件、会话材料或任何真实连接信息。
- 只有确定了具体集成后，才允许添加只含占位符的 `.env.example`。
- 对敏感数据使用最小权限、最小保留时间与可撤销授权。
- 真实数据、生产资源和支付始终视为高风险边界。

### 7.2 钩子行为

`.codex/hooks/guard_secrets.py` 在下列入口检查明显凭据：

- `UserPromptSubmit`：阻止在发送给 Codex 的提示中暴露疑似秘密。
- `PreToolUse`：检查补丁、写文件内容和命令负载，阻止将疑似秘密写入工作区。

允许的安全示例：

```dotenv
API_KEY=${API_KEY}
DATABASE_URL=${DATABASE_URL}
TOKEN=<REDACTED>
```

### 7.3 命令规则

`.codex/rules/safety.rules` 负责两类控制：

- 直接阻止：不可逆本地清理、Git 历史破坏和强制远程推送。
- 执行前审批：包发布、发行版本创建、镜像推送、基础设施变更、集群或 Helm 写入、MCP 授权变更和代码托管登录变更。

规则不能替代第三方工具自身的权限控制。对连接器中的远程写入，仍需遵守 `AGENTS.md` 与相关 skill 中的明确批准要求。

## 8. 运维与外部环境扩展

本模板不选择云平台或可观测性供应商。项目确定供应商后，按以下顺序扩展：

1. 使用 `$architecture-decision` 记录供应商、环境模型、数据流、可用性目标和成本边界。
2. 使用 `$security-risk-review` 审查账号、权限、日志数据、生产边界和撤销路径。
3. 使用 `$integration-onboarding` 配置经过批准的非生产连接。
4. 使用 `$release-readiness` 定义流水线、部署验证、告警与回滚。
5. 将新增 MCP、代理或 skill 配置纳入本地验证脚本，并更新本指南矩阵。

在供应商和权限未明确前，不向模板添加虚构的 MCP 地址、部署命令或凭据变量。

## 9. 验证与排查

### 9.1 离线验收

```bash
python3 scripts/verify_codex_setup.py
python3 -m py_compile .codex/hooks/guard_secrets.py scripts/verify_codex_setup.py
```

离线脚本检查：

- TOML 与 JSON 配置是否可读取。
- 七个代理是否完整，质量和安全代理是否保持只读。
- 八个 skills 是否具有中文正文、中文界面元数据和正确默认提示语。
- 官方文档 MCP 是否已在模板配置中声明。
- 钩子是否覆盖输入、补丁与写入内容，并正确区分疑似秘密和占位符。
- 规则是否覆盖破坏性、发布、基础设施和授权类风险。
- 文档与流程是否保持通用中文模板定位。
- 本机可见的插件能力，不执行登录或远程写入。

### 9.2 Skill 校验

使用 Codex 自带的 skill 校验脚本逐项验证新增能力：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/product-intake
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/integration-onboarding
```

对其余六个 skill 使用相同命令执行校验。

### 9.3 MCP 与功能核对

```bash
codex features list
codex mcp get openaiDeveloperDocs
```

若官方文档 MCP 不可读取，先检查项目是否受信任、配置是否已加载，再按官方文档重新配置。账号型插件未授权不会阻塞模板离线验收。

### 9.4 常见问题

| 现象 | 处理方式 |
| --- | --- |
| 项目级配置未加载 | 确认项目已标记为可信，并从项目根目录重新启动 Codex |
| skill 未显示 | 检查目录为 `.agents/skills/<name>/SKILL.md` 并运行 skill 校验 |
| 安全钩子拦截测试文本 | 使用环境变量或脱敏占位符；测试疑似秘密时在运行时生成输入 |
| 外部插件未显示 | 在本机安装或启用相应插件后重新检查；模板本身仍可验收 |
| 需要发布或部署 | 先完成安全与发布准备审查，再获取逐项批准 |

## 10. 强制确认事项

遇到以下任何情形，代理必须停下并取得用户明确确认：

- 接入、注册、登录、授权或移除外部服务。
- 向远程服务写入、推送代码、发布制品或创建发行版本。
- 执行部署、基础设施、集群、监控配置或回滚动作。
- 处理真实用户数据、敏感业务数据或生产资源。
- 使用支付能力、执行交易、启用计费功能或开通付费 API。
- 自动化访问账号，或扩大现有账号权限范围。

## 11. 官方参考

- [Codex 配置参考](https://developers.openai.com/codex/config-reference)
- [Codex 自定义代理](https://developers.openai.com/codex/subagents#custom-agents)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Codex Hooks](https://developers.openai.com/codex/hooks#config-shape)
- [Codex Rules](https://developers.openai.com/codex/rules)

本指南是项目模板的一部分。新增代理、skill、外部能力或安全策略时，应同步更新指南和离线验收脚本。
