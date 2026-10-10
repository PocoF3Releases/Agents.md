# XiaomiParts, device UX and localization

## UI history

The October 10 Compose screens supersede the old XML dialog-padding and MiSound toolbar work. Historical acceptance remains in [V-PARTS](../state/validation.md#v-parts) and [V-UI](../state/validation.md#v-ui); do not apply those retired view-specific fixes to Compose.

## Preserve functionality

Thermal profiles retain the vendor-backed model and clearer names, icons and details. Per-app assignment must survive lifecycle changes without writing global preferences or resetting silently. Preserve Benchmark/Gaming touch enable, response, sensitivity and edge resistance. Historical routing used `appName`/`packageName`; storage used `gameMode,response,sensitivity,resistant` consumed by ThermalUtils. Guard missing nodes rather than assuming every stock control exists.

Preserve per-app refresh, Smooth Display, charging control, KGSL/GPU information, ZRAM/power controls and lifecycle-safe Clear Speaker. Smooth Display remains Alioth Settings overlay-owned. Compose owns edge-to-edge insets through its scaffold; do not add legacy toolbar insets. Presentation changes must not trade away working behavior.

MiSound headphone profiles do not establish a speaker mode. Historical `ro.vendor.audio.soundfx.type=mi` / `isSupportSpeaker` references were insufficient; explicit speaker switches were guarded for `thyme`, not Alioth. Do not port them blindly. [Detailed touch/MiSound lessons](dolby-audio.md).

## Translation workflow

Read target-local `parts/AGENTS.md`, AGENTS.md or TRANSLATING.md; resolve the current branch before changing strings. Compare base values/strings.xml with the locale and translate every missing user-visible key within the requested scope. Preserve resource/package identifiers, `%1$s`/`%d` placeholders, escaping, apostrophes and markup. Validate XML, missing/duplicate keys and placeholder equivalence. Keep translation commits resource-only unless code/UI work is requested. Honor manual/local translation requests; do not silently substitute an API workflow. Older notes record completed locale sets, not proof no strings were added later.

## Touch and lifecycle foundations

Keep the existing per-app service and four-value profile contract. Alioth aim/stability/expert settings use separate keys; expert presets apply last because individual writes disable expert mode. Global polling takes priority and replays the foreground profile when disabled. Other SM8250 devices retain legacy dispatch. Sysfs persistence follows successful writes including close. Clear Speaker is visible-screen scoped, requests transient focus, rejects communication mode and stops on focus/routing/error loss. Historical Java/stub tests do not certify Android 17.

## Alioth ultrasound proximity

Alioth 05f9b24 patches the exact stock MIUS zero-result poll timeout branch to retry after its existing flush check and mutex unlock. Stock maps the eight-second idle timeout to EIO, causing repeated sensor-service errors. Preserve genuine errors and event handling. Extraction is guarded by stock/patched SHA-256, is idempotent and rejects unknown binaries; inspect extract-files for the exact hashes before operating on a new dump.

Recorded temporary mount stopped idle errors and delivered near/far events (0/5 cm); the maintainer reported proximity working in a call. This is scoped acceptance of that test, not proof for all call apps or other SM8250 devices. Keep the source extraction fix and packaged blob consistent; do not require a permanent root mount. Later AW8697 work is owned by [haptics](haptics.md).

## HBM brightness recovery — October 9 maintenance

Common `6916b8c` preserves successful MIN/PEAK writes and independent Smooth Display changes across refresh-service recreation. `cd19c9c` validates/stages regional thermal maps, atomically publishes then restarts mi_thermald; preparation failure retains the active map/daemon. Stock limits remain unchanged. HBM disable keeps a brightness backup on settings failure, reports failure and retries during boot; failed sysfs disable retains enabled state. An off state without a backup never changes brightness. [Source evidence](../state/validation.md#v-source-20261009), [HBM tests](../state/validation.md#v-hbm-recovery).

## October 10 touch controls

Common [b1ff3a7](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/b1ff3a7) routes zero response/sensitivity through the existing Alioth reset helper. FocalTech modes 2/3 accept 1–5, clamp raw zero to 1, and use firmware default 3. Explicit tuning and other-device dispatch are preserved.

[c06d749](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/c06d749) replaces the expert slider with a tuning-mode selector, groups main/fine manual adjustments, and keeps edge protection independent. Off/preset/global-override states hide controls that do not apply. The page queries Alioth HAL ranges, reads the edge default, preserves old integer presets and manual values, and offers per-app reset without changing enable state. Help replaces the unrelated thermal information/search actions on this page. Firmware presets are alternatives to manual tuning, not quality rankings; maximum values are not universally better.

The global responsiveness setting takes priority; saved per-app tuning is paused until it is disabled. Manual zero restores firmware defaults. Edge zero explicitly disables filtering; a new/reset Alioth profile uses the HAL default (2 in the inspected kernel). The global option does not change display refresh rate. New strings use Android resource fallback; retained locale files are untouched. Host state tests do not establish translated or rendered UI acceptance.

[Validation and deployment limits](../state/validation.md#v-device-20261010).

## Kotlin and Compose migration — October 10

Common `7c9eb73` finishes eight feature-scoped commits: shared Compose/utilities, display, global touch polling, speaker, MiSound, refresh modes, thermal/touch/reference, and entry-point/resource cleanup. All source folders are Kotlin; old layouts/preference XML/custom preference views and unused drawables are removed. Keep translated strings/arrays, launcher/tile/profile icons and the cleaning tone. Default DP preferences, package keys, boot/manifest entry points, sysfs/HAL protocols and regional policy tables remain compatible.

Use checkout-provided AndroidX and Soong’s matching Compose compiler (inspected UI 1.12.0-alpha01, Material3 1.5.0-alpha16, Kotlin/Compose compiler 2.2.0); do not introduce Gradle or replace platform modules. Screens refresh hardware-owned state on resume. Row switches and sliders carry accessible semantics. Profile detail formatting uses the non-formatting resource overload when no arguments exist, preserving literal percent text.

[Validation and integration limits](../evidence/device-20261010.md#compose-migration). The initial renamed test app did not establish system-UID/HAL behavior. The subsequent production-app rework is recorded separately below. [Build guard](../operations/android-tooling.md#build-environment) preserves incremental output; a module dry run is not proof of bounded execution.

## Production Compose adaptation — October 10

Common `4919bf4` aligns Parts with the maintainer’s ROM Settings: platform surface tokens and variable fonts, compact font-aware toolbars, grouped outer/inner corners, 2 dp row gaps, pill primary switches and check/cross thumbs. Thermal rows separate profile selection from touch actions. Touch keeps presets, manual main/fine controls and independent edge protection. Reference lists use consistent Compose outline icons on tonal circles; details use padded text and separate CPU panels. Choice radio groups scroll and dismiss on selection or Back. [Verification](../evidence/device-20261010.md#settings-aligned-compose-revision).

Keep checkout dependencies: Material3 1.5.0-alpha16, runtime/UI 1.12.0-alpha01. Runtime 1.13.0-alpha01 release notes were checked (mutation-policy and saved-state APIs, minification flag syntax); using those APIs would require a separately reviewed shared SDK update. No shared prebuilt, build config or resource IDs changed for this adaptation.

[Production verification](../evidence/device-20261010.md#production-compose-adaptation) distinguishes staged XiaomiParts-only installation, actual system-UID checks and hardware readback from host fixtures. Reuse isolated compiler/dex tools with temporary outputs; never infer bounded work from a module dry run.

The pinned toolbar, bounded wide-window content and consumed edge/keyboard insets remain. Decorative AGSL/blur headers were retired to match Settings. Slider thumb/track morphs, fine/system expansion springs, discrete values and gesture-end persistence remain. Activities stay explicitly resizable without fixed orientation. Larger-font dialog, landscape and keyboard screenshots were checked on the production app.

Feedback uses amplitude-capable Alioth touch waveforms, 14 ms non-repeating/40 ms throttled, respecting user/view settings with platform fallback. Alioth has no PWLE/envelope capability; VibrationEffect.Builder envelope/preset methods are API 37.2, absent this API-37 checkout. Do not fake capabilities or upgrade shared SDK modules for an app test. Speaker data source must be set before preferred-device/listener requests; native MediaPlayer returns NO_INIT before initialization.

Production is tested through a staged single-app `/data/app` update with UID 1000/Enforcing. That update overrides later ROM base APKs: inspect `pm path` and remove the system-app update through package manager before ROM-base acceptance. Keep screenshots/recordings and raw preferences private; publish sanitized evidence. Original hardware/user settings are restored after tests.
