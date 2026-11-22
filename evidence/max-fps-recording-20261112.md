# Maximum-FPS recording recheck — November 12, 2026

**Source/host checked; no demonstrated defect, source change or Android rebuild.**

Checked the current framework source (historical `53e0061d824e3c6c571aebe95fb7bfa83258b3e6`)
and its separate maximum-FPS implementation (historical `ff797bd505489ea4b7e3cba85b5dec9f9d0b1f93`).
The selected EvoX upstream is unchanged and contained. The local recovery overlay
and [recording-blur fixes](source-refresh-20261112.md#recording-blur) remain intact.
No empty commit, history rewrite or new product test/scaffolding was added.

## Verified behavior

- Maximum FPS has its own `config_screenRecorderHighRefreshRate` capability and
  `screenrecord_max_fps` preference. Neither blur opt-in nor Keep blur determines
  its availability or effective request in legacy, small-screen or large-screen UI.
- Supported-device preference defaults remain unchanged. Lower quality masks the
  effective maximum-FPS request while retaining the saved choice for later use.
  Both recording services apply the field before startup; live taps/camera changes
  preserve it without attempting to reconfigure an active encoder.
- Maximum mode follows the active physical display mode, bypasses only the normal
  recording cap, and checks default encoder/decoder size, alignment and frame-rate
  limits. Bitrate arithmetic uses a wide intermediate and clamps to encoder bounds.
  AVC/HEVC maximum mode lets the recorder choose a suitable profile/level; normal
  recording retains existing profile and cap behavior.
- Virtual-display rate/mirror configuration remains correctly forwarded through
  the current MediaProjection builder API. Devices without high-refresh opt-in
  retain the current ROM's legacy sizing, rate and bitrate behavior.

## Checks

| Host check | Result |
| --- | --- |
| Actual codec/sizing/configuration method bodies | 21 groups pass; includes 250 deterministic capability trials and 100 comparisons with the current upstream legacy methods |
| Actual complete parcel model and preference repository | 4,096 parcel round trips and 4,096 copy checks; 4 default profiles, 32 saved-choice profiles and 64 isolated writes pass |
| Actual intent factories and initial service methods | 4,096 legacy configurations and 4,096 Binder-start configurations pass; 4 startup-failure boundaries pass |
| Actual live service updates and request/gating expressions | 4,096 update-preservation combinations, 1,536 request combinations and 256 availability profiles pass |

The matrix covers four audio modes, both capture-target shapes, display IDs,
AVC/HEVC, Lower quality, maximum FPS and both blur choices. Encoder checks include
fractional limits, coupled dimensions, alignment, bitrate bounds/overflow, probe
failure cleanup and physical-rate versus application-rate selection. Java host
compilation passes `-Xlint:all -Werror`; Kotlin checks use checkout tools. Fourteen
plumbing source hashes and the recorder hash still match the clean checkout.
Independent review found no actionable maximum-FPS mismatch.

## Limits

Android Parcel/Intent/preferences/codec/display/recorder boundaries are modeled.
Some checks compile exact source fragments, not whole services or Compose UIs.
These results do not establish delivered/sustained FPS, recorded quality, hardware
codec selection, actual Binder integration or device rendering. No module/ROM
build, installclean, phone changes or flash was performed. A future rebuilt ROM
needs end-to-end recording/playback checks for runtime acceptance.

Inherited legacy app-selector default-display routing remains unchanged; no new
maximum-FPS regression was established there. Raw fixtures and receipts remain
private; this is the portable source/host result, not a new release manifest.
