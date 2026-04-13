#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


REPO_ROOT = Path(__file__).resolve().parents[3]
CLEANUP_SCRIPT = Path(__file__).with_name("cleanup_temp_files.py")


def resolve_variant_dir(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def require_command(name: str) -> str:
    command = shutil.which(name)
    if command:
        return command
    raise SystemExit(f"{name} not found in PATH.")


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

    latexmk = require_command("latexmk")
    require_command("xelatex")

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
        check=True,
    )

    if not pdf_file.is_file():
        raise SystemExit(f"Expected PDF not found after compile: {pdf_file}")

    subprocess.run([sys.executable, str(CLEANUP_SCRIPT), str(variant_dir)], check=True)
    print(pdf_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
