# <Topic> — evidence record (<YYYY-MM-DD>)

Template only: replace placeholders and omit irrelevant sections. Do not manufacture a pending task to fill a heading.

## Scope and provenance

- Written on:
- Evidence observed on:
- Device / target / Android branch, if applicable:
- Owning repository and branch:
- Immutable source commit and relevant paths:
- Input artifacts, hashes and availability:
- Durable owner (repository-relative path):
- Supersedes / conflicts with (path and reason, or none):

## Conclusion

Describe the final decision, its applicability and what remains unknown. State whether work is active, completed or closed; an old pending item is not new authorization.

## Change and rationale

- Failure and root cause:
- Final change, paths and commit:
- Exact technical identifiers needed for reuse:
- Rejected alternative, reason and replacement:

## Evidence and validation

| Claim | Evidence label | Source / command / result | Limits |
| --- | --- | --- | --- |
| <claim> | <source-checked / host-tested / agent-observed-runtime / user-confirmed / untested / historical> | <precise reference> | <what this does not prove> |

Include short shareable decisive output, artifact SHA-256/size, partition distinctions or dependency/call-flow notes when relevant. Preserve original observation dates; distinguish recorded tests from this session's tests.

## Continuation, only when applicable

State the next authorized action or the smallest missing evidence needed. Use `none` for closed work; do not invent a test campaign or require a rebuild by default.

## Repository maintenance

- Updated durable owner:
- Current-state change, or not applicable:
- Routing/evidence availability change, or not applicable:
- Validation actually performed:
- Unperformed checks and limitations:

## Publication review

Confirm that secrets and unrelated personal information were removed, home paths normalized, and excerpts are permitted to be shared. Keep raw proprietary dumps and generated client-memory stores out. Record the resulting commit separately after publication; do not invent a self-referential commit SHA.
