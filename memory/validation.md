# Validation register

All entries below summarize **recorded evidence**, not fresh tests by this reorganization. Source presence, host checks, device observation, user acceptance and publication are distinct. Follow a linked record only when its detail is needed. Unknown present device/root/install state remains unknown.

## V-A16

**Imported from this conversation on 2026-09-27; no fresh device commands in this update.** The maintainer reported Android 16 built, clean-installed and rooted with Magisk. After the AC-4 video test, the maintainer confirmed "Yes, sounds good." This establishes audible playback for that sample, not all presentations, codecs or routes. Exact installed ZIP hash and exported test transcript are unavailable here.

Prior-session summaries report boot/rootdir checks and Bluetooth dependency review; these remain reported results, not newly reproduced tests. No Bluetooth headphones or WFD receiver were available. Do not certify headset audio, WFD streaming, all controller inputs or Android 16 camera modes. Draft artwork is not publication evidence.

## V-AC4

**2026-09-24 — agent-observed-runtime and user-confirmed.** Rebuilt non-rooted Android 17 user build dated 05:07:46 UTC; the user supplied the rebuild. Explicit OMX.dolby.ac4.decoder test of the official 32-second stereo/48 kHz sample returned 800 input samples, 800 output buffers, **6144000 PCM bytes**, 5970795 nonzero bytes, eos=true / PASS. Output was audio/raw, two channels, pcm-encoding=2. The diagnostic is silent; the user separately confirmed audible playback in a player whose identity was not established.

Opt-in on/off, 32/64-bit syntax checks were recorded. Acceptance supersedes the UnsupportedIndex/helper-lookup failures for this stream only, not every AC-4 presentation, app, multichannel/offload path or Dolby effect. [Full ABI/audit/test record](../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md); [reusable diagnostic](../evidence/ac4/README.md).

## V-PARTS

**2026-09-24 — source-checked and user-confirmed.** Final common `3c30e7d` passed recorded source/diff checks; maintainer approved the System Profile screenshot/result. Earlier `db27251` was insufficient. Shared per-app source is not a separately executed per-app visual test. No original screenshot is stored here. [Approval and exact implementation](../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## V-UI

**2026-09-24 — source checks and publication only.** Common e0fd9ba (MiSound duplicate title) and hardware_xiaomi 59188cf (reset buttons/current-locale profile labels) were committed and pushed in this conversation. SettingsLib API/layout review, five built-in Russian label mappings and diff checks passed as applicable. Neither change was built or tested on-device in those turns; screenshots establish the earlier defects only. Dolby README 3b8b33e was documentation-only. No new remote source-head survey or installed-artifact verification is implied by this September 27 summary.

## V-CAMERA

**2026-09-23 — agent-observed-runtime, host packaging checks; closed by maintainer 2026-09-24.** Exact APK identity is owned by [camera](miuicamera.md). Apktool 3.0.3 assembly and zipalign -c -P 16 4 passed. Temporary Magisk su -mm mount over the system APK matched the accepted SHA-256; it disappears on reboot. No ROM was rebuilt/flashed for these tests. Preferences were restored; installed CHI hash `8927747617c3729e2590ee06e3c9c1416182dab909647a7af044764459c76224` was unchanged.

| Clip suffix (VID_20260923_) | Mode | Measured output / result |
| --- | --- | --- |
| 172458 | Main 4K30 | 3840x2160, ~30.03 fps; decode passed |
| 172540 | Main 4K60 | 3840x2160, ~60.04 fps; decode passed |
| 172705 | Ultrawide 1080p30 | 1920x1080, ~30.05 fps; decode passed |
| 173205 | Final APK, ultrawide -> 4K30 | 3840x2160, ~30.03 fps; decode passed |
| 173302 | Ultrawide UI 1080p60 | 1920x1080, ~30.05 fps; not 60fps proof |
| 173400 | Final APK 4K60 | 3840x2160, ~60.04 fps; decode passed |

Final transitions restored 1x without Java/native or DSX10/MNDS errors; inspected frames lacked earlier stripes. Short clips do not validate every feature, long-run thermals or every lens transition. Some earlier CHIEISV3 logging remained. Ultrawide 4K is guarded, not implemented. [Full original output/installation record](../archive/2026-09-26/today/2026-09-23-camera-video-validation.md); [closure](../archive/2026-09-26/today/2026-09-24-camera-finalized.md). Older HEIF/native/JNI/cache tests remain historical within [camera history](../archive/2026-09-26/memory/miuicamera-history.md).

## V-NFC

**2026-09-22 — recorded build and runtime validation.** Rebuilt fix `8be75516d6d3cfff3a95ca2f249f0b36ceededb9` removed the tight NFC client received bad message loop from fresh boot and camera logs; the affected capture previously had about 183784 matches. This validates the SNxxx teardown regression, not all NFC transactions or other HAL implementations. [Exact original finding](../archive/2026-09-26/memory/nfc.md).

## V-BOOT

**2026-09-23 — recorded read-only device observation.** Running `4.19.325-cip136-st20-perf-g10f8a106de65`, user build, enforcing SELinux, Magisk available, boot complete. Earlier `78d5b0cd5d26` did not contain the tested fixes. WIL6210, DMABUF_SYSFS_STATS and FUSE_BPF were disabled. Captured counts changed: WiGig PCIe 53 -> 0; invalid ASoC routes 4 -> 0; white-LHBM reads 2 -> 0; Cirrus PDN 2 -> 2. These were captures, not matched-duration performance measurements.

Ultrasound poll errors remained. No fatal crash/ANR or restarting service was found in the captured new boot; services/sensor enumeration/thermal observations are not acoustic, proximity, camera, Bluetooth, transaction or charger-speed tests. Later libmeminfo evidence supersedes only the log-spam portion below. [Exact boot scope](../archive/2026-09-26/today/2026-09-23-latest-kernel-boot-verification.md).

## V-MEMINFO

**2026-09-24 — user-confirmed.** Maintainer reported optional DMA-BUF iterator log spam resolved at recorded `09538b6`. This does not add the missing kernel accounting backend, prove every diagnostic is clean or establish first inclusion in a ZIP. Implementation preceded the later message/commit preparation. [Classification and limits](../archive/2026-09-26/today/2026-09-24-changelog-delta-index.md).

## V-DOLBY

**Historical — control-transport observations, not acoustic certification.** A capture reported captured=1, attachmentAcknowledged=1, pregain ACK 23698 and zero status/failure/retry counts; route/profile/reset acknowledgments were seen. These do not prove all audible DSP/VQE/game processing. Earlier property/SELinux failures explain captured=0. Old MiSound probes altered settings and were not fully restorative; do not call them read-only. [Reconciled evidence](../archive/2026-09-26/today/2026-09-24-rework-memory-reconciliation.md).

## V-PLATFORM

**Historical — source-checked changes and separately scoped tests.** Rootdir's 17-change record documents packaged-binary/kernel/init checks and exact commits; later published notes establish announcement, not a test of every removed service. Old Bionic/DS4/HEIF successes, Turnip shell-domain results and unvalidated DeviceAsWebcam work retain their original limits; do not turn imported summaries into current installation proof. [Rootdir record](../archive/2026-09-26/today/2026-09-23-sm8250-rootdir-android17-modernization.md); [all imported memory sources](../archive/2026-09-26/today/2026-09-22-codex-memory-import.md).

## V-RELEASE

**Maintainer-supplied publication evidence.** September 22/23 notes establish the cumulative semantic baseline, not a commit-perfect ZIP manifest. [The active ledger](android16-android17-release-state.md) owns publication status; original drafts, source JSON and published-ledger context remain in the archive. No next ZIP hash/inclusion or newly researched upstream ROM delta is known.

## V-INDEX

**2026-09-24 — recorded host tests.** repoindex 1.1.0 / c79c150 had 20 fixture regressions, Python compilation and diff checks pass. Read-only status of the older Android database reported 1751834 files / 10137789 symbols, scan date 2026-09-09, schema 2, coverage unknown. No fresh scan or speed benchmark occurred. Header extraction is heuristic; incremental indexing and atomic multi-output transactions were not implemented. [Full tooling evidence](../archive/2026-09-26/today/2026-09-24-repoindex-upgrade.md).

## V-KNOWLEDGE

**Historical governance evidence:** the first September 26 review recorded 22 unit tests and 95 local references; the follow-up recorded 115 references without rerunning unchanged tests. Its eight paired-model replay scenarios were not executed. These are not fresh Sol/Astra benchmarks. [First record](../archive/2026-09-26/today/2026-09-26-agent-memory-guidance-review.md); [follow-up](../archive/2026-09-26/today/2026-09-26-astra-sol-compatibility.md). Results of this structural migration are recorded separately in [archive/README.md](../archive/README.md).

Official-guidance refresh 2026-09-27: fetched the Astra skills/prompts article and memory documentation, then updated completion and recall guidance. This is a documentation review, not a paired-model evaluation. See [maintenance](agent-memory-workflow.md#official-guidance-reviewed-2026-09-27).

## Availability

Shareable historical Android records remain under archive/2026-09-26; personal client-memory exports were removed. Selected AC-4 Java/output files remain active. Raw camera clips, full logcats, original screenshots, stock/Marble ELF dumps, WSL checkouts, local indexes and session transcripts were not made available merely by this move. Canonical APK delivery is on GitLab. Request only the identified missing artifact when needed for a new conclusion; never substitute a different stock version silently.
