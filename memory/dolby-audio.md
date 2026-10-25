# Dolby and AC-4

## Scope and ownership

Alioth uses legacy Audio HAL 6.0 / DAX3-era components including `libhwdap.so`, `libswgamedap.so` and `libswvqe.so`. Blob presence, UUIDs and control acknowledgments do not establish audible processing. Do not assume modern spatializer support or transplant a Codec2 design.

Standalone `hardware/xiaomi/dolby` owns app/UI and shared DMS policy; frameworks/av owns native lifecycle, flags and effect transport; common/device configuration owns genuine platform opt-ins. [Source ownership and observed heads](../state/repositories.yaml).


## Accepted AC-4 integration

The opted-in OMX path uses `media.dolby_ac4_21_entry_tables`: stock table A is 256 bytes; B/C each have 21 entries / 84 bytes. Private request size is 452 bytes with tables at `0x1c`, `0x11c`, `0x170`; legacy size remains 444 bytes. The opted-in index is `0x6f400009`, not default `0x6f400008`. Keep the default shared enum and Codec2 behavior unchanged. Relevant framework revisions: the historical candidate, the historical candidate, the historical candidate.

Common [428db4a](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/428db4a8318ba1c109ced5526e2596d8d9e88279) enables the option; [e019493](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/e019493ff423ad760403e54beb692f92d9089ad2) packages `libstagefright_omx.vendor` and restores `/vendor/lib/vndk/libstagefright_omx.so` -> `/vendor/lib/libstagefright_omx.so`. Wrong index caused UnsupportedIndex `0x8000101a` / configure -1010. After that correction, `Error 4 in dlb_ac4dec_input_stage_open` came from the obfuscated helper-library lookup / `function_a`, `function_b`, `function_c` resolution, not bad table contents. [V-AC4](../state/validation.md#v-ac4) owns decoding, audible acceptance and test limits.

Do not import a complete legacy VNDK, redirect current OMX foundation to v33, or add an unproven foundation compatibility link. Shipped Dolby already uses `libstagefright_foundation-v33.so`; current OMX uses current foundation. Stock/Shipped Alioth decoder code/rodata matched after dependency rewriting. Marble's 64-bit Codec2 component is not this ABI; its B/C dimensions were not established. Audio and OMX services remain 32-bit; no 64-bit-only migration was delivered. [Full audit and failure progression](dolby-audio.md).

## VoIP, game audio and recovery

Historical voice-chat symptoms were quieter/thinner speaker sound and delayed recovery. Relevant state includes communication playback/recording, route, DAP/offload, track flags, bypass/pregain, VQE and game DAP. Preserve the requested enabled preference while bypassing unsuitable processing and restoring media state. A coarse app-only bypass is not stock-equivalent. Keep calls, call screening and communication distinctions; confirm native state before persisting. Use opt-in VQE and acknowledged effect attachment/recovery, not competing controllers.

Recorded signatures included `MODE_IN_COMMUNICATION`, `voice-speaker-stereo`, ACDB 10011 -> 15 and `SET_CONFIG ... Invalid argument`. Do not change ACDB mappings or copy a MIUI whitelist whose 16 kHz mono/property assumptions are absent. A vendor_init denial on `vendor_dolby_config_prop` explained configured qdsp but native `control=none, captured=0`; establish property/SELinux ownership before interpreting retries. Empty override XML may correctly mean native factory tuning. Historical package `co.aospa.dolby.xiaomi` used `.DolbySettingsActivity`, not an assumed DolbyService; recheck current source before commands.

[V-DOLBY](../state/validation.md#v-dolby) separates historical transport ACKs from acoustic proof. Material 3/expressive UI must not imply unsupported audio capabilities. [Reconciled detailed lessons](dolby-audio.md).

## Retained UI behavior

September 24 [59188cf](https://github.com/PocoF3Releases/hardware_xiaomi/commit/59188cf) restores separate current-profile/all-profile reset icon buttons with existing confirmation dialogs. Built-in profile names resolve from current Compose resources via ui/ProfileLabel.kt rather than cached engine strings; summary, picker, equalizer heading and custom-profile base selectors follow language changes. User-created names remain literal. Russian resources already existed; this fixes stale display labels, not missing translations. [V-UI](../state/validation.md#v-ui).

[3b8b33e](https://github.com/PocoF3Releases/hardware_xiaomi/commit/3b8b33e) corrects dolby/Readme.md: independent default-off audio.legacy_dap_integration and media.dolby_ac4_21_entry_tables gates, product/package ownership and accepted AC-4 scope. It adds no runtime behavior.

## Audio HAL VNDK paths

The stock 32-bit VNDK directory contains regular OMX/foundation/xlog files.
Shipped AC-4/DDP/plugin libraries use rewritten `libstagefright_foundation-v33.so`;
current vendor OMX uses current foundation by basename. `libxlog.so` is already
packaged at `vendor/lib/vndk/libxlog.so`, referenced by audio and sound-trigger
HALs. No evidence justified additional foundation or 64-bit VNDK symlinks.

A historical config audit parsed all audio XMLs, resolved policy includes/routes,
checked microphone-array lengths and both 769-path mixer graphs, and found
monotonic volume curves. Sixteen obsolete COMP1/COMP2 controls were removed.
Twenty effect libraries being mapped is not audible activation proof; idle DSP
control-read errors must not be mistaken for an active-route failure. Bluetooth,
USB, calls, recording and hotword paths require their actual endpoints.

## Final capture-library correction

`external/tinycompress:lineage-24.0` restores full-buffer blocking capture reads
required by the legacy HAL, consumes POLLIN-ready data and accumulates short
reads. Final the historical candidate terminates on backend EOF and clears poll state. Audio HAL
links libtinycompress. Recorded host sanitizer and ARM/ARM64 executable/compiler
checks passed; that earlier check did not establish installed inclusion. The
[October 25 recording audit](../evidence/recording-voice-20261025.md) now confirms
the original installed/build library match. A later
[short-read recovery fix](../evidence/voice-message-recovery-20261025.md) was
temporarily tested and the original phone libraries restored; the new build
artifact requires a ROM rebuild. This is not proof
all Telegram/WhatsApp voice-message failures are fixed. Source identity and
cross-repository grouping: [audit](../state/changelog-audit.md).

## Legacy output callback ABI

Stock primary C device API3.0 does not guarantee newer stream callback slots. Guard them before reading private state; HIDL version upgrades do not repair the backend ABI. [Targeted fixes and validation](../evidence/hal-regressions-20261024.md) retain HAL6.0 and stock processing.

## Alioth native game-audio backend audit

The [October 25 audit](../evidence/dolby-backend-20261025.md) separates the shipped
Qualcomm switch/package protocol from the unrelated FPSOP controls, records
existing mixer/calibration coverage and records final qcom-qdsp APK phone
acceptance: three on/off cycles, active/inactive process restart, silent game/media
PCM playback and complete temporary-overlay restoration with SELinux enforcing.
A native control ACK is not audible processing or complete gameplay acceptance.

The [expanded audio/Parts audit](../evidence/alioth-audio-integration-20261025.md)
records the native MiSound EQ C-string contract, immediate game communication
bypass, native readback tests and consolidated commits. Existing karaoke/voice
hooks and VQE presence do not authorize global activation.

The [recording/voice audit](../evidence/recording-voice-20261025.md) confirms
native AEC/NS and PCM VoIP integration, targeted recording/duplex phone results
and the separate translation-resource history. No further DSP opt-in was justified.

The [voice-message/VoIP recovery audit](../evidence/voice-message-recovery-20261025.md)
records a reproduced compressed-capture short-read errno/stale-tail defect, its
standalone tinycompress fix, host/native shared-library regressions and codec/
restart/duplex acceptance. Nonblocking behavior and translation commits are separate.

The [MiSound recovery audit](../evidence/misound-recovery-20261025.md) records the
controlled-handover failure and repair, rapid communication start/stop and actual
earpiece/speaker tests for On, Off and disabled pause. Dolby needed no new fix.

The [control-loss/server-restart follow-up](../evidence/misound-control-restart-20261025.md)
fixes recovery after prolonged MiSound ownership contention, including initially
contested startup. Retain the control listener through bounded retries and restore
saved tuning on regain. Final APK tests cover server restarts and requested Off;
Dolby needed no additional source change.
