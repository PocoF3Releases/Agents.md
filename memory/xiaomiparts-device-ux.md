# XiaomiParts, device UX and localization

## Final dialog correction

Common-tree `3c30e7d416cd91e51c1c95ce81d55b20e60c570c` fixes `parts/src/org/lineageos/settings/thermal/ThermalSettingsFragment.java` / `showProfileDialog`: measure overlap with actual topPanel/buttonPanel, clip rows between them and add only required padding while preserving original padding. Update padding only when needed to avoid layout loops. This supersedes `db27251`, whose fixed-inset removal let rows draw below the title and Cancel. System/per-app dialogs share source, but only the System Profile result has supplied visual acceptance. [V-PARTS](../state/validation.md#v-parts).

## Preserve functionality

Thermal profiles retain the vendor-backed model and clearer names, icons and details. Per-app assignment must survive lifecycle changes without writing global preferences or resetting silently. Preserve Benchmark/Gaming touch enable, response, sensitivity and edge resistance. Historical routing used `appName`/`packageName`; storage used `gameMode,response,sensitivity,resistant` consumed by ThermalUtils. Guard missing nodes rather than assuming every stock control exists.

Preserve per-app refresh, Smooth Display, charging control, KGSL/GPU information, ZRAM/power controls and lifecycle-safe Clear Speaker. Smooth Display remains Alioth Settings overlay-owned. Prefer collapsible System Profile, top-right search/info, stable item sizes, consistent sliders, compact tonal selectors and correct scrolling. Avoid duplicate Android 16+ system-bar insets already owned by CollapsingToolbarBaseActivity. Presentation changes must not trade away working behavior.

MiSound headphone profiles do not establish a speaker mode. Historical `ro.vendor.audio.soundfx.type=mi` / `isSupportSpeaker` references were insufficient; explicit speaker switches were guarded for `thyme`, not Alioth. Do not port them blindly. [Detailed touch/MiSound lessons](dolby-audio.md).

## Translation workflow

Read target-local `parts/AGENTS.md`, AGENTS.md or TRANSLATING.md; resolve the current branch before changing strings. Compare base values/strings.xml with the locale and translate every missing user-visible key within the requested scope. Preserve resource/package identifiers, `%1$s`/`%d` placeholders, escaping, apostrophes and markup. Validate XML, missing/duplicate keys and placeholder equivalence. Keep translation commits resource-only unless code/UI work is requested. Honor manual/local translation requests; do not silently substitute an API workflow. Older notes record completed locale sets, not proof no strings were added later.

[Final UX record](xiaomiparts-device-ux.md) and [translation record](xiaomiparts-device-ux.md) preserve prior detail. No new UI build or per-app test is claimed by this consolidation.

## MiSound title correction

September 24 source change [e0fd9ba](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/e0fd9ba) hides both action-bar and collapsing titles in DiracActivity, sizes the toolbar to navigation content and disables expansion. The logo and back navigation remain. This prevents duplicate branding and blank expanded space. [V-UI](../state/validation.md#v-ui) records its untested-on-device status.

## September 28 source additions

Common 71b3157 extends the existing per-app touch page, not a duplicate game service. Alioth firmware-backed aim sensitivity, tap stability and three expert presets are added; response/sensitivity use range 1..5. Preserve old four-value profiles. Zero selects firmware defaults/individual tuning; apply expert presets last because individual writes disable expert mode. Global sampling owns its preset while enabled and refreshes the foreground profile when disabled. Other devices keep existing controls. Locale commits 5d1ff87 and 0290d37 extend translations; validate newly introduced strings separately. Stock/shipped/installed HAL identity and kernel modes were inspected; resource/host tests passed, but this is not full new-UI device acceptance.

0d7df19 reports buffered sysfs write failures, including close failures, instead of saving false success. Clear Speaker requests transient focus, prefers the built-in speaker, rejects communication mode, stops on focus loss/non-speaker routes/errors and is scoped to the visible screen. Refresh-service destruction state is visible to Binder callbacks. Host write tests and stub-assisted Java compilation passed; recorded node checks were on Android 16, not new Android 17 runtime certification. 9af4ed6 removes unused sensor helpers.

## Alioth ultrasound proximity

Alioth 05f9b24 patches the exact stock MIUS zero-result poll timeout branch to retry after its existing flush check and mutex unlock. Stock maps the eight-second idle timeout to EIO, causing repeated sensor-service errors. Preserve genuine errors and event handling. Extraction is guarded by stock/patched SHA-256, is idempotent and rejects unknown binaries; inspect extract-files for the exact hashes before operating on a new dump.

Recorded temporary mount stopped idle errors and delivered near/far events (0/5 cm); the maintainer reported proximity working in a call. This is scoped acceptance of that test, not proof for all call apps or other SM8250 devices. Keep the source extraction fix and packaged blob consistent; do not require a permanent root mount. Later AW8697 work is owned by [haptics](haptics.md).

## October 9 source checkpoint

Common `6916b8c` persists last successful per-app MIN/PEAK writes and retains
independent Smooth Display changes before restore/reapply, including recreation.
New APK device acceptance is pending. `cd19c9c` stages and validates the selected
regional thermal map, atomically publishes it and then restarts mi_thermald;
preparation failure retains the active map and daemon. Stock maps/limits unchanged.
See [reported validation](../state/validation.md#v-source-20261009).

## HBM brightness recovery — October 9 maintenance

If restoring SCREEN_BRIGHTNESS failed when disabling HBM, DisplayUtils discarded
the saved previous brightness and reported success. The fix keeps the backup,
reports failure and saves HBM off, then retries brightness recovery during boot
restoration. Failed sysfs disable retains the existing state. Successful recovery
clears the backup; an off state without a backup does not alter brightness.
[Host regression evidence](../state/validation.md#v-hbm-recovery).
