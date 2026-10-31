# Source refresh — 2026-10-31

## Scope and result

`source-checked`, `host-tested`, `build-graph-tested`. Updated the existing
`~/evo` checkout for `lineage_alioth-cp2a-user`; no ROM/APK build, installclean,
flashing or device test was performed in this refresh. Previous runtime evidence
does not certify this newly synchronized combination.

All 1,265 source projects synchronized; 44 project HEADs changed. The final
source-project worktrees are clean. All 43 selected maintained GitHub build
forks, the separate main-ROM hardware/interfaces fork and 11 other recorded
repository tips match their published refs (55 total). The GitLab camera tip
also matches its selected `aosp-17` branch. Private signing repositories and
research dumps were not modified. Existing output and unrelated local tooling
were preserved; normal build-graph regeneration removed one obsolete installed
font-overlay output.

## Replayed and published branches

| Component | Published candidate | Latest selected upstream | Custom commits |
| --- | --- | --- | --- |
| `bootable/recovery` | [9f67850ac4a5](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery/commit/9f67850ac4a5d7787ca7543263bd47586a5bc80f) | [fbfd88cd3383](https://github.com/Evolution-X/bootable_recovery/commit/fbfd88cd338311e59a9c132485d63f9ec77fd9f3) | 13 |
| `device/qcom/sepolicy_vndr/legacy-um` | [657627c7d1b1](https://github.com/PocoF3Releases-Recovery/android_device_qcom_sepolicy_vndr_legacy-um/commit/657627c7d1b1dcb42de2cc08e9ced9c5d1889b31) | [d8b5ffdf5107](https://github.com/LineageOS/android_device_qcom_sepolicy_vndr/commit/d8b5ffdf51074f0931096991d9e9a9294ad31c98) | 1 |
| `system/sepolicy` | [abbbf28774b4](https://github.com/PocoF3Releases-Recovery/android_system_sepolicy/commit/abbbf28774b4e3dc03bdd3bfde06e4148f5fd482) | [dd9d56abe059](https://github.com/Evolution-X/system_sepolicy/commit/dd9d56abe0590484ae145337ae1e728db9b2d57a) | 2 |
| `frameworks/base` | [faeec1083640](https://github.com/PocoF3Releases/frameworks_base/commit/faeec1083640f2b3982869c0de4d57c2f3ce4b1a) | [da7f9e011d0a](https://github.com/Evolution-X/frameworks_base/commit/da7f9e011d0ab4d4dca1ffa0a8ef671427f14405) | 8 |

All 24 custom commits retain author identity, author date and subject. Framework
and policy range-diffs are unchanged. EvolutionX had rewritten older framework
and recovery history: replay used the previously verified upstream boundaries,
rather than duplicating old upstream commits selected by a naive merge-base.
Each public update used its exact expected old tip with `--force-with-lease`;
backup refs and the original pinned manifest remain private under `.repo`.

The recovery graphics conflict overlaps upstream transparent/opaque drawing
fast paths. Kept the equivalent upstream implementation and retained our canvas,
clipping, rotation and panel-timing work. The other 12 recovery patches remain
unchanged. Existing signature verification, secure ADB/menu enablement, credential
UI, local installation and Magisk/APatch features remain in the source.

The kernel base did not advance, so its approved custom history was retained
without config changes or unnecessary defconfig regeneration. Dolby, MiSound
and Parts fixes, including their separate translation commits, are preserved.

## Recovery integration

The canonical [local manifests](https://github.com/PocoF3Releases-Recovery/local_manifests/commit/1816695ed87b4f3b49f54859500a64d6d08a70d4)
are current. Their deployed branch-tracking XML, apply runner and patch series
match; no new pin or manifest-source change was needed. All six build/make
linkfiles remain intact. After checkout, reapplied the four authored recovery
patches: one framework, one Alioth and two common-device patches. The idempotent
preflight reports zero pending patches afterward. These stay local overlays;
they were not pushed into the ROM device/framework branches.

Local source identities after applying overlays:

| Path | Local HEAD | Public relationship |
| --- | --- | --- |
| `frameworks/base` | `4fb9fff603cbe73f0a59515fa1bb78b9a7bd0996` | Public tip plus authored recovery overlay |
| `device/xiaomi/alioth` | `d5966c2e90954f28700fc1ee4df4e6d70a51eee6` | Public tip plus authored recovery overlay |
| `device/xiaomi/sm8250-common` | `36a1fc954f3a74767bdcea156dd87ccc10d568b8` | Public tip plus authored recovery overlay |

## Verification and limits

- Full network sync at `-j50`, followed by full local checkout, passed. Two
  clean repositories (`external/libpng`, `system/netd`) needed targeted
  `--force-sync` network repair after hook/object metadata changed; both had
  complete Git bundles saved first. No source edits were discarded.
- The final pinned manifest and before/after inventories are retained privately
  in `~/evo/.repo/source-refresh-20261031/`.
- 128 GMS/Xiaomi APK/APEX/JAR files have valid ZIP containers; no unresolved LFS
  pointers were found. This is presence/container validation, not runtime testing.
- The minui conflict regression compares actual old/new fill and glyph routines
  across 640 rotation, format, alpha, clipping and overscan cases. Output matches
  under Clang `-Wall -Wextra -Werror` plus AddressSanitizer/UBSan. The fixture and
  logs remain private, outside production source commits.
- `. build/envsetup.sh`, `lunch lineage_alioth-cp2a-user`, then `m -j4 nothing`
  passed after regenerating the Soong/Make graph. Build concurrency is independent
  of the requested Repo `-j50`. This proves graph readiness, not a complete ROM
  compile, signing, packaging, boot or device acceptance.
- Parts APK/device checks remain deferred as previously recorded. Existing
  output is not evidence of artifacts compiled from these new heads.
- The old `/usr/bin/repo` launcher still prints its update notice; the sync itself
  passed. Its pre-existing local cache-permission workaround was preserved.

## Next build

The checkout is prepared for the user’s normal release build:

```bash
. build/envsetup.sh && lunch lineage_alioth-cp2a-user && m installclean && m evolution
```

This refresh did not run that release command. Keep ordinary incremental rebuilds
free of unnecessary installclean steps.
