# Android 17 Device-Tree Workspace

## Purpose

This is the durable cross-tree map for POCO F3 / `alioth` Android 17 device-side work.

The working set consists of three directly related repositories:

```text
device/xiaomi/alioth          -> PocoF3Releases/device_xiaomi_alioth
device/xiaomi/sm8250-common   -> PocoF3Releases/device_xiaomi_sm8250-common
device/xiaomi/camera          -> PocoF3Releases/device_xiaomi_camera
```

A 2026-09-23 source archive was supplied with the complete working trees **including `.git` directories**. In a session where that archive is attached, the extracted trees are real non-shallow Git worktrees and may be edited/committed directly after verifying/normalizing archive metadata.

The archive itself is not stored in this knowledge repository. This file stores the durable topology and workflow; see the dated import record for the exact snapshot fingerprint and SHAs.

## Current Android 17 repository baseline

All three repositories use branch `aosp-17`, track `origin/aosp-17`, and the imported local HEADs matched the live GitHub branch heads when verified on 2026-09-23.

```text
PocoF3Releases/device_xiaomi_alioth
branch: aosp-17
HEAD: 503f821f233a9821d770db863a01ac8abc08732f

PocoF3Releases/device_xiaomi_sm8250-common
branch: aosp-17
HEAD: 6e964d1447daa2e90007d36115ba4975f1309360

PocoF3Releases/device_xiaomi_camera
branch: aosp-17
HEAD: 433cf879cb10dcf3e682ea515ebc507170c6b3d8
```

Before making a new patch from an uploaded workspace snapshot, compare each local `HEAD` with the current remote `aosp-17` head. Do not build new work on a stale archive snapshot without deliberately rebasing/resetting/fetching as appropriate.

## Cross-tree ownership and dependency graph

### `device/xiaomi/alioth`

Device-specific POCO F3 configuration.

Verified relationships:

```text
BoardConfig.mk
  -> include device/xiaomi/sm8250-common/BoardConfigCommon.mk

device.mk
  -> inherit device/xiaomi/sm8250-common/kona.mk
  -> include device/xiaomi/camera/miuicamera.mk
  -> inherit vendor/xiaomi/alioth/alioth-vendor.mk

lineage_alioth.mk
  -> TARGET_USES_MIUI_CAMERA := true
  -> TARGET_INCLUDES_MIUI_CAMERA := true
  -> inherit device/xiaomi/alioth/device.mk
```

Use this tree for Alioth-only behavior: board/device flags, Alioth overlays, display/audio tuning, device thermal/health implementation, device-specific SELinux, properties, and proprietary-file ownership.

### `device/xiaomi/sm8250-common`

Shared Qualcomm SM8250/Kona platform configuration used by Alioth and related devices.

Important ownership includes:

- `BoardConfigCommon.mk` for common architecture/kernel/partition/platform board configuration;
- `kona.mk` for shared product packages, permissions, platform features and vendor inheritance;
- common audio, media, Bluetooth, Wi-Fi, rootdir/init, overlays and SELinux;
- XiaomiParts under `parts/`;
- common proprietary-file lists and extraction tooling.

`kona.mk` includes `XiaomiParts` in `PRODUCT_PACKAGES` and inherits:

```text
vendor/xiaomi/sm8250-common/sm8250-common-vendor.mk
```

The XiaomiParts subtree contains its own `parts/AGENTS.md`; read it before translation/localization work in `parts/`.

### `device/xiaomi/camera`

Shared Xiaomi/MiuiCamera compatibility and integration tree.

`alioth/device.mk` includes:

```make
include device/xiaomi/camera/miuicamera.mk
```

`miuicamera.mk` owns the integration of camera permissions/configuration/device-feature XMLs, MiuiCamera compatibility packages/shims, camera SELinux, overlay packaging, and vendor camera inheritance:

```text
vendor/xiaomi/camera/camera-vendor.mk
```

Camera feature development remains **paused**. The tree is available as part of the device-tree workspace and may be inspected when another device-tree change depends on it, but do not resume abandoned MiuiCamera/VideoSAT feature experiments unless the user explicitly reopens camera work. For that recovery state, read `continue-later/CAMERA.md`.

## Working from an uploaded full-Git archive

ZIP extraction can lose Unix executable and symlink metadata. A raw extracted workspace may therefore look dirty even when its source contents match Git exactly.

For the 2026-09-23 archive, the only extraction-induced differences were:

```text
alioth:
  extract-files.py       100755 -> 100644
  reorder-libs.py        100755 -> 100644
  setup-makefiles.py     100755 -> 100644
  vendorsetup.sh         100755 -> 100644

sm8250-common:
  .clang-format          missing symlink
  extract-files.py       100755 -> 100644
  setup-makefiles.py     100755 -> 100644
  sort-blobs-list.sh     100755 -> 100644

camera:
  extract-files.py       100755 -> 100644
  reorder-libs.py        100755 -> 100644
  setup-makefiles.py     100755 -> 100644
```

The tracked `sm8250-common/.clang-format` entry is a symlink whose target is:

```text
../../../build/soong/scripts/system-clang-format
```

Restore archive metadata before editing/committing. After normalization, all three imported worktrees were clean:

```text
## aosp-17...origin/aosp-17
```

Do not accidentally commit ZIP-induced mode changes or the missing `.clang-format` symlink as source changes.

## Safe patch workflow

For future work using a supplied full-Git archive:

1. Extract the archive while preserving `.git`.
2. Restore any ZIP-lost executable/symlink metadata and confirm `git diff --summary` is empty.
3. Run `git status --short --branch` in all three repositories.
4. Confirm the target repository's local `HEAD` against live `origin/aosp-17` / GitHub before editing.
5. Read the relevant existing subsystem memory and source-local `AGENTS.md` files before changing code.
6. Make the smallest change in the repository that owns the behavior.
7. Verify with `git diff --check` plus the narrowest relevant build/static test.
8. Commit in the **actual repository being changed**. Do not combine unrelated alioth/common/camera changes into one repository commit.
9. Follow `memory/git-history-conventions.md` for subjects and AI attribution.
10. Push only after the patch/verification state is coherent.

## Commit subject scope

Use repository-scoped subjects consistent with existing project history, for example:

```text
alioth: <area>: <change>
sm8250-common: <area>: <change>
camera: <area>: <change>
```

Camera feature work is still governed by the paused-camera rule even though the camera Git tree is present in the workspace.

## Source precedence

When this device-tree workspace and older Agents records disagree:

1. current live repository state and current device/runtime evidence;
2. a freshly verified full-Git workspace snapshot;
3. current durable subsystem memory / current dated record;
4. older historical notes.

Never assume an uploaded archive remains current indefinitely simply because it contains `.git` history.

## Post-resync ownership checkpoint

See [the latest repository index](../today/2026-09-23-repository-resync-index.md) for current heads. `hardware/xiaomi` is a standalone reusable integration repository and stays there; directory relocation alone is not portability. Platform patch removal requires an equivalent device-side extension point and evidence that behavior is preserved. No migration was performed during this index refresh.

## September 24 baseline update

See [current baseline checkpoint](../today/2026-09-24-repository-baseline-alignment.md) for current branches, mandatory camera dependencies and documentation updates. This supersedes earlier checkout/head routing, not historical test evidence.
