# CodeBuddy 通用初始化指南

## 1. 模板目标

本目录提供可复制到任意项目根目录的 CodeBuddy 项目级研发模板。它以中文定义七类职责、八个流程技能、安全审批和公开文档 MCP，仅建立研发协作基础，不创建业务应用，也不连接生产、真实支付或真实用户数据。

本模板采用 CodeBuddy 官方确认的项目机制：`CODEBUDDY.md`、`.codebuddy/settings.json`、`.codebuddy/agents/`、`.codebuddy/skills/` 与项目根级 `.mcp.json`。它不是插件包，因此没有 `.codebuddy-plugin/` 或插件根级组件目录。

## 2. 复制与目录

```text
codebuddy/
├── CODEBUDDY.md
├── .codebuddy/
│   ├── settings.json
│   ├── agents/                  # 七个 Subagents
│   ├── skills/                  # 八个 Skills
│   └── hooks/guard_secrets.py
├── .mcp.json                    # 项目 MCP
├── scripts/verify_codebuddy_setup.py
└── docs/CodeBuddy-初始化指南.md
```

复制本目录内容到目标项目根目录即可。个人覆盖项和本地凭据配置放在 `.codebuddy/settings.local.json` 或工具批准的安全存储中，并不得提交版本库。

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

## 4. 设置、MCP 与 Hooks

`.codebuddy/settings.json` 使用项目共享配置注册保守权限和安全 hooks：

- 拒绝读取本地环境秘密文件。
- 对发布、部署、镜像推送、集群及基础设施写入类 shell 操作要求人工审批。
- `UserPromptSubmit` 检查用户提示中的明显凭据。
- `PreToolUse` 检查文件写入、shell 和 MCP 外部动作。

项目根级 `.mcp.json` 仅预置公开的 `openaiDeveloperDocs`：`https://developers.openai.com/mcp`。CodeBuddy 首次连接项目作用域 MCP 时可能要求用户审核并批准服务信息，这一步不得绕过。

## 5. 外部集成矩阵

| 能力 | 初始验证方式 | 限制 |
| --- | --- | --- |
| OpenAI 文档 MCP | 公开文档查询 | 模板已声明 |
| GitHub | 非生产仓库只读检查 | PR 写入、推送、release 需确认 |
| 浏览器与设计工具 | 测试页面或设计副本 | 登录及写入需确认 |
| Linear 与文档产物 | 测试项目只读优先 | 创建和编辑需确认 |
| Stripe | 测试模式 | 禁止真实付款与退款 |
| 部署/监控 | 选择供应商后接入 | 不预置生产操作 |

凭据只通过环境变量、OAuth 授权存储或 CodeBuddy 提供的安全机制保存；文档和配置示例不得包含真实值。

## 6. 初始化验证

执行离线检查：

```bash
python3 scripts/verify_codebuddy_setup.py
```

在 CodeBuddy IDE 中进行人工运行时检查：

1. 打开项目并确认 `CODEBUDDY.md`、Subagents 与 Skills 可见。
2. 使用 `/skills` 检查八个项目技能。
3. 使用 `/hooks` 审查项目 hook 的事件与命令。
4. 查看 MCP 配置并仅批准公开文档服务。
5. 以 `${API_KEY}` 测试占位符放行，以虚构令牌测试阻断。

当前模板不以本机桌面应用存在代替运行时加载验证；未实际在 IDE 内执行的步骤应标记为待人工确认。

## 7. 常见问题与升级

- 配置不加载：确认所有内容已复制到项目根目录，检查 JSON 语法并重新打开工作区。
- Hook 不工作：通过 `/hooks` 检查注册状态，并确认 `python3` 可用。
- MCP 被拒绝：复核服务地址及目标权限，只对公开服务或已批准的非生产服务授权。
- 工具升级：重新检查官方 Settings、Skills、Subagents、Hooks 与 MCP 文档，并再次执行离线和人工验收。

## 8. 官方依据

- [Settings Configuration](https://www.codebuddy.ai/docs/cli/settings)
- [CodeBuddy Code Skills](https://www.codebuddy.ai/docs/cli/skills)
- [Subagents User Guide](https://www.codebuddy.ai/docs/ide/Features/Subagents)
- [Hooks Reference](https://www.codebuddy.ai/docs/cli/hooks)
- [MCP Usage Documentation](https://www.codebuddy.ai/docs/cli/mcp)

本模板于 2026 年 5 月按上述公开资料建立。对于参考材料中未经官方规范确认的规则目录、自动上线或生产操作描述，本模板不予预置。
