# AI IDE Init Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Language: Chinese](https://img.shields.io/badge/docs-%E4%B8%AD%E6%96%87-blue.svg)](#项目简介)
[![Templates](https://img.shields.io/badge/templates-Codex%20%7C%20Cursor%20%7C%20CodeBuddy%20%7C%20TRAE-4c1.svg)](#已支持工具)

面向 AI IDE 与编程智能体的中文项目级初始化模板集合，为 [OpenAI Codex](https://developers.openai.com/codex)、[Cursor](https://www.cursor.com/)、[CodeBuddy](https://www.codebuddy.ai/) 和 [TRAE](https://www.trae.cn/) 提供可复制、可审查、可离线验证的研发协作基线。

## 项目简介

当团队使用不同 AI IDE 开发同一类项目时，常见问题不是“工具能否写代码”，而是缺少稳定的协作规则、安全边界、职责分工和验收流程。本项目将这些基线整理为四套**独立可复制**的模板：

- 统一七类研发职责：产品、设计体验、前端、后端、质量、运维、安全。
- 统一八类交付流程：从需求收敛到接入管理与发布准备。
- 使用每个工具已经确认支持的原生配置格式，而不是将某一工具配置机械移植到其他工具。
- 默认执行凭据零入库、非生产验证优先、外部高风险动作审批的安全原则。
- 提供离线校验脚本，确保模板结构、中文内容、MCP 基线与安全防护可复核。

本项目**不包含**具体业务应用、云厂商部署配置、生产凭据、真实支付流程或自动发布逻辑。

## 已支持工具

| 模板 | 原生配置覆盖 | 已交付能力 | 运行时验收状态 |
| --- | --- | --- | --- |
| [`codex/`](codex/) | `AGENTS.md`、`.codex/`、`.agents/skills/` | 配置、7 个代理、8 个 Skills、MCP、Hooks、Rules | 支持离线验证与 MCP 配置读取 |
| [`cursor/`](cursor/) | `AGENTS.md`、`.cursor/rules/`、`.cursor/agents/`、`.cursor/skills/` | 7 个 Agents、8 个 Skills、MCP、Hooks | Cursor CLI 可在复制后的独立项目发现 MCP，仍需用户审批加载 |
| [`codebuddy/`](codebuddy/) | `CODEBUDDY.md`、`.codebuddy/settings.json`、`.codebuddy/agents/`、`.codebuddy/skills/`、`.mcp.json` | 7 个 Subagents、8 个 Skills、MCP、Hooks | 离线验证通过；需在桌面端确认加载 |
| [`trae/`](trae/) | `AGENTS.md`、`.agents/skills/` | 七类职责协作规则、8 个 Skills | 离线验证通过；MCP、智能体与沙箱需在 IDE 内配置确认 |

> TRAE 模板采取保守策略：仅提交当前已确认的项目资产，不创建缺少稳定官方文件规范的 `.trae/` 配置。

## 核心能力

### 七类研发职责

| 职责标识 | 主要职责 | 安全边界 |
| --- | --- | --- |
| `product-planner` | 产品目标、用户、范围、优先级、需求澄清与验收标准 | 不替用户批准高风险动作 |
| `experience-designer` | UI、UX、视觉方向、信息架构、交互与可访问性 | 外部设计资产写入前确认 |
| `frontend-engineer` | 界面实现、组件质量、状态管理、可访问性和前端测试 | 不擅自发布生产界面 |
| `backend-engineer` | API、数据模型、集成、鉴权、错误处理与测试 | 不使用真实密钥或生产资源 |
| `quality-engineer` | 测试策略、验收矩阵、回归风险和质量门禁 | 默认只读审查 |
| `operations-engineer` | 环境、CI/CD、部署准备、监控与回滚 | 默认仅规划和验证非生产环境 |
| `security-architect` | 凭据、隐私、第三方访问、支付、发布与生产风险 | 默认只读审查并报告阻断项 |

### 八个通用流程

| Skill | 使用时机 | 交付物 |
| --- | --- | --- |
| `product-intake` | 新项目、想法模糊或新增功能前 | 需求基线与验收标准 |
| `delivery-orchestration` | 需要多职责协同交付时 | 阶段、依赖和交接物 |
| `experience-specification` | 页面、交互或视觉工作前 | 体验规格与可访问性检查点 |
| `architecture-decision` | 技术选型或接口边界发生取舍时 | 架构决策记录 |
| `quality-gate` | 交付验证或发布判断前 | 测试矩阵与门禁结论 |
| `release-readiness` | 进入环境验证或准备发布前 | 非生产验证、监控与回滚方案 |
| `security-risk-review` | 涉及敏感数据、外部服务或高风险动作前 | 风险、控制措施与阻断项 |
| `integration-onboarding` | 接入 MCP、插件或连接器时 | 接入边界和验证结果 |

## 目录结构

```text
ai-ide-init-template/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── scripts/
│   └── verify_all_templates.py
├── codex/
│   ├── AGENTS.md
│   ├── .codex/
│   ├── .agents/skills/
│   ├── docs/
│   └── scripts/
├── cursor/
│   ├── AGENTS.md
│   ├── .cursor/
│   ├── docs/
│   └── scripts/
├── codebuddy/
│   ├── CODEBUDDY.md
│   ├── .codebuddy/
│   ├── .mcp.json
│   ├── docs/
│   └── scripts/
└── trae/
    ├── AGENTS.md
    ├── .agents/skills/
    ├── docs/
    └── scripts/
```

每个工具目录均为自包含模板。将某一个目录的**内容**复制到目标项目根目录后即可使用，不依赖本仓库其他模板目录。

## 快速开始

### 1. 获取模板

```bash
git clone https://github.com/ligyDt/ai-ide-init-template.git
cd ai-ide-init-template
```

### 2. 选择工具并复制

例如，要为一个现有项目接入 Cursor 模板：

```bash
cp -R cursor/. /path/to/your-project/
cd /path/to/your-project
python3 scripts/verify_cursor_setup.py
```

其他工具对应命令：

```bash
# Codex
cp -R codex/. /path/to/your-project/
python3 /path/to/your-project/scripts/verify_codex_setup.py

# CodeBuddy
cp -R codebuddy/. /path/to/your-project/
python3 /path/to/your-project/scripts/verify_codebuddy_setup.py

# TRAE
cp -R trae/. /path/to/your-project/
python3 /path/to/your-project/scripts/verify_trae_setup.py
```

> 复制到已有项目之前，应先检查目标项目已有规则文件并合并冲突内容，避免覆盖团队约定。

### 3. 在 AI IDE 中确认加载

| 工具 | 复制后检查事项 |
| --- | --- |
| Codex | 信任项目配置后检查 Agents、Skills、Hooks 与 `openaiDeveloperDocs` MCP |
| Cursor | 检查 Rules、Agents、Skills、Hooks 面板；首次 MCP 加载前审阅审批提示 |
| CodeBuddy | 检查 `CODEBUDDY.md`、Subagents、Skills、`/hooks` 与项目 MCP |
| TRAE | 检查 `AGENTS.md` 与 Skills；按官方界面人工配置 MCP、智能体与沙箱 |

## 安全设计

### 凭据与数据

- 禁止在版本库、规则、Skills、Hooks、MCP 配置或示例文档中保存真实令牌、密码、Cookie、私钥、连接串和生产资源标识。
- 示例仅使用 `${API_KEY}`、`${DATABASE_URL}`、`<REDACTED>` 等占位符。
- 真实凭据应存入环境变量、OAuth 授权存储或目标工具提供的安全存储机制。

### 外部服务与审批

模板预置或指导添加的唯一无凭据 MCP 是公开 OpenAI 开发文档服务：

```text
https://developers.openai.com/mcp
```

对 GitHub、Browser/Chrome、Figma、Canva、Linear、Documents、Presentations、Spreadsheets、Stripe 与部署监控能力采用以下规则：

- 首次验证仅限已有团队**非生产环境**中的只读操作。
- 任何外部创建、编辑、发布、部署、账号授权、真实数据处理或生产访问均须单独确认。
- Stripe 仅限测试模式，不允许默认触发真实支付、退款或生产账户操作。
- 云部署、监控与告警能力在具体项目选定供应商后再接入。

### 自动防护

- Codex 和 Cursor 模板提供规则与 Hooks，以约束疑似凭据写入和危险外部动作。
- CodeBuddy 模板通过项目 settings 与 Hooks 阻止明显凭据写入，并对高风险操作要求审批。
- TRAE 当前不伪造未确认的仓库级 Hook 格式，指南明确要求在 IDE 中配置权限与人工复核。

## 验证

在本仓库根目录运行统一验证：

```bash
python3 scripts/verify_all_templates.py
```

验证内容包括：

- 必需目录、配置文件、代理和 Skills 是否完整。
- JSON、TOML 与 Python 脚本是否能够加载。
- 用户可见文档是否以中文为主且不残留业务专属语义。
- 凭据阻断是否覆盖提示和写入场景，并放行安全占位符。
- Cursor 是否能在复制后的独立项目中只读发现公开 MCP。
- CodeBuddy 与 TRAE 是否明确标记需要在桌面 IDE 中人工确认的运行时步骤。

本模板的“通过”仅表示初始化结构与安全基线验收完成，不代表任何第三方账号已经授权，也不代表生产发布已经获批。

## 各工具详细指南

- [Codex 初始化指南](codex/docs/Codex-初始化指南.md)
- [Cursor 初始化指南](cursor/docs/Cursor-初始化指南.md)
- [CodeBuddy 初始化指南](codebuddy/docs/CodeBuddy-初始化指南.md)
- [TRAE 初始化指南](trae/docs/TRAE-初始化指南.md)

## 设计原则

1. **原生能力优先**：每种 AI IDE 只使用其已确认支持的项目级机制。
2. **可独立复制**：任一工具目录复制后即可使用，不依赖软链接和共享运行时文件。
3. **中文协作基线**：让需求、风险、验收和交接物对团队可读可复核。
4. **默认安全保守**：外部读写、支付、发布和生产动作需要明确授权。
5. **可离线验收**：未登录外部账号时也能验证模板结构和本地安全逻辑。

## 贡献

欢迎补充新的 AI IDE 适配、修正文档或增强离线验证。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并确认新增配置有公开依据、示例不包含秘密材料、验证脚本已通过。

安全问题请遵循 [SECURITY.md](SECURITY.md)，不要在公开 Issue 中披露真实凭据或可利用漏洞细节。

## 参考资料

- [OpenAI Codex 配置参考](https://developers.openai.com/codex/config-reference)
- [OpenAI Codex 自定义代理](https://developers.openai.com/codex/subagents#custom-agents)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [Cursor Rules](https://docs.cursor.com/en/context)
- [Cursor MCP](https://docs.cursor.com/context/model-context-protocol)
- [Cursor 2.4：Subagents 与 Skills](https://cursor.com/changelog/2-4)
- [CodeBuddy Settings](https://www.codebuddy.ai/docs/cli/settings)
- [CodeBuddy Skills](https://www.codebuddy.ai/docs/cli/skills)
- [CodeBuddy Subagents](https://www.codebuddy.ai/docs/ide/Features/Subagents)
- [CodeBuddy Hooks](https://www.codebuddy.ai/docs/cli/hooks)
- [CodeBuddy MCP](https://www.codebuddy.ai/docs/cli/mcp)
- [TRAE 智能体](https://docs.trae.cn/ide/agent)
- [TRAE MCP](https://docs.trae.cn/ide/model-context-protocol)

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
