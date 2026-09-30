# Maintain the workhub

## One owner per fact

| Information | Owner |
| --- | --- |
| Enduring project rules | `AGENTS.md` |
| Material current state and task routing | `CURRENT_STATE.md` |
| Technical behavior, root cause, constraints | One `memory/` topic |
| Public refs and observed checkout divergence | `state/repositories.yaml` |
| Acceptance scope | Stable `V-*` entry in `state/validation.md` |
| Published baseline / unannounced candidates | `state/releases.md` |
| Detailed decisive output | A small linked `evidence/<topic>/` record |
| Task discovery | `INDEX.yaml` |

Update owners in place. Do not create session diaries or duplicate the same
technical explanation in state, evidence and index. Keep historical details in
the sanitized archive; link only the relevant record. A draft or old next step
never becomes an active assignment by being imported.

## Record a change

Capture observation date, repo/branch/source identity, failure, final behavior,
relevant symbols/artifact hashes, actual validation and remaining limits.
Use [the record template](../templates/record.md) only when a separate handoff or
complex finding needs it. Preserve useful rejected approaches with the reason
and replacement; remove obsolete guidance from the active topic.

Use these labels consistently: `source-checked`, `build-tested`, `host-tested`,
`device-tested`, `user-confirmed`, `historical`, `unverified`. Labels combine;
none implies another. Record a temporary deployment separately from packaged
and flashed inclusion. Commit IDs rewritten away remain historical evidence,
not current checkout targets. Recheck relevant remote refs before publication.

For a chat without PC access, include enough public source and sanitized evidence
to explain the conclusion. A local path identifies missing material, not access.
Ask for the smallest missing artifact only if the task depends on it. Do not
claim that copied notes synchronize ChatGPT/Codex account memory.

## Git and privacy

Preserve unrelated work and upstream authorship. Use a component-scoped subject,
a factual body and actual validation. For actual assistant edits use:

```text
Co-authored-by: codex <noreply@openai.com>
```

Use the public project identity and noreply Git attribution. Do not invent a
model identity or add AI trailers to untouched upstream imports. Follow the
current request's commit/push scope; verify the resulting remote ref. When a
history rewrite is explicitly authorized, preserve a recovery copy and use an
explicit expected-head `--force-with-lease`. Do not rewrite history merely to
update this database's saved heads.

Publish no credentials, private keys, personal contact/payment data, device
serials, raw environment dumps or unrelated client-memory exports. Normalize
home paths to `~/`. Public project URLs and proprietary-source references stay.
Keep raw dumps, videos and verbose logs private; publish only necessary sanitized
excerpts with identity and scope. [Historical privacy boundary](../archive/PRIVACY.md).

## Local checks

```bash
python3 scripts/check.py
python3 scripts/validate_knowledge.py --json
```

The full check runs structural validation, disposable fixture tests and Git
whitespace checks. It performs no network/model/device calls and requires no
GitHub Actions. Repair relevant failures and rerun affected checks; avoid
unrelated ROM builds or repeating checks after a prose-only final response.

Use UTF-8 without BOM, LF, plain headings, matching fenced code, relative links,
unique YAML keys and quoted dates. Keep stable validation anchors. Format C/C++
with its own clang-format config; clang-format does not format this Markdown/YAML.
Do not alter frozen archive content during routine maintenance.

The validator checks active local links/anchors, routing, archive integrity,
repository identities, common sensitive-data patterns and context byte budgets.
It does not certify external URLs, technical truth, all secret formats, runtime
behavior or actual token use. [Model guidance](../references/openai-guidance.md)
and [retrieval checks](../references/cold-start-checks.md) are optional references.
