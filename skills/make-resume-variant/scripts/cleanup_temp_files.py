#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]

TEMP_DIR_EXACT = {"preview", "preview_v2", ".ocr-tmp"}
TEMP_DIR_PATTERNS = ("*-preview-*", "*_preview-*")
TEMP_FILE_PATTERNS = (
    ".DS_Store",
    "*.aux",
    "*.log",
    "*.out",
    "*.fls",
    "*.fdb_latexmk",
    "*.xdv",
    "*.synctex*",
    "missfont.log",
    "*preview*.png",
    "*preview*.pdf",
)


def normalize_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def matches_any(name: str, patterns: Tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def is_temp_dir(path: Path) -> bool:
    return path.name in TEMP_DIR_EXACT or matches_any(path.name, TEMP_DIR_PATTERNS)


def is_temp_file(path: Path) -> bool:
    return matches_any(path.name, TEMP_FILE_PATTERNS)


def cleanup_target(target: Path) -> None:
    if not target.exists():
        print(f"Cleanup target not found, skipping: {target}", file=sys.stderr)
        return

    if target.is_dir() and is_temp_dir(target):
        shutil.rmtree(target, ignore_errors=True)
        return

    if target.is_file():
        if is_temp_file(target):
            target.unlink(missing_ok=True)
        return

    dir_paths = sorted(
        (path for path in target.rglob("*") if path.is_dir() and is_temp_dir(path)),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for dir_path in dir_paths:
        shutil.rmtree(dir_path, ignore_errors=True)

    if not target.exists():
        return

    for file_path in target.rglob("*"):
        if file_path.is_file() and is_temp_file(file_path):
            file_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove LaTeX, preview, and OCR temp files from the repo or specific paths.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional target paths. Relative paths are resolved from the repo root.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.paths:
        cleanup_target(REPO_ROOT)
        return 0

    for raw_target in args.paths:
        cleanup_target(normalize_path(raw_target))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
