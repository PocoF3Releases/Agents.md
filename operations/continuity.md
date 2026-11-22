# Resume and task continuity

Normal startup is AGENTS.md + CURRENT_STATE.md, then one relevant topic.
After resume, compaction, a handoff or uncertain state, use this protocol instead
of loading all topics and old plans. Global host guidance still applies.

## Establish the right checkout

Confirm physical cwd, Git top-level/common directory, branch/HEAD and existing
edits; identify component roots inside an Android Repo workspace. Read the
effective CODEX_HOME's CONTINUITY.md, applicable AGENTS chain and relevant skill
bodies. Use exact casing: a directory named Agents.md is not an instruction file.

`~/evo/.workhub` and `~/Agents.md` can be separate checkouts. Use the current
task's named owner and compare relevant revisions before crossing copies.
Do not pull, reset or switch work just to make a saved record match reality.

## Recover one task

Read the current user scope and exact checkpoint from the handoff, then that
record and the relevant topic. Never select a different chat's task by recency.
Compare saved identity/edits with live state before using its next action.
Missing context calls for narrow recovery, not invented progress or permission.

Preserve source/artifact/test identities across rebases. A new HEAD does not
inherit old build/device acceptance. Check uncertain side effects before retrying.
Old logs and plans authorize no work; keep unrelated edits and parked tasks intact.

## Bound the current milestone

Record one objective, authorized actions/exclusions, required checks and completion
condition. Finish with a verified result, no-defect finding or explicit blocker.
Do not expand subsystems or manufacture changes to fill a backlog.

## Keep separate private records

Use `.codex/tasks/<unique-task-key>.md` in the owning checkout. Concurrent chats
and forks use distinct records; Android work may bind several components in one
Workhub-owned record. Include the exact path in handoffs. Never maintain a shared
mutable current-task.md or overwrite another owner's continuation.

Atomically replace only your record after meaningful progress, changed scope,
failure or before handoff. Keep owner/UTC, goal, permissions, workspace/Git roots,
branch/HEAD, existing edits, exact checks/identities/limits, unfinished work and
one next action. Link fact owners rather than copying transcripts. Omit secrets,
device identifiers and private reasoning; task files must stay out of public Git.

For denied, pending, failed or uncertain tools, use [bounded recovery](tooling-recovery.md).
Do not retry or route around a platform restriction. Reconcile newer receipts and
active ownership before resuming any saved action.

## Share rules across clients

[Global Codex](../templates/global-AGENTS.md), [global Claude](../templates/global-CLAUDE.md),
[workspace](../templates/android-root-AGENTS.md) and [component](../templates/component-AGENTS.md)
templates need verified local paths and deliberate merging into existing guidance.
Windows/WSL homes and credentials are separate. These files install no hooks,
tools, account memory or permissions.

CLAUDE.md imports shared entrypoints; `.claude/skills/` links the canonical
`.agents/skills/` bodies. Update the original. For client discovery/import/setup
details use [Claude setup](claude-code.md), not another copy of this protocol.
For a handoff, transfer sanitized task facts and establish the receiving owner;
do not claim native chat-history, credential or tool-access migration.

Discover tools in the active executor; PC browser, cloud browser, Windows and WSL
access differ. Markdown grants no access. Public findings go through
[maintenance](maintenance.md); only their decisive scope belongs in a fact owner.
