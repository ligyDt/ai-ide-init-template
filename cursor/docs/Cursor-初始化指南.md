# Cursor 通用初始化指南

## 1. 目标与边界

本模板用于在任意新项目中建立中文研发协作基线，覆盖产品、体验、前端、后端、质量、运维和安全七类职责，以及需求收敛到发布准备的八个流程技能。模板不包含业务代码，也不承诺自动发布或连接生产系统。

本目录内容可单独复制到新项目根目录。复制后，项目将包含 `AGENTS.md` 与 `.cursor/`，由 Cursor 使用项目规则、子代理、skills、MCP 和安全 hooks。

## 2. 目录结构

```text
cursor/
├── AGENTS.md
├── .cursor/
│   ├── rules/                 # 项目级 MDC 规则
│   ├── agents/                # 七个项目级子代理
│   ├── skills/                # 八个流程 skills 与八个补充能力 skills
│   ├── project-context.md     # 项目上下文、技术栈、领域词表和约束
│   ├── memory.md              # 长期偏好、决策和复盘摘要
│   ├── errors.md              # 错误免疫库
│   ├── rules.md               # 项目专属工程规则
│   ├── mcp.json               # 公开文档 MCP
│   ├── hooks.json             # 安全 hook 注册
│   └── hooks/guard_secrets.py
├── scripts/verify_cursor_setup.py
└── docs/Cursor-初始化指南.md
```

`.cursorrules` 已不作为本模板入口；通用约束使用 `.cursor/rules/*.mdc` 与 `AGENTS.md`。

### 2.1 能力配置全景

| 层级 | Cursor 承载位置 |
| --- | --- |
| 认知与上下文层 | `.cursor/project-context.md`、README |
| 角色与人格层 | `.cursor/agents/*.md` |
| 工程规范与约束层 | `.cursor/rules/*.mdc`、`.cursor/rules.md` |
| 自动化执行层 | `.cursor/skills/*`、`.cursor/hooks.json` |
| 安全与合规层 | `.cursor/hooks/guard_secrets.py`、安全规则 |
| 学习与自进化层 | `.cursor/memory.md`、`.cursor/errors.md` |
| 协同与沟通层 | `delivery-orchestration` 与 Agents 交接协议 |
| 平台与可观测层 | `release-readiness`、`cicd-integration`、`performance-analysis` |

## 3. 使用方式

1. 将本目录下所有内容复制到目标项目根目录。
2. 在 Cursor 中信任该项目后，检查 Rules、Agents、Skills 和 Hooks 面板中是否可见项目配置。
3. 需求尚未清晰时使用 `product-intake`；确定交付范围后使用 `delivery-orchestration`。
4. 实现前后按需使用体验、架构、质量、安全和发布流程技能。
5. 执行本地校验：

```bash
python3 scripts/verify_cursor_setup.py
```

本机安装 Cursor Agent CLI 时，验证脚本还会对复制后的独立项目执行 MCP 只读发现检查。当前模板位于外层仓库的 `cursor/` 子目录中，Cursor CLI 可能以外层 Git 根作为项目根，因此不能直接以嵌套维护位置的发现结果代替复制使用场景。

```bash
python3 scripts/verify_cursor_setup.py
```

该检查仅应显示 `openaiDeveloperDocs` 为未加载或等待审批状态，不会授权或调用远程服务。

## 4. 角色与协作

| 角色 | 调用时机 | 主要产物 |
| --- | --- | --- |
| `product-planner` | 新想法或范围不清 | 目标、范围、验收标准 |
| `experience-designer` | 有界面或交互流程 | 用户流程与体验规格 |
| `frontend-engineer` | 前端实现与验证 | 界面代码与测试结果 |
| `backend-engineer` | API、数据或集成 | 接口、模型与服务验证 |
| `quality-engineer` | 验收和回归检查 | 缺陷、覆盖缺口与门禁结论 |
| `operations-engineer` | 环境和发布准备 | 非生产验证、监控与回滚方案 |
| `security-architect` | 外部系统或敏感操作 | 风险、控制与阻断项 |

质量与安全角色默认只读审查；需要它们实施修改时，主会话必须明确变更范围和授权边界。

## 5. Skills 组合

| Skill | 用途 |
| --- | --- |
| `product-intake` | 收敛需求基线 |
| `delivery-orchestration` | 分解跨角色交付顺序 |
| `experience-specification` | 定义交互与可访问性要求 |
| `architecture-decision` | 记录技术决策 |
| `quality-gate` | 形成验证与门禁结论 |
| `release-readiness` | 规划非生产发布准备 |
| `security-risk-review` | 检查安全高风险动作 |
| `integration-onboarding` | 管理 MCP 与连接器接入 |

推荐组合为：`product-intake` -> `delivery-orchestration` -> 体验/架构技能 -> 工程实现 -> `quality-gate` 与 `security-risk-review` -> `release-readiness`。

补充能力 skills：`prompt-template-library`、`test-generation`、`performance-analysis`、`internationalization-support`、`documentation-generation`、`dependency-vulnerability-scan`、`cicd-integration`、`monorepo-awareness`。

## 6. MCP 与外部集成

模板只预置 `openaiDeveloperDocs`，其地址为公开的 `https://developers.openai.com/mcp`，用于查阅 OpenAI 与 Codex 官方开发文档，不要求在仓库中保存凭据。

| 能力 | 使用场景 | 初始验证 | 限制 |
| --- | --- | --- | --- |
| GitHub | Issue、PR、CI | 已授权非生产仓库只读查询 | 推送、发布前确认 |
| Browser / Chrome | 页面测试 | 本地或已授权测试页面 | 不自动登录外部账号 |
| Figma / Canva | 设计交付 | 指定测试文件只读或副本 | 写入前确认 |
| Linear | 需求跟踪 | 已有测试项目只读查询 | 新建或修改前确认 |
| Documents / Presentations / Spreadsheets | 研发产物 | 本地产物优先 | 外部写入前确认 |
| Stripe | 支付设计 | 测试模式 | 禁止真实交易 |
| 部署与监控 | 运行保障 | 待选供应商 | 不默认配置生产能力 |

## 7. Hooks 与安全策略

`.cursor/hooks.json` 注册四类门禁：用户提示提交、文件编辑或写入、Shell 命令、MCP 调用。`guard_secrets.py` 会拦截明显令牌、私钥、真实数据库凭据等内容，并允许 `${API_KEY}`、`${DATABASE_URL}` 和 `<REDACTED>` 等占位符。

发布包、强制推送、正式 release、镜像推送、基础设施修改、集群修改、部署、支付或授权变化会要求用户审批。Hook 是补充保护，不替代人工审查与最小权限设置。

## 8. 排错与升级复核

- Agents 或 Skills 不显示：确认目录位于目标项目根的 `.cursor/` 下，并重启 Cursor。
- MCP 不可见：检查 `.cursor/mcp.json` 为合法 JSON，并在工具面板重新加载。
- Hook 未执行：检查 Hooks 输出面板、Python 可用性和 `.cursor/hooks/guard_secrets.py` 路径。
- Cursor 升级后：重新对照官方 Rules、MCP、Skills、Subagents 与 Hooks 文档，执行验证脚本并在 IDE 内手动触发一次占位符放行与伪造令牌阻断测试。

## 9. 官方依据

- [Cursor Rules](https://docs.cursor.com/en/context)
- [Cursor MCP](https://docs.cursor.com/context/model-context-protocol)
- [Cursor 2.4：Subagents 与 Skills](https://cursor.com/changelog/2-4)

本模板于 2026 年 5 月按本机可见 Cursor Agent 能力和上述官方资料整理；工具升级后需要复核配置格式。
