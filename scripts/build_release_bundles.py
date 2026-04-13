#!/usr/bin/env python3
from __future__ import annotations

import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple


PROJECT_NAME = "make_tsinghua_style_resume_skill"
VERSION = "v0.3.0"
REPO_ROOT = Path(__file__).resolve().parents[1]
RELEASE_READMES_DIR = REPO_ROOT / "release-readmes"


COMMON_AGENT_FILES = (
    ".gitignore",
    "resume_master_source.md",
    "profile_photo.png",
    "latex template/resume_tsinghua_purple.tex",
    "skills/make-resume-variant/SKILL.md",
    "skills/make-resume-variant/references/content-selection.md",
    "skills/make-resume-variant/references/pdf-review-checklist.md",
    "skills/make-resume-variant/scripts/cleanup_temp_files.py",
    "skills/make-resume-variant/scripts/cleanup_temp_files.sh",
    "skills/make-resume-variant/scripts/compile_resume.py",
    "skills/make-resume-variant/scripts/compile_resume.sh",
    "skills/make-resume-variant/scripts/inspect_resume_pdf.py",
    "skills/make-resume-variant/scripts/inspect_resume_pdf.sh",
    "skills/make-resume-variant/scripts/tool_paths.py",
)

MANUAL_TEMPLATE_FILES = (
    ".gitignore",
    "resume_master_source.md",
    "profile_photo.png",
    "latex template/resume_tsinghua_purple.tex",
    "latex template/resume_tsinghua_purple.pdf",
)


@dataclass(frozen=True)
class ReleaseBundle:
    key: str
    zip_name: str
    package_root: str
    readme_source: str
    included_files: Tuple[str, ...]


def build_release_bundles() -> Tuple[ReleaseBundle, ...]:
    return (
        ReleaseBundle(
            key="claude-code",
            zip_name=f"{PROJECT_NAME}-release-claude-code-minimal-{VERSION}.zip",
            package_root=f"{PROJECT_NAME}-release-claude-code-minimal-{VERSION}",
            readme_source="README.claude-code.md",
            included_files=(
                "AGENTS.md",
                "CLAUDE.md",
                ".claude/skills/make-resume-variant/SKILL.md",
            )
            + COMMON_AGENT_FILES,
        ),
        ReleaseBundle(
            key="codex",
            zip_name=f"{PROJECT_NAME}-release-codex-minimal-{VERSION}.zip",
            package_root=f"{PROJECT_NAME}-release-codex-minimal-{VERSION}",
            readme_source="README.codex.md",
            included_files=(
                "AGENTS.md",
                "skills/make-resume-variant/agents/openai.yaml",
            )
            + COMMON_AGENT_FILES,
        ),
        ReleaseBundle(
            key="manual-template",
            zip_name=f"{PROJECT_NAME}-release-manual-template-{VERSION}.zip",
            package_root=f"{PROJECT_NAME}-release-manual-template-{VERSION}",
            readme_source="README.manual-template.md",
            included_files=MANUAL_TEMPLATE_FILES,
        ),
    )


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def iter_files(root: Path) -> Iterable[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def build_bundle(bundle: ReleaseBundle) -> Path:
    zip_path = REPO_ROOT / bundle.zip_name
    if zip_path.exists():
        zip_path.unlink()

    readme_path = RELEASE_READMES_DIR / bundle.readme_source
    if not readme_path.is_file():
        raise FileNotFoundError(f"Release README not found: {readme_path}")

    with tempfile.TemporaryDirectory(prefix=f"{bundle.key}-release-") as tmp_dir:
        package_root = Path(tmp_dir) / bundle.package_root
        package_root.mkdir(parents=True, exist_ok=True)

        copy_file(readme_path, package_root / "README.md")

        for rel_path_str in bundle.included_files:
            src = REPO_ROOT / rel_path_str
            if not src.is_file():
                raise FileNotFoundError(f"Release source file not found: {src}")
            copy_file(src, package_root / rel_path_str)

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in iter_files(package_root):
                arcname = file_path.relative_to(package_root.parent)
                zip_file.write(file_path, arcname)

    return zip_path


def main() -> int:
    built_paths = [build_bundle(bundle) for bundle in build_release_bundles()]
    for built_path in built_paths:
        print(built_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
