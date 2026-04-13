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

    def test_project_skill_wrapper_exists(self) -> None:
        wrapper_skill = REPO_ROOT / ".claude" / "skills" / "make-resume-variant" / "SKILL.md"
        self.assertTrue(wrapper_skill.is_file())

    def test_project_skill_wrapper_points_to_shared_skill(self) -> None:
        wrapper_skill = REPO_ROOT / ".claude" / "skills" / "make-resume-variant" / "SKILL.md"
        content = wrapper_skill.read_text(encoding="utf-8")

        self.assertIn("../../../skills/make-resume-variant/SKILL.md", content)
        self.assertIn("../../../skills/make-resume-variant/references/content-selection.md", content)
        self.assertIn("../../../skills/make-resume-variant/references/pdf-review-checklist.md", content)


if __name__ == "__main__":
    unittest.main()
