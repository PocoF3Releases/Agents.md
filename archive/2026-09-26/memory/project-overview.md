# PocoF3Releases Project Overview

## Primary target

- Device: POCO F3
- Codename: `alioth`
- SoC family: Qualcomm SM8250 lineage / Snapdragon 870-class target
- ROM family: Evolution X
- Active development focus: Android 17 / AOSP-17
- Maintenance context also exists for Android 16

## Main repositories

Frequently relevant trees include:

```text
device_xiaomi_alioth
device_xiaomi_sm8250-common
device_xiaomi_camera
vendor_xiaomi_alioth
vendor_xiaomi_sm8250-common
vendor_xiaomi_camera
hardware_xiaomi
android_hardware_nxp_nfc
frameworks_av
frameworks_base
kernel_xiaomi_sm8250
references_code
```

## Ownership boundaries

General ownership rules used in the project:

- `device/xiaomi/alioth`: device-specific configuration.
- `device/xiaomi/sm8250-common`: shared SM8250 platform behavior.
- `device/xiaomi/camera`: Xiaomi camera compatibility/integration.
- `hardware/xiaomi/dolby`: Dolby application/policy integration.
- `hardware/nxp/nfc`: source-built NXP NFC HAL and Alioth SNxxx teardown/runtime behavior.
- `frameworks/av`: AudioFlinger/effect lifecycle and framework-native audio changes.
- kernel tree: display, power, input, upstream/backport and device-kernel fixes.

## Core development principle

Prefer preserving stock ABI/partition/runtime behavior and adapting compatibility boundaries rather than replacing working proprietary components with broad reimplementations.

For reverse-engineered/proprietary subsystems:

1. identify real stock call flow;
2. verify symbol/ABI expectations;
3. make the smallest required compatibility change;
4. retain fail-closed behavior where unsupported;
5. require build/runtime evidence before widening scope.

## Device-specific constraints

Alioth uses legacy Audio HAL 6.0.

Modern spatial-audio architecture is not a supported target for this device. Dolby work should stay within supported legacy DAP/offload/VQE/game-audio paths.

## Validation philosophy

Old logs, blob presence, UUID declarations, or source-string matches are evidence, not proof of runtime activation.

Prefer:

- build success;
- host/unit tests where relevant;
- actual device logs;
- symbol/ELF checks;
- partition/package inspection;
- feature-level functional tests.

## Knowledge routing

Fresh agents should use the root [CURRENT_STATE.md](../CURRENT_STATE.md) and [INDEX.yaml](../INDEX.yaml) to route directly to the relevant subsystem rather than scanning all dated records.

## Historical agent memory archive

The [2026-09-22 Codex memory export](../today/2026-09-22-codex-memory-import.md) preserves the complete stored memory collection, including original summaries, raw memory notes, and ad-hoc updates.

It is a **cold archive**. Consult it only for missing historical investigation details, provenance/conflict resolution, or explicit memory-recovery requests. Recheck live device and repository state before using an old claim. Newer subsystem records take precedence.
