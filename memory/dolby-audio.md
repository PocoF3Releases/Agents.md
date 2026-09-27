# Dolby and AC-4

## Scope and ownership

Alioth uses legacy Audio HAL 6.0 / DAX3-era components including `libhwdap.so`, `libswgamedap.so` and `libswvqe.so`. Blob presence, UUIDs and control acknowledgments do not establish audible processing. Do not assume modern spatializer support or transplant a Codec2 design.

Standalone `hardware/xiaomi/dolby` owns app/UI and shared DMS policy; frameworks/av owns native lifecycle, flags and effect transport; common/device configuration owns genuine platform opt-ins. [Source ownership and observed heads](repositories/TRACKED_HEADS.yaml).

Android 16 sample playback was subsequently confirmed by the maintainer; see [V-A16](validation.md#v-a16). Detailed measurements below retain their Android 17 provenance.

## Accepted AC-4 integration

The opted-in OMX path uses `media.dolby_ac4_21_entry_tables`: stock table A is 256 bytes; B/C each have 21 entries / 84 bytes. Private request size is 452 bytes with tables at `0x1c`, `0x11c`, `0x170`; legacy size remains 444 bytes. The opted-in index is `0x6f400009`, not default `0x6f400008`. Keep the default shared enum and Codec2 behavior unchanged. Relevant framework revisions: `801d9c6ecd`, `6c0db963ed5111efb8d6e9820de7b19dc241ab05`, `ae242b56da334c3b1605bbbc526cc4e8a47cce45`.

Common `428db4a` enables the option; `e019493` packages `libstagefright_omx.vendor` and restores `/vendor/lib/vndk/libstagefright_omx.so` -> `/vendor/lib/libstagefright_omx.so`. Wrong index caused UnsupportedIndex `0x8000101a` / configure -1010. After that correction, `Error 4 in dlb_ac4dec_input_stage_open` came from the obfuscated helper-library lookup / `function_a`, `function_b`, `function_c` resolution, not bad table contents. [V-AC4](validation.md#v-ac4) owns decoding, audible acceptance and test limits.

Do not import a complete legacy VNDK, redirect current OMX foundation to v33, or add unsupported foundation/xlog links. Shipped Dolby already uses `libstagefright_foundation-v33.so`; current OMX uses current foundation. Stock/Shipped Alioth decoder code/rodata matched after dependency rewriting. Marble's 64-bit Codec2 component is not this ABI; its B/C dimensions were not established. Audio and OMX services remain 32-bit; no 64-bit-only migration was delivered. [Full audit and failure progression](../archive/2026-09-26/today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## VoIP, game audio and recovery

Historical voice-chat symptoms were quieter/thinner speaker sound and delayed recovery. Relevant state includes communication playback/recording, route, DAP/offload, track flags, bypass/pregain, VQE and game DAP. Preserve the requested enabled preference while bypassing unsuitable processing and restoring media state. A coarse app-only bypass is not stock-equivalent. Keep calls, call screening and communication distinctions; confirm native state before persisting. Use opt-in VQE and acknowledged effect attachment/recovery, not competing controllers.

Recorded signatures included `MODE_IN_COMMUNICATION`, `voice-speaker-stereo`, ACDB 10011 -> 15 and `SET_CONFIG ... Invalid argument`. Do not change ACDB mappings or copy a MIUI whitelist whose 16 kHz mono/property assumptions are absent. A vendor_init denial on `vendor_dolby_config_prop` explained configured qdsp but native `control=none, captured=0`; establish property/SELinux ownership before interpreting retries. Empty override XML may correctly mean native factory tuning. Historical package `co.aospa.dolby.xiaomi` used `.DolbySettingsActivity`, not an assumed DolbyService; recheck current source before commands.

[V-DOLBY](validation.md#v-dolby) separates historical transport ACKs from acoustic proof. Material 3/expressive UI must not imply unsupported audio capabilities. [Reconciled detailed lessons](../archive/2026-09-26/today/2026-09-24-rework-memory-reconciliation.md).

## Latest UI and documentation changes

September 24 [59188cf](https://github.com/PocoF3Releases/hardware_xiaomi/commit/59188cf) restores separate current-profile/all-profile reset icon buttons with existing confirmation dialogs. Built-in profile names resolve from current Compose resources via ui/ProfileLabel.kt rather than cached engine strings; summary, picker, equalizer heading and custom-profile base selectors follow language changes. User-created names remain literal. Russian resources already existed; this fixes stale display labels, not missing translations. [V-UI](validation.md#v-ui).

[3b8b33e](https://github.com/PocoF3Releases/hardware_xiaomi/commit/3b8b33e) corrects dolby/Readme.md: independent default-off audio.legacy_dap_integration and media.dolby_ac4_21_entry_tables gates, product/package ownership and accepted AC-4 scope. It adds no runtime behavior.
