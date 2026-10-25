# Collect next-release history

Use `scripts/release_history.py` inside the existing Linux checkout. This tool
runs Git reads and optionally creates local retention refs under refs/changelog;
it never syncs, checks out code, builds, flashes or generates release prose.
Four lightweight snapshot workers avoid contending with the active ROM build.

## Current preparation

October 20 is the last published build, confirmed by the maintainer October 25.
Private working files live under `~/evo/.repo/changelog-next-20261025/`:

- baseline-20261020.json: 1,265 pinned projects from the contemporaneous saved
  October 20 post-migration manifest. Exact published ZIP-to-source identity
  remains unproven; do not relabel this as an artifact-extracted manifest.
- source-checkpoint-20261025.json: actual local heads and trees, including the
  four applied recovery overlays. This is a checkpoint during the rebuild.
- history-final-evidence.json: net source deltas and unpaired commit candidates.
- release-context.json: published baseline, previous-post hashes, artifact gap
  and an empty list of approved user-facing deltas. No next post is generated.
- review-decisions.json: known existing-backport/configuration topics are barred
  from being treated as new features; no changelog items are approved yet.
- README.txt: exact rerun commands and scope. Raw inventories remain private.

Both snapshots have local retention refs to survive history rewrites/GC. Existing
output files and retention refs cannot be silently replaced. Supply a new output
filename for a new checkpoint. No tags, public backup branches or ROM changes.

## Comparison and eligibility

Equal commit/tree projects are suppressed. Symmetric stable-patch comparison
removes equivalent cherry-picks and rebases; empty metadata commits are skipped.
A disposable isolated Git index also checks whether candidate patches already
exist in the baseline, without touching the checkout/index. Changes to files
with no remaining net delta and LFS storage-only configuration are excluded.
Candidate records include the final net diff summary. This is evidence collection,
not automatic semantic classification: adapted patches, partial squashes, merges,
reversions and previously announced behavior require final-diff review. A
candidate subject alone never establishes a new feature or runtime acceptance.

Before writing copy, review every candidate against the net diff, October 20
saved posts and the cumulative announced-topic ledger. The saved October 20
copy is a conservative topic reference; exact published Telegram text was not
independently supplied. Omit docs/tests/tooling, dropped
experiments, repeated recovery/Parts/Dolby features and message-only rewrites.
Group shared main/recovery copies once. Move only genuine, still-present
user-visible changes into the reviewed list; preserve per-feature test limits.

After the rebuild, retain its exact source manifest and ZIP hash, confirm input
heads did not move during compilation and reconcile the completed artifact with
the checkpoint. Do not call a current checkout snapshot the build's manifest.
Publication and device acceptance remain separate from successful collection.

Eight disposable checks passed: message rewrite, equivalent repick, real addition,
identical-tree squash, dirty-input rejection, ancestor revert/reapply, immutable
output and repository-storage-only changes. No Android build,
output cleanup or device operation was performed for this preparation.

The completed collection found 1,210 unchanged project heads, four unchanged
trees and 51 net-changed projects. Two baseline-present and 17 net-neutral
commits were suppressed in addition to patch-equivalent replays. A GMS delta
changes only LFS storage configuration. The remaining 179 commit candidates
are not 179 new features; semantic and artifact-inclusion review is still required.
