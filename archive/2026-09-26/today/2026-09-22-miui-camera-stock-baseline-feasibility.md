# MiuiCamera stock-baseline feasibility audit — 2026-09-22

## Scope

Assess whether Alioth's stock Xiaomi Camera is a better AOSP-17 reliability/backend baseline than continuing to expand the Universal 5.x mod compatibility layer.

This investigation is static/binary/repository analysis only. No stock-camera AOSP-17 runtime build has been validated yet.

## Current production baseline

The active 5.x camera state remains:

```text
device_xiaomi_camera:aosp-17
d928f68b12f46e532a3e4735f4401c99359fdd52
camera: alioth: Use logical SAT camera for photo zoom
```

Runtime already proves:

- Photo uses logical camera 4 backed by physical [0,2];
- CameraDevice and Photo capture session stay alive during 0.6x/1x/2x handoffs;
- capability cache remains stable;
- JPEG utility JNI is healthy;
- warmed SAT app-side transitions are 250-299 ms, median 262 ms.

This stock investigation does not invalidate or replace those results.

## Exact APK identities

### Stock Alioth APK

```text
file: MiuiCamera_stock.apk
size: 101247458 bytes
SHA-256: 148bd6e51621fe6cebface28263041e58854bac99349712ca450e3ed3158e9a4
dex count: 3
arm64-v8a JNI count: 24
embedded version string: 4.5.003090.0
```

### Current mod APK

```text
file: MiuiCamera(1).apk
size: 223027095 bytes
SHA-256: 1f57cc75346461c4950daa41d10bb127caaab4bd153c316d2ea1c8c7c853d5b3
dex count: 8
arm64-v8a JNI count: 42
```

## Native-library comparison

Every one of the stock APK's 24 arm64 JNI library names exists in the mod APK.

Only four are byte-identical:

```text
libbarhopper_v3.so
libcamera_arcsoft_handgesture.so
libcamera_handgesture_mpbase.so
libhandengine.arcsoft.so
```

Twenty shared JNI libraries differ in binary content.

The mod adds 18 more arm64 libraries:

```text
libAIPOSE.so
libMiVideoSDK.so
libcamera_memory_util_jni.so
libcamera_mi_handgesture.so
libjpeg.so
libmialgo_ai_vision.so
libmialgo_utils.so
libmiffmpeg.so
libmiocr.so
libmiocr_tokenizer.so
libmiocr_wrapper.so
libmpbase.so
librender_engine.so
libtailor.so
libturbojpeg.so
libxcrash.so
libxcrash_dumper.so
libxmi_slow_motion_mein.so
```

Conclusion: the mod has a substantially larger and newer native compatibility surface. Stock gives a more internally matched Alioth-era app/native pairing.

## Feature-gate/static-code comparison

DEX/string scan:

```text
symbol / feature              stock   mod
isSupportedOpticalZoom        yes     yes
isSupportOpticalZoom          no      yes
supportAlgoUp                 no      yes
UniversalSettings             no      yes
getVideoSATCameraId           yes     yes
```

This is important because the current 5.x logical-SAT patch had to work around the newer/Universal feature path querying `isSupportOpticalZoom()`, while the Alioth profile exposed `isSupportedOpticalZoom()`, plus persisted Universal Settings state.

The exact stock binary lacks that newer Universal path. Likewise, the mod-only `supportAlgoUp` path is the reason the current integration needs Alioth-specific native-pixel-mode handling.

These are examples of compatibility work caused by grafting the newer Universal application architecture onto Alioth, not evidence that the underlying SM8250 camera provider is fundamentally incapable.

## Current patch-surface evidence

At:

```text
PocoF3Releases/device_xiaomi_camera:aosp-17
d928f68b12f46e532a3e4735f4401c99359fdd52
```

the `patches/` directory contains 20 maintained APK patches.

They cover areas including:

- HEIF;
- front-video behavior;
- logical SAT;
- native pixel mode;
- capability/config caching;
- gallery integration;
- optional metadata/roles;
- Universal settings.

Do not automatically port this patch set to stock. Each stock change must be justified by a stock runtime failure.

## Lower-layer issues remain independent

Changing application APKs does not solve:

### VideoSAT

The provider currently exposes logical roles 60/61 for [0,2], but VideoSAT role 62 is absent.

Both exact APKs contain `getVideoSATCameraId`, so stock does not supply the missing provider role.

### Persist calibration

CHI reports missing dual-camera persist calibration before provider registration.

The provider still registers and logical Photo SAT works. Existing init/sepolicy already provide the camera persist path/access and the supplied boot log had no camera SELinux denial.

Stock could behave differently in image processing, but it cannot reconstruct missing calibration data. Do not ship guessed calibration blobs.

## AOSP-17 integration strategy

If stock is tested, preserve the existing platform compatibility work first:

- Android-17 camera SELinux/domain handling;
- required privileged/default permissions and hidden-API allowance;
- current CamX/device configuration;
- legacy DisplayConfig service compatibility in the display HAL;
- Qualcomm gralloc;
- camera OpenCL layout where actually required;
- ExtraPhoto/gson where exposed;
- proven JNI/linker compatibility pieces.

Do not bring back broad symlink farms or random compatibility libraries. Use linker/native-loader/logcat evidence.

## Source-tree warning

The exact stock APK has only three dex files.

The current `PocoF3Releases/decompiled_miui_camera:aosp-17` / Library `decoded.zip` tree has eight dex trees and Universal-style code. It remains useful for reference/history, but is not byte-for-byte source for this exact stock APK.

A real stock-camera development branch should be decompiled from:

```text
SHA-256 148bd6e51621fe6cebface28263041e58854bac99349712ca450e3ed3158e9a4
```

and should use a clearly separate identity from the current Universal/mod worktree.

## Proposed runtime experiment

Create an isolated stock AOSP-17 baseline. Keep the current 5.x branch/build intact.

First build rule:

```text
exact stock APK
+ minimum existing AOSP compatibility backend
+ no Universal 5.x smali patch stack
+ no speculative new compatibility libraries
```

Test:

```text
camera startup
rear Photo
1x -> 0.6x -> 1x -> 2x
captures at 0.6x / 1x / 2x
48 MP
front Photo
rear Video
front Video
macro / slow motion where available
ExtraPhoto handoff where available
```

Triage order:

1. crash/fatal signal;
2. linker/native-loader;
3. permission/SELinux/service failure;
4. role/camera selection;
5. capture/video save correctness;
6. AF/AE/HDR/image quality;
7. timing/performance.

## Decision rule

Do not migrate the release camera merely because stock is smaller.

Promote stock to the primary baseline only if runtime evidence shows that it provides a cleaner and more reliable Alioth/AOSP backend with fewer device-specific compatibility patches while retaining the required features.

Until then:

```text
5.x = current validated production/feature baseline
stock = strong backend-first candidate pending isolated AOSP-17 validation
```
