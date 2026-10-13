# Android 17 implementation and verification status

Observed October 14, 2026. This is a source and component acceptance record,
not a new ROM release declaration. [Current heads](repositories.yaml) and the
[post-sync audit](../evidence/post-sync-source-audit-20261011.json) own source identity.
Older evidence revisions below are historical tested candidates, not branch tips.

## Added and retained

- XiaomiParts migrated from Java/XML screens to Kotlin/Compose, with compact
  settings rows, adaptive layouts, consistent icons and selected icon circles.
  Thermal controls remain expandable without repeating the selected profile.
  Touch tuning, refresh controls, speaker cleaning and display controls remain.
- Dolby follows Parts styling with compact game controls and icon selectors.
  Approved branding and genre icons remain; no replacement UI experiment is pending.
- MiSound replaces Dirac naming and implementation. Saved settings and both
  current and legacy Quick Settings tiles work. The legacy component bridge is
  intentional compatibility for existing tiles, not a second Dirac implementation.
- MiSound DSP work runs on a process-owned worker; immutable state feeds the UI
  and tiles. Accepted writes survive navigation, retries are bounded, and audio
  service restart recovery preserves settings.
  [Final compiled and installed candidate](../evidence/legacy-hardware-research-20261011.json).
- Parts/Dolby/SystemUI translation gaps, including Kabyle, were addressed.
  Placeholder, inheritance, duplicate-key and AAPT2 checks passed in the recorded
  audit. MiSound, Hi-Fi and headset model names use canonical untranslated names.
  [Translation audit and limits](../evidence/production-final-translations-20261011.json).
- Compatible Gerrit changes retained original authorship: IWLAN service config,
  FPC cancellation handling and flashlight recovery. Changes were adapted to
  current code rather than blindly enabling capabilities.
  [Component validation](../evidence/lineage-gerrit-applied-20261011.json).
- Removed block writeback throttling configuration and its manual UFS latency
  write. Kernel import and regeneration of all 12 defconfigs remain separate.
  [Configuration verification](../evidence/wbt-removal-20261011.json).

## Removed or deliberately excluded

Retired Parts Java/XML UI, unused proximity wrappers, unused resources and
temporary implementation harnesses were removed where identified. Authored
production test/documentation additions were omitted during cleanup; existing
upstream regression tests, required sensor test HAL code, icon license notices
and the explicitly non-product haptics renderer were retained.

The unused Dolby documentation image and generated Alioth Python cache were
removed in the recorded source audit. Approved production branding remains.

Do not reintroduce the rejected universal HIDL-to-AIDL shim, speculative allocator
replacement, memory-stat rename, hardcoded API-numbered linker configuration or
aggressive realtime scheduling. Source research found no need for these changes.
The audited 845 common/alioth vendor ELF files had no text relocations.
[Research findings](../evidence/legacy-hardware-research-20261011.json).

Aggregation overlays with no current consumers, unverified swappiness and TP10
tuning, popup-camera/UDFPS and other non-alioth changes were not applied.
Flashlight recovery does not establish hardware intensity support.

## How history was cleaned

The recorded first consolidation changed 205 Codex-attributed first-parent
commits into 181 feature commits across 14 maintained branches. Incremental UI
fixes were folded into their final feature implementations; unrelated changes and
upstream authorship remained separate. Commit descriptions were rewritten against
actual diffs rather than generic completion text.

A subsequent merge of translations into implementation commits was rejected and
corrected. Translation changes remain standalone resource commits, consolidated
by topic such as Parts device-control translations, without add/revert churn.
Independent kernel imports and generated defconfigs remain separate.

Before/after production trees and modes were compared; history-only rewrites
preserved approved behavior. Recovery refs and explicit expected-head
force-with-lease were used for authorized rewrites, followed by remote checks.
Earlier rewrite IDs are historical; use the source map for final heads.

## What is verified

- All 16 maintained A17 build checkouts are clean and match live fork heads after
  resync. No approved source implementation was lost.
- Parts/Dolby recorded UI checks covered compact rows, selectors, icons, margins
  and expanded/collapsed thermal controls on the phone. These are scoped visual
  checks, not every possible screen/font-scale combination.
- The final MiSound APK compiled and matched its installed hash. Saved toggles,
  scenes, presets, navigation persistence, both tiles and automatic audioserver
  restart recovery passed on an SDK 37 user build; original device settings were restored.
- Current kernel/selected partition metadata passed host VINTF compatibility:
  shipping API 30, FCM 7, kernel 4.19.325.
  [Exact metadata scope](../evidence/vintf-compatibility-20261011.json).
- Fingerprint cancellation, IWLAN binding and flashlight restart behavior have
  the bounded component evidence linked above. No enrolled-fingerprint unlock,
  carrier Wi-Fi calling or physical torch-strength fault certification is implied.

## Remaining work and candidate opportunities

The October 14 native-recovery run completed a fresh full production build,
packaging/VINTF/APEX-policy checks and no-wipe secure recovery OTA installation.
Android booted the new incremental under enforcing SELinux, with saved settings
and data integrity preserved. [Exact scope](../evidence/evox-native-recovery-20261014.md).
CTS/VTS, car projection and measured performance remain unestablished. Protected
credential support is a later, unpublished candidate awaiting build/device checks.

Framework sync selection is now explicit: the local override uses
PocoF3Releases/cnb for both framework repositories. Targeted sync passed without
changing their maintained heads. [Override and verification](../operations/framework-manifest.md)
also correct the earlier inherited-default interpretation.

Android Auto has a recorded framework registration fix, but wired/wireless
projection on the rebuilt ROM remains unverified. MiSound headset-specific routes
and live call bypass need suitable connected hardware/call conditions.

Torch intensity, USB webcam, Smart 5G and power-off alarms remain research
candidates requiring HAL, host, modem or RTC validation before enabling flags.
No new implementation is promised or scheduled by this record. Battery bypass,
platform spatializer/head tracking and full PWLE support remain unestablished.

The repeated post-reboot ADB disappearance has an observed Windows host recovery
procedure, not a proven universal USB/kernel fix. Recovery fastbootd acceptance
remains separate from the completed full-ROM OTA and scoped app verification.

[Current implementation commits](implementation-commits.md) links each retained feature to its repository.
