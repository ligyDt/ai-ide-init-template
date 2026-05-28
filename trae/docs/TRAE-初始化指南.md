# TRAE 通用初始化指南

## 1. 目标与范围

本模板用于将中文多角色研发流程带入 TRAE 项目，覆盖产品、体验、工程、质量、运维和安全协作。本阶段不提供业务代码、不连接真实服务、不自动发布，也不写入任何凭据。

依据当前可核验的 TRAE 官方能力与本机安装状态，本模板提交 `AGENTS.md` 和 `.agents/skills/`。TRAE 官方资料确认了 Skills、`AGENTS.md`、自定义智能体、MCP 与自定义沙箱等能力，但本次未获取可稳定提交到仓库的全部项目配置文件格式，因此其余能力通过 IDE 内设置步骤启用，不创建推测性 `.trae/` 文件。

## 2. 目录与复制

```text
trae/
├── AGENTS.md
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

将本目录内容复制到目标项目根目录后，在 TRAE 中打开项目，确认指令和 Skills 能被识别。若工具版本要求通过设置面板导入技能，应选择本项目中的 `.agents/skills/` 内容，并保留相同安全边界。

### 能力配置全景

| 层级 | TRAE 保守承载位置 |
| --- | --- |
| 认知与上下文层 | `.agents/project-context.md`、README |
| 角色与人格层 | `AGENTS.md` 七类职责协议 |
| 工程规范与约束层 | `.agents/rules.md` |
| 自动化执行层 | `.agents/skills/*` |
| 安全与合规层 | `security-risk-review` 与安全约束 |
| 学习与自进化层 | `.agents/memory.md`、`.agents/errors.md` |
| 协同与沟通层 | `delivery-orchestration` |
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

## 5. IDE 内接入与安全检查

以下操作需要在 TRAE 当前版本提供的界面内完成，并在具体项目中人工复核：

1. 在 MCP 设置中添加公开 OpenAI 文档服务 `https://developers.openai.com/mcp`，仅用于公开文档查询。
2. 需要 GitHub、设计、浏览器、任务或文档连接时，只选择已有团队非生产资源，先进行只读验证。
3. 需要自定义智能体时，将本模板七类职责文本映射到 IDE 可用 Agent，不赋予超出任务所需的工具权限。
4. 使用自定义沙箱或权限功能限制任意外部写入、部署和生产访问。
5. TRAE 未由本模板注册仓库级 hook，因此使用前仍需人工审查提示和变更中是否含有密钥。

Stripe 仅能在测试模式下评估接入；真实付款、退款、生产发布、真实数据和自动化账号访问均需另行明确确认。

## 6. 验证

离线验证命令：

```bash
python3 scripts/verify_trae_setup.py
```

人工验收清单：

- 在 TRAE 中打开复制后的项目，确认 `AGENTS.md` 与八个 Skills 可用。
- 检查公开文档 MCP 是否仅配置了无凭据地址，并按首次授权提示审阅。
- 检查自定义智能体与沙箱设置是否由当前工具版本支持并符合非生产边界。
- 以占位符示例检查文档不会诱导写入真实秘密值。

## 7. 官方依据

- [创建并管理智能体](https://docs.trae.cn/ide/agent)
- [MCP 概览](https://docs.trae.cn/ide/model-context-protocol)
- [SOLO Agent](https://docs.trae.cn/ide/solo-coder)

本模板于 2026 年 5 月按可获得的 TRAE CN 官方入口与本机应用能力整理。获得明确的仓库级配置格式后，可在保持安全边界的前提下补充原生配置与运行时验证。
