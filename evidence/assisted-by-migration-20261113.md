# AI attribution and canonical-history integrity — 2026-11-13

Fork-local assisted commits use exactly one `Assisted-by: LLM - GPT-6.1 Sol Max`
trailer. Older model-creation footers are removed from our local changes.
Canonical upstream objects keep their original messages and IDs, including
already-merged assistance credits; those objects must never be relabelled.

## Complete history check

The saved original and first rewritten graphs were compared for all 50 maintained
repositories and 105 published branches. Exact reachable-set bijections,
ordered parent mappings, raw human identities/dates and code trees show no lost
commits. Three explicit documentation/reference updates were accounted separately.
Protected private signing-key and decompiled-camera repositories remain excluded.

The attribution rewrite incorrectly changed 417 shared canonical objects:
nine in AV and 408 in framework base. Restoring their original objects repairs
canonical ancestry. The 180 owned/fork-local AI-creation footers are cleaned;
four accepted upstream credits retain their original upstream messages.

## Current framework integration

[6f165815e06c](https://github.com/PocoF3Releases/frameworks_av/commit/6f165815e06ce56875cc41e22d499047db48f691)
is based on EvoX `80917b1522f1eb87b9d8d2bdc143d17b9e9d787b`, with six retained
feature commits and the new upstream Bluetooth codec-preservation fix.

[5dec056e50a8](https://github.com/PocoF3Releases/frameworks_base/commit/5dec056e50a89199c4320161f197e6a856607509)
is based on EvoX `31ed74aff113fe73828829c44a73032d48530b2e`, with eleven retained
feature commits and twelve new upstream commits. Every retained feature patch ID
matches its original; whole-series merge composition gives the same final trees.
Both candidates have zero commits behind their selected canonical upstream.

## Acceptance boundaries

These are source, Git-graph and host checks. No new Android build, installclean,
flash or device test is claimed. The thirteen genuine upstream changes alter
the complete framework trees. Historical build/phone evidence keeps its original
source IDs and artifact hashes; those results do not certify the refreshed base.
Historical links are remapped only when the complete code tree stays identical.
The routing ledger points to the current candidates.

Authored recovery overlays are replayed and checked with the mail-patch preflight.
Tracking-branch manifests retain their source selections. Original refs, full
old/new object maps, graph proofs and detailed regressions remain private.
Publication requires frozen target OIDs, exact expected-head leases and remote
read-back. Existing local work is preserved; parked investigations stay parked.

Observed kernel-version literals remain `4.19.325-Redline-2f2467b-cip136` and
`4.19.325-Redline-cd1f8df-cip136` in their original dated evidence. No renamed
commit alias is substituted into a version string from a tested binary.
