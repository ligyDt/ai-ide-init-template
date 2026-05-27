#!/usr/bin/env python3
"""运行四套 AI IDE 模板的离线验证并报告可验证边界。"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("Codex", ROOT / "codex/scripts/verify_codex_setup.py"),
    ("Cursor", ROOT / "cursor/scripts/verify_cursor_setup.py"),
    ("CodeBuddy", ROOT / "codebuddy/scripts/verify_codebuddy_setup.py"),
    ("TRAE", ROOT / "trae/scripts/verify_trae_setup.py"),
)


def run(name: str, script: Path) -> bool:
    if not script.is_file():
        print(f"[失败] {name}：缺少验证脚本 {script.relative_to(ROOT)}")
        return False
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=script.parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    label = "通过" if result.returncode == 0 else "失败"
    print(f"[{label}] {name}：模板结构{'已完成' if result.returncode == 0 else '未通过'}")
    if result.stdout:
        for line in result.stdout.rstrip().splitlines():
            print(f"  {line}")
    if result.stderr:
        for line in result.stderr.rstrip().splitlines():
            print(f"  {line}")
    return result.returncode == 0


def report_detection() -> None:
    print("\n本机工具发现状态：")
    for label, commands, apps in (
        ("Codex", ("codex",), ()),
        ("Cursor", ("cursor-agent", "cursor"), ("/Applications/Cursor.app",)),
        ("CodeBuddy", ("codebuddy",), ("/Applications/CodeBuddy CN.app", "/Applications/CodeBuddy.app")),
        ("TRAE", ("trae",), ("/Applications/Trae CN.app", "/Applications/TRAE SOLO CN.app", "/Applications/Trae.app")),
    ):
        found = next((command for command in commands if shutil.which(command)), None)
        if found:
            print(f"- {label}：命令行工具可发现（{found}）。")
        elif any(Path(app).exists() for app in apps):
            print(f"- {label}：桌面应用可发现，但无可调用 CLI；项目加载需在 IDE 中人工确认。")
        else:
            print(f"- {label}：未发现本机工具；运行时加载需在安装后人工确认。")
    print("- 在线授权、第三方连接、外部写入、支付、部署和生产访问：均未执行。")


def main() -> int:
    passed = True
    for name, script in CHECKS:
        passed = run(name, script) and passed
    report_detection()
    if not passed:
        print("\n聚合验收失败，请修复上方问题后重新执行。")
        return 1
    print("\n四套模板离线聚合验收通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
