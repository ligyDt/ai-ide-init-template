#!/usr/bin/env python3
"""Bootstrap installer for the ai-ide-init-template skill."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


REPO_URL = "https://github.com/ligyDt/ai-ide-init-template.git"


def find_local_repo(start: Path) -> Path | None:
    for path in (start, *start.parents):
        script = path / "scripts/install_template.py"
        if script.is_file() and (path / "README.md").is_file():
            return path
    return None


def strip_from_git(args: list[str]) -> list[str]:
    return [arg for arg in args if arg != "--from-git"]


def value_after(args: list[str], flag: str) -> str | None:
    try:
        return args[args.index(flag) + 1]
    except (ValueError, IndexError):
        return None


def run_installer(source: Path, args: list[str]) -> int:
    command = [sys.executable, str(source / "scripts/install_template.py"), *args]
    return subprocess.run(command, cwd=source, check=False).returncode


def main() -> int:
    args = sys.argv[1:]
    explicit_source = value_after(args, "--source")
    if explicit_source:
        return run_installer(Path(explicit_source).resolve(), args)

    if "--from-git" not in args:
        local_repo = find_local_repo(Path(__file__).resolve())
        if local_repo is not None:
            return run_installer(local_repo, args)

    with tempfile.TemporaryDirectory(prefix="ai-ide-init-template-") as temp:
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, temp],
            check=True,
            text=True,
        )
        return run_installer(Path(temp), strip_from_git(args))


if __name__ == "__main__":
    raise SystemExit(main())
