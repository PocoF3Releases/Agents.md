# Release ledger and changelog workflow

## Authority

Android 17 recorded published semantic baseline: **23.09.2026 / Android 17 / Evolution X v12.2**, established by maintainer-supplied September 22/23 published notes. Exact ZIP hashes and included-commit manifest were not supplied. Publication evidence is not a device test, and rebases/new timestamps do not make old features new. [V-RELEASE](validation.md#v-release).

## Android 16 release preparation

Previous published baseline supplied by the maintainer: **14.09.2026 / Evolution X v11.11**. Already announced: RAM/ART and cgroup v2 ZRAM configuration, legacy thermal/touch/Smooth Display fixes, camera permissions and vendor/SELinux cleanup, Dolby call/VoIP bypass and VQE controls, Bluetooth controller recovery and DS4/composite support.

The maintainer subsequently reported a clean Android 16 installation with Magisk and confirmed AC-4 sound. The September 27 draft covers later camera compatibility/4K60 guards, Parts UI/thermal/MiSound rework, AC-4 and Dolby recovery, independent high-FPS recording/blur changes, startup/charging/audio/kernel cleanup and NFC compatibility. Verify branch inclusion before asserting every feature is in a downloadable artifact. Android 17 camera tests are not fresh Android 16 tests. [V-A16](validation.md#v-a16).

Draft date: **27.09.2026**, Android 16 / v11.11. The maintainer later explicitly reported Android 16 already released. The exact newer publication date, artifact and links were not identified; do not label it wholly unpublished or reuse September 14 links. Keep Android 16 and Android 17 baselines separate. Clean install from Android 17 is the maintainer-supplied migration instruction.

## Android 17 post-September 23 delta

The first validated post-baseline changes were:

- **AC-4:** opted-in legacy OMX initialization/index/helper lookup now decodes the tested stereo stream; audible playback confirmed. See audio and V-AC4.
- **Thermal Profiles:** shared dialog clipping/spacing correction, with System Profile user approval. See device UX and V-PARTS.

Additional source-completed candidates with no recorded UI device acceptance: MiSound duplicate-title removal and Dolby reset-button/profile-locale fixes. Keep separate from the two validated entries above until build inclusion and acceptance are established; see [V-UI](validation.md#v-ui).

libmeminfo `09538b6` is earlier implementation with later confirmation/preparation; it may be an optional unannounced maintenance note, not newly implemented that day. Portability guards, history rewrites, documentation, repoindex, stock/Marble audits and this reorganization are not new ROM features. No donor codec, extra foundation/xlog links or 64-bit-only conversion was delivered. Final next-build metadata and upstream ROM delta remain unknown. [Detailed classification](../archive/2026-09-26/today/2026-09-24-changelog-delta-index.md).

## Already announced — cumulative ledger

| Cutoff | Already included user-visible families; exclude equivalent later rebases |
| --- | --- |
| 16.09.2026 | Legacy VDS pacing/screen-recording tuning and GPU BPF access; kernel 4.19.325-cip136/dimming/brightness fixes; power/init/FastRPC/task-profile cleanup; configured CPU ceilings preserved; removal of broad game frequency spoof; route/endpoint Dolby tuning, VQE recovery and Settings controls; Alioth mixer cleanup. |
| 22.09.2026 | MiuiCamera native/JNI/ExtraPhoto/cache integration, CameraX/MiSys removal, Photo/Video logical SAT paths, Camera2 vendor input; XiaomiParts expressive UI, thermal/touch/per-app refresh, guarded HBM/DC/touch, Clear Speaker, MiSound, self-contained resources/translations; Dolby ownership/routing/game effects/DSP recovery/UI/DMS/translations; source-built audio battery listener; DisplayConfig/gralloc/C2D/MediaCodec compatibility; battery replacement/Health/current/JEITA/charging/KGSL/thermal/userfaultfd/DWC3 work; NFC teardown fix; ART speed/profile/RAM-tier defaults. |
| 23.09.2026 | Main 4K60 corruption/session fixes, tested main 4K30/60 and ultrawide 1080p, guarded ultrawide 4K and safe return to 1x, buffer compatibility; obsolete startup/services/node writes and network/database defaults; invalid audio routes/headphone/mixer cleanup and two-input recording policy; Android Health charging ownership; WiGig/LHBM/NNAPI and diagnostics cleanup; USB readiness/configuration and NFC svc/property handling; obsolete Wi-Fi/radio/performance/network/QCC/build/thermal hooks and Camera/Dialer alignment. |

Earlier release highlights also included native 48MP QCFA (not fake 12-to-48MP scaling), Macro, front video and metadata/media/SELinux fixes. The older September 22 VideoSAT-pending language is superseded only within the final September 23 tested scope; it does not establish ultrawide true 60fps. Historical VDS inclusion is not proof it survived a later source resync.

The [complete original release ledger](../archive/2026-09-26/memory/android16-android17-release-state.md) retains all former heads and exact chronology. These historical head lists are not competing current source maps.

## Produce and publish notes

Resolve the previous published baseline and relevant live heads from [the source map](repositories.yaml). Compare semantic changes, not timestamps alone. Group user-visible deltas by subsystem; omit empty sections, reverted experiments, docs-only work and already-announced equivalents. Separate device changes from verified ROM-wide changes. Use wording proportionate to source/build/runtime evidence.

Write a grouped main post and a substantially shorter Telegram/mirror version, then choose three concise banner highlights from that same delta. Do not invent versions, build dates, download locations or install requirements. Only after publication or an explicit new-baseline declaration update this ledger and CURRENT_STATE; record exact artifact identities when available.

Android 16 maintenance used Evolution X v11.11 and applicable Parts/thermal/touch, cgroup/ZRAM/ART/haptic/Smooth Display/camera permission and Dolby lifecycle backports. Verify API/resource applicability before any new port; Android 17 removals are not automatically valid on Android 16. Artwork conventions live only in [release assets](../operations/release-artwork.md).

## Later source-completed candidates

For a new A17 changelog, also evaluate these against the actual release artifact:

| Candidate | Evidence and wording limit |
| --- | --- |
| Stock-backed AW8697 HAL, stock drive/DTS, corrected strength and texture feedback | Device and user acceptance is scoped to the rebuilt baseline plus temporary corrected HAL; source pushed. Do not advertise primitives/PWLE. |
| Alioth ultrasound timeout retry | Near/far events and user call-proximity confirmation on a temporary deployment; production extraction fix exists. |
| Extra Alioth touch controls and translations | Supported blob/kernel controls and host/resource checks; no full new A17 UI acceptance. |
| Parts write errors / Clear Speaker lifecycle / refresh-service hardening | Source/host checks; do not claim broad acoustic or A17 runtime validation. |
| Sensors and fingerprint service lifetime fixes | Target compilation/source checks, not biometric certification. |

These are candidates, not an assertion that a published ZIP contains them.
Keep haptics source consolidation, firmware documentation and this workhub
reorganization out of user-visible feature counts.
