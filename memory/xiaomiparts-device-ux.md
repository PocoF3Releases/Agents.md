# XiaomiParts, device UX and localization

## Final dialog correction

Common-tree `3c30e7d416cd91e51c1c95ce81d55b20e60c570c` fixes `parts/src/org/lineageos/settings/thermal/ThermalSettingsFragment.java` / `showProfileDialog`: measure overlap with actual topPanel/buttonPanel, clip rows between them and add only required padding while preserving original padding. Update padding only when needed to avoid layout loops. This supersedes `db27251`, whose fixed-inset removal let rows draw below the title and Cancel. System/per-app dialogs share source, but only the System Profile result has supplied visual acceptance. [V-PARTS](validation.md#v-parts).

## Preserve functionality

Thermal profiles retain the vendor-backed model and clearer names, icons and details. Per-app assignment must survive lifecycle changes without writing global preferences or resetting silently. Preserve Benchmark/Gaming touch enable, response, sensitivity and edge resistance. Historical routing used `appName`/`packageName`; storage used `gameMode,response,sensitivity,resistant` consumed by ThermalUtils. Guard missing nodes rather than assuming every stock control exists.

Preserve per-app refresh, Smooth Display, charging control, KGSL/GPU information, ZRAM/power controls and lifecycle-safe Clear Speaker. Smooth Display remains Alioth Settings overlay-owned. Prefer collapsible System Profile, top-right search/info, stable item sizes, consistent sliders, compact tonal selectors and correct scrolling. Avoid duplicate Android 16+ system-bar insets already owned by CollapsingToolbarBaseActivity. Presentation changes must not trade away working behavior.

MiSound headphone profiles do not establish a speaker mode. Historical `ro.vendor.audio.soundfx.type=mi` / `isSupportSpeaker` references were insufficient; explicit speaker switches were guarded for `thyme`, not Alioth. Do not port them blindly. [Detailed touch/MiSound lessons](../archive/2026-09-26/today/2026-09-24-rework-memory-reconciliation.md).

## Translation workflow

Read target-local `parts/AGENTS.md`, AGENTS.md or TRANSLATING.md; resolve the current branch before changing strings. Compare base values/strings.xml with the locale and translate every missing user-visible key within the requested scope. Preserve resource/package identifiers, `%1$s`/`%d` placeholders, escaping, apostrophes and markup. Validate XML, missing/duplicate keys and placeholder equivalence. Keep translation commits resource-only unless code/UI work is requested. Honor manual/local translation requests; do not silently substitute an API workflow. Older notes record completed locale sets, not proof no strings were added later.

[Original UX record](../archive/2026-09-26/memory/xiaomiparts-device-ux.md) and [translation record](../archive/2026-09-26/memory/localization.md) preserve prior detail. No new UI build or per-app test is claimed by this consolidation.

## MiSound title correction

September 24 source change [e0fd9ba](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/e0fd9ba) hides both action-bar and collapsing titles in DiracActivity, sizes the toolbar to navigation content and disables expansion. The logo and back navigation remain. This prevents duplicate branding and blank expanded space. [V-UI](validation.md#v-ui) records its untested-on-device status.
