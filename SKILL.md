---
name: ai-ide-init-template
description: |
  AI IDE 项目初始化模板安装器。把 Codex、Cursor、CodeBuddy 或 TRAE 的项目级初始化能力安装到目标项目：
  项目上下文、角色分工、流程 Skills、安全边界、MCP 基线、Hooks、Rules、TRAE Commands 和离线验证脚本。
  当用户说「安装 AI IDE 初始化模板」「给项目接入 Codex/Cursor/CodeBuddy/TRAE 初始化能力」
  「只安装这些 Skills」「把这个模板装到项目里」「初始化 AI IDE 项目治理」时使用。
allowed-tools: Read, Grep, Glob, Bash
---

# AI IDE Init Template

将本仓库作为一个可直接安装的 Agent Skill 使用。它不创建业务应用，而是把 AI IDE 在进入业务前需要准备好的项目上下文、角色分工、流程 Skills、安全边界和验证脚本安装到目标项目。

## 先判断目标

收到用户请求后，先确认或推断三件事：

1. 目标工具：`codex`、`cursor`、`codebuddy` 或 `trae`。
2. 目标目录：要安装到哪个项目根目录。
3. 安装模式：
   - `full`：完整项目基线，包含规则、Agents、Skills、Hooks、MCP、TRAE Commands 和验证脚本。
   - `skills`：只安装 16 个流程与补充能力 Skills。
   - `installer-skill`：只安装项目内可继续调用的安装型 Skill。

如果目标目录已有同名规则、Agents、Skills、Hooks、MCP 或脚本，先用 dry-run 展示冲突路径，不直接覆盖。

## 执行命令

在本 Skill 目录或本仓库根目录内执行：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --target /path/to/project --dry-run
```

用户确认后再执行真实安装：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --target /path/to/project
```

只安装 Skills：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --mode skills --target /path/to/project
```

只安装项目内安装型 Skill：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --mode installer-skill --target /path/to/project
```

需要覆盖已有文件时，必须先说明将覆盖的路径，并取得明确确认后再加 `--overwrite`。

## 安全边界

- 不保存、不生成、不复制真实访问令牌、密码、Cookie、私钥、生产资源标识或真实连接串。
- 不默认启用外部账号授权、支付、部署、生产访问、远程写入或真实数据处理。
- 完整安装后，运行目标项目内的 `scripts/verify_<tool>_setup.py`。
- 安装完成后，提醒用户在对应 IDE 中确认规则、Agents、Skills、Hooks、MCP 和 TRAE Commands 是否加载。

## 输出格式

完成后输出：

- 目标工具、目标目录和安装模式。
- 写入的关键路径。
- 冲突文件和处理方式。
- 验证命令及结果。
- IDE 内仍需人工确认的步骤。
