@AGENTS.md

## Claude Code

- This repository supports Claude Code through a project `CLAUDE.md` file and a project skill wrapper under `.claude/skills/`.
- For resume-variant work, use the project skill at `.claude/skills/make-resume-variant/SKILL.md`.
- For interview-driven master-source completion, use the project skill at `.claude/skills/interview-resume-source/SKILL.md`.
- Keep the shared workflow logic in `skills/make-resume-variant/`; the Claude Code skill is only a compatibility wrapper and should not become a second source of truth.
- Keep the master-source interview workflow in `skills/interview-resume-source/`; the Claude Code wrapper should only point to it.
- Do not add project-specific Claude subagents under `.claude/agents/` unless a later task clearly requires them. The current project goal is shared skill compatibility, not custom subagent behavior.
