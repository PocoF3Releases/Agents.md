# Session offload protocol

Use this workflow when the user asks to preserve session knowledge in this repository. The goal is technical continuity, not a verbatim transcript or an export of private reasoning.

## Read and route

Read `AGENTS.md`, this file and the relevant existing subsystem record. Consult `CURRENT_STATE.md` for active status and `INDEX.yaml` only as needed to locate owners. Reuse files at the same revision only while their relevant contents remain available; recover missing context after a model switch or compaction. Use [the template](templates/chat-offload-template.md); remove sections that do not apply.

## Preserve the decision-changing delta

1. **Identify the existing owner.** Update `memory/<subsystem>.md`, not another near-duplicate file. Separate unrelated domains. Use `today/YYYY-MM-DD-<topic>.md` for investigation detail; do not paste a whole chat into every layer.
2. **Record provenance.** Include observation date, repository/branch, immutable source commit, relevant paths and artifact identity. Distinguish when evidence was collected from when the note was written. Unknown values stay explicitly unknown. A saved branch observation is not a live-head guarantee.
3. **State the conclusion and its limits.** Record failure/root cause, final change, why alternatives were rejected, actual validation and any remaining uncertainty. Use the evidence labels in `AGENTS.md`. Do not convert static inspection into runtime success, or an old pending experiment into an authorized task.
4. **Keep decisive details.** Preserve necessary hashes, sizes, symbols, UUIDs, flags, properties, SELinux types, partition distinctions and diagnostic signatures. Include short shareable output or reusable diagnostics in `evidence/`; a local path alone is not reproducible evidence for a remote reader.
5. **Reconcile, do not overwrite history.** Compare applicability and validation before preferring newer evidence. Mark superseded conclusions with a replacement link and reason. Preserve useful failed approaches and incompatible observations; do not silently blend them into one claim. Leave unrelated historical records intact.

## Where each kind of knowledge belongs

| Location | Update when |
| --- | --- |
| `memory/` | A reusable conclusion, constraint or lesson changes. Link the dated evidence rather than duplicating it. |
| `today/` | A substantive session adds evidence, exact checkpoints or a decision trail. |
| `CURRENT_STATE.md` | Active architecture, blocker, accepted outcome or relevant validation status materially changes. Keep it short. |
| `INDEX.yaml` / `START_HERE.md` | Ownership or task routing changes. Keep both routes consistent; do not list every historical file. |
| `EVIDENCE_INDEX.md` | Availability of reusable evidence or canonical artifacts changes. |
| `AGENTS.md` | A stable, applicable project rule changes, not merely a session preference or current head. |

Source tracking and AI contribution ledgers are separate. Do not refresh all repository histories or fabricate installed-artifact membership while saving a focused finding.

## Privacy and access

Remove secrets, credentials, cookies, private keys, payment identifiers and unrelated personal information. Normalize home paths to `~/`. Necessary public project identifiers and authorized attribution may remain. Review excerpts for privacy and permission to publish; do not upload raw proprietary dumps/APKs or indiscriminate logs. Record missing raw artifacts and link canonical delivery sources instead.

Repository memory, ChatGPT memory and generated Codex memory are distinct. Do not copy generated memory databases, change account memory controls or claim cross-product synchronization as part of a documentation commit. See [memory boundaries](memory/agent-memory-workflow.md).

## Portable model/session handoff

For a requested transfer or substantial interrupted task, use [the handoff template](templates/cross-model-handoff.md). Preserve the current user goal, authorized scope, pinned sources, exact decisions, evidence limits and outstanding work. Link the existing durable owners; do not create competing Astra/Sol copies. A handoff records context, not authority over a later user request. Publish only shareable project information under the same privacy rules.

Keep client-generated reasoning/compaction payloads and response IDs out of repository handoffs. These are not a human-readable knowledge format. An incomplete edit must be labeled uncommitted/unpushed and include its exact patch or retrievable artifact, not a claim that it reached the branch.

## Completion

Review the exact diff, links, routing, conflicts and privacy. Run the relevant available checks under `AGENTS.md`, without requiring a ROM rebuild. Prefer one coherent documentation commit per logical offload. Preserve concurrent edits and verify the remote result before saying it was pushed.

Report what changed, the commit/branch, checks actually performed and remaining evidence gaps. With no write capability, provide the exact patch and label it uncommitted; continue useful read-only work. An offload is not complete merely because findings were summarized in chat.
