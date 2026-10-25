# Validation register

Date source/build/runtime evidence.

## V-HAPTICS

**2026-10-04 — source/build/host/device-tested, scoped.** That HAL candidate
passed 21/21 predefined effect/strength gain checks (48/80/128), three supported
stock primitives, timed amplitude and cancellation under enforcing SELinux.
AAC native/limited-HE1 rendering and bounded PCM refills passed isolated tests.
Temporary mount restored; no permanent/full RichTap acceptance; app-facing RichTap unverified.
No PWLE/unsupported primitives. October 8 LOW_TICK fallback has commit-reported
temporary tests; installed identity is unknown. September 30 user acceptance is historical.
[Exact scope and restoration](../evidence/haptics/2026-10-04.md).

## V-AC4

**2026-09-24 — device-tested and user-confirmed.** Non-root A17 user build;
explicit `OMX.dolby.ac4.decoder`, official 32-second stereo/48 kHz sample:
800 inputs, 800 output buffers, **6144000 PCM bytes**, 5970795 nonzero,
EOS/PASS, `audio/raw`, two channels, pcm-encoding=2. The diagnostic was silent;
user separately confirmed audible playback in an unidentified player.
Opt-in on/off and 32/64-bit syntax checks were recorded. This validates that
stream, not all presentations, multichannel/offload, apps or Dolby processing.
[Diagnostic](../evidence/ac4/README.md) · [full ABI/failure progression](../memory/dolby-audio.md).

## V-PARTS

**2026-09-24 — source-checked and user-confirmed.** Common [3c30e7d](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/3c30e7d416cd91e51c1c95ce81d55b20e60c570c) System
Profile dialog correction was approved visually; earlier [db27251](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/db2725133559f011a1565663bb11de076790d73b) was
insufficient. Shared per-app implementation is not a separate visual test.
[Exact record](../memory/dolby-audio.md).

## V-UI

**2026-09-24 — source-checked and pushed.** Common [e0fd9ba](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/e0fd9bac1fa69915345f91a41257a4119e479b70) removes duplicate
MiSound titles; hardware [59188cf](https://github.com/PocoF3Releases/hardware_xiaomi/commit/59188cfbdba67b63ecf1882cf6bba94cf33cf35a) restores reset buttons and current-locale
profile labels. Resource/API/diff checks passed; no build/device test in those
turns. Dolby README [3b8b33e](https://github.com/PocoF3Releases/hardware_xiaomi/commit/3b8b33ec182663b992cc4234c72a72fadf193a43) was documentation-only.

## V-TOUCH

**September 28 — recorded source/host checks.** Supported touch controls,
translations, hardware-write/lifecycle guards and blob/kernel inspection passed
scoped checks; not full A17 UI acceptance. [Scope](../memory/xiaomiparts-device-ux.md).

## V-PROXIMITY

**Recorded temporary device test and user confirmation.** Alioth the recorded candidate
MIUS timeout correction stopped the observed idle error and delivered 0/5 cm
near/far events. User reported proximity working during a call. This does not
cover every call app/device; production uses the extraction/blob fix without
root. [Guard and ownership](../memory/xiaomiparts-device-ux.md#alioth-ultrasound-proximity).

## V-CAMERA

**2026-09-23 — device tests and host packaging; finalized September 24.**
[Camera](../memory/miuicamera.md) owns accepted APK identity and limitations.
Apktool 3.0.3 and 16 KiB zipalign check passed. Temporary APK mount matched hash;
no ROM build/flash, settings restored, installed CHI hash unchanged.

| Clip suffix | Mode | Output |
| --- | --- | --- |
| 172458 | Main 4K30 | 3840×2160, ~30.03 fps |
| 172540 | Main 4K60 | 3840×2160, ~60.04 fps |
| 172705 | Ultrawide 1080p30 | 1920×1080, ~30.05 fps |
| 173205 | Ultrawide → 4K30 guard | 3840×2160, ~30.03 fps |
| 173302 | Ultrawide UI 1080p60 | 1920×1080, ~30.05 fps; not true 60fps |
| 173400 | Final APK 4K60 | 3840×2160, ~60.04 fps |

Clips are `VID_20260923_*`; decode passed. Final transitions restored 1x;
inspected frames lacked stripes, with no new Java/native or DSX10/MNDS failure.
Earlier CHIEISV3 logging remained. Short clips do not prove long-run thermals
or all features.

## V-NFC

**2026-09-22 — recorded build/device validation.** SNxxx queue fix the recorded candidate
removed the repeated bad-message loop from new boot/camera captures (earlier
capture ~183784 matches). Not all NFC transactions/HALs. [Record](../memory/kernel-frameworks.md).

## V-BOOT

**2026-09-23 — historical read-only boot observation.** Kernel
`4.19.325-cip136-st20-perf-g10f8a106de65`, user build, enforcing, Magisk,
boot complete. Captured WiGig errors 53→0, invalid ASoC routes 4→0,
LHBM reads 2→0, Cirrus PDN 2→2. These are capture counts, not matched-duration
benchmarks. WIL6210/DMABUF_SYSFS_STATS/FUSE_BPF disabled; no captured fatal
crash/ANR/restarting service. Old ultrasound issue is superseded by V-PROXIMITY;
latest haptics kernel identity is in V-HAPTICS. [Full scope](../memory/kernel-frameworks.md).

## V-MEMINFO

**2026-09-24 — user-confirmed symptom resolution.** Optional DMA-BUF iterator
log spam resolved at recorded the recorded candidate. No missing kernel accounting backend
was added. The correction is provided by an upstream dependency; it is not a maintained fork.
[Classification](releases.md).

## V-DOLBY

**Historical control-transport checks.** Captured effect ownership/attachment,
pregain ACK 23698 and route/profile/reset acknowledgments do not prove acoustic
DSP/VQE/game behavior. Earlier property/SELinux failures explain capture failures.
Some MiSound probes changed settings and were not fully restorative.
[Reconciled evidence](../memory/dolby-audio.md).

## V-PLATFORM

**Source checks and separately scoped historical results.** Rootdir's 17-change
record identifies packaged binaries, kernel nodes and init ownership. Publication
is not testing of every service. Bionic/DS4/HEIF/Turnip/DeviceAsWebcam findings
retain their original limits. [Rootdir evidence](../memory/kernel-frameworks.md).

## V-RELEASE

[Release ledger](releases.md) owns maintainer-supplied publication status.
No next ZIP hash or exact included-commit manifest is established by source
completion, a draft banner or a rebased commit date.

## V-INDEX

**Historical A17, September 2026.** [Recorded checks, snapshot and limits](../operations/repoindex.md#active-build-tree-and-historical-indexes).
No new A17 indexing or benchmark here.

## V-REF-INDEX

**2026-10-25, host/source-checked.** Both bundles passed deep checks; standalone suite: 81 tests.
[Audit and scope](../operations/repoindex.md#checked-coverage-and-speed).
Implementation hashes passed; other files use metadata. No ROM/device test or
future freshness guarantee.

## V-KNOWLEDGE

[Guidance](../references/openai-guidance.md) applied; [routing](../references/cold-start-checks.md)
tested locally. These are not paired Astra/Sol runs, API-cost or device tests.

## V-RECOVERY

**2026-09-30 — inventory only:** refs/tools inspected. No Windows reinstall,
WSL export/import, credential recovery or ROM build. Backups need restore testing.

## Availability

Selected sanitized evidence is supplied; raw dumps, logs, clips, projects and
private backups are not. Request only needed artifacts. Archives authorize no work.

## V-PBRP

Recorded October 5/7 build/device acceptance and its remaining limits are in
[historical evidence](../evidence/recovery-system-overlay-20261009.md#historical-acceptance).
Current repairs are V-PBRP-20261009; branch HEAD differs from October 7 assets.

## V-SOURCE-20261009

**2026-10-09 — source-checked.** Maintained ROM heads/product integration and
separate recovery source reviewed; prior recovery-core edits preserved. No new build/device test. [Scope](changelog-audit.md).

## V-CHANGELOG

**2026-10-09 — source/host checked.** All 19 organization repositories and 16
custom ROM inputs reviewed; selected heads matched, tracked trees clean at audit.
Product/library gates, companion controls and canonical camera APK hash checked.
Full/short posts fit Telegram limits. [Audit](changelog-audit.md) owns details.
No new device test.

## V-HBM-RECOVERY

**2026-10-09 — host-tested.** Common the recorded candidate: actual display utility
compiled with JDK 21/Android stubs; settings/sysfs failure, boot retry, normal
disable and no-backup cases pass. Baseline the recorded candidate reproduces false success.
No APK/device test or `~/evo/out` access. [Behavior](../memory/xiaomiparts-device-ux.md#hbm-brightness-recovery--october-9-maintenance).

## V-PBRP-20261009

User build and temporary slot-B test: password decryption and bundled Magisk
installation succeed; ADB decrypted=true and shell intact afterward.
[Exact fixes/artifacts/limits](../evidence/recovery-system-overlay-20261009.md).

## V-DEVICE-20261010

[Audit and limits](../evidence/device-20261010.md).

## V-EVOX-NATIVE-RECOVERY-20261014

**2026-10-14.** [Evidence](../evidence/evox-native-recovery-20261014.md): clean-installed user release/kernel #1; Settings/Wi-Fi pass. Heading verified; password/Weaver unverified.

## V-ADRENO-20261024

**2026-10-24 — source/build/host/device tested.** [GPU](../evidence/adreno-audit-20261024.md):
68 app checks/ABI×3; 633 Khronos: 556 pass/76 unsupported/1 warning/0 failures.
Counter regressions pass; 64 teardowns end at zero; 4 display wakes pass.
Temporary enforcing kernel; boot restored; partition unchanged.
Not full conformance/release.

## V-HARDWARE-20261024

[Device](../evidence/hardware-audit-20261024.md) · [HAL](../evidence/hal-regressions-20261024.md).

## V-DISPLAY-20261025

[Device evidence](../evidence/display-recovery-20261025.md); [resync/build](../evidence/source-refresh-20261025.md).

## V-SUBSYSTEM-INVENTORY-20261025

[Source/build inventory; scoped device observations](../evidence/subsystem-inventory-20261025.md).

## V-TURNIP-20261025

[Bounded build/device tests; cancelled, stock restored; no production acceptance](../evidence/turnip-evaluation-20261025.md).
