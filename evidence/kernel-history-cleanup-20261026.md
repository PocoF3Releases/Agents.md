# Kernel feature consolidation and strict-warning restoration

Date: 2026-10-26. Source-checked and host-tested; build result recorded below.

## Correction

Removing fatal-warning flags is not a warning fix. The maintainer rejected that
approach. The production, generated-config and standalone-test warning-policy
commits were removed from the reconstructed history, rather than followed by
revert commits. Original `-Werror` settings and `CONFIG_CC_WERROR=y` are restored.
Runtime assertions and diagnostic warnings remain enabled.

## History integrity

The range after `360466aec8e4ed01c64a62d0d768108aa39737be` has 193 commits instead
of 244. Only the 137 maintainer-authored, Codex-coauthored changes were eligible;
these now form 86 feature commits. Consolidation stays within contiguous eligible
runs so protected upstream dependency points retain the exact same source trees.
All 107 protected commits retain byte-identical patches, original messages,
author/committer identities and dates. Ancestor rewrites necessarily change some
commit hashes. Imported authorship and attribution are retained.

Final source: [edb46ba39783](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/edb46ba397834c339d4341bb8664935c1fdcbf4b).
Its complete tree is `7c7b5da89267d3f962a20768b9d3b8c73ff94509`, exactly matching
the implementation checkpoint before the three warning-policy changes. No real
implementation was removed. No system-side source or thermal protection changed.
A local safety ref retains the original history. [Full source mapping](kernel-history-map-20261026.json)
distinguishes feature mappings from exact complete-tree equivalents; historical
runtime and build identities must not be relabeled as tests of a new intermediate
commit.

## Verification

Both retained JPEG regression programs pass under their restored fatal-warning
recipes: 4,503 change-base cases and 7,596 fence-map cases, including bounds,
sentinels and metadata assertions. The existing output configuration was reconciled
with olddefconfig; its only change was `CC_WERROR n -> y`.

Strict Image, module stage (MODPOST: zero configured modules), DTBs and fresh
exported-header validation all pass with checkout Clang 21. The three build logs
contain no compiler warning/error diagnostics. Actual scheduler compile commands
contain `-Werror`; both JPEG recipes contain `-Wall -Wextra -Werror`.
Image SHA-256: `e016262220cb160ce76aed8359961456c0da3048b334f566b018be39f4274010`.
The consolidated aosp-17 branch was pushed with the exact expected old-head lease;
the remote head was verified afterward.

The cumulative whitespace check retains one pre-existing line in the protected
luka177 backlight change; it was not silently edited as part of this own-history
cleanup. W=1/sparse auditing remains incomplete; a normal build is not a claim
that every optional diagnostic or architecture is warning-free. Previous phone
acceptance remains historical and scoped to its recorded source/artifact. No
phone image was replaced for a history rewrite and warning-severity restoration.
