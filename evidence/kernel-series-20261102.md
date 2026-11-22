# Kernel series consolidation — 2026-11-02

`history-verified`, `tree-equivalent`, `build-tested`. User requested fewer,
higher-quality commits after the [documentation removal/topic pass](kernel-history-20261102.md).

Follow-up source repair and broader checks: [W=123 audit](kernel-w123-20261102.md).

## Published result

`89aca84b51ad0d68997d344cc159788edeace578`
on `aosp-17` reduces **880 → 751 custom commits** (129 fewer). The shared
Qualcomm base and original 158-commit vendor foundation remain intact. No code,
comment, configuration, file mode or artifact was added/removed from the source
tree; its Git tree is exactly `0536e2fa8b87e8f5a29163e13289cab8102efd98`, identical to the prior head.
The documentation removed in the preceding pass remains removed.

There are 53 focused consolidations and nine clearer standalone messages. The
new descriptions explain final behavior, not intermediate work or generic
“finalize” stages. Examples: QCE engine/clock teardown, MTP transfer validation,
CVP ioctl/poll/MMIO ownership, CNSS interface contracts, CS35L41 calibration and
WALT/RCU consumer contracts. Mechanical helper/declaration cleanups stay within
their subsystem. Largest consolidated diff: 363 changed lines/seven files (CVP);
all others are smaller. No consolidated patch exceeds sixteen files.

Independent runtime fixes, external authors’ patches and original upstream
certification/origin metadata stay separate. In particular, protected interface
transitions remain ordering barriers; independent display/thermal/audio bugs
and generated configuration/source-fragment boundaries were not bulk-squashed.
The topic blocks from the previous pass remain in place.

## Verification

- All 722 development changes map to 593 commits above the unchanged foundation.
  No empty or unaccounted commit. [Complete map](kernel-series-20261102.json).
- All 540 remaining standalone patches have byte-identical diffs. Of these,
  531 also have identical messages; the other nine are explicitly reworded
  Codex-owned messages. Author/committer identity and date fields are preserved
  for standalone patches, including all 155 protected non-owned/imported ones.
- Consolidation is limited to the same original author identity with existing
  Codex attribution. Author metadata comes from the first member and committer
  metadata from the last. Existing additional attribution is retained; no human
  sign-off/review certification was invented or assigned to unrelated changes.
- All recorded same-file, upstream-order and protected interface dependency
  edges pass after ordering/grouping. The final Git tree is byte-identical,
  which includes every generated defconfig and all build/version scripts.
- The exact-tree prior full W=1/Werror compile remains applicable. The private
  incremental `W=1 KCFLAGS=-Werror Image` target also passed for the final source
  ID with zero compiler diagnostics. Existing kernel-doc reports remain; no
  warning flags or checks were suppressed. No ROM build/installclean/device test.
- GitHub recognizes the Codex co-author on all 509 remaining attributed commits.
  Fork-local trailer endings were checked without rewriting shared upstream.
- The kernel release is `4.19.325-Redline-89aca84-cip136`. Generated SCM/version metadata
  naturally changes; this is not a binary-identical Image claim.

Final Image SHA-256: `fc78f110640a89caa470d253522901cdea4feb3fb2e83dfa19c387c5ce769623`.
Resolved config SHA-256: `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`.

## Publication and recovery

Force-pushed with exact expected old tip `e26284f541876a3f3f9611740db500f00c7f3aea`
and verified the remote head. The backup ref is
`refs/backup/kernel-consolidate-20261102/original`; its custom-history bundle is
verified. Private plan, dependencies, merge descriptions, preservation receipts
and logs are in `~/evo/.repo/kernel-consolidate-20261102/`.

The earlier full-build Image was saved before the private output was reused.
ROM output, system-side sources, device trees, recovery patches and the phone
were not changed. The sparse backlog and earlier phone tests keep their
historical identities and limits; they were not rerun or relabelled as current.
