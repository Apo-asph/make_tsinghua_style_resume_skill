@AGENTS.md

## Claude Code

- This repository supports Claude Code through a project `CLAUDE.md` file and a project skill wrapper under `.claude/skills/`.
- For resume-variant work, use the project skill at `.claude/skills/make-resume-variant/SKILL.md`.
- Keep the shared workflow logic in `skills/make-resume-variant/`; the Claude Code skill is only a compatibility wrapper and should not become a second source of truth.
- Do not add project-specific Claude subagents under `.claude/agents/` unless a later task clearly requires them. The current `v0.3.0` goal is project skill compatibility, not custom subagent behavior.
