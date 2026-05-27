#!/usr/bin/env python3
"""CodeBuddy 项目 hook：拦截明显凭据并审批高风险外部操作。"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


DIRECT = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
)
ASSIGNMENT = re.compile(
    r"(?ix)\b(API_KEY|ACCESS_TOKEN|AUTH_TOKEN|SESSION_TOKEN|SECRET_KEY|"
    r"CLIENT_SECRET|DATABASE_URL|PASSWORD|COOKIE|OPENAI_API_KEY|"
    r"ANTHROPIC_API_KEY|STRIPE_SECRET_KEY|GITHUB_TOKEN)\b\s*[:=]\s*"
    r"[\"']?([^\s\"']{16,})"
)
URI_CREDENTIAL = re.compile(
    r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://"
    r"[^/\s:@]+:([^@\s/]{8,})@"
)
SAFE_PARTS = ("${", "<", "example", "placeholder", "changeme", "redacted", "your_", "xxxxx")
RISKY = re.compile(
    r"(?ix)(git\s+push\b.*(?:--force|-f\b)|\b(?:npm|pnpm|yarn)\s+publish\b|"
    r"\bgh\s+release\s+create\b|\bdocker\s+push\b|"
    r"\b(?:terraform|tofu)\s+(?:apply|destroy)\b|"
    r"\bkubectl\s+(?:apply|delete|patch|replace|rollout)\b|"
    r"\bhelm\s+(?:install|upgrade|uninstall)\b|"
    r"\b(?:authorize|login|deploy|payment|charge|refund)\b)"
)


def values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(values(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(values(item))
        return result
    return []


def secret(text: str) -> bool:
    if any(pattern.search(text) for pattern in DIRECT):
        return True
    for pattern in (ASSIGNMENT, URI_CREDENTIAL):
        for match in pattern.finditer(text):
            value = match.group(match.lastindex or 1).lower()
            if not any(marker in value for marker in SAFE_PARTS):
                return True
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0
    content = "\n".join(values(payload))
    event = payload.get("hook_event_name", "")
    if secret(content):
        reason = "检测到疑似凭据材料。请使用环境变量或脱敏占位符，不要提交真实秘密值。"
        if event == "PreToolUse":
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                },
                sys.stdout,
                ensure_ascii=False,
            )
            return 0
        print(reason)
        return 2
    if event == "PreToolUse" and RISKY.search(content):
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": "该操作可能写入外部系统、发布、部署或改变授权，请明确批准目标环境。",
                }
            },
            sys.stdout,
            ensure_ascii=False,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
