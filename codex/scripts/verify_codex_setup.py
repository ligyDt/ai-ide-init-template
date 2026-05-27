#!/usr/bin/env python3
"""验证通用中文 Codex 研发模板的配置、安全门禁与可发现能力。"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".codex" / "config.toml"
HOOKS = ROOT / ".codex" / "hooks.json"
GUARD = ROOT / ".codex" / "hooks" / "guard_secrets.py"
RULES = ROOT / ".codex" / "rules" / "safety.rules"
GUIDE = ROOT / "docs" / "Codex-初始化指南.md"

AGENTS = (
    "product-planner",
    "experience-designer",
    "frontend-engineer",
    "backend-engineer",
    "quality-engineer",
    "operations-engineer",
    "security-architect",
)
READ_ONLY_AGENTS = {"quality-engineer", "security-architect"}
SKILLS = (
    "product-intake",
    "delivery-orchestration",
    "experience-specification",
    "architecture-decision",
    "quality-gate",
    "release-readiness",
    "security-risk-review",
    "integration-onboarding",
)
PLUGIN_MARKERS = (
    ("GitHub", "/github/"),
    ("Browser", "/browser/"),
    ("Chrome", "/chrome/"),
    ("Figma", "/figma/"),
    ("Canva", "/canva/"),
    ("Linear", "/linear/"),
    ("Documents", "/documents/"),
    ("Presentations", "/presentations/"),
    ("Spreadsheets", "/spreadsheets/"),
    ("Stripe", "/stripe/"),
)


def fail(message: str) -> None:
    raise AssertionError(message)


def text(path: Path) -> str:
    if not path.is_file():
        fail(f"缺少必需文件：{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def contains_chinese(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value))


def run_guard(payload: dict[str, object]) -> dict[str, object] | None:
    result = subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=True,
    )
    if not result.stdout:
        return None
    return json.loads(result.stdout)


def validate_config() -> None:
    config = tomllib.loads(text(CONFIG))
    if config.get("sandbox_mode") != "workspace-write":
        fail("项目沙箱模式必须保持为 workspace-write")
    if config.get("approval_policy") != "on-request":
        fail("项目审批策略必须保持为 on-request")
    if config.get("sandbox_workspace_write", {}).get("network_access") is not False:
        fail("工作区沙箱默认不得开放网络")
    features = config.get("features", {})
    for feature in ("hooks", "multi_agent", "apps"):
        if features.get(feature) is not True:
            fail(f"必须显式启用能力：{feature}")
    agent_config = config.get("agents", {})
    if agent_config.get("max_threads") != 7 or agent_config.get("max_depth") != 1:
        fail("多代理并发或深度配置与模板约定不一致")
    app_defaults = config.get("apps", {}).get("_default", {})
    if app_defaults.get("destructive_enabled") is not False:
        fail("应用破坏性工具默认必须关闭")
    if app_defaults.get("open_world_enabled") is not False:
        fail("应用开放网络工具默认必须关闭")
    docs_mcp = config.get("mcp_servers", {}).get("openaiDeveloperDocs", {})
    if docs_mcp.get("url") != "https://developers.openai.com/mcp":
        fail("官方文档 MCP 地址缺失或被更改")
    if docs_mcp.get("enabled") is not True:
        fail("官方文档 MCP 必须保持启用")


def validate_agents() -> None:
    for name in AGENTS:
        path = ROOT / ".codex" / "agents" / f"{name}.toml"
        config = tomllib.loads(text(path))
        if config.get("name") != name:
            fail(f"代理名称不匹配：{name}")
        if not contains_chinese(str(config.get("description", ""))):
            fail(f"代理说明必须使用中文：{name}")
        if not contains_chinese(str(config.get("developer_instructions", ""))):
            fail(f"代理指令必须使用中文：{name}")
        if name in READ_ONLY_AGENTS and config.get("sandbox_mode") != "read-only":
            fail(f"审查代理必须为只读：{name}")


def validate_skills() -> None:
    for name in SKILLS:
        skill = ROOT / ".agents" / "skills" / name / "SKILL.md"
        metadata = ROOT / ".agents" / "skills" / name / "agents" / "openai.yaml"
        skill_text = text(skill)
        metadata_text = text(metadata)
        if not skill_text.startswith("---\n"):
            fail(f"skill 缺少前置元数据：{name}")
        if f"name: {name}" not in skill_text:
            fail(f"skill 名称不匹配：{name}")
        if not contains_chinese(skill_text):
            fail(f"skill 正文必须使用中文：{name}")
        if f"${name}" not in metadata_text:
            fail(f"skill 默认提示语必须显式引用自身：{name}")
        if not contains_chinese(metadata_text):
            fail(f"skill 界面元数据必须使用中文：{name}")
    if (ROOT / ".agents" / "skills" / "project-intake" / "SKILL.md").exists():
        fail("旧的专用需求 skill 尚未移除")
    onboarding = text(
        ROOT / ".agents" / "skills" / "integration-onboarding" / "agents" / "openai.yaml"
    )
    if "openaiDeveloperDocs" not in onboarding:
        fail("集成接入 skill 未声明官方文档 MCP 依赖")


def validate_chinese_and_generic_scope() -> None:
    markdown_paths = [ROOT / "AGENTS.md", GUIDE]
    markdown_paths.extend(ROOT / ".agents" / "skills" / name / "SKILL.md" for name in SKILLS)
    forbidden = ("酒" + "店", "旅" + "行", "抓" + "取")
    for path in markdown_paths:
        value = text(path)
        if len(re.findall(r"[\u4e00-\u9fff]", value)) < 20:
            fail(f"面向用户的文档中文内容不足：{path.relative_to(ROOT)}")
        for term in forbidden:
            if term in value:
                fail(f"通用模板中仍包含专用领域措辞：{path.relative_to(ROOT)}")


def validate_guard() -> None:
    text(GUARD)
    fake_secret = "abcdefghijkl" + "mnopqrstuv0123456789"
    safe_key = "API" + "_KEY=${API_KEY}"
    if run_guard({"hook_event_name": "UserPromptSubmit", "prompt": f"使用 {safe_key}"}) is not None:
        fail("安全环境变量占位符被错误拦截")
    prompt_value = "OPENAI" + "_API_KEY=" + fake_secret
    prompt_blocked = run_guard({"hook_event_name": "UserPromptSubmit", "prompt": prompt_value})
    if not prompt_blocked or prompt_blocked.get("decision") != "block":
        fail("提示输入中的疑似凭据未被拦截")
    patch_value = "+ ACCESS" + "_TOKEN=" + fake_secret
    patch_blocked = run_guard(
        {"hook_event_name": "PreToolUse", "tool_input": {"patch": patch_value}}
    )
    if (
        not patch_blocked
        or patch_blocked.get("hookSpecificOutput", {}).get("permissionDecision") != "deny"
    ):
        fail("补丁负载中的疑似凭据未被拦截")
    uri_value = "DATA" + "BASE_URL=postgresql://demo:" + fake_secret + "@db.test/app"
    write_blocked = run_guard(
        {"hook_event_name": "PreToolUse", "tool_input": {"content": uri_value}}
    )
    if not write_blocked:
        fail("文件写入负载中的疑似连接凭据未被拦截")
    placeholder_value = "DATA" + "BASE_URL=${DATABASE_URL}\nTOKEN=<REDACTED>"
    placeholder = run_guard(
        {"hook_event_name": "PreToolUse", "tool_input": {"new_string": placeholder_value}}
    )
    if placeholder is not None:
        fail("脱敏写入模板被错误拦截")


def validate_hooks_and_rules() -> None:
    hooks = json.loads(text(HOOKS))
    hook_text = json.dumps(hooks, ensure_ascii=False)
    for marker in ("UserPromptSubmit", "PreToolUse", "apply_patch", "exec_command"):
        if marker not in hook_text:
            fail(f"安全钩子未覆盖：{marker}")
    rules = text(RULES)
    required = (
        '["git", "reset", "--hard"]',
        '["git", "push"',
        '"publish"',
        '["terraform", "tofu"]',
        '["kubectl"',
        '["codex", "mcp"',
    )
    for marker in required:
        if marker not in rules:
            fail(f"安全规则未覆盖关键风险：{marker}")
    if "match =" not in rules or "not_match =" not in rules:
        fail("安全规则必须包含匹配与非匹配用例")


def report_integrations() -> None:
    cache = Path.home() / ".codex" / "plugins" / "cache"
    skill_paths = [str(path) for path in cache.rglob("SKILL.md")] if cache.exists() else []
    print("外部集成检测报告（未执行登录、远程读取或写入）：")
    print("- OpenAI 官方文档 MCP：模板已声明，配置结构已验证；在线连通性另行核验。")
    for label, marker in PLUGIN_MARKERS:
        if any(marker in path for path in skill_paths):
            print(f"- {label}：模板支持，本机插件可见；授权状态需在非生产任务中单独验证。")
        else:
            print(f"- {label}：模板支持，本机未发现插件；未接入不阻塞离线验收。")
    print("- 部署与监控：保留扩展入口，待选定供应商和非生产环境后接入。")


def main() -> int:
    validate_config()
    validate_agents()
    validate_skills()
    validate_chinese_and_generic_scope()
    validate_guard()
    validate_hooks_and_rules()
    print("AI IDE Init Template 离线验证通过。")
    report_integrations()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
