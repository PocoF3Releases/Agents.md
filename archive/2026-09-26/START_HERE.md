# Start here

Designed for GPT-6 Astra, GPT-5.6 Sol and other assistants with repository access only. No PC, WSL, phone, terminal or hidden memory is required to recover the recorded project state.

1. Read [agent rules](AGENTS.md) and [current state](CURRENT_STATE.md) at the chosen revision; reuse text only if it is still available in the current context. Recover missing sections after a model switch or compaction.
2. Pick **one** route below; read its durable record and linked evidence only.
3. For new code work, verify the relevant repository/branch using [source tracking](memory/repositories/TRACKED_HEADS.yaml). For a changelog, the published semantic baseline matters more than new commit timestamps.
4. If a task needs unavailable device/dump evidence, follow [remote workflow](REMOTE_WORKFLOW.md). Do not request the entire WSL checkout.

| Task | Read next |
| --- | --- |
| Next changelog | [Preparation](today/2026-09-24-changelog-preparation.md), [today-only delta](today/2026-09-24-changelog-delta-index.md), [published baseline](memory/android16-android17-release-state.md) |
| Dolby / AC-4 | [Durable audio](memory/dolby-audio.md), [AC-4/Parts evidence](today/2026-09-24-ac4-validation-and-thermal-dialog.md) |
| XiaomiParts / thermal dialog | [Parts](memory/xiaomiparts-device-ux.md), [accepted fix](today/2026-09-24-ac4-validation-and-thermal-dialog.md) |
| Camera (finalized; no planned work) | [Camera](memory/miuicamera.md), [final recording tests](today/2026-09-23-camera-video-validation.md) |
| Rootdir / device trees | [Workspace ownership](memory/device-tree-workspace.md), [rootdir evidence](today/2026-09-23-sm8250-rootdir-android17-modernization.md) |
| Kernel / boot | [Kernel](memory/kernel-frameworks.md), [boot capture conclusions](today/2026-09-23-latest-kernel-boot-verification.md) |
| NFC | [NFC](memory/nfc.md), [teardown fix](today/2026-09-22-nxp-nfc-teardown-regression.md) |
| Build flags | [Build optimization](memory/android-build-optimization.md) |
| repoindex / source indexing | [Tool guidance](memory/reference-indexes.md), [upgrade and safe migration](today/2026-09-24-repoindex-upgrade.md) |
| Source/dump availability | [Evidence index](EVIDENCE_INDEX.md), [reference guide](memory/reference-indexes.md) |
| Agent instructions / Astra-Sol compatibility | [Shared memory workflow and official sources](memory/agent-memory-workflow.md) |
| Requested model/session handoff | [Portable handoff template](templates/cross-model-handoff.md) |
| Save new findings | [Offload protocol](OFFLOAD_PROTOCOL.md) |

Other topics are routed in [INDEX.yaml](INDEX.yaml); use it as an alternative router, not an extra mandatory read. Imported snapshots, old rollback plans and contribution ledgers are historical reference, not a default reading list. Do not require a recursive tree count before answering a focused request.

## Copyable handoff

> Use PocoF3Releases/Agents.md on main. Read AGENTS.md, START_HERE.md and CURRENT_STATE.md, then only my task's route. You have repository access only; do not assume access to my PC/WSL/device. Use recorded evidence with its validation scope, verify relevant source when needed, and ask only for a specific missing artifact if it blocks a new conclusion. Use CURRENT_STATE.md and the release route for the published semantic cutoff. A repository read or commit does not synchronize account memory. After switching models or losing context, recover the relevant instructions and evidence; do not assume earlier reads or tool access survived.
