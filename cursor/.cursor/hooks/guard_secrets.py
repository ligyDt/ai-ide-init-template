#!/usr/bin/env python3
"""拦截 Cursor 负载中的明显凭据，并对高风险外部动作要求审批。"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


DIRECT = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b"),
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
RISKY_COMMANDS = re.compile(
    r"(?ix)(git\s+push\b.*(?:--force|-f\b)|\b(?:npm|pnpm|yarn)\s+publish\b|"
    r"\bgh\s+release\s+create\b|\bdocker\s+push\b|"
    r"\b(?:terraform|tofu)\s+(?:apply|destroy)\b|"
    r"\bkubectl\s+(?:apply|delete|patch|replace|rollout)\b|"
    r"\bhelm\s+(?:install|upgrade|uninstall)\b|"
    r"\b(?:login|authorize|deploy|payment|charge|refund)\b)"
)


def flatten(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(flatten(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(flatten(item))
        return result
    return []


def likely_secret(text: str) -> bool:
    if any(pattern.search(text) for pattern in DIRECT):
        return True
    for pattern in (ASSIGNMENT, URI_CREDENTIAL):
        for match in pattern.finditer(text):
            value = match.group(match.lastindex or 1).lower()
            if not any(part in value for part in SAFE_PARTS):
                return True
    return False


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "write"
    try:
        payload = json.load(sys.stdin)
    except (TypeError, json.JSONDecodeError):
        return 0
    content = "\n".join(flatten(payload))
    if likely_secret(content):
        print("检测到疑似凭据材料。请使用环境变量或脱敏占位符，禁止写入真实秘密值。")
        return 2
    if mode in {"shell", "mcp"} and RISKY_COMMANDS.search(content):
        json.dump(
            {
                "permission": "ask",
                "user_message": "该动作可能造成外部写入、发布、部署或授权变更，请确认目标为已批准环境。",
                "agent_message": "高风险外部动作需要用户明确批准后才可继续。",
            },
            sys.stdout,
            ensure_ascii=False,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
