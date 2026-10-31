# Dolby equalizer error and translation review — 2026-10-31

## Changes

- [Equalizer enable error reporting](https://github.com/PocoF3Releases/hardware_xiaomi/commit/2d69c48f6f086ab838192fe3cb521782b28ee358): the new GEQ Turn on action previously discarded RuntimeException, assuming the controller always published an error. A native SET failure or readback mismatch could leave the prior activeState intact. Publish the existing equalizer error indicator locally, clear it on successful retry, and rethrow CancellationException.
- [Separate localization commit](https://github.com/PocoF3Releases/hardware_xiaomi/commit/8119f09b8af17ea23ec3aebea6b40137eac27408): add all 17 new control/section/bypass strings to the remaining 77 locale folders. Existing Russian text is unchanged. Locale text was authored with AI assistance after the public Google translation endpoint rate-limited the initial batch, which was stopped; no native-speaker review is claimed.

## Verification

Extracted Kotlin enable-action regression fails on the original body with Native failure was not shown; the final body passes failed-write reporting, successful retry clearing and cancellation propagation. The extraction exposes the launch Job for assertions without changing the tested action body. Fixtures remain private under ~/evo/.repo/dolby-review-20261031; none are added to the production repository.

All 17 keys are present in all 78 supported locale directories. XML parsing, duplicate names, format placeholders and git whitespace checks pass. AAPT2 compiles the complete resource directory. Shared words such as Dutch Games are valid translations, not a reason to force different spelling. No source/index rebuild or untranslated English placeholder values were inserted to fill gaps.

XiaomiDolby builds successfully with the checkout user product and -j4; Kotlin, resource linking, R8, signing and dexpreopt complete. APK SHA-256: `60d02053f4ef24083d93c4a837f2a7410c9f1ecfac6aca4b364e45a3f8d8ac2e`. The build retains the toolchain warning that this R8 compiler reports API 37 above its supported API 36; it is not suppressed or attributed to the locale/error fix. No installclean or full ROM build was run.

No device installation or fresh acoustic/backend test was performed for these two changes. The native DAP protocol, tuning values, saved-settings keys and translations in Russian are unchanged. Prior hardware limitations in the [DAP audit](dolby-dap-params-20261031.md) still apply.
