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
- [Recovery interface replay](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/ed805fb928a6bdf63db7e2832cb958c4526a17a3)
- [Main interface replay](https://github.com/PocoF3Releases/android_hardware_interfaces/commit/4ec9178671c470cd57e8b1e5f91591b482c883cc)

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
