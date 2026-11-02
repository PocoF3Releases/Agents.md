@AGENTS.md
@CURRENT_STATE.md

# Claude Code entrypoint

Use the same maintained rules and topic owners as other assistants. Read
`operations/claude-code.md` for WSL locations, model selection and setup; do not
load all evidence or source inventories. After compaction, explicitly reread
the [continuity protocol](operations/continuity.md),
`.agents/skills/alioth-resume/SKILL.md` and the relevant topic. Keep writable
task records separate across concurrent chats/clients; cite the source on handoff.

Claude-specific discovery lives in `.claude/skills/`; the linked skill bodies
remain in `.agents/skills/`. Update the original, not a second copy. Local tool
availability and authentication must be checked, never inferred from this file.
