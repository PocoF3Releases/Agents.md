# Alioth project history and working memory

Reconciled **2026-10-09** from source audit, maintained topics, recorded evidence
and this session's instructions. Portable repository memory; no account-memory
synchronization. Current heads, artifacts and test scope stay in their owners.

## Project and working agreement

POCO F3 / Redmi K40 (alioth), Mi 11X identity aliothin; Evolution X Android 17
is current in `~/evo`. A16 is separate; no active checkout identified. Recovery
uses Android 14 PBRP userspace in `~/pbrp-alioth` for A17 compatibility.
Use user builds, preserve unrelated edits and keep hardware/xiaomi standalone.
Camera is finalized unless explicitly reopened. Builds/flashing/history rewrites
need scoped authorization. Old records are evidence, never assignments.

## How the current implementation emerged

- September device integration: MIUI Camera native/JNI/cache work and 48MP,
  macro/front video; XiaomiParts, thermal/touch/refresh and MiSound redesign;
  Dolby routing/control recovery; charging/startup/kernel/display/NFC cleanup.
- September 23 camera acceptance: main 4K30/60 and ultrawide 1080p; unsupported
  ultrawide 4K guarded. True ultrawide 60fps unproven. Camera then closed.
- September 24: Dolby AC-4 stereo diagnostic and listening acceptance, corrected
  Thermal Profiles dialog. Dolby reset/localization and MiSound title source fixes.
- Late September: supported firmware touch controls and safer Parts lifecycle;
  temporary ultrasound correction accepted during a call. A16 clean-install
  AC-4 playback/release reported; artifact/date not identified.
- September 30–October 4: stock AW8697 driver/DTS and corrected gains 48/80/128;
  seven effects, three stock primitives, bounded PCM and isolated AAC/limited HE1
  renderer. Generated effects retired. Full app-facing RichTap/PWLE absent.
- October 5–7: PBRP release, FBE teardown/Format Data, shared-runtime sload fix,
  secure Qualcomm library lookup, hardware labels and haptic writes. Infrastructure
  now enforces; shared recovery remains permissive. Published assets and latest
  source are separate identities.
- October 7–8: atomic thermal maps, modem MCFG handling without optional metadata,
  readable cache markers, preserving external refresh changes; fuel-gauge/touch/
  fast-charge safeguards and kernel build maintenance. LOW_TICK uses a stock
  light-tick approximation. Scoped commit-reported tests do not certify a ROM.
- October 9: audited maintained organization sources and required camera input;
  regenerated cumulative full/short initial Telegram notes. Removed retired forks
  and upstream head inventories from ongoing tracking. No new build or flash.

## Decisions worth retaining

Do not restore unavailable forks or rebased patches by age/SHA alone. Compare
semantic behavior and current upstream ownership. AC-4 is the opted-in legacy
32-bit OMX path, not a donor Codec2/blanket VNDK migration. Root mounts are
research; production fixes belong in source/packaging/policy. Parked GPU/Turnip/
frame-generation work has no accepted general performance result. Keep thermal
protection. PBRP uses update_engine; external high-speed installer was not imported.

## Recover detail only when needed

[Current topics](../CURRENT_STATE.md), [sources](../state/repositories.yaml),
[validation](../state/validation.md), [releases](../state/releases.md),
[portable evidence](../evidence/README.md), and [archive skeleton](../archive/README.md).
Final topics retain useful rejected approaches and scoped acceptance. The empty
archive skeleton stays out of startup. This summary creates no new test, release or pending task.
