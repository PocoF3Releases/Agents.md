# Android 17 source refresh — October 25, 2026

Source preparation and component verification; no new ROM/device acceptance.

## Sync and replay

All 1,265 projects completed network/checkout sync (`repo -j50`). All 43
maintained checkout forks were checked against 40 selected upstreams; three
standalone sources have no separate upstream. Private keys and research sources
were untouched. Existing output and backup refs were preserved.

Only the framework and hardware-interface maintained bases advanced. Eight
framework and two recovery hardware-interface commits were replayed with equal
range-diffs and preserved authorship. The main ROM hardware-interface branch
keeps only its audio callback fix; recovery crypto variants remain separate.
All other maintained forks were already current; no artificial commits added.

The two related Alioth compositor commits are consolidated without changing
the final device tree. Generic bounded UI queue recovery moves to common Kona
product configuration; Alioth panel constants remain local. Generated 42 view
flag accessors equal the prior tested values, the Choreographer blob is unchanged,
and 51 extracted-state-machine host checks pass. This adds no physical panel modes.

All four authored recovery overlays reapplied; idempotent preflight has zero
pending patches. Public shared ROM tips exclude these local overlays. Existing
manifest links and patch payloads remain unchanged. Seven GMS LFS assets are
materialized, and 106 tracked APK/APEX assets have valid ZIP headers.

## Current implementations

- [Common UI recovery](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/0c2346d1bf9522de2aa4cc292c12185667ef968d)
- [Alioth compositor profile](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/7c7229bdb805456900b817ebf023aab69bcb94a8)
- [Framework replay](https://github.com/PocoF3Releases/frameworks_base/commit/bfe244147a01a5933f444f27a4403ae19f4d2582)
- [Recovery interface replay](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/0b8a8b3905ebc98f87004f23a18d245e516c8f8f)
- [Main interface replay](https://github.com/PocoF3Releases/android_hardware_interfaces/commit/810a827dcdfb8e7c7cdfda5b1d1e659bab5aa010)

New upstream HFR behavior remains behind unset opt-ins with preserving defaults.
No unverified camera tuning is enabled. No kernel base movement occurred, so no
new defconfig regeneration was needed. The upstream AudioSystem shim revert
does not remove the retained AudioTrack shim module.

## Host tool caveat

The existing repo-tool optional-cache permission workaround was preserved.
Its dirty `git_config.py` blocks automatic tool replacement; source sync used
`REPO_SKIP_SELF_UPDATE=1`. This is separate from clean Android project sources.

## Verification

Build graph and generated view flags passed for `lineage_alioth-cp2a-user`.
SystemUI, recovery, recovery-storage, sepolicy.recovery, camera.device@3.2-impl
and android.hardware.audio@6.0-impl passed `m -j6`. Normal selinux_policy, Settings (including Evolver resources), LineageCustomizer,
WallpaperPicker2 and SurfaceFlinger also passed `m -j6`. Six build/make links and selected-base
ancestry passed. A second-model source review found no blockers.

All 44 GitHub branch tips were verified after publication (five changed). The
recovery manifest and GitLab camera branch were verified current and unchanged.
Explicit expected-head leases protected rewritten branches; backup refs remain.

No installclean, full-ROM build, flash or new device test was performed.
[Source ledger](../state/repositories.yaml) separates public tips and local
recovery overlays. Earlier phone tests retain their original artifact scope.

## Final replay audit

A second source audit compared all 43 checkout forks with saved pre-sync public
heads and re-read all 44 GitHub branch tips. Unchanged commits remain identical;
the ten replayed framework/recovery-interface commits retain stable patch IDs,
authorship, author dates and messages. The separate main ROM audio callback patch
also retains its original patch ID. The consolidated Alioth final timing tree
is identical; the common addition contains only the intended five flag-wiring files.
All four local recovery commits match the SHA-256-checked authored mail patches,
and idempotent preflight again reports zero pending. Source trees remain clean.

Display changes apply to **normal Android**: the common value set uses the
`system` container, and generated `android.view.flags.Flags` accessors return true
for both recovery flags. Alioth's normal generated vendor properties contain the
120 Hz SurfaceFlinger work durations. Recovery's distinct 120 Hz UI preference
does not change either system configuration. Common flag files and product wiring
are identical before/after applying the recovery overlay.

No source corrections or repeated builds were needed after this audit. The
component passes above remain applicable to unchanged inputs; full production
ROM packaging and testing of that resulting build remain outstanding.

## Upstream-facing commit messages

Reviewed custom messages in the shared ROM framework, NFC, compression, Qualcomm
HAL and Xiaomi HAL forks. Most subjects already describe components rather than
Alioth. Seven messages across six branches were revised: camera session identity,
extended audio callbacks (main and recovery copies), composer compatibility, and
three Qualcomm descriptions containing obsolete model-generation boilerplate.
The camera description retains its default-off Xiaomi fallback requirement;
composer describes legacy clients rather than one device's proprietary binary.
Audio validation remains explicitly scoped to Alioth, without claiming other
HALs were device-tested. Existing coauthor attribution and original authorship,
author dates and unrelated imported messages were preserved.

| Repository | Current branch tip |
| --- | --- |
| android_hardware_interfaces (recovery) | [0b8a8b3905eb](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/0b8a8b3905ebc98f87004f23a18d245e516c8f8f) |
| frameworks_av | [1e7787289cec](https://github.com/PocoF3Releases/frameworks_av/commit/1e7787289cecdb5b029edfb6829ccee3965b6038) |
| hardware_qcom-caf_sm8250_audio | [e5644bea3660](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_audio/commit/e5644bea36605d39bc1412f6b1d8f4c5ec029cc1) |
| hardware_qcom-caf_sm8250_display | [50389bd77670](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_display/commit/50389bd776702a3a94d46be3027ce4e5a7c3b572) |
| hardware_qcom-caf_sm8250_media | [60f362cedc69](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media/commit/60f362cedc690153ac5fb5824327fec66361d598) |
| android_hardware_interfaces | [810a827dcdfb](https://github.com/PocoF3Releases/android_hardware_interfaces/commit/810a827dcdfb8e7c7cdfda5b1d1e659bab5aa010) |

Each rewritten commit retains its exact tree and parent-to-commit patch; each
branch retains the full binary diff from its selected upstream. All six public
tips were lease-protected and read back after pushing. Original device/backend
names remain where they identify actual implementation constraints. Historical
measurement records retain their original test revisions; this metadata-only
rewrite adds no new build/runtime acceptance and needs no rebuild. All four
recovery overlays remain applied, with zero pending patches.
