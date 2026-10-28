# Redline kernel identity — October 28, 2026

## Published source

[Redline branding](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6b3cb6eb71683641de1fb4cdfd9c8e2dcca183ee)
contains only the version script and shared Xiaomi identity fragment.
[Generated configurations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1e45b8cc1cbb9229a464395b5a8e12d8b4bc349c)
are a separate commit produced by `scripts/update_defconfig -j 4`.
The repository URL and branch remain
`PocoF3Releases/kernel_xiaomi_sm8250`, `aosp-17`. GitHub About identifies
Redline, Xiaomi SM8250 and Linux 4.19 CIP;
the upstream homepage is retained.

The real `kernelrelease` target produces:

```text
4.19.325-Redline-1e45b8c-cip136
```

The seven hexadecimal characters identify the actual build source. They are not
a hard-coded release label. The maintained `localversion-cip` value is appended
after that ID; `localversion-st` remains in source for upstream provenance but
is omitted from the displayed release. Neither upstream metadata file nor any
CIP/ST implementation is removed. Explicit Android/KMI arguments, saved SCM
archives, dirty markers and automatic-SCM opt-out behavior retain their roles.
Exact Git tags retain source identification for automatic-SCM builds.

The common Xiaomi fragment supplies `CONFIG_LOCALVERSION="-Redline"`. All twelve
configurations were regenerated with `scripts/update_defconfig -j 4`; every
other generated-config line is identical. Alioth's freshly resolved configuration
differs from the installed production configuration only in LOCALVERSION.
Makefile `NAME = "People's Front"` and the root README remain byte-identical
to the pre-branding base. Local Git abbreviation is seven characters; actual
object IDs and immutable links retain their full identity.

## Verification and deployment boundary

Shell syntax, **14 private version regressions** and the actual kernelrelease
target pass with the checkout toolchain. Cases cover clean/dirty Git, differing
core.abbrev settings, tags, Android/KMI arguments, automatic-SCM opt-out, saved
SCM exports, absent CIP metadata, build-path spaces and localversion extensions.
The version script is byte-identical to that fourteen-case tested blob;
regeneration, commit boundaries and kernelrelease were rechecked after the split.
Source whitespace checks pass. Strict checkpatch has only the existing
coauthor/missing-human-DCO metadata findings; no certification was invented.
No tests or generated verification output enter kernel history.

**No full branded Image was built or flashed in this update.** The phone keeps
its [previously accepted main kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1efb0bf8d7a52abc450285c470bb34c28ad57dfd),
whose strict W=1/Werror and enforcing phone coverage is recorded in the
[sparse acceptance](kernel-sparse-errors-20261028.md). The new name appears on
the next rebuild/install. System-side sources and runtime C/assembly behavior,
security/debug settings and thermal protection are unchanged by branding.

## Deferred diagnostics

The [review backlog](kernel-sparse-backlog-20261028.md) preserves **all 2,954
remaining sparse warnings** at that accepted source, including exact locations,
source permalinks and emitted type context. All remain unreviewed; no automatic
waiver, sparse-clean claim or additional fix is implied. No new sparse count or
kernel-doc audit is claimed for this identity-only commit.

Private commands, fixtures, configuration diffs and GitHub metadata readback are
retained under `~/evo/.repo/kernel-redline-20261028/`. Corrected history,
regeneration and final identity receipts are in
`~/evo/.repo/kernel-redline-correction-20261028/`.
