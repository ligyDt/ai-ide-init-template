#!/usr/bin/env python3
"""阻止提示输入与工具负载中明显的凭据材料。"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


DIRECT_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
]

ASSIGNMENT_PATTERN = re.compile(
    r"""(?ix)
    \b(
        OPENAI_API_KEY|ANTHROPIC_API_KEY|STRIPE_SECRET_KEY|GITHUB_TOKEN|
        AWS_SECRET_ACCESS_KEY|API_KEY|ACCESS_TOKEN|AUTH_TOKEN|SESSION_TOKEN|
        MCP_TOKEN|SECRET_KEY|PRIVATE_KEY|CLIENT_SECRET|DATABASE_URL|PASSWORD|COOKIE
    )\b
    \s*[:=]\s*
    ["']?([^\s"']{16,})
    """
)

URI_CREDENTIAL_PATTERN = re.compile(
    r"""(?ix)
    \b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://
    [^/\s:@]+:([^@\s/]{8,})@
    """
)

PLACEHOLDER_FRAGMENTS = (
    "${",
    "$",
    "<",
    "example",
    "placeholder",
    "changeme",
    "replace",
    "your_",
    "your-",
    "redacted",
    "xxxxx",
)


def contains_likely_secret(text: str) -> bool:
    if any(pattern.search(text) for pattern in DIRECT_PATTERNS):
        return True
    for match in ASSIGNMENT_PATTERN.finditer(text):
        value = match.group(2).lower()
        if not any(fragment in value for fragment in PLACEHOLDER_FRAGMENTS):
            return True
    for match in URI_CREDENTIAL_PATTERN.finditer(text):
        value = match.group(1).lower()
        if not any(fragment in value for fragment in PLACEHOLDER_FRAGMENTS):
            return True
    return False


def string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(string_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(string_values(item))
        return values
    return []


def checked_text(payload: dict[str, Any]) -> str:
    event_name = payload.get("hook_event_name")
    if event_name == "UserPromptSubmit":
        return str(payload.get("prompt", ""))
    if event_name == "PreToolUse":
        return "\n".join(string_values(payload.get("tool_input", {})))
    return ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0

    if not contains_likely_secret(checked_text(payload)):
        return 0

    reason = (
        "检测到疑似凭据材料。请改用环境变量名称或脱敏占位符，不要写入秘密值。"
    )
    if payload.get("hook_event_name") == "PreToolUse":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    else:
        output = {"decision": "block", "reason": reason}

    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
