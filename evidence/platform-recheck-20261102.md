# Platform recheck — 2026-11-02

## Confirmed F2FS correction

Published and persistently installed:
[7285847](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7285847f4a2af70e52e7b41a22485307d6a018c9),
`f2fs: Initialize field sizes for legacy statistics attributes`.
One source line; no configuration, HAL, device-tree or ABI-layout change.

The CIP sized-access backport omitted `.size` in `F2FS_STAT_ATTR`. Its four
32-bit checkpoint/GC statistics therefore entered the wrong-type branch on
read, raising the filesystem error path and setting `SBI_NEED_FSCK` rather
than returning a count. The four attributes are registered on Alioth userdata.
The old phone nodes were checked for presence only, avoiding deliberate error
flagging on the live filesystem.

The missing initializer is present in the
[Android common stable backport](https://android.googlesource.com/kernel/common/+/e85a99db9ab85dfc30d93b0ca0e9156f3127f55a).
Yongpeng Yang's original authorship is preserved; the commit credits Sasha
Levin's legacy-macro adaptation. Other size-aware safeguards are retained,
instead of reverting the earlier correction or importing unrelated accounting
changes. Independent review confirmed the field types, registration and failure
path, with no blocking finding.

## Verification and installed identity

- Extracted actual helper/macro host tests, Clang Werror plus ASan/UBSan:
  old 20/20 failure-branch hits; fixed 20/20 correct values and no error-branch
  hits. Covers four fields and unsigned boundaries. The test substitutes a
  failure counter for kernel error handling; it is not 20 real filesystem marks.
- Affected W=1/Werror compilation and targeted Sparse passed without diagnostics;
  strict code-hunk checkpatch passed. Full production-config Image/modules/DTBs
  passed W=1 with compiler Werror. Existing unrelated kernel-doc warnings remain.
- Exact running version: `4.19.325-Redline-7285847-cip136`. Temporary boot passed
  before active-slot installation. Boot-partition hash equals the tested image;
  original Magisk ramdisk preserved, local original-boot backup verified.
- Phone: 100 reads across all four counters returned numeric values; five
  1-MiB generated-file copy/rename/checksum cycles passed, with no new critical
  kernel messages in the marked test window. All 19 PCM audio cases passed.
  Post-install reboot and counter checks passed; SELinux Enforcing, taint 0,
  mi_thermald running. Task staging removed; no wipe or settings reset.

Private source/build/runtime receipts: `~/evo/.repo/platform-recheck-20261102`.
Tests and logs are outside production kernel commits.

## Upstream triage and remaining work

Gerrit 509994's CMA bitmap guard was not imported: this tree already clears
`count` on both activation failures and rejects zero count before bitmap access.
The Dell-dock change requires unavailable hardware and was not imported.
Charging-bypass proposals 511471/511472 are pending analysis, not accepted
Alioth features; cmi measurements do not prove Alioth behavior, error handling
or charge-pump/thermal interactions. No bypass setting was enabled.

The [broader compatibility plan](kernel-contract-plan-20261102.md) remains
incomplete. Continue runtime-log/consumer review and legitimate stock/reference
backend correlation; retain external audio/cellular limits and skip the paused
boundary task. Donor GPU/Turnip experiments remain parked.

## Display policy checkpoint

Read-only phone verification closes the old “RRO needs next build” limitation.
Installed `android.overlay.device` APK hash equals the current build artifact:
`c44579703ab16d195cbce8a6729cf179f1a80fa7f88a89b6b3b2922a432bda54`.
Overlay lookup returns low-zone 120 Hz; DisplayDeviceConfig reports the expected
threshold 0.21259843 (legacy brightness 55) and ambient threshold -1. No
DeviceConfig or screen preference was changed. This establishes installed policy,
not a new optical comparison: manual 60/120 luminance mismatch remains unresolved.
