from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "make-resume-variant" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import photo_utils


PNG_300X400 = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x01,"
    b"\x00\x00\x01\x90"
    b"\x08\x02\x00\x00\x00"
    b"\x00\x00\x00\x00"
)

JPEG_1X1 = (
    b"\xff\xd8"
    b"\xff\xe0\x00\x10"
    b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    b"\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x00\x03\x11\x00"
    b"\xff\xd9"
)


class PhotoToolsTests(unittest.TestCase):
    def test_png_dimension_reader(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.png"
            photo_path.write_bytes(PNG_300X400)
            width, height = photo_utils.read_png_dimensions(photo_path)
            self.assertEqual((width, height), (300, 400))

    def test_jpeg_dimension_reader(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.jpg"
            photo_path.write_bytes(JPEG_1X1)
            width, height = photo_utils.read_jpeg_dimensions(photo_path)
            self.assertEqual((width, height), (1, 1))

    def test_assess_photo_within_range(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.png"
            photo_path.write_bytes(PNG_300X400)
            assessment = photo_utils.assess_photo(photo_path, min_ratio=0.6, max_ratio=1.0)
            self.assertEqual(assessment.status, "ok")
            self.assertFalse(assessment.needs_crop)

    def test_assess_photo_too_wide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.png"
            photo_path.write_bytes(PNG_300X400.replace(b"\x00\x00\x01,", b"\x00\x00\x02\x58", 1))
            assessment = photo_utils.assess_photo(photo_path, min_ratio=0.6667, max_ratio=1.0)
            self.assertEqual(assessment.status, "too_wide")
            self.assertTrue(assessment.needs_crop)

    def test_build_crop_box_for_tall_photo(self) -> None:
        crop_box = photo_utils.build_crop_box(600, 1200, target_ratio=2.0 / 3.0)
        self.assertEqual(crop_box, (0, 150, 600, 900))

    def test_build_crop_box_for_wide_photo(self) -> None:
        crop_box = photo_utils.build_crop_box(1200, 600, target_ratio=1.0)
        self.assertEqual(crop_box, (300, 0, 600, 600))

    def test_prepare_photo_script_reports_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.png"
            photo_path.write_bytes(PNG_300X400)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "prepare_photo.py"), str(photo_path)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status=ok", result.stdout)

    def test_crop_uses_sips_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "profile_photo.png"
            output_path = Path(tmp_dir) / "out.png"
            photo_path.write_bytes(PNG_300X400)

            with mock.patch("photo_utils.crop_with_pillow", return_value=False):
                with mock.patch("photo_utils.shutil.which", return_value="/usr/bin/sips"):
                    with mock.patch("photo_utils.sys.platform", "darwin"):
                        with mock.patch("photo_utils.subprocess.run") as mock_run:
                            photo_utils.crop_photo_center(photo_path, target_ratio=1.0, output_path=output_path)

            mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
