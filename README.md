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

<div style="overflow-x:auto;">
<table>
  <thead>
    <tr>
      <th style="position: sticky; left: 0; z-index: 1; background: #fff; min-width: 128px;">模板</th>
      <th style="min-width: 260px;">原生配置覆盖</th>
      <th style="min-width: 260px;">已交付能力</th>
      <th style="min-width: 280px;">运行时验收状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="position: sticky; left: 0; z-index: 1; background: #fff;"><a href="codex/"><code>codex/</code></a></td>
      <td><code>AGENTS.md</code><br><code>.codex/config.toml</code><br><code>.codex/agents/*.toml</code><br><code>.codex/hooks.json</code><br><code>.codex/rules/safety.rules</code><br><code>.agents/skills/*</code></td>
      <td>项目级 Codex 配置<br>7 个自定义代理<br>8 个流程 Skills<br>公开文档 MCP<br>密钥检测 Hooks<br>危险命令 Rules</td>
      <td>离线验证通过<br>可读取 <code>openaiDeveloperDocs</code> MCP 配置<br>外部账号授权不作为离线验收条件</td>
    </tr>
    <tr>
      <td style="position: sticky; left: 0; z-index: 1; background: #fff;"><a href="cursor/"><code>cursor/</code></a></td>
      <td><code>AGENTS.md</code><br><code>.cursor/rules/*.mdc</code><br><code>.cursor/agents/*.md</code><br><code>.cursor/skills/*/SKILL.md</code><br><code>.cursor/mcp.json</code><br><code>.cursor/hooks.json</code></td>
      <td>Cursor 项目规则<br>7 个项目 Agents<br>8 个项目 Skills<br>公开文档 MCP<br>提示、写入、Shell、MCP 安全 Hooks</td>
      <td>离线验证通过<br>Cursor CLI 可在复制后的独立项目发现 MCP<br>MCP 加载仍需用户审批</td>
    </tr>
    <tr>
      <td style="position: sticky; left: 0; z-index: 1; background: #fff;"><a href="codebuddy/"><code>codebuddy/</code></a></td>
      <td><code>CODEBUDDY.md</code><br><code>.codebuddy/settings.json</code><br><code>.codebuddy/agents/*.md</code><br><code>.codebuddy/skills/*/SKILL.md</code><br><code>.codebuddy/hooks/guard_secrets.py</code><br><code>.mcp.json</code></td>
      <td>CodeBuddy 项目说明<br>7 个 Subagents<br>8 个 Skills<br>项目 Settings 权限<br>公开文档 MCP<br>凭据与高风险动作 Hooks</td>
      <td>离线验证通过<br>本机可发现桌面应用<br>无可调用 CLI，运行时加载需在 IDE 内确认</td>
    </tr>
    <tr>
      <td style="position: sticky; left: 0; z-index: 1; background: #fff;"><a href="trae/"><code>trae/</code></a></td>
      <td><code>AGENTS.md</code><br><code>.agents/skills/*/SKILL.md</code></td>
      <td>TRAE 通用协作入口<br>七类职责说明<br>8 个 Agent Skills<br>非生产接入与人工验收指引</td>
      <td>离线验证通过<br>不提交未确认的 <code>.trae/</code> 项目配置<br>MCP、智能体与沙箱需在 IDE 内配置确认</td>
    </tr>
  </tbody>
</table>
</div>

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

### 根目录文件

| 路径 | 能力描述 |
| --- | --- |
| [`README.md`](README.md) | GitHub 项目首页，说明模板定位、能力矩阵、复制方式、安全边界和验证方法 |
| [`LICENSE`](LICENSE) | MIT 开源协议 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 贡献规则，约束新增模板、官方依据、验证要求和秘密材料处理 |
| [`SECURITY.md`](SECURITY.md) | 安全报告方式与模板安全基线 |
| [`scripts/verify_all_templates.py`](scripts/verify_all_templates.py) | 聚合验证入口，依次运行四套模板的离线检查并报告本机工具可发现状态 |

### `codex/` 模板

| 路径 | 能力描述 |
| --- | --- |
| [`codex/AGENTS.md`](codex/AGENTS.md) | Codex 项目级中文总规则，定义协作、安全和外部服务边界 |
| [`codex/.codex/config.toml`](codex/.codex/config.toml) | Codex 项目配置，设置沙箱、审批、多代理、Apps 和公开文档 MCP |
| `codex/.codex/agents/*.toml` | 7 个 Codex 自定义代理，覆盖产品、体验、前端、后端、质量、运维和安全职责 |
| [`codex/.codex/hooks.json`](codex/.codex/hooks.json) | Codex Hook 注册文件，接入提示和工具负载安全检查 |
| [`codex/.codex/hooks/guard_secrets.py`](codex/.codex/hooks/guard_secrets.py) | 凭据检测脚本，阻止明显密钥、私钥、连接串和非占位秘密值 |
| [`codex/.codex/rules/safety.rules`](codex/.codex/rules/safety.rules) | 危险命令规则，覆盖强制推送、发布、部署、基础设施和授权变更 |
| `codex/.agents/skills/*/SKILL.md` | 8 个通用流程 Skills，从需求收敛到集成接入 |
| `codex/.agents/skills/*/agents/openai.yaml` | Codex Skills 的中文界面元数据 |
| [`codex/docs/Codex-初始化指南.md`](codex/docs/Codex-初始化指南.md) | Codex 模板复制、验证、MCP、Hooks、Rules 和外部集成指南 |
| [`codex/scripts/verify_codex_setup.py`](codex/scripts/verify_codex_setup.py) | Codex 模板离线验证脚本 |

### `cursor/` 模板

| 路径 | 能力描述 |
| --- | --- |
| [`cursor/AGENTS.md`](cursor/AGENTS.md) | Cursor 项目中文总约束，定义协作职责与安全边界 |
| `cursor/.cursor/rules/*.mdc` | Cursor 原生 Rules，覆盖协作、安全和外部集成规则 |
| `cursor/.cursor/agents/*.md` | 7 个 Cursor 项目 Agents |
| `cursor/.cursor/skills/*/SKILL.md` | 8 个 Cursor 项目 Skills |
| [`cursor/.cursor/mcp.json`](cursor/.cursor/mcp.json) | Cursor 项目 MCP，仅声明公开 OpenAI 开发文档服务 |
| [`cursor/.cursor/hooks.json`](cursor/.cursor/hooks.json) | Cursor 原生 Hook 注册，覆盖提示、写入、Shell 和 MCP 事件 |
| [`cursor/.cursor/hooks/guard_secrets.py`](cursor/.cursor/hooks/guard_secrets.py) | Cursor 安全脚本，拦截明显凭据并对高风险动作要求审批 |
| [`cursor/docs/Cursor-初始化指南.md`](cursor/docs/Cursor-初始化指南.md) | Cursor 模板复制、CLI 验证、Rules、Agents、Skills、Hooks 和 MCP 指南 |
| [`cursor/scripts/verify_cursor_setup.py`](cursor/scripts/verify_cursor_setup.py) | Cursor 模板离线验证脚本，并在临时独立项目中检查 MCP 可发现性 |

### `codebuddy/` 模板

| 路径 | 能力描述 |
| --- | --- |
| [`codebuddy/CODEBUDDY.md`](codebuddy/CODEBUDDY.md) | CodeBuddy 项目自动读取的中文核心说明 |
| [`codebuddy/.codebuddy/settings.json`](codebuddy/.codebuddy/settings.json) | CodeBuddy 项目共享配置，定义保守权限和 Hooks |
| `codebuddy/.codebuddy/agents/*.md` | 7 个 CodeBuddy Subagents |
| `codebuddy/.codebuddy/skills/*/SKILL.md` | 8 个 CodeBuddy Skills，含最小工具权限声明 |
| [`codebuddy/.codebuddy/hooks/guard_secrets.py`](codebuddy/.codebuddy/hooks/guard_secrets.py) | CodeBuddy Hook 脚本，拦截提示和工具负载中的秘密值及高风险动作 |
| [`codebuddy/.mcp.json`](codebuddy/.mcp.json) | CodeBuddy 项目 MCP，仅声明公开 OpenAI 开发文档服务 |
| [`codebuddy/docs/CodeBuddy-初始化指南.md`](codebuddy/docs/CodeBuddy-初始化指南.md) | CodeBuddy Settings、Subagents、Skills、MCP、Hooks 和 IDE 人工验收指南 |
| [`codebuddy/scripts/verify_codebuddy_setup.py`](codebuddy/scripts/verify_codebuddy_setup.py) | CodeBuddy 模板离线验证脚本 |

### `trae/` 模板

| 路径 | 能力描述 |
| --- | --- |
| [`trae/AGENTS.md`](trae/AGENTS.md) | TRAE 项目中文总约束，组织七类职责与高风险审批边界 |
| `trae/.agents/skills/*/SKILL.md` | 8 个 TRAE Agent Skills，覆盖通用交付流程 |
| [`trae/docs/TRAE-初始化指南.md`](trae/docs/TRAE-初始化指南.md) | TRAE Skills、MCP、自定义智能体、沙箱和人工验收指南 |
| [`trae/scripts/verify_trae_setup.py`](trae/scripts/verify_trae_setup.py) | TRAE 保守模板离线验证脚本，确认未提交推测性 `.trae/` 配置 |

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
