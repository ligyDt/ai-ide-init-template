---
name: ai-ide-init-template
description: 将 AI IDE Init Template 的初始化能力安装到 Codex、Cursor、CodeBuddy 或 TRAE 项目中。用于新项目需要直接接入项目上下文、角色分工、流程 Skills、安全边界、MCP 基线、Hooks 和离线验证脚本，或只安装跨工具通用 Skills 时。
allowed-tools: Read, Grep, Glob, Bash
---

# AI IDE 初始化模板安装

把本仓库中的初始化能力安装到目标项目。支持 Codex、Cursor、CodeBuddy 和 TRAE；默认安装完整项目基线，也可以只安装 Skills 或只安装本安装型 Skill。

## 安装前确认

1. 确认目标工具：`codex`、`cursor`、`codebuddy` 或 `trae`。
2. 确认目标项目根目录，避免把模板装到模板仓库本身。
3. 读取目标目录已有的规则、Agents、Skills、Hooks、MCP 和安全配置；如存在同名文件，先向用户说明冲突。
4. 不读取、不复制、不生成真实凭据、Cookie、私钥、生产资源标识或真实连接串。

## 推荐命令

在本仓库内安装完整模板：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --target /path/to/project
```

在目标项目已经安装本 Skill 后，也可以从 Skill 自带脚本执行：

```bash
python3 .agents/skills/ai-ide-init-template/scripts/install_template.py --from-git --tool codex --target /path/to/project
python3 .cursor/skills/ai-ide-init-template/scripts/install_template.py --from-git --tool cursor --target /path/to/project
python3 .codebuddy/skills/ai-ide-init-template/scripts/install_template.py --from-git --tool codebuddy --target /path/to/project
```

只安装流程与补充 Skills：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --mode skills --target /path/to/project
```

把这个安装型 Skill 装入目标项目，便于后续在 IDE 内继续调用：

```bash
python3 scripts/install_template.py --tool <codex|cursor|codebuddy|trae> --mode installer-skill --target /path/to/project
```

未克隆本仓库时，从 GitHub 临时拉取后安装：

```bash
python3 <skill-path>/scripts/install_template.py --from-git --tool <codex|cursor|codebuddy|trae> --target /path/to/project
```

## 执行规则

- 先使用 `--dry-run` 展示将写入的路径。
- 默认不覆盖已有文件；只有用户明确同意时才添加 `--overwrite`。
- 安装完整模板后，执行目标目录中的 `scripts/verify_<tool>_setup.py`。
- 只安装 Skills 时，检查对应目录：
  - Codex：`.agents/skills/`
  - Cursor：`.cursor/skills/`
  - CodeBuddy：`.codebuddy/skills/`
  - TRAE：`.agents/skills/`，并在 TRAE 设置中启用 `.agents` 技能目录；完整模板还会安装 `.trae/rules/`、`.trae/commands/`、`.trae/skills/` 与 Spec/Plan 目录。
- 对外部账号授权、生产访问、支付、部署、远程写入和真实数据处理保持未启用状态，必须在目标项目内另行审批。

## 输出

- 目标工具与安装模式。
- 写入或跳过的路径。
- 发现的冲突和处理方式。
- 已执行的验证命令及结果。
- IDE 内仍需人工确认的加载步骤。
