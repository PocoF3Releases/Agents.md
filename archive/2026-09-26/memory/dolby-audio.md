# Dolby / Xiaomi Audio Durable Knowledge

## Latest AC-4 validation — September 24

Alioth's opted-in 21-entry OMX integration now decodes the official 32-second stereo/48 kHz AC-4 sample to 6,144,000 PCM bytes with EOS; the user also confirmed audible playback on the rebuilt non-rooted user build. The necessary final device fix restores `/vendor/lib/vndk/libstagefright_omx.so` as a symlink to the current vendor OMX helper. No extra foundation/xlog symlinks were justified. Keep the private request/index changes default-off for other devices and do not generalize this result to Codec2 or all Dolby versions.

See [the detailed checkpoint](../today/2026-09-24-ac4-validation-and-thermal-dialog.md).

## Device limitation

Alioth uses legacy Audio HAL 6.0.

Modern Android spatial-audio support is out of scope for this device. Do not design the Dolby stack around unsupported modern spatializer assumptions.

## Stock proprietary components

Important Alioth/Xiaomi audio components include:

```text
libhwdap.so
libswgamedap.so
libswvqe.so
```

Stock properties/reference data indicate DAX3-era Dolby integration.

Blob presence and UUID registration alone do not prove that an effect path is active at runtime.

## Ownership

Preferred layering:

- app/policy/UI in `hardware/xiaomi/dolby`;
- framework-native lifecycle, track flags, attachment/recovery logic in `frameworks/av`;
- device/common properties/configuration in `sm8250-common` only when truly device/platform scoped.

Avoid putting global Dolby policy into device-specific glue when it belongs in the Dolby integration layer.

## VoIP/game-audio problem domain

Observed user-visible issue: enabling in-game voice chat can make speaker output quieter/thinner and may not immediately recover when voice chat is disabled.

Reference analysis found that stock Xiaomi behavior coordinates:

- DAP/offload state;
- track state;
- communication playback/recording lifecycle;
- route changes;
- bypass/pregain;
- game DAP / VQE.

A coarse app-only bypass is not equivalent to stock behavior.

## Durable implementation direction

Work completed across the project has included:

- bypassing inappropriate processing during calls/VoIP;
- tracking communication playback/recording lifecycle;
- confirming native settings before persisting state;
- opt-in VQE for game voice sessions;
- route synchronization;
- effect attachment acknowledgement/recovery;
- pregain recovery;
- hardened AudioEffect transport;
- track-flag forwarding;
- passive policy ownership rather than competing controllers.

## Reference rule

Use decompiled/vendor reference code to reconstruct behavior only where headers, call flow and stock state support the implementation.

Do not infer unsupported features from dormant code.

## UI direction

Dolby UI work has used Material 3 / expressive styling while preserving the actual legacy device capabilities.

UI polish must not imply unsupported spatial-audio features.

## Validation

Use a combination of:

- host/native tests;
- app tests;
- route/effect dumps;
- device logcat;
- actual game + VoIP reproduction.

Passing host tests does not substitute for full Alioth device acceptance.

## Historical rework lessons retained

Use mode-based communication handling rather than MIUI game whitelists when the symptom is shared across VoIP apps. Property/SELinux ownership must be established before interpreting DAP retries. Native attachment/pregain acknowledgments prove control transport, not acoustic output. Empty profile override maps may correctly use native factory tuning. Keep shared DMS/Dolby ownership in standalone `hardware/xiaomi`.

See [reconciled rework evidence](../today/2026-09-24-rework-memory-reconciliation.md) for failure signatures, historical validation and superseded status.
