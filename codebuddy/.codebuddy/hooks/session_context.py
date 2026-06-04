#!/usr/bin/env python3
"""Inject lightweight project guidance at CodeBuddy session start."""

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        pass
    message = (
        "已加载 AI IDE 初始化模板：先读取 CODEBUDDY.md、.codebuddy/project-context.md、"
        ".codebuddy/rules/、.codebuddy/rules.md、.codebuddy/memory.md 与 .codebuddy/errors.md；"
        "复杂任务优先使用 Plan Mode，外部写入、支付、部署和生产访问必须先确认。"
    )
    print(
        json.dumps(
            {
                "continue": True,
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": message,
                },
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
