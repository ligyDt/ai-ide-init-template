#!/usr/bin/env python3
"""离线验证 CodeBuddy 通用中文研发模板。"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = (
    "product-planner", "experience-designer", "frontend-engineer",
    "backend-engineer", "quality-engineer", "operations-engineer",
    "security-architect",
)
SKILLS = (
    "product-intake", "delivery-orchestration", "experience-specification",
    "architecture-decision", "quality-gate", "release-readiness",
    "security-risk-review", "integration-onboarding",
)
SUPPLEMENTAL_SKILLS = (
    "prompt-template-library", "test-generation", "performance-analysis",
    "internationalization-support", "documentation-generation",
    "dependency-vulnerability-scan", "cicd-integration", "monorepo-awareness",
)
ALL_SKILLS = SKILLS + SUPPLEMENTAL_SKILLS
CODEBUDDY_RULES = (
    "general-workflow/RULE.mdc",
    "security-and-access/RULE.mdc",
    "frontend-experience/RULE.mdc",
    "backend-api-data/RULE.mdc",
)
CODEBUDDY_COMMANDS = (
    "intake.md",
    "plan-delivery.md",
    "review-safety.md",
    "summarize-pr-info.md",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"缺少文件：{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def invoke(payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / ".codebuddy/hooks/guard_secrets.py")],
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True,
        text=True,
        check=False,
    )


def validate_structure() -> None:
    for path in (
        ROOT / "CODEBUDDY.md",
        ROOT / ".codebuddy/settings.json",
        ROOT / ".codebuddy/models.json",
        ROOT / ".codebuddy/plans/README.md",
        ROOT / ".mcp.json",
        ROOT / ".codebuddy/hooks/guard_secrets.py",
        ROOT / ".codebuddy/hooks/session_context.py",
        ROOT / ".codebuddy/project-context.md",
        ROOT / ".codebuddy/memory.md",
        ROOT / ".codebuddy/errors.md",
        ROOT / ".codebuddy/rules.md",
        ROOT / "docs/CodeBuddy-初始化指南.md",
    ):
        read(path)
    if (ROOT / ".codebuddy-plugin").exists():
        fail("项目模板不得混入 CodeBuddy 插件元数据目录")
    for name in AGENTS:
        content = read(ROOT / ".codebuddy/agents" / f"{name}.md")
        if f"name: {name}" not in content or not re.search(r"[\u4e00-\u9fff]", content):
            fail(f"Subagent 内容不完整：{name}")
    for name in ALL_SKILLS:
        content = read(ROOT / ".codebuddy/skills" / name / "SKILL.md")
        if f"name: {name}" not in content or "allowed-tools:" not in content:
            fail(f"Skill 元数据或最小权限不完整：{name}")
    for name in CODEBUDDY_RULES:
        content = read(ROOT / ".codebuddy/rules" / name)
        if not content.startswith("---\n") or "description:" not in content or "enabled: true" not in content:
            fail(f"CodeBuddy 项目规则元数据不完整：{name}")
    for name in CODEBUDDY_COMMANDS:
        content = read(ROOT / ".codebuddy/commands" / name)
        if not content.startswith("---\n") or "description:" not in content:
            fail(f"CodeBuddy 项目命令元数据不完整：{name}")
    context = read(ROOT / ".codebuddy/project-context.md")
    for marker in ("技术栈", "核心架构", "领域词表", "关键约束", "已知技术债"):
        if marker not in context:
            fail(f"项目上下文模板缺少栏目：{marker}")
    guide = read(ROOT / "docs/CodeBuddy-初始化指南.md")
    for marker in (
        "CodeBuddy 与 WorkBuddy 边界",
        "WorkBuddy",
        "不假设 WorkBuddy 复用",
        ".codebuddy/commands",
        "WorkBuddy 人工使用建议",
        "先本地后远程",
        "https://www.codebuddy.cn/docs/cli/codebuddy-dir",
        "https://www.codebuddy.cn/docs/ide/Rules",
        "https://www.codebuddy.cn/docs/ide/User-guide/Slash-Commands",
        "https://www.codebuddy.cn/docs/ide/Features/models",
        "https://www.codebuddy.cn/docs/ide/Features/Plan-Mode",
        "https://www.codebuddy.cn/docs/ide/Features/Subagents",
        "https://www.codebuddy.cn/docs/ide/Features/Skills",
        "https://www.codebuddy.cn/docs/ide/Features/Hooks",
        "https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Efficient-Tips",
        "../../docs/reference/official-sources.md",
    ):
        if marker not in guide:
            fail(f"CodeBuddy 指南缺少产品边界说明：{marker}")


def validate_config() -> None:
    settings = json.loads(read(ROOT / ".codebuddy/settings.json"))
    hooks = settings.get("hooks", {})
    for event in ("SessionStart", "UserPromptSubmit", "PreToolUse"):
        if event not in hooks:
            fail(f"缺少 CodeBuddy 安全 hook：{event}")
    denied = settings.get("permissions", {}).get("deny", [])
    if "Read(.env)" not in denied:
        fail("项目配置未限制秘密环境文件读取")
    models = json.loads(read(ROOT / ".codebuddy/models.json"))
    if set(models) != {"models", "availableModels"} or models["models"] or models["availableModels"]:
        fail("models.json 必须保持无真实密钥的空项目级配置")
    mcp = json.loads(read(ROOT / ".mcp.json"))
    docs = mcp.get("mcpServers", {}).get("openaiDeveloperDocs", {})
    if docs.get("type") != "http" or docs.get("url") != "https://developers.openai.com/mcp":
        fail("公开 OpenAI 文档 MCP 配置不正确")


def validate_guard() -> None:
    session = subprocess.run(
        [sys.executable, str(ROOT / ".codebuddy/hooks/session_context.py")],
        input=json.dumps({"hook_event_name": "SessionStart"}, ensure_ascii=False),
        capture_output=True,
        text=True,
        check=False,
    )
    session_output = json.loads(session.stdout)
    if session_output.get("hookSpecificOutput", {}).get("hookEventName") != "SessionStart":
        fail("SessionStart 上下文注入 hook 输出不正确")
    fake = "OPENAI_API_KEY=abcdefghijklmnopqrstuv0123456789"
    result = invoke({"hook_event_name": "UserPromptSubmit", "prompt": fake})
    if result.returncode != 2:
        fail("用户提示中的伪造凭据未被阻止")
    result = invoke({"hook_event_name": "PreToolUse", "tool_input": {"content": fake}})
    output = json.loads(result.stdout)
    if output.get("hookSpecificOutput", {}).get("permissionDecision") != "deny":
        fail("文件写入中的伪造凭据未被拒绝")
    result = invoke({"hook_event_name": "PreToolUse", "tool_input": {"content": "API_KEY=${API_KEY}\nTOKEN=<REDACTED>"}})
    if result.stdout or result.returncode != 0:
        fail("安全占位符被误拦截")
    result = invoke({"hook_event_name": "PreToolUse", "tool_input": {"command": "docker push registry.example/app:test"}})
    output = json.loads(result.stdout)
    if output.get("hookSpecificOutput", {}).get("permissionDecision") != "ask":
        fail("危险外部命令未要求审批")
    result = invoke({"hook_event_name": "PreToolUse", "tool_name": "mcp__deploy__release", "tool_input": {"action": "deploy"}})
    output = json.loads(result.stdout)
    if output.get("hookSpecificOutput", {}).get("permissionDecision") != "ask":
        fail("危险 MCP 操作未要求审批")


def validate_content() -> None:
    paths = [ROOT / "CODEBUDDY.md", ROOT / "docs/CodeBuddy-初始化指南.md"]
    paths.extend(ROOT / ".codebuddy" / name for name in ("project-context.md", "memory.md", "rules.md", "errors.md"))
    paths.extend(ROOT / ".codebuddy/skills" / name / "SKILL.md" for name in ALL_SKILLS)
    paths.extend(ROOT / ".codebuddy/rules" / name for name in CODEBUDDY_RULES)
    paths.extend(ROOT / ".codebuddy/commands" / name for name in CODEBUDDY_COMMANDS)
    paths.append(ROOT / ".codebuddy/plans/README.md")
    forbidden = ("酒" + "店", "旅" + "行", "抓" + "取")
    for path in paths:
        value = read(path)
        if len(re.findall(r"[\u4e00-\u9fff]", value)) < 15:
            fail(f"中文内容不足：{path.relative_to(ROOT)}")
        if any(term in value for term in forbidden):
            fail(f"仍含业务专属措辞：{path.relative_to(ROOT)}")


def main() -> int:
    validate_structure()
    validate_config()
    validate_guard()
    validate_content()
    print("CodeBuddy 模板离线验证通过。")
    print("- 已验证：CODEBUDDY.md、Subagents、Skills、Rules、Commands、models.json、Plan 目录与 Hooks。")
    if shutil.which("codebuddy"):
        print("- CodeBuddy CLI：本机可见，可继续进行项目加载检查。")
    else:
        print("- CodeBuddy CLI：本机未发现；桌面端加载状态需人工确认。")
    print("- 外部账号、在线 MCP 与 IDE 内 hook 触发：未执行，不阻塞离线验收。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
