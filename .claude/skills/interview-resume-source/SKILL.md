---
name: interview-resume-source
description: Conduct a structured interview to fill, repair, or clarify `resume_master_source.md`, then update the file with verified facts and explicit pending items. Use when Claude Code needs to interview the user in rounds and turn the answers into a cleaner master resume source.
---

# Interview Resume Source

This file is the Claude Code compatibility wrapper for the canonical project skill.

## Source of Truth

- First read `../../../skills/interview-resume-source/SKILL.md` and follow it as the canonical workflow.
- Do not fork or duplicate that workflow here unless the repository intentionally decides to maintain separate Claude Code behavior later.

## Supporting Files

- When the canonical skill tells you to read references, load:
  - `../../../skills/interview-resume-source/references/interview-outline.md`
- Use scripts from `../../../skills/interview-resume-source/scripts/`.

## Invocation Notes

- Run project scripts from the repository root, for example:
  - `python skills/interview-resume-source/scripts/audit_resume_source.py`
- The root `CLAUDE.md` imports `AGENTS.md`, so project-level guardrails and cleanup rules still apply.
