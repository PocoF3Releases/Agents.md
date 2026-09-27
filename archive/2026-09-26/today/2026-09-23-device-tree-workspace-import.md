# 2026-09-23 — Android 17 Device-Tree Full-Git Workspace Import

## Scope

A full source archive was supplied containing these three POCO F3 Android 17 device trees, including each repository's `.git` directory:

```text
alioth/
sm8250-common/
camera/
```

The purpose of this import was to establish a commit-capable local workspace for future device-side work and persist enough metadata in `Agents.md` that a later session can recover the source topology without rediscovering it.

## Archive identity

```text
size:   14,007,102 bytes
sha256: 40a675158fb9570e33709c25005cd19b46e0d0462fb7e0ac54172f018e23d009
```

The archive bytes are not stored in this repository; this fingerprint identifies the imported snapshot used for this record.

## Verified repository state

### Alioth device tree

```text
repository: PocoF3Releases/device_xiaomi_alioth
remote:     https://github.com/PocoF3Releases/device_xiaomi_alioth
branch:     aosp-17
upstream:   origin/aosp-17
HEAD:       503f821f233a9821d770db863a01ac8abc08732f
commits reachable from HEAD: 186
tracked files: 66
shallow repository: false
git fsck --no-dangling: clean
```

HEAD commit:

```text
503f821f233a9821d770db863a01ac8abc08732f
2026-09-19T08:48:57+03:00
alioth: Expose stock speaker tuning without platform spatial audio
```

Remote refs carried in the archive include `aosp-15`, `aosp-16`, and `aosp-17`.

### SM8250 common device tree

```text
repository: PocoF3Releases/device_xiaomi_sm8250-common
remote:     https://github.com/PocoF3Releases/device_xiaomi_sm8250-common
branch:     aosp-17
upstream:   origin/aosp-17
HEAD:       6e964d1447daa2e90007d36115ba4975f1309360
commits reachable from HEAD: 1129
tracked files: 435
shallow repository: false
git fsck --no-dangling: clean
```

HEAD commit:

```text
6e964d1447daa2e90007d36115ba4975f1309360
2026-09-21T20:55:51+03:00
sm8250-common: art: Precompile unprofiled apps with speed filter
```

Remote refs carried in the archive include `aosp-15`, `aosp-16`, and `aosp-17`.

### Camera integration tree

```text
repository: PocoF3Releases/device_xiaomi_camera
remote:     https://github.com/PocoF3Releases/device_xiaomi_camera
branch:     aosp-17
upstream:   origin/aosp-17
HEAD:       433cf879cb10dcf3e682ea515ebc507170c6b3d8
commits reachable from HEAD: 26
tracked files: 65
shallow repository: false
git fsck --no-dangling: clean
```

HEAD commit:

```text
433cf879cb10dcf3e682ea515ebc507170c6b3d8
2026-09-22T14:37:13+03:00
camera: alioth: Use logical SAT camera for video zoom
```

Remote refs carried in the archive include `aosp-14`, `aosp-15`, `aosp-15-disable-checkelf`, `aosp-16-pipa`, and `aosp-17`.

## Live GitHub verification

On 2026-09-23, the live GitHub `aosp-17` branch heads were checked directly and matched the imported local worktrees exactly:

```text
device_xiaomi_alioth         503f821f233a9821d770db863a01ac8abc08732f
device_xiaomi_sm8250-common  6e964d1447daa2e90007d36115ba4975f1309360
device_xiaomi_camera         433cf879cb10dcf3e682ea515ebc507170c6b3d8
```

Therefore this archive was a current branch-head snapshot at the time of import.

## ZIP metadata normalization

Initial `git status` showed modifications even though source contents were unchanged. `git diff --summary` proved these were ZIP extraction metadata losses:

- executable bits lost from extraction/setup helper scripts in all three repositories;
- `sm8250-common/.clang-format` was a tracked symlink (mode `120000`) absent after extraction.

The symlink target stored in Git is:

```text
../../../build/soong/scripts/system-clang-format
```

The extracted workspace was normalized by restoring the expected executable bits and recreating the symlink. After normalization all three repositories reported a clean `aosp-17...origin/aosp-17` status.

This normalization is required before future source edits, otherwise an unrelated commit could accidentally contain mode changes or deletion of `.clang-format`.

## Verified cross-tree integration

Source inspection established the direct build relationships:

```text
alioth/BoardConfig.mk
  -> device/xiaomi/sm8250-common/BoardConfigCommon.mk

alioth/device.mk
  -> device/xiaomi/sm8250-common/kona.mk
  -> device/xiaomi/camera/miuicamera.mk
  -> vendor/xiaomi/alioth/alioth-vendor.mk

sm8250-common/kona.mk
  -> packages XiaomiParts
  -> vendor/xiaomi/sm8250-common/sm8250-common-vendor.mk

camera/miuicamera.mk
  -> camera permissions/config/device features
  -> compatibility packages/shims/SELinux/overlay
  -> vendor/xiaomi/camera/camera-vendor.mk
```

`alioth/lineage_alioth.mk` currently sets both:

```make
TARGET_USES_MIUI_CAMERA := true
TARGET_INCLUDES_MIUI_CAMERA := true
```

## Current use rule

This full-Git workspace is the preferred local source substrate when it is available in the current session because it permits direct inspection, patching, normal Git commits, history queries and clean diffs without reconstructing trees from web snippets.

However:

- compare local HEAD to live GitHub before starting a new patch;
- keep each repository's changes/commits isolated;
- do not treat the presence of `camera/` as authorization to resume paused camera feature experiments;
- source-local instructions such as `sm8250-common/parts/AGENTS.md` take precedence for their subtree;
- the archive is not persisted by `Agents.md`; only this knowledge record is durable.

## Durable routing

See:

- `memory/device-tree-workspace.md` — durable workspace topology and safe workflow;
- `memory/project-overview.md` — wider PocoF3Releases repository ownership;
- `memory/git-history-conventions.md` — commit subject/attribution/history rules;
- `continue-later/CAMERA.md` — paused camera recovery baseline.
