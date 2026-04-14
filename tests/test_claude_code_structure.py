from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ClaudeCodeStructureTests(unittest.TestCase):
    def test_claude_md_imports_agents_md(self) -> None:
        claude_md = REPO_ROOT / "CLAUDE.md"
        self.assertTrue(claude_md.is_file())

        content = claude_md.read_text(encoding="utf-8")
        self.assertIn("@AGENTS.md", content)

    def test_project_skill_wrappers_exist(self) -> None:
        resume_variant_wrapper = REPO_ROOT / ".claude" / "skills" / "make-resume-variant" / "SKILL.md"
        interview_wrapper = REPO_ROOT / ".claude" / "skills" / "interview-resume-source" / "SKILL.md"
        self.assertTrue(resume_variant_wrapper.is_file())
        self.assertTrue(interview_wrapper.is_file())

    def test_resume_variant_wrapper_points_to_shared_skill(self) -> None:
        wrapper_skill = REPO_ROOT / ".claude" / "skills" / "make-resume-variant" / "SKILL.md"
        content = wrapper_skill.read_text(encoding="utf-8")

        self.assertIn("../../../skills/make-resume-variant/SKILL.md", content)
        self.assertIn("../../../skills/make-resume-variant/references/content-selection.md", content)
        self.assertIn("../../../skills/make-resume-variant/references/pdf-review-checklist.md", content)

    def test_interview_wrapper_points_to_shared_skill(self) -> None:
        wrapper_skill = REPO_ROOT / ".claude" / "skills" / "interview-resume-source" / "SKILL.md"
        content = wrapper_skill.read_text(encoding="utf-8")

        self.assertIn("../../../skills/interview-resume-source/SKILL.md", content)
        self.assertIn("../../../skills/interview-resume-source/references/interview-outline.md", content)


if __name__ == "__main__":
    unittest.main()
