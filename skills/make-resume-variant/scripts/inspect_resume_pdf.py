#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional


REPO_ROOT = Path(__file__).resolve().parents[3]
GHOSTSCRIPT_CANDIDATES = ("gs", "gswin64c", "gswin32c")


def resolve_pdf_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def resolve_preview_dir(raw_path: str, pdf_dir: Path) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else pdf_dir / path


def find_ghostscript() -> str:
    for command_name in GHOSTSCRIPT_CANDIDATES:
        command = shutil.which(command_name)
        if command:
            return command
    candidate_text = ", ".join(GHOSTSCRIPT_CANDIDATES)
    raise SystemExit(f"Ghostscript not found in PATH. Tried: {candidate_text}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render PDF preview images with Ghostscript and report page count.",
    )
    parser.add_argument("pdf_path", help="PDF path. Relative paths are resolved from the repo root.")
    parser.add_argument(
        "preview_dir",
        nargs="?",
        help="Optional preview directory. Relative paths are resolved from the PDF directory.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    pdf_path = resolve_pdf_path(args.pdf_path)
    if not pdf_path.is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    pdf_dir = pdf_path.parent
    pdf_stem = pdf_path.stem

    if args.preview_dir:
        preview_dir = resolve_preview_dir(args.preview_dir, pdf_dir)
        preview_dir.mkdir(parents=True, exist_ok=True)
    else:
        safe_stem = pdf_stem.replace(" ", "_")
        preview_dir = Path(tempfile.mkdtemp(prefix=f"{safe_stem}-preview-"))

    ghostscript = find_ghostscript()
    subprocess.run(
        [
            ghostscript,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=pngalpha",
            "-r144",
            "-o",
            str(preview_dir / "page-%02d.png"),
            str(pdf_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )

    page_count = len(list(preview_dir.glob("page-*.png")))
    if page_count == 0:
        raise SystemExit(f"No preview images were generated for {pdf_path}")

    print(f"pdf={pdf_path}")
    print(f"page_count={page_count}")
    print(f"preview_dir={preview_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
