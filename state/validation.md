# Validation register

Observation dates and scope below survive a new chat. Reading a record does not
rerun a test. Source checks, target builds, host tests, device behavior and user
acceptance are separate evidence. No entry certifies an entire ROM.

## V-HAPTICS

**2026-09-30 — source/build/host/device-tested and user-confirmed, scoped.**
Final stock-backed HAL and device integration are pushed. Baseline and corrected
candidate passed 21 effect/strength combinations, callback, amplitude,
cancellation, invalid-input and long-request checks. Foreground Tremor feedback
completed; user accepted improvement but did not claim HyperOS parity. The
corrected binary was temporarily mounted under the normal service/domain with
enforcing SELinux; next-build inclusion remains distinct. No primitives/PWLE
advertised. [Exact artifacts, results and deployment](../evidence/haptics/2026-09-30.md).
This supersedes the earlier generated-primitive/pending-reconnection checkpoint.

## V-A16

**Reported during September 27 work; no new device test in this documentation update.**
Maintainer reported clean Android 16 install with Magisk, then audible/clear AC-4
sample playback. Later explicitly stated A16 had been released; exact newer ZIP,
date and links remain unknown. Prior boot/rootdir/Bluetooth dependency checks
were reported, not reproduced here. No Bluetooth audio headset or WFD receiver
was available; do not certify those paths or transfer A17 camera tests to A16.

## V-AC4

**2026-09-24 — device-tested and user-confirmed.** Non-root A17 user build;
explicit `OMX.dolby.ac4.decoder`, official 32-second stereo/48 kHz sample:
800 inputs, 800 output buffers, **6144000 PCM bytes**, 5970795 nonzero,
EOS/PASS, `audio/raw`, two channels, pcm-encoding=2. The diagnostic was silent;
user separately confirmed audible playback in an unidentified player.
Opt-in on/off and 32/64-bit syntax checks were recorded. This validates that
stream, not all presentations, multichannel/offload, apps or Dolby processing.
[Diagnostic](../evidence/ac4/README.md) · [full ABI/failure progression](../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## V-PARTS

**2026-09-24 — source-checked and user-confirmed.** Common `3c30e7d` System
Profile dialog correction was approved visually; earlier `db27251` was
insufficient. Shared per-app implementation is not a separate visual test.
[Exact record](../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## V-UI

**2026-09-24 — source-checked and pushed.** Common `e0fd9ba` removes duplicate
MiSound titles; hardware `59188cf` restores reset buttons and current-locale
profile labels. Resource/API/diff checks passed; no build/device test in those
turns. Dolby README `3b8b33e` was documentation-only.

## V-TOUCH

**September 28 recorded source/host checks.** Common `71b3157`, `5d1ff87`,
`0290d37`, `0d7df19`, `9af4ed6` add supported touch controls/translations and
harden Parts hardware writes/lifecycle. Blob/kernel support inspected and
host/resource checks passed; not full new-UI A17 acceptance. [Scope](../memory/xiaomiparts-device-ux.md).

## V-PROXIMITY

**Recorded temporary device test and user confirmation.** Alioth `05f9b24`
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
or all features. [Full results](../archive/2026-09-26/today/2026-09-23-camera-video-validation.md).

## V-NFC

**2026-09-22 — recorded build/device validation.** SNxxx queue fix `8be75516`
removed the repeated bad-message loop from new boot/camera captures (earlier
capture ~183784 matches). Not all NFC transactions/HALs. [Record](../archive/2026-09-26/memory/nfc.md).

## V-BOOT

**2026-09-23 — historical read-only boot observation.** Kernel
`4.19.325-cip136-st20-perf-g10f8a106de65`, user build, enforcing, Magisk,
boot complete. Captured WiGig errors 53→0, invalid ASoC routes 4→0,
LHBM reads 2→0, Cirrus PDN 2→2. These are capture counts, not matched-duration
benchmarks. WIL6210/DMABUF_SYSFS_STATS/FUSE_BPF disabled; no captured fatal
crash/ANR/restarting service. Old ultrasound issue is superseded by V-PROXIMITY;
latest haptics kernel identity is in V-HAPTICS. [Full scope](../archive/2026-09-26/today/2026-09-23-latest-kernel-boot-verification.md).

## V-MEMINFO

**2026-09-24 — user-confirmed symptom resolution.** Optional DMA-BUF iterator
log spam resolved at recorded `09538b6`. No missing kernel accounting backend
was added. Local upstream ownership is now verified in the source map.
[Classification](../archive/2026-09-26/today/2026-09-24-changelog-delta-index.md).

## V-DOLBY

**Historical control-transport checks.** Captured effect ownership/attachment,
pregain ACK 23698 and route/profile/reset acknowledgments do not prove acoustic
DSP/VQE/game behavior. Earlier property/SELinux failures explain capture failures.
Some MiSound probes changed settings and were not fully restorative.
[Reconciled evidence](../archive/2026-09-26/today/2026-09-24-rework-memory-reconciliation.md).

## V-PLATFORM

**Source checks and separately scoped historical results.** Rootdir's 17-change
record identifies packaged binaries, kernel nodes and init ownership. Publication
is not testing of every service. Bionic/DS4/HEIF/Turnip/DeviceAsWebcam findings
retain their original limits. [Rootdir evidence](../archive/2026-09-26/today/2026-09-23-sm8250-rootdir-android17-modernization.md).

## V-RELEASE

[Release ledger](releases.md) owns maintainer-supplied publication status.
No next ZIP hash or exact included-commit manifest is established by source
completion, a draft banner or a rebased commit date.

## V-INDEX

**2026-09-24 host tests; September 30 read-only metadata refresh.** repoindex
1.1.0 / `c79c150` passed 20 recorded regressions. Current stored A17 scan is
September 28: 1756352 files, 10180486 symbols, schema 2, coverage known,
zero recorded errors, excludes `out` and VCS metadata. `live_tree_verified=false`;
no new scan or benchmark in this update. [Usage/limits](../operations/repoindex.md).

## V-KNOWLEDGE

[Official guidance](../references/openai-guidance.md) was fetched and applied;
[routing scenarios](../references/cold-start-checks.md) exercise fresh-context
retrieval locally. Structural checks are not paired Astra/Sol model runs, API
cost measurements or device validation.

## V-RECOVERY

**2026-09-30 — inventory/documentation.** Source refs and local tools were
inspected. No Windows reinstall, WSL export/import, credential recovery or ROM
build was performed. Private backup usability still requires an actual restore test.

## Availability

This repository includes selected sanitized evidence and public source references.
Raw clips, screenshots, complete logs, stock ELF/APK dumps, Ghidra projects,
local SQLite databases and private backups are not supplied by reading it.
Request only the artifact needed for a new conclusion; never silently substitute
a different firmware. Archived data is historical and does not authorize old tasks.
