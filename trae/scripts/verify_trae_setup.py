#!/usr/bin/env python3
"""离线验证 TRAE 通用中文研发模板的保守资产。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


def main() -> int:
    visible = [ROOT / "AGENTS.md", ROOT / "docs/TRAE-初始化指南.md"]
    for name in SKILLS:
        skill = ROOT / ".agents/skills" / name / "SKILL.md"
        content = read(skill)
        if not content.startswith("---\n") or f"name: {name}" not in content:
            fail(f"Skill 元数据不完整：{name}")
        visible.append(skill)
    forbidden_paths = (
        ROOT / ".trae",
        ROOT / ".mcp.json",
        ROOT / ".agents/agents",
    )
    if any(path.exists() for path in forbidden_paths):
        fail("发现尚未确认可提交的 TRAE 原生项目配置")
    for path in visible:
        content = read(path)
        if len(re.findall(r"[\u4e00-\u9fff]", content)) < 15:
            fail(f"中文内容不足：{path.relative_to(ROOT)}")
        if any(term in content for term in ("酒" + "店", "旅" + "行", "抓" + "取")):
            fail(f"仍包含业务专属语义：{path.relative_to(ROOT)}")
    guide = read(ROOT / "docs/TRAE-初始化指南.md")
    for marker in ("https://developers.openai.com/mcp", "人工", "未获取", "不创建"):
        if marker not in guide:
            fail(f"指南未说明保守接入边界：{marker}")
    print("TRAE 模板离线验证通过。")
    print("- 已验证：AGENTS.md 与八个可复制流程 Skills 的结构及中文安全边界。")
    print("- 需人工确认：TRAE IDE 中的 MCP、自定义智能体、沙箱与运行时加载状态。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
