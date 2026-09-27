# Astra-Sol knowledge compatibility — 2026-09-26

## Scope and provenance

User-requested follow-up to support GPT-5.6 Sol alongside GPT-6 Astra in `PocoF3Releases/Agents.md`. Starting branch: `main`; observed parent: `6dba4ebe760ec244e4109e23e9ba0f4273e0827a`; base tree: `ba7be8906d8a064b214316593803056261c659cd`.

Official documentation was searched and read on September 26, 2026. The [shared guide](../memory/agent-memory-workflow.md) links the model-specific GPT-5.6 guidance, Sol model page, Astra prompting article, ChatGPT product guide, Codex instruction/memory guidance and API compaction documentation. This extends the [earlier review](2026-09-26-agent-memory-guidance-review.md); that record remains historical evidence of its own checks.

## Findings and changes

Both model families' official guidance supports lean instructions. Sol support does not justify restoring an always-read archive, repeated rules or rigid recipes for Astra. A concrete gap in the prior instructions was the unconditional prohibition on rereading an already-read revision: after a model/client switch or context loss, necessary text may no longer be available.

The shared instructions now permit targeted recovery of missing context while retaining same-revision reuse when the content is actually available. Model names no longer imply tools, local/device access or chosen reasoning settings.

The durable guide documents one readable data format for both models, optional task scaffolding, stable schema/path ownership, actual-access-dependent execution and the boundary between portable project facts and opaque client/API state. It does not claim that encrypted reasoning or compaction payloads can be moved between models.

[The handoff template](../templates/cross-model-handoff.md) preserves authorized scope, immutable source identities, decisions, evidence labels, unpublished patches and remaining work. [Eight optional replay cases](../templates/model-compatibility-checks.md) define comparable observable behavior; they are not mandatory startup steps and have not been run against both models.

`INDEX.yaml` keeps schema version 1 and adds ordinary path entrypoints plus descriptive compatibility metadata to the existing `agent_memory` route. No parallel model-owned knowledge store, vector database, embeddings job, generated-memory import or API configuration was introduced.

## Validation

The unchanged repository validator, Git blob `56c7a2ca0db88d09c2fe53b243b001d82bf92766`, was reconstructed from the previously fetched source and hash-verified before execution. The six modified documents' original contents were likewise verified against remote blob hashes before editing.

The host check uses complete candidate governance text and a bounded inventory of paths established by pinned connector metadata. It checks route/link target existence, duplicate YAML keys, schema shape and the root instruction budget; it does not imply all unchanged target contents were reread. Parsed comparison preserves the normal read order, every non-agent-memory subsystem mapping and the full maintenance mapping. Exact changed-file scope and whitespace were reviewed separately.

Result: **PASS, 115 local references**, using 60 recorded metadata paths plus three locally present new files. Root `AGENTS.md` is 5,292 UTF-8 bytes, below the project 8 KiB guardrail. This is not a model context-window or performance measurement.

To repeat in a complete checkout:

```sh
python3 scripts/validate_knowledge.py templates/cross-model-handoff.md templates/model-compatibility-checks.md today/2026-09-26-astra-sol-compatibility.md
```

Python validation results are static compatibility evidence only. The validator and its unit tests are not modified; its prior 22-test result belongs to the earlier review and is not presented as a new test run here. No Sol/Astra paired inference evaluation, token/latency benchmark, ROM build, device test or GitHub Actions run was performed. Container DNS prevented a clone; source reads and publication use the connector, and local checks use a reconstructed partial snapshot rather than a full checkout.

## Preserved state

No changes to `CURRENT_STATE.md`, accepted runtime evidence, camera closure, recorded source heads, release baseline, Git attribution conventions or historical archives. No client model selection, thinking setting, account memory or Codex store was changed. Compatibility is guidance-reviewed and statically checked, not empirically certified across all model/client combinations.
