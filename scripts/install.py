#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


RUNTIME_TARGETS = {
    "antigravity": Path(".gemini/config/plugins/pig-stack"),
    "cursor": Path(".cursor/plugins/pig-stack"),
    "claude": Path(".claude/plugins/pig-stack"),
    "codex": Path(".codex/skills/pig-stack"),
    "opencode": Path(".config/opencode/skills/pig-stack"),
}

COPY_ITEMS = (
    "plugin.json",
    ".cursor-plugin",
    ".claude-plugin",
    "assets",
    "agents",
    "docs",
    "rules",
    "skills",
    "scripts",
    ".atl",
    "README.md",
)


def install_target(
    source_root: Path,
    dest_path: Path,
    mode: str,
    dry_run: bool,
) -> str:
    if dry_run:
        return f"DRY-RUN {mode}: {source_root} -> {dest_path}"

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.is_symlink() or dest_path.is_file():
        dest_path.unlink()
    elif dest_path.exists():
        shutil.rmtree(dest_path)

    if mode == "symlink":
        os.symlink(source_root, dest_path, target_is_directory=True)
        return f"LINKED: {dest_path} -> {source_root}"

    dest_path.mkdir(parents=True, exist_ok=True)
    for item in COPY_ITEMS:
        src = source_root / item
        if not src.exists():
            continue
        dst = dest_path / item
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return f"COPIED: {source_root} -> {dest_path}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install pig-stack into one or more agent runtimes")
    parser.add_argument(
        "--target",
        choices=(*RUNTIME_TARGETS.keys(), "all"),
        default="antigravity",
    )
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    source_root = args.source.resolve()
    home = args.home.resolve()
    targets = list(RUNTIME_TARGETS.keys()) if args.target == "all" else [args.target]

    for name in targets:
        dest = home / RUNTIME_TARGETS[name]
        status = install_target(source_root, dest, args.mode, args.dry_run)
        print(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
