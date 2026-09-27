# Android 16 / Android 17 Release-State Memory

## Pending next release

Generate from [the latest preparation packet](../today/2026-09-24-changelog-preparation.md), including its final camera/AC-4 evidence and user-validated Thermal Profiles item. The shipped cutoff is now 23.09.2026, confirmed by the maintainer-supplied published changelog. The next draft contains only the subsequent delta.

Historical release evidence only. Repository/commit lists in this file describe earlier releases, not current tracking. Use `repositories/TRACKED_HEADS.yaml` for the current organization set.

## Authoritative published baseline — 23.09.2026

The maintainer supplied the published 22.09.2026 and 23.09.2026 changelogs directly and identified September 23 as the latest release. This advances the semantic shipped cutoff to **23.09.2026, Android 17 / Evolution X v12.2**. It supersedes earlier preparation-only instructions to retain September 22. Exact artifact hashes/manifests were not supplied; do not fabricate a commit-perfect shipped manifest.

The September 22 published notes confirm the existing baseline below: camera runtime/JNI/ExtraPhoto/caching and Photo/Video SAT paths; XiaomiParts overhaul; Dolby/game-audio/UI and source-built battery listener; display/media/Camera2 compatibility; battery/charging/kernel work; NFC teardown; framework integration and ART precompilation.

The September 23 published notes additionally include all of the following, which must be excluded from the next release's new-feature list:

- **Camera:** main 4K60 corruption fix, main 4K30/60 and ultrawide 1080p recording validation, VideoSAT session/stability fixes, unsupported ultrawide 4K guard, safe return to 1x on resolution changes, and Alioth camera-buffer compatibility.
- **System:** obsolete Android 11–13 startup cleanup, unused Qualcomm services/helpers and failed node initialization removal, Android 17 startup modernization, automatic mobile-network selection and standard database durability settings.
- **Audio:** invalid startup speaker/audio routes, unsupported headphone controls, obsolete mixer configuration and restoration of two-input recording policy.
- **Charging:** removal of competing charging-control handling, Android Health ownership and charging-preference consistency.
- **Kernel/display:** unused WiGig disablement, unsupported local-HBM calibration guard, NNAPI boost group and reduced battery/thermal/touch/multimedia/amplifier diagnostics.
- **USB/NFC:** controller readiness/init handling, unsupported USB configuration prevention, svc NFC command compatibility, NFC property handling and absent kernel-interface handling.
- **Cleanup:** obsolete Wi-Fi migration/factory hooks, radio fallbacks/diagnostics, unsupported performance nodes, unused vendor networking/QCC, obsolete build/experimental thermal configuration and Camera/Dialer product alignment.
- **ROM-side:** the published release already describes the Android 17 device rebuild and updated camera/kernel/audio/system integration. Do not repeat generic rebuild language without a new identified release.

These are published semantic claims, not new runtime tests performed during this documentation update. Existing technical evidence still constrains precision: ultrawide 4K is disabled, and ultrawide UI 60fps was not measured at 60fps. The older September 23 draft files are archival and must not be reused as new-feature candidates.

See [today-only reconciliation](../today/2026-09-24-changelog-delta-index.md) for the remaining release candidates and maintenance-only work.

## Purpose

This file preserves release-era decisions and changes that are useful when preparing future POCO F3 / alioth Evolution X builds.

Treat dates/versions below as historical checkpoints, not automatically as the newest release.

For changelog generation, this file is also the **semantic release cutoff ledger**. A feature recorded as shipped here must not be listed again in a later changelog merely because Git history was rebased/recreated with newer SHAs or timestamps.

## Android 17 checkpoint

Known release line:

```text
Android 17
Evolution X v12.2
```

### Device/common changes

Durable Android 17 work has included:

- removal of obsolete Android 17 resource overrides;
- preservation of legacy Xiaomi thermal profiles;
- guarded touch settings;
- avoidance of obsolete memory-cgroup writes on cgroup v2;
- applying ZRAM page-cluster via init;
- RAM-tier ART defaults for 6/8 GB variants;
- removal of retired seamless-transfer flags;
- SELinux labeling for the haptic resonance node;
- Smooth Display wiring through Alioth Settings overlays.

### MiuiCamera

Release-era MiuiCamera improvements have included:

- native 48 MP QCFA capture;
- removal of fake 12 MP -> 48 MP upscaling;
- reworked Alioth camera defaults;
- Macro restoration;
- Xiaomi metadata / legacy HAL compatibility;
- photo saving and video-recording fixes;
- front-camera video crash fixes;
- auxiliary-camera overlay cleanup;
- Android 13 media/default-permission alignment;
- Google Lens property deduplication;
- SELinux alignment;
- vendor camera allowlist;
- numeric CamX log mask.

Later 2026-09-22 work further finalized the MiuiCamera 5.x native-library packaging; see the current MiuiCamera memory and dated records.

### Dolby

Release-era Dolby work has included:

- bypass behavior during calls/VoIP;
- confirmation of native state before persisting;
- communication playback/recording lifecycle tracking;
- opt-in VQE for game voice sessions;
- VQE application/UI styling.

### Frameworks/av

A durable Xiaomi compatibility change supports legacy single-role tag lookup.

## Android 17 shipped baseline — 16.09.2026

The 16.09.2026 build is the previous release cutoff for the 22.09.2026 device-side changelog.

The following features were **already included in the 16.09 build** and must not be re-listed as new solely because later history rewrites gave equivalent work newer SHAs/dates:

### Display / frameworks

- legacy VDS refresh pacing opt-in in SurfaceFlinger;
- Alioth screen-recording tuning for the legacy display stack;
- SELinux property labeling for legacy VDS refresh pacing;
- GPU-service access to pinned BPF map metadata.

### Kernel / brightness

- Linux 4.19.325-cip136 rebase;
- exposure-dimming gain fixes;
- low-brightness interpolation/transition fixes;
- correct brightness restoration when leaving dimming/blank states.

### SM8250 common / power / init

- removal of unsupported PowerHAL tuning nodes;
- recovery trigger cleanup;
- FastRPC shell-copy mount permission fix;
- removal of unshipped Qualcomm services and obsolete camera-model copies;
- disabled unsupported THP helper auto-start;
- migration from legacy direct cgroup/writepid placement to named task profiles;
- launch/camera boosts preserving configured CPU ceilings;
- removal of broad game CPU-frequency reporting spoof.

### Dolby

The 16.09 build already included the then-current Dolby improvements for:

- stock endpoint tuning selection by media route;
- media-route tracking;
- VQE recovery when effects become inactive/control-lost;
- VQE controls moved into Settings;
- coalesced communication lifecycle restore requests;
- portrait/landscape speaker tuning selection.

### Alioth audio

- mixer-overlay parser cleanup;
- removal of invalid/unavailable mixer controls and paths.

These are semantic shipped features. If equivalent code is later squashed or reauthored, it remains part of the 16.09 baseline.

## Android 17 shipped baseline — 22.09.2026

The 22.09.2026 build advances the Android 17 / Evolution X v12.2 device-side release cutoff.

### Live branch heads treated as included

At changelog-generation time, the following current heads were treated as part of the 22.09 build baseline:

```text
decompiled_miui_camera:aosp-17
  b07f52816f7a105e9906992717f6705fd1637767
  MiuiCamera: alioth: Enable VideoSAT on logical SAT camera

device_xiaomi_camera:aosp-17
  433cf879cb10dcf3e682ea515ebc507170c6b3d8
  camera: alioth: Use logical SAT camera for video zoom

android_hardware_nxp_nfc:lineage-24.0
  8be75516d6d3cfff3a95ca2f249f0b36ceededb9
  nfc: nxp: Keep client queue valid during teardown

device_xiaomi_sm8250-common:aosp-17
  6e964d1447daa2e90007d36115ba4975f1309360
  sm8250-common: art: Precompile unprofiled apps with speed filter

hardware_xiaomi:cnb
  cab7a52105183c03ed90f219250e88fb6e7d36db
  permissions: Align Dolby allowlists with manifests

frameworks_base:cnb
  e72fb05db5ebccb0a78aa2702bef32b40fe875fa
  Camera2: Reject malformed Xiaomi vendor input tuples

frameworks_av:cnb
  8fc27178f6fa4a1a1eb0cc3df66b33109f0ed300
  stagefright: Report Dolby AC-4 table initialization failures

frameworks_native:cnb
  3f05b77cf5e204a9c4104fc27850d899518cb2a2
  SurfaceFlinger: Add opt-in legacy VDS refresh pacing

device_evolution_sepolicy:cnb
  a3c8552ced9f49c6aa3ac0f9a180652118169d72
  sepolicy: Label the legacy product fingerprint as build metadata

device_xiaomi_alioth:aosp-17
  503f821f233a9821d770db863a01ac8abc08732f
  alioth: Expose stock speaker tuning without platform spatial audio

kernel_xiaomi_sm8250:aosp-16
  425cd7391fc50d7799a20fe88413c0437315f118
  arm64: dts: alioth: Restore unverified battery current limit

hardware_qcom-caf_sm8250_media:cnb
  6b3d466f134ef3b3f8b1da5c7ffa8bb234249292
  media: Refresh C2D surfaces when color range or PI layout changes

hardware_qcom-caf_sm8250_display:cnb
  0e25857599b3a609e957a0d0418ec2b3dd264480
  display: Bridge legacy IDisplayConfig 1.9 to 2.0

vendor_xiaomi_sm8250-common:aosp-17
  3ef058e565741ebf797bad84936295d621f0cfbc
  sm8250-common: Stop selecting the prebuilt audio battery listener

hardware_qcom-caf_sm8250_audio:cnb
  0782faad5715864c62912fda9749836d3f1cdd70
  audio: Prefer AIDL Health and harden battery-listener lifecycle
```

`system_sepolicy:cnb` remained at `7e8e659bade0aa0e9247e107dc2f2d51851a059d`, whose GPU BPF metadata fix was already part of the 16.09 baseline.

### New semantic delta shipped in the 22.09 build

#### MiuiCamera

The 22.09 build includes the device-side work for:

- stock-compatible native camera runtime layout;
- MiuiCamera JPEG utility JNI integration;
- removal of the obsolete HIDL transport dependency from that JNI path;
- stock Alioth ExtraPhoto companion support;
- persistent camera-capability caching, eliminating repeated capability reconstruction;
- CameraX vendor-extension removal;
- unused MiSys camera integration cleanup;
- improved Xiaomi Camera2 reprocess/vendor-input compatibility;
- logical SAT camera path for Photo zoom;
- logical SAT camera path for Video zoom.

Evidence caveat:

- the native JPEG-utility compatibility and capability-cache fixes are runtime validated;
- the newest VideoSAT logical-role-60 implementation is **included in the build but still pending rebuilt-device runtime acceptance**;
- therefore release wording should say `added logical SAT path/support` rather than claiming seamless VideoSAT is confirmed.

#### XiaomiParts / device UX

The 22.09 build includes the major Android 17 XiaomiParts rework:

- Android 17 expressive Settings styling;
- finalized Alioth vendor-backed thermal profile model;
- per-app thermal switching and gaming-touch lifecycle improvements;
- clearer thermal profile names, icons and decoded detail UI;
- collapsible System Profile section;
- app/package search;
- per-app refresh-rate control adapted to Android 17;
- safer HBM/DC-dimming/touch-state handling;
- lifecycle-safe Clear Speaker playback;
- MiSound effect lifecycle and route-aware controls;
- self-contained app resources;
- completed locale translation set;
- compact MiSound header/control polish.

#### Dolby / audio

The 22.09 build includes the newer shared Dolby integration and associated audio work:

- serialized/recoverable DAP runtime ownership;
- improved stock-compatible routing/communication handling;
- Alioth HyperOS game-audio effect integration;
- hardened DSP volume synchronization / AudioServer recovery;
- stronger AudioEffect transport/error handling;
- refined equalizer/settings hierarchy;
- Android 17 expressive Dolby UI;
- completed Dolby locale translations;
- shared DMS policy/vendor capability initialization;
- source-built audio battery listener path.

#### Display / media / frameworks

The 22.09 build includes:

- improved high-refresh screen recording and blur handling;
- HBM zero-window handling;
- Xiaomi Camera2 reprocess input configuration support and malformed-input rejection;
- legacy DisplayConfig 1.9 -> 2.0 compatibility bridge;
- legacy Adreno/gralloc validation hardening;
- balanced C2D/GPU mapping lifetimes;
- C2D surface refresh when color range or PI layout changes;
- MediaCodec surface-generation recovery;
- current legacy Dolby DAP lifecycle/framework integration.

#### Kernel / battery / charging

The 22.09 build adds the post-16.09 kernel/device work for:

- replacement-battery support;
- Android battery property exposure;
- battery-current normalization at the Android Health boundary;
- JEITA battery-ID failure handling;
- charging-control backend cleanup;
- KGSL/GPU compatibility sysfs and memory/reclaim hardening;
- bounded Xiaomi thermal-message handling;
- userfaultfd memcg ownership ordering fix;
- USB DWC3 run-stop polling pacing.

#### NFC

The 22.09 build includes the runtime-validated NXP teardown fix:

```text
8be75516d6d3cfff3a95ca2f249f0b36ceededb9
nfc: nxp: Keep client queue valid during teardown
```

It preserves the upstream UAF mitigation while preventing the tight repeated:

```text
NFC client received bad message
```

loop during teardown.

#### Build/runtime optimization

The build includes the current Android 17 ART/dexpreopt direction:

- RAM-tier ART defaults for Alioth variants;
- unprofiled preinstalled code compiled with the `speed` compiler filter;
- profile-guided behavior preserved where profiles are available.

### 22.09 changelog highlight vocabulary

Suitable user-facing highlight wording for this release:

```text
Camera Runtime & SAT
XiaomiParts Overhaul
Dolby / Game Audio
NFC Fix
```

Do not use `VideoSAT Fixed` until the current role-60 recording acceptance test passes.

## Android 16 checkpoint

Known maintenance release line:

```text
Android 16
Evolution X v11.11
```

Android 16 received applicable backports/parallel maintenance for:

- XiaomiParts thermal/touch behavior;
- cgroup v2 / ZRAM handling;
- RAM-tier ART defaults;
- haptic resonance labeling;
- Smooth Display overlay;
- MiuiCamera permissions/SELinux/vendor-camera cleanup;
- Dolby call/VoIP and VQE lifecycle changes.

When porting an Android 17 change to Android 16, verify framework/API/resource applicability first. Do not copy Android 17-only resource removals blindly.

## Release-note highlights historically used

Useful concise highlight wording has included themes such as:

```text
Native 48MP
Macro Restored
Front Video Fixed
```

Keep highlights tied to user-visible behavior, while the full changelog can name implementation areas.

## Maintenance rule

For every new release:

1. identify the previous shipped baseline in this file;
2. compare current branch heads/current trees against that baseline;
3. treat rewritten/rebased equivalents as already shipped when their feature is in the prior semantic baseline;
4. group changes by subsystem;
5. omit internal experiments/reverted/docs-only commits;
6. distinguish ROM-side rebuild/version bumps from device-specific changes;
7. keep Telegram mirror notes much shorter than the full changelog;
8. record the new build date, semantic baseline and useful current heads here after the build is published.
