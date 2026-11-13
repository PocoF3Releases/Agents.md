# Android 17 implementation and verification status

**Source checkpoint: November 13, 2026.** The [source ledger](repositories.yaml)
owns current public/local identities. [Current verification](../evidence/source-refresh-20261113.md)
is Git/source/host work; build/device acceptance remains dated in
[validation](validation.md), not transferred to a new base by a rebase.

## Added and retained

| Area | Retained implementation and owner |
| --- | --- |
| XiaomiParts | Kotlin/Compose, compact Settings rows, icon selectors, expandable thermal/touch controls and translations; [device UX](../memory/xiaomiparts-device-ux.md) |
| Dolby / MiSound | Native stock effect controls, saved-state/communication recovery, independent translation commits and canonical branding; [audio](../memory/dolby-audio.md) |
| Haptics | Stock-backed effects/primitives and bounded fallback; [vibrator](../memory/haptics.md) |
| Camera | Finalized approved modes and compatibility guards; [camera](../memory/miuicamera.md) |
| Kernel / device services | Redline, kernel/HAL contracts, rootdir/SELinux integration and preserved thermal protection; [platform](../memory/kernel-frameworks.md) |
| Recovery | Native ROM recovery, PIN/read-only storage, local packages, checked installers and secure ADB action; [recovery](../memory/evox-recovery.md) |

MiSound's legacy tile component is an intentional compatibility bridge, not a
second Dirac backend. Model/headset branding stays untranslated; settings text
and placeholders use the separate resource commits. Kernel imports preserve
authorship; defconfigs are generated separately with the repository script.

## Removed or deliberately excluded

Retired Java/XML Parts UI, dead resources and identified obsolete services were
removed in their recorded component audits. Do not restore rejected universal
HIDL-to-AIDL shims, speculative allocator/linker replacements, aggressive realtime
tuning or unused device/SKU features. Keep upstream tests, required sensor HAL
code, icon licenses and explicitly non-product diagnostics.

The LZ4 OTA/snapshot experiment was withdrawn. It is not part of the current
recovery workflow. Standalone PBRP and old repository snapshots are historical
references, not active ROM dependencies.

## Current source verification

All 50 maintained repos/105 published heads were read back; all 41 configured
upstream routes have zero missing commits. The resolved manifest binds 44 build
routes. Four unchanged recovery patches reproduce the exact live overlay trees,
and all three runner preflights pass. Existing local edits were preserved.

Canonical upstream commits retain their IDs/messages; assisted fork-local changes
use the current disclosure rule. Translation changes remain separate from feature
implementations. Use [retained feature links](implementation-commits.md), not
superseded fixup IDs, for current source navigation.

## Acceptance limits and future work

Recorded Parts/audio/module/phone checks remain scoped to their stated artifacts.
Native-recovery PIN/local-package acceptance does not establish password, Weaver,
every image target or every storage scheme. The latest source refresh adds no new
ROM build, flash, CTS/VTS, acoustic/headset, car-projection or physical accessory
certification. Source branch heads do not identify the installed build.

Display color mismatch, haptics scale-zero/physical calibration and untested
peripheral paths remain in their topic owners. Do not enable torch intensity,
platform spatializer/head tracking, battery bypass, unsupported panel modes or
other speculative features from these notes alone. No new feature is promised or
scheduled; paused/restricted investigations stay paused until properly resumed.
