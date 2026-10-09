# Maintain the workhub

## One owner per fact

| Information | Owner |
| --- | --- |
| Enduring rules | [AGENTS.md](../AGENTS.md) |
| Current state/routing | [CURRENT_STATE.md](../CURRENT_STATE.md) |
| Technical behavior/constraints | One [memory/](../memory/) topic |
| Refs/checkout divergence | [state/repositories.yaml](../state/repositories.yaml) |
| Acceptance scope | Stable `V-*` entry in [validation](../state/validation.md) |
| Published/candidate changes | [state/releases.md](../state/releases.md) |
| Decisive diagnostics | Linked [evidence](../evidence/) record |
| Discovery | [INDEX.yaml](../INDEX.yaml) |

Update owners, not session diaries. Link historical records rather than duplicating
technical explanations. Imported drafts/old next steps are not assignments.

Track heads only for PocoF3Releases and maintainer-owned sources/tools. Do not add
upstream dependencies or retired forks to the repository ledger. Keep necessary
integration evidence in its topic owner without an ongoing upstream head inventory.

## Record a change

Keep observation date, repo/branch/source identity, failure/final behavior,
symbols/artifact hashes, validation and limits. Use [the template](../templates/record.md)
only for a separate handoff/complex finding. Retain useful rejected approaches
with reasons and replacements; remove obsolete active guidance.

Labels: `source-checked`, `build-tested`, `host-tested`, `device-tested`,
`user-confirmed`, `historical`, `unverified`. They can combine; none implies
another. Distinguish temporary deployment from packaged/flashed inclusion.
Rewritten-away commits are historical, not current targets; verify remote refs
before publication.

For readers without PC access, provide public sources and sanitized evidence.
Local paths identify missing material, not access. Request only artifacts needed
for the task; copied notes do not synchronize account memory.

## Git and privacy

Preserve unrelated work and upstream authorship. Use a component-scoped subject,
factual body and actual validation. Assistant edits use this trailer:

```text
Co-authored-by: codex <noreply@openai.com>
```

Use public project identity/noreply attribution; no invented model identity or
AI trailers on untouched upstream imports. Follow requested commit/push scope and
verify the remote ref. Authorized history rewrites require a recovery copy and
explicit expected-head `--force-with-lease`; saved heads alone justify no rewrite.

Publish no credentials, keys, contact/payment data, device serials, environment
dumps or unrelated client-memory exports. Use `~/` paths. Retain public URLs and
proprietary-source references; keep raw dumps/videos/logs private and publish only
necessary sanitized excerpts with identity/scope. [Privacy boundary](../archive/PRIVACY.md).

## Local checks

```bash
python3 scripts/check.py
# Structural diagnostics only:
python3 scripts/validate_knowledge.py --json
```

The full check runs structural validation, disposable fixtures and Git whitespace
checks; no network/model/device calls or GitHub Actions. Fix relevant failures,
rerun affected checks and avoid unrelated builds or repeating checks after a
prose-only response.

Use UTF-8 without BOM, LF, plain headings, matched fences, relative links, unique
YAML keys and quoted dates. Preserve stable anchors. Archive previous logs only when useful; the maintained
archive is currently an empty skeleton.
Format C/C++ with its own clang-format config, not Markdown/YAML.

Validation covers links/anchors, routing, archive integrity, repository identities,
common sensitive patterns and context budgets; it cannot certify external URLs,
technical truth, all secrets, runtime behavior or actual tokens. Optional:
[model guidance](../references/openai-guidance.md), [retrieval checks](../references/cold-start-checks.md).
