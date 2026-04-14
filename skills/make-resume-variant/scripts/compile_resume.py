#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from photo_utils import assess_photo, find_preferred_photo
from tool_paths import CommandResolutionError, build_command_env, find_latexmk, find_xelatex


REPO_ROOT = Path(__file__).resolve().parents[3]
CLEANUP_SCRIPT = Path(__file__).with_name("cleanup_temp_files.py")
PREPARE_PHOTO_SCRIPT = Path(__file__).with_name("prepare_photo.py")


def resolve_variant_dir(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def format_hint_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile a resume variant directory with latexmk and clean temp files.",
    )
    parser.add_argument(
        "target",
        help="Variant directory name under the repo root, or an absolute variant directory path.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    variant_dir = resolve_variant_dir(args.target)
    if not variant_dir.is_dir():
        raise SystemExit(f"Variant directory not found: {variant_dir}")

    slug = variant_dir.name
    tex_file = variant_dir / f"{slug}.tex"
    pdf_file = variant_dir / f"{slug}.pdf"

    if not tex_file.is_file():
        raise SystemExit(f"Expected TeX file not found: {tex_file}")

    photo_path = find_preferred_photo(variant_dir)
    if photo_path:
        assessment = assess_photo(photo_path)
        if assessment.needs_crop:
            photo_hint = format_hint_path(photo_path)
            script_hint = format_hint_path(PREPARE_PHOTO_SCRIPT)
            print(
                (
                    f"Warning: {assessment.message} "
                    f"After user approval, prefer center-cropping the variant photo copy with "
                    f"`python {script_hint} {photo_hint} --crop-center`."
                ),
                file=sys.stderr,
            )

    try:
        latexmk = find_latexmk()
        xelatex = find_xelatex()
    except CommandResolutionError as exc:
        raise SystemExit(str(exc))

    subprocess.run(
        [
            latexmk,
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            tex_file.name,
        ],
        cwd=variant_dir,
        env=build_command_env((latexmk, xelatex)),
        check=True,
    )

    if not pdf_file.is_file():
        raise SystemExit(f"Expected PDF not found after compile: {pdf_file}")

    subprocess.run([sys.executable, str(CLEANUP_SCRIPT), str(variant_dir)], check=True)
    print(pdf_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
