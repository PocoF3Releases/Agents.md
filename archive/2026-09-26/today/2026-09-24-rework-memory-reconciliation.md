# Rework memory reconciliation

Imported useful technical lessons from saved project notes and reconciled them with the current repository. This update does not rerun old tests or establish that historical commit IDs remain reachable. Local-memory paths are not needed to use this record.

## Dolby lifecycle and control evidence

Historical VoIP failures correlated `MODE_IN_COMMUNICATION`, a speaker-to-`voice-speaker-stereo` route transition, ACDB `10011` to `15`, and `EffectHAL ... SET_CONFIG ... Invalid argument`. The relevant design was mode-based Dolby bypass that preserves the voice path and requested enabled preference, then restores media state. Do not change ACDB mappings or transplant a game/package whitelist merely because audio becomes quiet; MIUI package-specific handling depended on a 16 kHz mono stream and `audio_game_sound_volume_gap_switch` unavailable in this AOSP context.

Historical implementation touched `DolbyEngine.kt`, `DolbyController.kt` and `DolbyAudioEffect.kt` in standalone `hardware/xiaomi/dolby`. Preserve communication/call/call-screening distinctions and vendor/Android effect ownership. Resolve current source before editing; old branch names and intermediate hashes are not current authority.

A past installation selected `ro.vendor.audio.dolby.dap.control=qdsp` in its build properties, but `vendor_init` was denied setting `vendor_dolby_config_prop`, leaving native state `control=none, captured=0`. The lesson is to inspect property ownership/SELinux before treating retry counts as evidence of a functioning DSP path. Shared DMS policy belongs with standalone Xiaomi hardware; do not duplicate ownership in the common tree.

A later historical capture reported `captured=1`, `attachmentAcknowledged=1`, pregain acknowledgement `23698`, and zero status/failure/retry counts during playback. Speaker tuning selection, profile changes and reset paths were acknowledged. This proves control transport/bookkeeping, not audible DSP output, all effect modes or acoustic quality. Empty profile XML maps can mean factory-native tuning with no user overrides; they do not by themselves mean missing tuning.

The historical app identity was `co.aospa.dolby.xiaomi`, settings activity `.DolbySettingsActivity`; a assumed `DolbyService` endpoint was incorrect. Confirm identities against current source before issuing device commands. Old MiSound probes changed settings and were not fully restorative; do not label them read-only. Old CodecProbe dex artifacts were not reusable merely because a filename existed.

## XiaomiParts / touch and MiSound

Benchmark/Gaming per-app controls must retain enable/disable plus response, sensitivity and edge-resistance settings. Historical routing opened `TouchSettingsFragment` with `appName` and `packageName`; profile storage carried `gameMode,response,sensitivity,resistant`, consumed by `ThermalUtils`. Package-specific controls should load/save the intended app profile instead of silently writing global persistent preferences.

The earlier UI migration used AndroidX `SeekBarPreference`; `CollapsingToolbarBaseActivity` owned Android 16+ system-bar insets. Avoid duplicate screen padding. The later accepted Thermal Profiles fix measures dialog panel overlap; it is not a reason to restore global/fixed inset workarounds.

MiSound headphone profile selection is not speaker-effect support. Historical `ro.vendor.audio.soundfx.type=mi` and `isSupportSpeaker` references did not prove Alioth support: explicit speaker switches found in the reference were guarded for `thyme`. Do not port those commands blindly or claim a new speaker mode is complete.

## Reconciled status, not a new backlog

- AC-4 is now validated for the recorded stereo sample and audible playback; older notes saying it is unvalidated are superseded.
- Thermal Profiles dialog fix is user-approved.
- Camera is finalized with accepted limits and no future work planned. Older paused/Stage-3/stock-app experiment plans are historical only.
- Rootdir cleanup and camera video fixes were already announced in the September 23 release. Old ownership-audit next steps do not automatically become active tasks again.
- Old 22-repository counts, local branch states and source heads are historical; use current remote tracking.
- `hardware/xiaomi` remains standalone; use `user` builds only and do not rebuild without an explicit request.
- VQE/game-effect enable properties and Dolby ACKs alone remain insufficient for claims about audible processing quality. No new testing of those features is asserted here.

This upload is documentation maintenance, not a new ROM feature or extension of today's AC-4/Parts-only functional changelog. Unrelated workstation/model/artwork memories were intentionally excluded.
