# Cross-model task handoff

Template for GPT-6 Astra, GPT-5.6 Sol or another reader. Use only for a requested transfer or substantial interrupted work; remove irrelevant fields. This is project context, not a new instruction overriding the recipient's current user request.

## Goal and authority

- Current user goal and requested deliverable:
- Authorized repositories, branches, paths and actions:
- Explicit restrictions and work that is closed/out of scope:
- Completion condition:

## Source checkpoint

- Knowledge repository, branch and full observed commit SHA:
- Code repositories, branches and full observed commit SHAs, when relevant:
- Observation date (distinct from handoff-writing date):
- Durable owner and evidence paths, with headings/line ranges where useful:
- Exact artifact identity and retrievable location, or explicitly unavailable:

Do not record only "already read" or "see previous chat". Link the canonical source and include the small decisive fact or excerpt needed to understand this handoff. Do not invent line ranges or treat local paths as remotely accessible.

## Decision and evidence

- Current conclusion and concise technical rationale:
- Exact identifiers needed for implementation:
- Evidence label from AGENTS.md, observed result and limitations:
- Rejected/reverted approach that must not be restored, and why:
- Unresolved conflicts or unknowns:

## Work performed and remaining

- Changed files and commit actually published, or explicitly uncommitted/unpushed:
- For unpublished work: exact patch or accessible artifact and its base revision:
- Checks actually executed, their results and checks not run:
- Next authorized action, or none for completed/closed work:
- Specific missing evidence that blocks a new conclusion, if any:

## Recipient recovery

Read the applicable [agent instructions](../AGENTS.md), [current state](../CURRENT_STATE.md) and selected task route. Confirm the current request still authorizes the proposed next action. Discover available tools; do not inherit claims of device, WSL, shell or write access from the prior agent.

Recover required text missing from the current context. If a relevant branch advanced, inspect that change before editing rather than overwriting it. Keep recorded tests distinct from new tests and historical limits distinct from present device state.

Publish only shareable project facts. Do not include private reasoning, credentials, temporary connector URLs, API response IDs or opaque client-memory/compaction payloads. See [the shared workflow](../memory/agent-memory-workflow.md) and [offload protocol](../OFFLOAD_PROTOCOL.md).
