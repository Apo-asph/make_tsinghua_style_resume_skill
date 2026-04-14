from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_release_bundles


class ReleaseBundleBuilderTests(unittest.TestCase):
    def test_release_bundle_count(self) -> None:
        bundles = build_release_bundles.build_release_bundles()
        self.assertEqual(len(bundles), 3)

    def test_release_readmes_exist(self) -> None:
        for bundle in build_release_bundles.build_release_bundles():
            readme_path = build_release_bundles.RELEASE_READMES_DIR / bundle.readme_source
            self.assertTrue(readme_path.is_file(), readme_path)

    def test_release_sources_exist(self) -> None:
        for bundle in build_release_bundles.build_release_bundles():
            for rel_path_str in bundle.included_files:
                src = REPO_ROOT / rel_path_str
                self.assertTrue(src.is_file(), src)

    def test_agent_bundles_include_photo_scripts(self) -> None:
        photo_script_paths = {
            "skills/make-resume-variant/scripts/photo_utils.py",
            "skills/make-resume-variant/scripts/prepare_photo.py",
            "skills/make-resume-variant/scripts/prepare_photo.sh",
        }
        for bundle in build_release_bundles.build_release_bundles():
            if bundle.key == "manual-template":
                continue
            self.assertTrue(photo_script_paths.issubset(set(bundle.included_files)))

    def test_agent_bundles_include_resume_source_interview_skill(self) -> None:
        shared_skill_files = {
            "skills/interview-resume-source/SKILL.md",
            "skills/interview-resume-source/references/interview-outline.md",
            "skills/interview-resume-source/scripts/audit_resume_source.py",
        }
        for bundle in build_release_bundles.build_release_bundles():
            if bundle.key == "manual-template":
                continue
            self.assertTrue(shared_skill_files.issubset(set(bundle.included_files)))

    def test_claude_and_codex_specific_interview_skill_files(self) -> None:
        bundle_map = {bundle.key: bundle for bundle in build_release_bundles.build_release_bundles()}
        self.assertIn(
            ".claude/skills/interview-resume-source/SKILL.md",
            bundle_map["claude-code"].included_files,
        )
        self.assertIn(
            "skills/interview-resume-source/agents/openai.yaml",
            bundle_map["codex"].included_files,
        )


if __name__ == "__main__":
    unittest.main()
