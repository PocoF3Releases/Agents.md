# Git and history conventions

## Commit scope

Use a descriptive repository/component subject, for example `sm8250-common: overlays: Remove obsolete Android 17 configuration`. For this knowledge repository, use `docs: <change>` or a similarly accurate tooling scope. Prefer one coherent commit over a sequence of incomplete intermediate states.

Preserve existing authorship and unrelated work. Use the maintainer's established author identity when the write tool supports author selection; otherwise disclose the connector-selected identity rather than claiming it was set.

## Attribution

Use the actual model and interface, not a copied historical example:

```text
Created using <actual model> via <actual interface>

Co-authored-by: codex <noreply@openai.com>
```

Include reasoning effort only when it is actually known; do not infer it from the model name. Use one AI co-author trailer, no trailing spaces, and no extra text after it. When the tool accepts a raw commit message, do not append a final newline after the trailer, matching the maintainer's formatting preference. This is a local convention, not a claim about GitHub's parser requirements.

## Safe delivery

Before writing, verify the destination branch and current parent. Preserve concurrent changes. Prefer a feature branch for a substantial rework; validate the relevant diff before merging. For atomic connector writes, build on the existing base tree, then update the ref without force. A commit object alone is not proof that a branch was updated.

History rewrites, force pushes, destructive resets and discarding local changes require explicit authorization for that operation. A general request to improve the repository does not authorize them. Do not prescribe `git reset --hard` as a routine synchronization step; inspect divergence and preserve local work first.

When an authorized squash/rewrite is appropriate, retain a reviewable final diff and upstream authorship. Generated vendor history should describe the final architecture, but do not rewrite it merely because old experiments exist.

## Evidence

Commit messages may include source/ABI rationale and the exact test scope. Distinguish source inspection, host tests and observed device results. Do not copy another session's validation claim or imply a ROM was rebuilt because documentation checks passed.
