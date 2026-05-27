#!/usr/bin/env python3
"""离线验证 Cursor 通用中文研发模板。"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
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


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"缺少文件：{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_guard(mode: str, payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / ".cursor/hooks/guard_secrets.py"), mode],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )


def validate_structure() -> None:
    for path in (
        ROOT / "AGENTS.md",
        ROOT / ".cursor/mcp.json",
        ROOT / ".cursor/hooks.json",
        ROOT / ".cursor/hooks/guard_secrets.py",
        ROOT / "docs/Cursor-初始化指南.md",
    ):
        read(path)
    for rule in ("000-collaboration.mdc", "001-security.mdc", "002-integrations.mdc"):
        value = read(ROOT / ".cursor/rules" / rule)
        if "alwaysApply: true" not in value or not re.search(r"[\u4e00-\u9fff]", value):
            fail(f"规则元数据或中文内容不完整：{rule}")
    for agent in AGENTS:
        value = read(ROOT / ".cursor/agents" / f"{agent}.md")
        if f"name: {agent}" not in value or not re.search(r"[\u4e00-\u9fff]", value):
            fail(f"子代理不完整：{agent}")
    for skill in SKILLS:
        value = read(ROOT / ".cursor/skills" / skill / "SKILL.md")
        if f"name: {skill}" not in value or not value.startswith("---\n"):
            fail(f"skill 元数据不完整：{skill}")


def validate_config_and_hooks() -> None:
    mcp = json.loads(read(ROOT / ".cursor/mcp.json"))
    if mcp.get("mcpServers", {}).get("openaiDeveloperDocs", {}).get("url") != "https://developers.openai.com/mcp":
        fail("公开 OpenAI 文档 MCP 配置不正确")
    hooks = json.loads(read(ROOT / ".cursor/hooks.json"))
    events = hooks.get("hooks", {})
    for event in ("beforeSubmitPrompt", "preToolUse", "beforeShellExecution", "beforeMCPExecution"):
        if event not in events:
            fail(f"缺少 Cursor hook 事件：{event}")
    fake = "OPENAI_API_KEY=abcdefghijklmnopqrstuv0123456789"
    if run_guard("prompt", {"prompt": fake}).returncode != 2:
        fail("提示中的伪造密钥未被阻止")
    if run_guard("write", {"new_string": "+ ACCESS_TOKEN=abcdefghijklmnopqrstuv0123456789"}).returncode != 2:
        fail("编辑负载中的伪造密钥未被阻止")
    if run_guard("write", {"content": "API_KEY=${API_KEY}\nTOKEN=<REDACTED>"}).returncode != 0:
        fail("安全占位符被误拦截")
    result = run_guard("shell", {"command": "terraform apply -auto-approve"})
    if result.returncode != 0 or json.loads(result.stdout).get("permission") != "ask":
        fail("危险 shell 动作未触发审批")
    result = run_guard("mcp", {"tool": "deploy", "arguments": {"target": "production"}})
    if not result.stdout or json.loads(result.stdout).get("permission") != "ask":
        fail("高风险 MCP 动作未触发审批")


def validate_content() -> None:
    visible = [ROOT / "AGENTS.md", ROOT / "docs/Cursor-初始化指南.md"]
    visible.extend(ROOT / ".cursor/skills" / item / "SKILL.md" for item in SKILLS)
    forbidden = ("酒" + "店", "旅" + "行", "抓" + "取")
    for path in visible:
        value = read(path)
        if len(re.findall(r"[\u4e00-\u9fff]", value)) < 15:
            fail(f"中文内容不足：{path.relative_to(ROOT)}")
        if any(term in value for term in forbidden):
            fail(f"存在业务专属残留：{path.relative_to(ROOT)}")


def main() -> int:
    validate_structure()
    validate_config_and_hooks()
    validate_content()
    print("Cursor 模板离线验证通过。")
    if shutil.which("cursor-agent"):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / ".cursor"
            target.mkdir()
            shutil.copy2(ROOT / ".cursor/mcp.json", target / "mcp.json")
            result = subprocess.run(
                ["cursor-agent", "mcp", "list"],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode == 0 and "openaiDeveloperDocs" in result.stdout:
            print("- Cursor Agent CLI：复制后的独立项目可发现公开文档 MCP，仍需用户审批后加载。")
        else:
            fail("Cursor Agent CLI 未能从复制后的独立项目发现公开文档 MCP")
    else:
        print("- Cursor Agent CLI：本机未发现；请在 Cursor IDE 中人工确认配置加载。")
    print("- 外部账号与 MCP 在线授权：未执行，不阻塞离线模板验收。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
