# Agent memory guidance review — 2026-09-26

## Scope and provenance

User-authorized governance and memory-access review of `PocoF3Releases/Agents.md`, observed from `main` at `f9424ece94c63fd003932f11af0b0242f1c0830d` (root tree `2ad8b00c30bc0002b6cb0210a870e77cc155a1e7`). Official OpenAI sources were checked on September 26, 2026 and are linked with their applicable guidance in [the durable workflow](../memory/agent-memory-workflow.md).

Review covered root instructions, startup/current-state routing, offload/remote workflows, reference-index guidance, Git conventions and the offload template. Repository tree metadata was used for route existence checks. It was not a reread of every historical archive, binary or downstream Android repository.

## Findings and final changes

The existing durable/detailed split was retained. Its main problems were an optional-versus-mandatory INDEX.yaml contradiction, repeated startup reads, fixed old-model attribution, insufficient distinction between generated memory and committed instructions, and no executable governance validator.

- AGENTS.md now makes instruction/data trust boundaries, revision reuse and task-sized validation explicit. Release details remain owned by CURRENT_STATE.md instead of being duplicated in the instruction file.
- START_HERE.md, README.md and INDEX.yaml route agent-memory work to one durable guide. Existing subsystem mappings, observed heads and maintenance policies remain unchanged; the router's new date does not claim refreshed device tests or source heads.
- OFFLOAD_PROTOCOL.md and its template preserve provenance, exact identifiers, rejected approaches, supersession and limits without requiring a transcript or redundant state updates.
- Git guidance uses actual model/interface attribution, preserves author/tool limitations and requires explicit authorization for destructive history operations.
- A network-free validator and isolated regression tests cover routing, duplicate YAML keys, local links and instruction size. Generated local memory/authentication files are ignored without blocking a future committed `.codex/config.toml`.

The directory layout and 8 KiB root-file budget are project engineering choices, not an official OpenAI memory schema or a measured model-speed improvement.

## Validation evidence

**Host-tested:** 22 isolated Python unit tests passed, covering valid/malformed indexes, duplicate keys, optional routing, missing targets, path traversal, symlink escape, external links, code-fence exclusions, reference links, UTF-8 size, additional files and connector inventory/candidate handling.

**Source-checked:** Reconstructed original START_HERE.md and INDEX.yaml were verified against GitHub blob hashes `6470fdb9aa1caf98de26c2adfdc9a3c37f96c564` and `a1424a8288c6a865953b2f110b41fe06bac43e39`. Parsed comparison preserved every pre-existing subsystem mapping and the complete maintenance mapping.

The candidate governance files, this evidence record and INDEX.yaml were checked against a pinned 70-path metadata inventory plus five locally present new candidate files. This proves checked target existence within that inventory, not review of unchanged target contents. Whitespace and exact candidate file scope were checked separately.

Reproduction in a complete checkout:

```sh
python3 scripts/validate_knowledge.py today/2026-09-26-agent-memory-guidance-review.md
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The review environment had Python and PyYAML 6.0.3, but container DNS could not resolve GitHub for a clone. Repository reads and publication therefore use the GitHub connector; local validation uses fetched/reconstructed text and verified metadata, not a claimed full Git checkout. No GitHub Actions run, ROM build, device test or model-behavior benchmark is claimed.

## Preserved state and limits

CURRENT_STATE.md, source-head snapshots, camera closure, accepted runtime records, release evidence and historical archives are unchanged. Camera remains finalized with no planned work, and this change does not publish a ROM changelog or reopen a test campaign.

No ChatGPT account memory, generated Codex store, local source index or client configuration was synchronized or modified. Existing historical prose is not wholesale rewritten; current routing governs its use. External URL/anchor checking, privacy review and technical claim validation are outside the automated checker's guarantee.
