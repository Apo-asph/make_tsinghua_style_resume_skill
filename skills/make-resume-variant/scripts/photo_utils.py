#!/usr/bin/env python3
from __future__ import annotations

import io
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


PHOTO_RATIO_MIN = 2.0 / 3.0
PHOTO_RATIO_MAX = 1.0
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg")
JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


class PhotoProcessingError(RuntimeError):
    pass


@dataclass(frozen=True)
class PhotoAssessment:
    photo_path: Path
    width: int
    height: int
    ratio: float
    min_ratio: float
    max_ratio: float
    status: str
    message: str
    needs_crop: bool
    target_ratio: Optional[float]
    crop_box: Optional[Tuple[int, int, int, int]]


def find_preferred_photo(base_dir: Path) -> Optional[Path]:
    for filename in ("profile_photo.png", "profile_photo.jpg", "profile_photo.jpeg"):
        candidate = base_dir / filename
        if candidate.is_file():
            return candidate
    return None


def read_image_dimensions(photo_path: Path) -> Tuple[int, int]:
    suffix = photo_path.suffix.lower()
    if suffix == ".png":
        return read_png_dimensions(photo_path)
    if suffix in {".jpg", ".jpeg"}:
        return read_jpeg_dimensions(photo_path)
    raise PhotoProcessingError(f"Unsupported photo format: {photo_path}")


def read_png_dimensions(photo_path: Path) -> Tuple[int, int]:
    with photo_path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise PhotoProcessingError(f"Invalid PNG file: {photo_path}")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width <= 0 or height <= 0:
        raise PhotoProcessingError(f"Invalid PNG dimensions: {photo_path}")
    return width, height


def read_jpeg_dimensions(photo_path: Path) -> Tuple[int, int]:
    with photo_path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            raise PhotoProcessingError(f"Invalid JPEG file: {photo_path}")

        while True:
            marker_prefix = handle.read(1)
            if not marker_prefix:
                break
            if marker_prefix != b"\xff":
                continue

            marker_code = handle.read(1)
            while marker_code == b"\xff":
                marker_code = handle.read(1)
            if not marker_code:
                break

            marker = marker_code[0]
            if marker in {0x01, 0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
                continue

            segment_length_bytes = handle.read(2)
            if len(segment_length_bytes) != 2:
                break
            segment_length = int.from_bytes(segment_length_bytes, "big")
            if segment_length < 2:
                raise PhotoProcessingError(f"Invalid JPEG segment in {photo_path}")

            if marker in JPEG_SOF_MARKERS:
                segment = handle.read(segment_length - 2)
                if len(segment) < 5:
                    break
                height = int.from_bytes(segment[1:3], "big")
                width = int.from_bytes(segment[3:5], "big")
                if width <= 0 or height <= 0:
                    raise PhotoProcessingError(f"Invalid JPEG dimensions: {photo_path}")
                return width, height

            handle.seek(segment_length - 2, io.SEEK_CUR)

    raise PhotoProcessingError(f"Could not read JPEG dimensions: {photo_path}")


def build_crop_box(width: int, height: int, target_ratio: float) -> Tuple[int, int, int, int]:
    current_ratio = width / height
    if abs(current_ratio - target_ratio) < 1e-6:
        return (0, 0, width, height)

    if current_ratio > target_ratio:
        crop_width = min(width, max(1, int(round(height * target_ratio))))
        offset_x = max(0, (width - crop_width) // 2)
        return (offset_x, 0, crop_width, height)

    crop_height = min(height, max(1, int(round(width / target_ratio))))
    offset_y = max(0, (height - crop_height) // 2)
    return (0, offset_y, width, crop_height)


def assess_photo(
    photo_path: Path,
    min_ratio: float = PHOTO_RATIO_MIN,
    max_ratio: float = PHOTO_RATIO_MAX,
) -> PhotoAssessment:
    width, height = read_image_dimensions(photo_path)
    ratio = width / height

    if ratio < min_ratio:
        crop_box = build_crop_box(width, height, min_ratio)
        return PhotoAssessment(
            photo_path=photo_path,
            width=width,
            height=height,
            ratio=ratio,
            min_ratio=min_ratio,
            max_ratio=max_ratio,
            status="too_tall",
            message=(
                f"Photo ratio {ratio:.4f} is taller than the recommended range "
                f"[{min_ratio:.4f}, {max_ratio:.4f}]."
            ),
            needs_crop=True,
            target_ratio=min_ratio,
            crop_box=crop_box,
        )

    if ratio > max_ratio:
        crop_box = build_crop_box(width, height, max_ratio)
        return PhotoAssessment(
            photo_path=photo_path,
            width=width,
            height=height,
            ratio=ratio,
            min_ratio=min_ratio,
            max_ratio=max_ratio,
            status="too_wide",
            message=(
                f"Photo ratio {ratio:.4f} is wider than the recommended range "
                f"[{min_ratio:.4f}, {max_ratio:.4f}]."
            ),
            needs_crop=True,
            target_ratio=max_ratio,
            crop_box=crop_box,
        )

    return PhotoAssessment(
        photo_path=photo_path,
        width=width,
        height=height,
        ratio=ratio,
        min_ratio=min_ratio,
        max_ratio=max_ratio,
        status="ok",
        message=(
            f"Photo ratio {ratio:.4f} is within the recommended range "
            f"[{min_ratio:.4f}, {max_ratio:.4f}]."
        ),
        needs_crop=False,
        target_ratio=None,
        crop_box=None,
    )


def get_powershell_command() -> Optional[str]:
    for command_name in ("pwsh", "powershell"):
        command = shutil.which(command_name)
        if command:
            return command
    return None


def crop_photo_center(
    photo_path: Path,
    target_ratio: float,
    output_path: Optional[Path] = None,
) -> Path:
    width, height = read_image_dimensions(photo_path)
    offset_x, offset_y, crop_width, crop_height = build_crop_box(width, height, target_ratio)

    if output_path is None:
        temp_dir = Path(tempfile.mkdtemp(prefix="photo-crop-"))
        output_path = temp_dir / photo_path.name
        replace_original = True
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        replace_original = False

    try:
        if crop_with_pillow(photo_path, output_path, offset_x, offset_y, crop_width, crop_height):
            pass
        elif sys.platform == "darwin" and shutil.which("sips"):
            crop_with_sips(photo_path, output_path, crop_width, crop_height)
        elif os.name == "nt" and get_powershell_command():
            crop_with_powershell(photo_path, output_path, offset_x, offset_y, crop_width, crop_height)
        else:
            raise PhotoProcessingError(
                "No supported photo crop backend found. Install Pillow, or use macOS sips / Windows PowerShell.",
            )

        if replace_original:
            output_path.replace(photo_path)
            return photo_path
        return output_path
    finally:
        if replace_original:
            temp_root = output_path.parent
            if temp_root.exists():
                shutil.rmtree(temp_root, ignore_errors=True)


def crop_with_pillow(
    photo_path: Path,
    output_path: Path,
    offset_x: int,
    offset_y: int,
    crop_width: int,
    crop_height: int,
) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False

    with Image.open(photo_path) as image:
        crop_box = (
            offset_x,
            offset_y,
            offset_x + crop_width,
            offset_y + crop_height,
        )
        cropped = image.crop(crop_box)
        save_kwargs = {}
        if image.format == "JPEG":
            save_kwargs["quality"] = 95
        cropped.save(output_path, format=image.format, **save_kwargs)
    return True


def crop_with_sips(photo_path: Path, output_path: Path, crop_width: int, crop_height: int) -> None:
    subprocess.run(
        [
            "sips",
            "-c",
            str(crop_height),
            str(crop_width),
            str(photo_path),
            "--out",
            str(output_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def crop_with_powershell(
    photo_path: Path,
    output_path: Path,
    offset_x: int,
    offset_y: int,
    crop_width: int,
    crop_height: int,
) -> None:
    powershell = get_powershell_command()
    if not powershell:
        raise PhotoProcessingError("PowerShell not found in PATH.")

    script_content = """
param(
  [string]$InputPath,
  [string]$OutputPath,
  [int]$OffsetX,
  [int]$OffsetY,
  [int]$CropWidth,
  [int]$CropHeight
)
Add-Type -AssemblyName System.Drawing
$image = [System.Drawing.Image]::FromFile($InputPath)
try {
  $bitmap = New-Object System.Drawing.Bitmap $CropWidth, $CropHeight
  try {
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
      $srcRect = New-Object System.Drawing.Rectangle $OffsetX, $OffsetY, $CropWidth, $CropHeight
      $destRect = New-Object System.Drawing.Rectangle 0, 0, $CropWidth, $CropHeight
      $graphics.DrawImage($image, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
      $extension = [System.IO.Path]::GetExtension($OutputPath).ToLowerInvariant()
      if ($extension -eq '.png') {
        $format = [System.Drawing.Imaging.ImageFormat]::Png
      } elseif ($extension -eq '.jpg' -or $extension -eq '.jpeg') {
        $format = [System.Drawing.Imaging.ImageFormat]::Jpeg
      } else {
        throw "Unsupported output format: $extension"
      }
      $bitmap.Save($OutputPath, $format)
    } finally {
      $graphics.Dispose()
    }
  } finally {
    $bitmap.Dispose()
  }
} finally {
  $image.Dispose()
}
"""
    with tempfile.TemporaryDirectory(prefix="photo-crop-ps-") as temp_dir:
        script_path = Path(temp_dir) / "crop_photo.ps1"
        script_path.write_text(script_content.strip(), encoding="utf-8")
        subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script_path),
                str(photo_path),
                str(output_path),
                str(offset_x),
                str(offset_y),
                str(crop_width),
                str(crop_height),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def format_assessment_lines(assessment: PhotoAssessment) -> List[str]:
    lines = [
        f"photo={assessment.photo_path}",
        f"width={assessment.width}",
        f"height={assessment.height}",
        f"ratio={assessment.ratio:.4f}",
        f"min_ratio={assessment.min_ratio:.4f}",
        f"max_ratio={assessment.max_ratio:.4f}",
        f"status={assessment.status}",
        f"needs_crop={'yes' if assessment.needs_crop else 'no'}",
        f"message={assessment.message}",
    ]
    if assessment.target_ratio is not None:
        lines.append(f"target_ratio={assessment.target_ratio:.4f}")
    if assessment.crop_box is not None:
        offset_x, offset_y, crop_width, crop_height = assessment.crop_box
        lines.append(f"crop_box={offset_x},{offset_y},{crop_width},{crop_height}")
    return lines
