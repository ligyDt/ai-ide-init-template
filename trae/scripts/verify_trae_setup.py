#!/usr/bin/env python3
"""离线验证 TRAE 通用中文研发模板资产。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
TRAE_NATIVE_SKILLS = ("trae-project-workflow",)
TRAE_RULES = (
    "general-rules.md",
    "security-and-access.md",
    "git-commit-message.md",
    "frontend/ui-experience.md",
    "backend/api-data.md",
)
TRAE_COMMANDS = (
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


def main() -> int:
    visible = [ROOT / "AGENTS.md", ROOT / "docs/TRAE-初始化指南.md"]
    for name in ALL_SKILLS:
        skill = ROOT / ".agents/skills" / name / "SKILL.md"
        content = read(skill)
        if not content.startswith("---\n") or f"name: {name}" not in content:
            fail(f"Skill 元数据不完整：{name}")
        visible.append(skill)
    for name in ("project-context.md", "memory.md", "rules.md", "errors.md"):
        visible.append(ROOT / ".agents" / name)
    context = read(ROOT / ".agents/project-context.md")
    for marker in ("技术栈", "核心架构", "领域词表", "关键约束", "已知技术债"):
        if marker not in context:
            fail(f"项目上下文模板缺少栏目：{marker}")
    for name in TRAE_NATIVE_SKILLS:
        skill = ROOT / ".trae/skills" / name / "SKILL.md"
        content = read(skill)
        if not content.startswith("---\n") or f"name: {name}" not in content:
            fail(f"TRAE 原生 Skill 元数据不完整：{name}")
        visible.append(skill)
    for name in TRAE_RULES:
        rule = ROOT / ".trae/rules" / name
        content = read(rule)
        if "---" not in content or not any(marker in content for marker in ("alwaysApply", "globs", "scene")):
            fail(f"TRAE 项目规则缺少生效属性：{name}")
        visible.append(rule)
    for name in TRAE_COMMANDS:
        command = ROOT / ".trae/commands" / name
        content = read(command)
        if not content.startswith("---\n") or "description:" not in content:
            fail(f"TRAE 项目命令元数据不完整：{name}")
        visible.append(command)
    for name in ("specs/README.md", "documents/README.md"):
        visible.append(ROOT / ".trae" / name)
    forbidden_paths = (
        ROOT / ".mcp.json",
        ROOT / ".agents/agents",
        ROOT / ".trae/agents",
        ROOT / ".trae/mcp.json",
        ROOT / ".trae/hooks.json",
        ROOT / ".trae/sandbox.json",
        ROOT / ".trae/skill-config.json",
    )
    if any(path.exists() for path in forbidden_paths):
        fail("发现尚未确认可提交的 TRAE 原生运行时配置")
    for path in visible:
        content = read(path)
        if len(re.findall(r"[\u4e00-\u9fff]", content)) < 15:
            fail(f"中文内容不足：{path.relative_to(ROOT)}")
        if any(term in content for term in ("酒" + "店", "旅" + "行", "抓" + "取")):
            fail(f"仍包含业务专属语义：{path.relative_to(ROOT)}")
    guide = read(ROOT / "docs/TRAE-初始化指南.md")
    for marker in (
        "https://developers.openai.com/mcp",
        ".trae/rules",
        ".trae/commands",
        "/spec",
        "/plan",
        "TRAE IDE 与 TRAE SOLO 边界",
        "人工",
        "不创建",
        "https://docs.trae.cn/ide/skills",
        "https://docs.trae.cn/ide/rules",
        "https://docs.trae.cn/ide/slash-commands",
        "https://docs.trae.cn/solo/spec-and-plan",
        "https://docs.trae.cn/ide/model-context-protocol",
        "https://docs.trae.cn/ide/agent",
        "../../docs/reference/official-sources.md",
        "不是 IDE Rules、Commands、MCP 或沙箱配置目录",
    ):
        if marker not in guide:
            fail(f"指南未说明 TRAE 接入边界：{marker}")
    print("TRAE 模板离线验证通过。")
    print("- 已验证：AGENTS.md、.agents 通用 Skills、.trae/rules、.trae/commands、.trae/skills 与 Spec/Plan 文档落点。")
    print("- 需人工确认：TRAE IDE 中的 MCP、自定义智能体、沙箱、.agents 技能目录开关与运行时加载状态。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
