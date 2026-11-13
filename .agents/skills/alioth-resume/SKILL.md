---
name: alioth-resume
description: Restore the correct Alioth checkout, scoped task and verification context after a handoff or compaction without launching work.
license: CC0-1.0
---

# Resume alioth platform work

Reread the Workhub's AGENTS.md and CURRENT_STATE.md, then follow
`operations/continuity.md` and this chat's exact private checkpoint. Revalidate
cwd/worktree, component roots, branch/HEAD and existing edits before continuing.
Read only the relevant topic; never select another task by recency.

This repository owns guidance/evidence, not Android sources. Resolve the task's
actual Linux checkout (`~/evo` is the usual workspace). Use the installed
`aosp-wsl` skill or `skills/aosp-wsl/SKILL.md`; for kernel/driver work also use the
relevant installed kernel skill. `operations/agent-skills.md` owns other routing.

Keep source, host, build and runtime evidence separate. For failed/denied/uncertain
tools follow `operations/tooling-recovery.md`. Preserve parked work and unrelated
edits. Skills and saved plans authorize no sync, build, flash or publication;
the current user scope and runtime approvals govern those actions.

Provenance: project workflow authored for this Workhub on 2026-10-23, CC0-1.0.
No third-party skill text or executable code is bundled here.
