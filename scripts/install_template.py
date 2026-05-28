#!/usr/bin/env python3
"""Install AI IDE initialization templates or skill sets into a target project."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_URL = "https://github.com/ligyDt/ai-ide-init-template.git"
TOOLS = ("codex", "cursor", "codebuddy", "trae")
TOOL_SKILL_DIRS = {
    "codex": Path(".agents/skills"),
    "cursor": Path(".cursor/skills"),
    "codebuddy": Path(".codebuddy/skills"),
    "trae": Path(".agents/skills"),
}
INSTALLER_SKILL_SOURCE = Path("skills/ai-ide-init-template")


def fail(message: str) -> None:
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(1)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install AI IDE Init Template assets into a target project."
    )
    parser.add_argument(
        "--tool",
        choices=TOOLS,
        required=True,
        help="Target AI IDE template to install.",
    )
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Target project root or skill root, depending on --mode.",
    )
    parser.add_argument(
        "--mode",
        choices=("full", "skills", "installer-skill"),
        default="full",
        help="Install the full template, only workflow skills, or the installer skill.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        help="Local ai-ide-init-template repository. Defaults to this checkout.",
    )
    parser.add_argument(
        "--from-git",
        action="store_true",
        help=f"Clone {REPO_URL} into a temporary directory and install from it.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files under the target path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned operations without writing files.",
    )
    return parser.parse_args()


def resolve_source(args: argparse.Namespace) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    if args.from_git:
        temp_dir = tempfile.TemporaryDirectory(prefix="ai-ide-init-template-")
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, temp_dir.name],
            check=True,
            text=True,
        )
        return Path(temp_dir.name), temp_dir
    source = args.source.resolve() if args.source else repo_root()
    if not (source / "README.md").is_file():
        fail(f"源目录不是有效模板仓库：{source}")
    return source, None


def copy_path(src: Path, dst: Path, overwrite: bool, dry_run: bool) -> None:
    if dst.exists():
        if not overwrite:
            fail(f"目标已存在，请先合并或使用 --overwrite：{dst}")
        action = "覆盖"
    else:
        action = "创建"

    if dry_run:
        print(f"[dry-run] {action} {dst} <- {src}")
        return

    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    print(f"{action} {dst} <- {src}")


def iter_full_template(source: Path, tool: str) -> list[tuple[Path, Path]]:
    template_root = source / tool
    if not template_root.is_dir():
        fail(f"源目录缺少工具模板：{template_root}")
    return [(item, Path(item.name)) for item in sorted(template_root.iterdir(), key=lambda path: path.name)]


def iter_skill_template(source: Path, tool: str) -> list[tuple[Path, Path]]:
    skill_root = source / tool / TOOL_SKILL_DIRS[tool]
    if not skill_root.is_dir():
        fail(f"源目录缺少 Skills：{skill_root}")
    return [(item, TOOL_SKILL_DIRS[tool] / item.name) for item in sorted(skill_root.iterdir(), key=lambda path: path.name)]


def iter_installer_skill(source: Path, tool: str) -> list[tuple[Path, Path]]:
    skill_source = source / INSTALLER_SKILL_SOURCE
    if not skill_source.is_dir():
        fail(f"源目录缺少安装型 Skill：{skill_source}")
    return [(skill_source, TOOL_SKILL_DIRS[tool] / skill_source.name)]


def main() -> int:
    args = parse_args()
    source, temp_dir = resolve_source(args)
    try:
        target = args.target.resolve()
        if args.mode == "full":
            entries = iter_full_template(source, args.tool)
        elif args.mode == "skills":
            entries = iter_skill_template(source, args.tool)
        else:
            entries = iter_installer_skill(source, args.tool)

        print(f"安装模式：{args.mode}")
        print(f"目标工具：{args.tool}")
        print(f"源目录：{source}")
        print(f"目标目录：{target}")
        for src, relative_dst in entries:
            copy_path(src, target / relative_dst, args.overwrite, args.dry_run)
        if args.mode == "full":
            verify_script = target / "scripts" / f"verify_{args.tool}_setup.py"
            if verify_script.exists() and not args.dry_run:
                print(f"建议执行：python3 {verify_script}")
        return 0
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
