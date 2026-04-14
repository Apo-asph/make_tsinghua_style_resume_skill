#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from photo_utils import (
    PHOTO_RATIO_MAX,
    PHOTO_RATIO_MIN,
    assess_photo,
    crop_photo_center,
    format_assessment_lines,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


def resolve_photo_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def resolve_output_path(raw_path: str, photo_path: Path) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else photo_path.parent / path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a profile photo ratio and optionally center-crop it to the supported range.",
    )
    parser.add_argument("photo_path", help="Photo path. Relative paths are resolved from the repo root.")
    parser.add_argument("--min-ratio", type=float, default=PHOTO_RATIO_MIN)
    parser.add_argument("--max-ratio", type=float, default=PHOTO_RATIO_MAX)
    parser.add_argument(
        "--crop-center",
        action="store_true",
        help="Center-crop the photo to the nearest supported ratio boundary.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. When omitted, crop is applied in place.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    photo_path = resolve_photo_path(args.photo_path)
    if not photo_path.is_file():
        raise SystemExit(f"Photo not found: {photo_path}")

    if args.min_ratio <= 0 or args.max_ratio <= 0 or args.min_ratio > args.max_ratio:
        raise SystemExit("Invalid ratio range.")

    assessment = assess_photo(photo_path, min_ratio=args.min_ratio, max_ratio=args.max_ratio)

    if args.crop_center and assessment.needs_crop:
        output_path = resolve_output_path(args.output, photo_path) if args.output else None
        final_path = crop_photo_center(photo_path, assessment.target_ratio, output_path=output_path)
        final_assessment = assess_photo(final_path, min_ratio=args.min_ratio, max_ratio=args.max_ratio)
        for line in format_assessment_lines(final_assessment):
            if line.startswith("status="):
                print("status=cropped")
            elif line.startswith("message="):
                print(
                    "message=Center-cropped photo to the supported ratio range "
                    f"[{final_assessment.min_ratio:.4f}, {final_assessment.max_ratio:.4f}]."
                )
            else:
                print(line)
        return 0

    for line in format_assessment_lines(assessment):
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
