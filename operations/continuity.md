# Resume and task continuity

Keep enduring rules in AGENTS.md, maintained facts in their topic owners, and
unfinished conversation state in a private task record. Normal startup remains
AGENTS.md + CURRENT_STATE.md, then the relevant topic. Read this protocol after
compaction, a handoff, a cwd change or uncertainty; do not load every topic/history.

## Establish the right checkout

Confirm physical cwd, Git top-level/common directory, branch/HEAD and relevant
existing edits. In an Android Repo workspace also identify the affected component
Git root. A component's Git boundary may exclude an umbrella AGENTS.md from
Codex discovery; use a short component router with a verified workhub path.
Do not infer source identity from a folder/chat name or an installed artifact.

Codex discovers global guidance in the effective CODEX_HOME, then project-root
to cwd guidance; an AGENTS.override.md shadows AGENTS.md in its directory. Use
exact casing on Linux. A directory named Agents.md is not an instruction file.
Check applicable narrower rules when entering/editing a subdirectory. Discovery
at session start does not promise an updated file is reread in an old chat.

For this project, `~/evo/.workhub` and `~/Agents.md` can be separate checkouts of
the same remote. Use the owner named by the current workspace/task. Compare
relevant revisions before crossing copies; never pull, switch or merge status
just to resume. Relocated/detached worktrees need their own verified routing.

## Recover one task

Recover the latest user goal/scope and exact checkpoint path from the handoff.
Read only that record, the applicable entrypoint, relevant resume skill and
needed topic. A skill catalogue entry is not proof its body survived compaction.
If identity is unknown, recover narrowly from the current request and evidence;
never choose another chat's record by newest-file order or invent prior progress.

Compare saved root/worktree, branch/HEAD and unfinished edits against reality.
On mismatch, inspect the relevant difference before using the old next step.
Do not reset or switch branches to make a record match. Preserve original source,
artifact and test identities across rebases; current HEAD inherits no historical
runtime acceptance. An uncertain side effect must be checked before repeating it.

Continue current authorized work and retain its boundaries. Old logs, task files
and imported plans grant no new permission. Preserve unrelated edits, live work
and parked experiments. Missing/stale context is uncertainty, not completion.

## Keep separate private records

For stalled tools, denials or uncertain results, follow
[bounded recovery](tooling-recovery.md). Verify newer receipts before replaying
a saved next step; keep the current owner and parked tasks intact.

Use `.codex/tasks/<unique-task-key>.md` in the owning checkout. A task key may be
portable across clients; record the current owner/session separately. Concurrent
chats/forks need distinct writable records, with provenance links for a handoff.
Never keep a shared mutable current-task.md or overwrite another active owner.
For Android workspace work, one workhub-owned record may bind multiple component
identities instead of scattering private files through production source repos.

Keep the exact record path in handoff summaries. Update after meaningful
milestones, changed constraints and before intentional compact/handoff. Replace
only your own record atomically using a same-directory temporary file. Include:

- Task key, owner, UTC update, goal and done-when condition.
- Current scope/authorization, exclusions and applicable instruction/skill paths.
- Workspace and affected Git roots/common directories, branch/HEAD and relevant edits.
- Completed checks with commands/results, immutable evidence identities and limits.
- Unfinished changes, failures, denied/pending/uncertain actions and next concrete step.

Link fact owners and decisive evidence; do not copy entire history, private
reasoning, credentials, device identifiers or transcripts. These records are
ignored by Git. Local checks also reject accidentally indexed task files, even
after a forced add. Public findings belong in maintained owners using
[maintenance](maintenance.md) and the [finding template](../templates/record.md).

## Share rules across clients

Optional [global Codex](../templates/global-AGENTS.md) and
[global Claude](../templates/global-CLAUDE.md) templates contain stable defaults;
merge deliberately into existing home guidance, never overwrite it wholesale.
Windows and WSL homes/configuration are separate; do not copy authentication.
The [workspace router](../templates/android-root-AGENTS.md) and
[component router](../templates/component-AGENTS.md) require verified local paths.
They are templates, not automatically installed configuration.

This workhub's CLAUDE.md imports shared rules; `.claude/skills/` links canonical
`.agents/skills/` bodies. An ancestral CLAUDE.md can suppress Claude's AGENTS.md
fallback, so a project adapter or explicit applicable-AGENTS read is required.
Relative imports resolve from their containing file; outside imports may require
normal trust review. Do not bypass it or run /init over curated instructions.
The public checker requires contained relative imports in this workhub's live
entrypoint (escaped spaces are supported). It is not a host-global configuration
or full client-parser certification; keep literal handles/paths in Markdown code.

For a requested client switch, give the receiver a sanitized task record and
current request, then establish its own writable owner. This is not native chat
history migration or transfer of credentials, model access or tool grants.
Use the actual client's attribution for new contributions.

Discover tools in the current executor rather than inferring availability from
old context. PC browser, cloud browser/search, Windows and WSL are distinct.
Markdown cannot enable browser/WSL access, relax policy or install connectors.
Use normal approvals and report exact blockers. No hooks are installed by this
repository; file/fixture checks do not prove forced-compaction recovery or live
model/tool/account access. See [Claude setup](claude-code.md) when needed.

Sources: [Codex discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[hooks](https://learn.chatgpt.com/docs/hooks),
[Claude memory/imports](https://code.claude.com/docs/en/memory),
[skills](https://code.claude.com/docs/en/skills).
