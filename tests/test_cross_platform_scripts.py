from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "make-resume-variant" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import compile_resume
import tool_paths


class CrossPlatformScriptTests(unittest.TestCase):
    def run_script(self, script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / script_name), *args],
            text=True,
            capture_output=True,
        )

    def test_cleanup_script_removes_temp_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            keep_file = root / "resume.tex"
            aux_file = root / "resume.aux"
            preview_dir = root / "preview"
            nested_preview_dir = root / "draft_preview-cache"

            keep_file.write_text("keep", encoding="utf-8")
            aux_file.write_text("temp", encoding="utf-8")
            preview_dir.mkdir()
            (preview_dir / "page-01.png").write_text("temp", encoding="utf-8")
            nested_preview_dir.mkdir()
            (nested_preview_dir / "page-02.png").write_text("temp", encoding="utf-8")

            result = self.run_script("cleanup_temp_files.py", str(root))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(keep_file.exists())
            self.assertFalse(aux_file.exists())
            self.assertFalse(preview_dir.exists())
            self.assertFalse(nested_preview_dir.exists())

    def test_compile_script_help(self) -> None:
        result = self.run_script("compile_resume.py", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("target", result.stdout)

    def test_compile_script_reports_missing_variant_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing_dir = Path(tmp_dir) / "missing"
            result = self.run_script("compile_resume.py", str(missing_dir))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Variant directory not found", result.stderr)

    def test_compile_script_builds_env_with_tool_dirs(self) -> None:
        env = compile_resume.build_command_env(
            (
                "/tmp/tools/texlive/bin/latexmk",
                "/tmp/tools/texlive/bin/xelatex",
            )
        )
        first_path_entry = env["PATH"].split(os.pathsep)[0]
        self.assertEqual(Path(first_path_entry), Path("/tmp/tools/texlive/bin").resolve())

    def test_inspect_script_help(self) -> None:
        result = self.run_script("inspect_resume_pdf.py", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("pdf_path", result.stdout)

    def test_inspect_script_reports_missing_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing_pdf = Path(tmp_dir) / "missing.pdf"
            result = self.run_script("inspect_resume_pdf.py", str(missing_pdf))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PDF not found", result.stderr)

    def test_windows_command_lookup_uses_common_texlive_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            command = root / "TeX Live" / "2026" / "bin" / "win32" / "xelatex.exe"
            command.parent.mkdir(parents=True)
            command.write_text("", encoding="utf-8")

            with mock.patch.object(tool_paths, "is_windows", return_value=True):
                with mock.patch.object(tool_paths, "iter_windows_roots", return_value=[root]):
                    with mock.patch("tool_paths.shutil.which", return_value=None):
                        resolved = tool_paths.find_xelatex()

            self.assertEqual(resolved, str(command))

    def test_windows_command_lookup_uses_env_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            command = Path(tmp_dir) / "ghostscript" / "gswin64c.exe"
            command.parent.mkdir(parents=True)
            command.write_text("", encoding="utf-8")

            with mock.patch.dict(os.environ, {"GHOSTSCRIPT": str(command)}, clear=False):
                resolved = tool_paths.find_ghostscript()

            self.assertEqual(resolved, str(command))


if __name__ == "__main__":
    unittest.main()
