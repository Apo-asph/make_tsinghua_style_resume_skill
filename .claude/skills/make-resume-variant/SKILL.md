---
name: make-resume-variant
description: Tailor a target-specific LaTeX resume variant in this project from `resume_master_source.md`, `profile_photo.png` or `profile_photo.jpg`, and `latex template/resume_tsinghua_purple.tex`, then compile the PDF, review layout, and refine after user approval. Use when Claude Code needs to create, update, or inspect a Chinese resume variant for research, R&D, algorithm, AI for Science, or high-potential applications.
---

# Make Resume Variant

This file is the Claude Code compatibility wrapper for the canonical project skill.

## Source of Truth

- First read `../../../skills/make-resume-variant/SKILL.md` and follow it as the canonical workflow.
- Do not fork or duplicate that workflow here unless the repository intentionally decides to maintain separate Claude Code behavior later.

## Supporting Files

- When the canonical skill tells you to read references, load:
  - `../../../skills/make-resume-variant/references/content-selection.md`
  - `../../../skills/make-resume-variant/references/pdf-review-checklist.md`
- Use scripts from `../../../skills/make-resume-variant/scripts/`.

## Invocation Notes

- Run project scripts from the repository root, for example:
  - `python skills/make-resume-variant/scripts/compile_resume.py <target-slug>`
  - `python skills/make-resume-variant/scripts/inspect_resume_pdf.py <pdf-path>`
  - `python skills/make-resume-variant/scripts/cleanup_temp_files.py [path ...]`
- The root `CLAUDE.md` imports `AGENTS.md`, so project-level guardrails and cleanup rules still apply.
