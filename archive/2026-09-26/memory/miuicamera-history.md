> HISTORICAL investigation archive. All next-step, pending-test and alternative-architecture plans below are closed by the maintainer. Use [the finalized camera record](miuicamera.md). Retained for technical provenance only.

# MiuiCamera Durable Knowledge

## Current camera checkpoint — 2026-09-23

Camera work was explicitly resumed and tested. The current delivery heads are
`device_xiaomi_camera:aosp-17` `6c25fe9babca33dfc37813be7a92f5bbbe4d6319` and GitLab
`vendor_xiaomi_camera:aosp-17` `f13797ef3d93508756e06a4a185c9208dbc3ee88`.
See [latest device validation](../today/2026-09-23-camera-video-validation.md) for artifact identity and evidence.

Main 4K30/60 works with the non-EIS logical-camera-4 session guard. Ultrawide
4K is blocked to prevent verified ISP scaler failures; this is a capability
guard, not implementation of ultrawide 4K. Ultrawide 1080p records, but the tested
1080p60 selection delivered about 30 fps. Resolution changes safely reset 0.6x
to 1x. The final APK was tested through a temporary Magisk system-path bind mount.

All older sections below are historical/reference context. In particular,
paused rollback SHAs, archived decoded-tree identities and abandoned-experiment
instructions do not override this new checkpoint or the canonical vendor APK.
Verify any reference tree against the APK before reuse.

## Source-of-truth rule

MiuiCamera 5.x mod is the authoritative feature/ABI baseline for current Alioth integration.

### Stock Alioth decompiled repository / Library mirror

The following are the **stock Alioth MiuiCamera reference tree**, not the authoritative 5.x mod source:

```text
https://github.com/PocoF3Releases/decompiled_miui_camera
Library: /decoded.zip
```

Use them as two access paths to the same **stock Alioth camera** source base:

- **GitHub `decompiled_miui_camera:aosp-17`** is authoritative for the latest pushed stock-reference state and commits;
- **Library `decoded.zip`** is preferred for full-tree local grep, cross-file smali analysis, bulk indexing, and tools that need the complete stock camera repository on disk;
- do **not** infer that code present there is present in the 5.x mod unless separately verified in the mod APK/worktree;
- do **not** build the production 5.x mod from this stock repo unless explicitly porting a stock implementation.

The shipped 5.x mod is a separate patched prebuilt/worktree integrated through `PocoF3Releases/device_xiaomi_camera:aosp-17`. Stock code is useful for device-specific behavior, camera-role mapping, provider expectations, compatibility logic, and reconstructing features that the mod needs on Alioth.

The archive contains its own `.git` data. Its embedded HEAD is:

```text
607a138f0a01d1ac0e03d2474ab53ee77af0daf0
Decompiled MiuiCamera
```

That commit is the direct parent of the current canonical `aosp-17` correction:

```text
99da18c1fc7d6657b847a2306b8903676e8d26c8
MiuiCamera: Keep capability cache allocation in init
```

Therefore treat `decoded.zip` as the same repository/source tree but not automatically as the newest pushed commit. Before making or describing source changes, compare its embedded HEAD with the current GitHub `aosp-17` head and account for any newer commits.

Verified current-session working paths:

```text
Library source:      /decoded.zip
materialized archive: /mnt/data/decoded.zip
extracted worktree:   /mnt/data/decoded_check/
```

The extraction was successfully completed and contains the full repository, including `.git/`, `AndroidManifest.xml`, resources, and the complete smali trees. The `/mnt/data/...` locations are ephemeral container paths; future chats should rematerialize the Library archive and re-extract if the working directory is not present.

Classification correction (2026-09-22): this repository/archive is the **stock Alioth camera**. Earlier notes that called it the decompiled 5.x mod source are superseded by this statement. Any structural finding taken from this tree must be treated as a stock reference unless the same implementation is independently confirmed in the 5.x mod.

Alioth stock camera is older 4.x and must not be treated as the feature binary baseline.

Stock camera/dump is useful for:

- provider availability;
- stock partition placement;
- device-specific compatibility blobs;
- comparing ABI/symbol behavior.

Same filename does not imply binary compatibility.

## Known MiuiCamera 5.x work

Durable feature/fix areas include:

- native 48 MP QCFA capture instead of fake 12 MP upscaling;
- Alioth camera defaults;
- standalone Macro restoration;
- Xiaomi metadata / legacy HAL compatibility;
- photo saving and video recording fixes;
- front-camera video crash fixes;
- improved AOSP stability;
- HEIF handling;
- Android 17 packaging/permissions/SELinux cleanup.

## CameraX

CameraX vendor-extension integration was removed because MiuiCamera does not depend on that provider.

Do not re-add the vendor extension JAR, its permissions or enable properties without a proven new dependency.

## MiSys

Unused MiSys camera integration was cleaned up from the current tree.

Do not restore broad MiSys compatibility solely because stock Xiaomi carried it; prove the current 5.x mod needs the path first.

## DisplayConfig / legacy MIUI callback ownership

Do not restore the old camera-side DisplayConfig matrix/callback workaround.

Legacy camera DisplayConfig compatibility is owned by the SM8250 display HAL. The display stack publishes a real `vendor.display.config@1.9/default` compatibility endpoint alongside its native 2.0 service and forwards the legacy camera API to the current implementation.

Relevant display checkpoint:

```text
0e25857599b3a609e957a0d0418ec2b3dd264480
display: Bridge legacy IDisplayConfig 1.9 to 2.0
```

ExtraPhoto integration does not change this ownership.

## OpenCL layout

Preserve the stock camera OpenCL bridge:

```text
system_ext/lib64/libcameraimpl.so
system_ext/lib64/libopencl-camera.so
```

`libcameraimpl.so` depends on `libopencl-camera.so`.

`libOpenCL_system.so` is a separate system_ext provider and does not replace the camera-specific bridge.

Vendor `libOpenCL.so` is still required by some embedded MiuiCamera 5.x libraries and should remain available/public.

## Proven APK-local JNI aliases

Runtime evidence supersedes the earlier "only two aliases" conclusion.

The following JNI libraries are directly loaded by MiuiCamera and need to be resolvable from the app namespace:

```text
libcamera_algoup_jni.xiaomi.so
libcamera_mianode_jni.xiaomi.so
libcamera_jpegutil_jni.xiaomi.so
```

The JPEG utility requirement was proven by device logcat during a real mode switch:

```text
nativeloader: Load libcamera_jpegutil_jni.xiaomi.so ...
dlopen failed: library "libcamera_jpegutil_jni.xiaomi.so" not found

CAM_JpegUtil: couldn't find libcamera_jpegutil_jni.xiaomi.so
CAM_JpegUtil: getPlanesExtra: inited = false
```

The exact 5.0 Beta 8.3 smali calls:

```java
System.loadLibrary("camera_jpegutil_jni.xiaomi")
```

The device-tree implementation is now present:

```text
63594546455453b7749556f9ff1679be00eb981e
camera: native: Add MiuiCamera JPEG utility JNI
```

Architecture:

```text
device/xiaomi/camera/prebuilts/system/lib64/libcamera_jpegutil_jni.xiaomi.so
    -> installed as /system/lib64/libcamera_jpegutil_jni.xiaomi.so

/system/priv-app/MiuiCamera/lib/arm64/libcamera_jpegutil_jni.xiaomi.so
    -> /system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

Pinned source:

```text
TOCO Global V13.0.4.0.SFNMIXM
SHA-1 d159aebabed57516153a2d203d6104c80b4c1a95
```

The prebuilt is kept directly in the device tree rather than the generated camera vendor repo.

A first rebuilt-device validation proved that the app-local JPEG utility alias is found, but loading then failed on the legacy dependency:

```text
library "libhidltransport.so" not found
needed by /system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

The existence of `libhidltransport.so` under vendor does not make it visible to MiuiCamera's system app linker namespace.

Current compatibility fix:

```text
9a4cf71fbbbb69e31d20ad158c338bd600a9261c
camera: native: Drop obsolete HIDL transport dependency
```

This modifies only:

```text
prebuilts/system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

by removing the obsolete `DT_NEEDED libhidltransport.so` entry. Do not expose/copy vendor `libhidltransport.so` into the platform app namespace as a workaround.

Runtime validation on the rebuilt image succeeded on 2026-09-22:

```text
nativeloader: Load .../libcamera_jpegutil_jni.xiaomi.so ...: ok
JpegUtil_JNI: Java_com_android_camera_JpegUtil_nativeClassInit: X
CAM_JpegUtil: getPlanesExtra: inited = true
```

`nativeGetPlanesExtra()` returned real SurfaceImage planes during multiple JPEG reprocess operations, and the post-processor proceeded to save JPEG data. The previous `libhidltransport.so` linker failure is gone. This compatibility fix is therefore runtime-validated.

Do not restore a broad symlink farm. Add only libraries proven live by runtime evidence.

## ExtraPhoto companion app

Full MiuiCamera document/ID-card/refocus behavior expects Xiaomi's `com.miui.extraphoto` companion.

For Alioth, use the actual stock `ExtraPhotoGlobal.apk`, not the older miatoll `MiuiExtraPhoto.apk` stack.

Stock-faithful partitioning:

```text
/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
/system_ext/framework/gson.jar
```

MiuiGallery is not a hard dependency for the Camera -> ExtraPhoto workflow. Gallery references are integration/query/broadcast hooks. Do not add MiuiGallery solely for ExtraPhoto.

The hard Java shared-library dependency is:

```text
gson.jar
```

Alioth stock exposes it as:

```xml
<library name="gson.jar"
         file="/system_ext/framework/gson.jar" />
```

The extracted Alioth `gson.jar` matches the stock dump identity:

```text
SHA-1 4e7699dde5290f45810a6aafb2e9ffd21db3be57
```

For the active Alioth Global Android 13 dump used by the build (`V816.0.3.0.TKHMIXM`), the stock ExtraPhoto APK identity is:

```text
/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
SHA-256 614c7c27ddf5cf14b5c7ae61c799643e6639d82a344e46c83200266efa3c1451
SHA-1   938f03ceb4641ed3a492b8fffe1e9358fdae73cb
size    227197486
```

A previously seen `eb8089...` / `227770926` object belongs to a different stock-dump revision and is not the reference for the active `~/miui/out` dump.

`ExtraPhotoGlobal.apk` already carries its large document/refocus native stack internally. Do not copy the old miatoll external `libgallery_*`, `librefocus*`, `libdoc_photo*`, or duplicate `libSNPE.so` set unless runtime proves a separate missing dependency.

Device-tree integration checkpoint:

```text
423ae8e4a44f2bf2ef99807179c27f4624689c18
camera: extraphoto: Add stock Alioth companion app support
```

The `proprietary-files.txt` section is:

```text
# ExtraPhoto
product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
system_ext/framework/gson.jar;MAKE_COPY_RULE_ONLY
```

ExtraPhoto's privileged allowlist belongs on `/product`, while the `gson.jar` shared-library declaration belongs on `/system_ext`.

`gson.jar` is intentionally a plain prebuilt copy, not a Soong Java module:

```text
vendor/xiaomi/camera/proprietary/system_ext/framework/gson.jar
    -> /system_ext/framework/gson.jar
```

Do not generate `dex_import { name: "gson" }` and do not add `gson` to `PRODUCT_PACKAGES`; that device-specific module is rejected by the generic shared-system-image check. Keep `MAKE_COPY_RULE_ONLY` on the proprietary-files entry.

## Native compatibility rules

Do not substitute older stock copies of private 5.x libraries without checking:

- `DT_NEEDED`;
- exported/imported symbols;
- GNU symbol versions;
- dynamic `dlopen` behavior;
- device feature runtime.

Known examples:

- private `libyuv.so` must retain required functions such as `ABGRToNV21`;
- private JPEG/TurboJPEG runtimes have distinct API/version requirements;
- private C++ runtime variants are both actively used.

## Packaging

Canonical MiuiCamera APK is kept in Git LFS.

Final architecture is direct `android_app_import` with `certificate: "platform"`.

No APK generation layer should be added unless a future requirement cannot be handled by the canonical prebuilt.

## Extract-utils section behavior

A section-only extraction such as:

```bash
./extract-files.py --section ExtraPhoto ~/miui/out
```

filters which blobs are copied and skips full vendor cleanup, but generated makefiles are **not section-filtered**.

Extract-utils still regenerates the whole:

```text
vendor/xiaomi/camera/Android.bp
vendor/xiaomi/camera/camera-vendor.mk
```

Therefore existing modules may move/reorder in the generated files even when their definitions are unchanged.

For the ExtraPhoto import, `libOpenCL_system`, `libcameraimpl`, and `libopencl-camera` were verified byte-for-byte identical as module definitions before and after generation. Their apparent large Git diff was ordering noise only.

## Capability-cache fix — runtime validation (2026-09-22)

The packaged cache fix is verified on device.

Fresh runtime reports all camera IDs `0..7`, then performs exactly 8 actual `E: initCameraCapabilitiesByCameraId()` calls — one for each camera ID. The pre-fix baseline was 104 calls. There are no later capability initializations during the tested mode switches, and the old `mCapabilities.get(id)=null` sequence is absent.

This validates the intended persistent-cache lifecycle and closes the capability-cache regression. Do not add constructor cache initialization, lazy post-reset allocation, or restore the removed per-camera `SparseArray` reallocations.

Mode-switch performance is improved enough that cache reconstruction is no longer present as a confounder, but not every switch is below MiuiCamera's 1000 ms warning threshold. Seven completed deliberate switches had a median total cost of 694 ms; five were below 1000 ms. The two slower completed samples were:

```text
163 -> 171:
  SWITCH_MODULE = 1118 ms
  HAL startPreview -> first frame = 639 ms

163 -> 162:
  SWITCH_MODULE = 1144 ms
  switch_module_setup = 545 ms
  cameraOpened -> createCaptureSession = 365 ms
  HAL createCaptureSession = 193 ms
  HAL startPreview -> first frame = 253 ms
```

The same named pre-fix examples were approximately 1270 ms for `163 -> 171` and 2172 ms for `163 -> 162`. Treat this as a useful single-run comparison, not a controlled benchmark. The durable conclusion is narrower: capability reconstruction is gone, so any remaining delay belongs in mode-specific app/session/HAL investigation rather than reopening the cache fix.

The JPEG utility compatibility remains healthy in the same run: `libcamera_jpegutil_jni.xiaomi.so` loads successfully, native initialization completes, and `getPlanesExtra` reports `inited = true`.
### Photo lens-switch stress validation

A later stress capture exercised 22 consecutive Photo-mode lens toggles. These are same-mode `163 -> 163` reselections driven by the zoom toggle, not the separate `163 -> 171` / `163 -> 162` module transitions.

Observed behavior:

```text
22 completed lens switches
median total cost: 854 ms
mean total cost:   861 ms
range:             732..961 ms
switches >= 1000 ms: 0
```

The lens mapping in this run is explicit:

- `0.6x` selects physical camera ID 2;
- `1x/2x` stays on physical camera ID 0.

Direction-specific timing:

```text
to camera ID 2 / 0.6x:
  n = 11
  median total = 917 ms
  median HAL preview -> first frame = 451 ms

to camera ID 0 / 1x-2x:
  n = 11
  median total = 823 ms
  median HAL preview -> first frame = 382 ms
```

The roughly 100 ms direction asymmetry is dominated by preview-to-first-frame latency rather than capability reconstruction. Camera-open-to-session time and module/session setup stay in the same general range in both directions.

Each physical-lens toggle performs a real close/open. Runtime reports `isSupportReplaceSession: false` and `openCamera: reusable = false`; do not force a replace-session or camera-reuse path without device/HAL evidence that Alioth supports it.

The capability cache remains stable under this heavier loop. The log contains two clean 8-camera initialization passes because the camera app process was intentionally killed/restarted once when its task was removed. After the second `0..7` initialization pass, the 22-switch stress loop triggers no additional `initCameraCapabilitiesByCameraId()` calls and no `mCapabilities.get(id)=null` messages.

For these same-mode lens switches, MiuiCamera's generic performance event logs `SWITCH_MODULE has no start time` while `ActivityBase.trackModeSwitchCost` still records the real end-to-end cost. Treat that message as an instrumentation limitation for same-mode lens reselection, not as a zero-duration switch.

A low-priority native warning remains: the 22-switch window emits 2040 `RefBase: Explicit destruction, weak count = 0` warnings, each followed by unavailable call-stack logging. The framework text itself warns that this can leak the small `weakref_impl` bookkeeping object. The log provides no PSS/RSS growth, OOM, crash, or progressive user-visible slowdown proving a material leak, so do not patch blindly; keep it as a separate native/vendor compatibility observation if long-duration stress later shows memory growth.

## Logical SAT Photo fix — implemented, runtime validation pending

The stress log proves the provider already exposes the rear main+ultrawide topology needed for seamless Photo zoom:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
role 62 -> absent
```

Current 5.x APK static analysis found the reason Photo never used role 60:

- `CameraSettings.F3()` is enabled by default because `pref_camera_dual_sat_enable_default=true`;
- `CameraSettings.l6()` additionally requires `DataItemFeature.E8()` and the presence of SAT role 60;
- role 60 is present at runtime;
- `DataItemFeature.E8()` calls `Common.isSupportOpticalZoom()`;
- the Alioth profile only implemented the differently named `isSupportedOpticalZoom() = true`, so it inherited `Common.isSupportOpticalZoom() = false`;
- the Universal mod's `modify.ConfigManager` persists the computed false value in `Download/XiaomiCamera/<device>.json`, so a profile-only rename is insufficient for already-used installations.

Fix:

```text
d928f68b12f46e532a3e4735f4401c99359fdd52
camera: alioth: Use logical SAT camera for photo zoom
```

Patch behavior:

1. add Alioth `isSupportOpticalZoom() = true` so the profile implements the API actually queried by `DataItemFeature`;
2. for the Alioth profile, bypass the stale generated `isSupportOpticalZoom=false` cache after the existing Universal Settings/disable-tele checks;
3. explicitly overlay `pref_camera_dual_sat_enable_default=true`.

With those conditions, the normal Photo camera-selection path uses `Camera2DataContainer.D()` (SAT role 60) and therefore camera ID 4. Because Alioth reports at least three lenses, `CameraSettings.J6()` is false in this path, so the 0.6x UI does not force the standalone ultrawide ID 2.

Expected runtime result after rebuilding the patched APK:

```text
Photo startup / selection: actual camera -> 4
0.6x / 1x / 2x taps: actual camera remains 4
no repeated physical cid 0 <-> 2 full-camera-change loop
HAL switches physical sensor inside logical camera 4
```

Do not claim a ~100 ms result until measured. The correct first acceptance test is topology: camera ID must remain 4 through repeated lens changes. Then measure `trackModeSwitchCost`, first-frame timing, visual continuity, capture correctness, HDR/night behavior and memory.

Video is separate. The current provider does not expose role 62, so this commit deliberately does not enable `supportVideoSAT()` or remap `getVideoSATCameraId()` to role 60.

### Decompiled-source identity caveat

The uploaded `MiuiCamera_stock.apk` contains three dex files, whereas `/decoded.zip` / `PocoF3Releases/decompiled_miui_camera` contains eight-dex Universal-style code and the `modify.*` package used by the 5.x mod. Treat the repository/archive as a useful reference/working tree whose exact stock provenance is not byte-for-byte established; use the actual stock APK for definitive stock comparisons and independently verify production-mod paths in the current 5.x APK.

## Seamless SAT / logical multi-camera feasibility

Alioth's vendor camera stack contains real multi-camera groundwork; it is not merely an app-side feature flag.

Current `vendor_xiaomi_alioth:aosp-17` evidence:

```text
vendor/etc/camera/camxoverridesettings.txt:
  multiCameraEnable=TRUE
  enableSensorHWSync=1
  multiCameraFrameSync=1

vendor packages:
  com.qti.node.dummysat
  libarcdualcamsat
  libarcmulticamsat
```

Therefore the hardware/CamX stack is capable of multi-camera operation in principle. However, this does **not** prove that the current Alioth camera provider exposes a usable Android logical camera combining the main and ultrawide sensors.

Runtime MiuiCamera evidence points at the missing layer:

```text
CAM_Camera2CompatAdapterRole: Warning: getVideoSATCameraId(): #init() failed, roleId=62
```

At the same time, Photo zoom currently resolves directly to separate physical IDs:

```text
0.6x -> camera ID 2
1x/2x -> camera ID 0
isSupportReplaceSession: false
openCamera: reusable = false
```

So the current app performs a full physical-camera close/open instead of using a persistent SAT/logical session.

Android's intended seamless architecture is one logical multi-camera device backed by multiple physical sensors. The app keeps one `CameraDevice` / session open and drives `CONTROL_ZOOM_RATIO`; the HAL can switch the active physical sensor without closing the logical device. On Alioth, `2x` is digital zoom on the main sensor because there is no telephoto camera, so the only physical transition needed for seamless zoom is ultrawide (ID 2) <-> main (ID 0).

Feasibility status: **promising but not yet proven at provider metadata level**.

Do not patch MiuiCamera to fake seamless switching or force `replaceSession` first. Before app changes, verify:

1. `dumpsys media.camera` / CameraCharacteristics for every camera ID;
2. which ID, if any, advertises `REQUEST_AVAILABLE_CAPABILITIES_LOGICAL_MULTI_CAMERA`;
3. `getPhysicalCameraIds()` membership and whether it includes IDs 0 and 2;
4. whether zoom-ratio result metadata exposes active physical camera changes;
5. whether Xiaomi vendor metadata/CHI role tables expose a SAT/VideoSAT logical role corresponding to MiuiCamera role 62.

If a suitable logical camera already exists, the expected implementation is mainly role mapping plus MiuiCamera selection policy. If no logical device exists, the next work is CHI/CamX usecase/logical-camera configuration in the proprietary provider stack; app-only changes cannot deliver modern seamless lens switching.

A ~100 ms target is realistic only for an **already-open logical camera lens transition** (roughly a few frames, depending on 30/60 fps, exposure convergence and HAL blending). It is not a realistic target for full physical close/open or cold camera app launch on this stack.

## Runtime validation checklist

Exercise:

- photo;
- video;
- front video;
- 48 MP;
- macro;
- slow motion;
- hand gesture;
- OCR/document;
- ID-card;
- ExtraPhoto handoff;
- night/portrait.

Capture linker/native-loader errors before adding more compatibility libraries.

## Mode-switch regression — capability cache

A second verified structural problem exists in the 5.0 Beta 8.3 camera-role/capability implementation.

Relevant files in the decompiled port:

```text
smali_classes2/d/c/a/q6/t8/b/q.smali
    Camera2CompatAdapterRole

smali_classes2/d/c/a/q6/t8/b/o.smali
    Camera2CompatAdapter
```

The async role initializer allocates a new shared `SparseArray` while iterating camera IDs, and the base `initCameraCapabilitiesByCameraId()` helper also replaces the shared capability array before inserting a single camera.

Observed runtime result:

```text
CAM_Camera2CompatAdapterRole: mCapabilities.get(id)=null id=0
CAM_Camera2CompatAdapterRole: mCapabilities.get(id)=null id=1
...
CAM_Camera2CompatAdapterRole: mCapabilities.get(id)=null id=6
CAM_Camera2CompatAdapterRole: role: 101 (...) <-> 7
```

So after initialization the shared cache can retain only the last camera entry instead of all camera IDs.

During mode switching, MiuiCamera therefore repeatedly rebuilds capabilities:

```text
CAM_Camera2CompatAdapter: E: initCameraCapabilitiesByCameraId(): 5
CAM_Camera2CompatAdapter: X: initCameraCapabilitiesByCameraId(): 5
CAM_Camera2CompatAdapter: E: initCameraCapabilitiesByCameraId(): 0
CAM_Camera2CompatAdapter: X: initCameraCapabilitiesByCameraId(): 0
```

A newer MiuiCamera 6.2 implementation confirms the intended design: camera capabilities are inserted into persistent caches with `put()`; the cache is not recreated for each camera.

This is not attributed to the OpenCL/symlink cleanup. The active device-tree patches do not modify the async initializer.

Fresh runtime after the JPEG/NFC fixes reproduced the cache bug exactly: asynchronous initialization processed camera IDs 0 through 7, then immediately reported `mCapabilities.get(id)=null` for IDs 0 through 6, leaving only camera 7 cached. The same run performed 104 capability initializations, heavily concentrated on IDs 0, 2 and 5 during mode switches.

Implemented source fix:

```text
4ba629723586315e06905b9c1b5d5104a1286a82
camera: capabilities: Preserve initialized camera cache
```

Patch:

```text
patches/camera-capabilities-cache.patch
```

It removes only the two erroneous per-camera/per-lookup SparseArray reallocations from `Camera2CompatAdapterRole.N()` and `Camera2CompatAdapter.K()`. The single legitimate cache allocation in role-adapter `init()` remains intact. Newer MiuiCamera independently confirms that capabilities should be inserted with `put()` into a persistent cache.

Fix status: **runtime-validated fixed on device**.


### Stock-reference verification of cache lifecycle

The stock Alioth decompiled camera reference tree is available at:

```text
PocoF3Releases/decompiled_miui_camera
Library /decoded.zip
```

This tree is useful for comparing lifecycle/ownership patterns, but it is **not** the production 5.x mod source.

Astra had additionally changed the base `Camera2CompatAdapter` constructor from a null cache to `new SparseArray()`, based on concern that removing the two bad reallocations could cause a null dereference.

That safeguard is **not required** for the real lifecycle:

```text
constructor:
    e = null

Camera2CompatAdapterRole.t()/init():
    reset() -> e = null
    e = new SparseArray(cameraIdCount)
    schedule async N()

N():
    reuse e
    K(id) for missing entries

K():
    e.put(id, capabilities)
```

The constructor allocation was ineffective as a reset safeguard anyway because `reset()` immediately nulled `e` before every initialization. It was also unnecessary because the only normal paths into `K()` are after role initialization has established the cache.

Newer MiuiCamera uses the same ownership model: the capability cache starts null, `reset()` nulls it, role `init()` allocates it once, and per-camera initialization only inserts with `put()`.

The stock-reference repo currently includes this lifecycle correction:

```text
99da18c1fc7d6657b847a2306b8903676e8d26c8
MiuiCamera: Keep capability cache allocation in init
```

Do not treat that commit itself as the shipped mod fix; the production/runtime fix remains the `device_xiaomi_camera` patch/prebuilt path.

The corrected apktool tree was then rebuilt locally from:

```text
~/evo17/out/camera-capabilities-cache/decoded
```

The rebuilt APK was aligned with the AOSP `zipalign -P 16` flow and placed into the canonical `vendor/xiaomi/camera` MiuiCamera prebuilt path for the next ROM/package build. This corrected lifecycle is now runtime-validated on device; the constructor allocation and post-reset lazy-allocation workarounds remain unnecessary.

Do **not** add constructor cache initialization or a broad post-reset lazy allocation in `K()`. A stale async initializer should not be allowed to silently recreate cache state after a reset.

## Logical SAT runtime validation — Stage 1/2 passed (2026-09-22)

This section supersedes every earlier logical-SAT note in this file that still says runtime validation is pending.

Canonical implementation:

```text
PocoF3Releases/device_xiaomi_camera:aosp-17
d928f68b12f46e532a3e4735f4401c99359fdd52
camera: alioth: Use logical SAT camera for photo zoom
```

Rebuilt-device runtime proves the intended architecture:

- Photo resolves to logical camera `4` (role 60, physical `[0,2]`).
- Same-mode Photo requests remain `cid: 4 -> 4`; camera 4 is explicitly excluded from close and reported as already open.
- Zoom changes update the existing repeating request; there is no Photo `createCaptureSession` during the zoom loops.
- CHI/CamX performs the lens handoff inside that logical session. After cold activation, `active_map=0x3` and the internal SAT master changes between the two rear pipelines.
- No physical camera `0 <-> 2` CameraDevice reopen occurs during Photo zoom.

Measured app-side SAT transition data from the validation log:

```text
Photo zoom-toggle actions:       20
completed sat_switch_163_0:      18
overall median:                  299 ms
overall mean:                    314 ms
overall range:                   250..458 ms
warmed second-run median:        262 ms
warmed second-run range:         250..299 ms
```

The first cold `1x -> 0.6x` click activates the second SAT pipeline (`active_map 0x2 -> 0x3`); the first logged internal master edge occurs about 617 ms after that click. The next equivalent `1x -> 0.6x` handoff reaches the logged master edge in about 306 ms. Logged `0.6x -> 1x` master edges can appear earlier (~105/117 ms), but one cold return briefly bounced before stabilizing. Therefore use MiuiCamera's `sat_switch` timing as the safer app-visible comparison metric rather than equating the first HAL master metadata edge with a fully settled visual transition.

Some CamX/CHI buffer notifications, SAT fallback messages and a first-mode-switch sensor warning appear during handoff, but the logical device/session survives and there is no fatal camera/app/linker regression. Do not patch those messages in isolation without a reproducible user-visible failure.

The same runtime log also keeps prior prerequisites healthy: exactly eight real capability-cache initialization calls occur for camera IDs `0..7`, no post-init null-cache sequence reappears, and JPEG utility JNI remains initialized.

### Dual-camera persist calibration warning

Boot-time CHI reports:

```text
OverwriteDualcamCaldata(): Fatal Error: calibration persist file lost!
OverwriteDualcamCaldata(): CameraRoleId 0 lost persist file
```

The QTI provider nevertheless registers immediately afterward and logical SAT works at runtime. Current `device_xiaomi_sm8250-common` init creates `/mnt/vendor/persist/camera`, sepolicy labels it `vendor_persist_camera_file`, and `hal_camera_default` already has read access; the supplied boot log contains no camera `avc: denied` event. The evidence therefore points to absent calibration data rather than a current SELinux access failure.

Do not copy random/fake calibration data into persist. Treat this as a Stage 3 quality/alignment risk until visual crossover/capture testing and a real `/mnt/vendor/persist/camera` inventory show whether anything actionable is missing.

### Current next step

Stage 3 is now current: run 50–100 Photo handoffs, verify captures/AF/AE/HDR and crossover continuity at `0.6x/1x/2x`, inspect the persist-camera inventory, and optionally pair the long run with `dumpsys meminfo` if RefBase warnings persist. No additional Photo SAT code patch is justified before that evidence.



## Stock Alioth camera as an AOSP backend-first baseline

Status: **promising alternative architecture, statically audited but not yet runtime-validated on AOSP 17.** This does **not** supersede the current 5.x production/Stage-3 SAT baseline until an isolated stock-camera build boots and passes the runtime matrix.

### Exact binary comparison

The actual uploaded stock and current mod APKs were compared directly rather than inferring from the decompiled reference repository.

```text
stock artifact:
  file: MiuiCamera_stock.apk
  size: 101247458 bytes
  SHA-256: 148bd6e51621fe6cebface28263041e58854bac99349712ca450e3ed3158e9a4
  dex files: 3
  arm64-v8a JNI libraries: 24

current mod artifact:
  file: MiuiCamera(1).apk
  size: 223027095 bytes
  SHA-256: 1f57cc75346461c4950daa41d10bb127caaab4bd153c316d2ea1c8c7c853d5b3
  dex files: 8
  arm64-v8a JNI libraries: 42
```

All 24 stock arm64 JNI library names also exist in the mod APK. However, only four shared libraries are byte-identical:

```text
libbarhopper_v3.so
libcamera_arcsoft_handgesture.so
libcamera_handgesture_mpbase.so
libhandengine.arcsoft.so
```

The other 20 shared JNI libraries are different builds. The mod additionally embeds 18 arm64 libraries:

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

Durable interpretation: moving to stock is not merely an older UI swap. It restores an Alioth-era Java/smali + native userspace pairing with a materially smaller compatibility surface. The Universal/mod application combines a much larger cross-device application/native stack with the Alioth SM8250 provider.

### Static feature-gate evidence

DEX/string inspection of the exact APKs found:

```text
stock:
  isSupportedOpticalZoom   present
  isSupportOpticalZoom    absent
  supportAlgoUp            absent
  UniversalSettings        absent
  getVideoSATCameraId      present

mod:
  isSupportedOpticalZoom   present
  isSupportOpticalZoom    present
  supportAlgoUp            present
  UniversalSettings        present
  getVideoSATCameraId      present
```

The stock APK also contains the camera version string `4.5.003090.0`.

This supports a key architectural conclusion: several fixes currently carried for the 5.x mod are adaptation work for the Universal/newer camera abstraction rather than proof that the Alioth camera backend itself is defective. Examples include the optical-zoom method-name/cache mismatch, `supportAlgoUp`/native-pixel-mode handling, optional newer-camera-role assumptions, and other cross-device compatibility paths.

At `device_xiaomi_camera:aosp-17 @ d928f68b12f46e532a3e4735f4401c99359fdd52`, the maintained `patches/` directory contains 20 APK patches. Do not assume every one is needed by stock.

### What stock will not solve by itself

Stock is not expected to repair lower-layer/provider state automatically:

- VideoSAT role 62 is absent in the current provider topology. Both exact APKs contain the VideoSAT getter path, so replacing the app cannot manufacture role 62.
- The boot-time missing dual-camera persist calibration warning remains a CHI/provider/persist concern. An app swap cannot recreate missing calibration data.
- A stock APK on AOSP 17 may still expose linker, permission, service, storage, or MIUI-framework assumptions. These must be established by runtime logs, not guessed.

### Reuse the existing AOSP compatibility backend

A stock-camera experiment should reuse the already-proven AOSP integration infrastructure first instead of rebuilding the platform side from zero. In particular, retain the existing Android-17 camera SELinux/domain handling, hidden-API whitelist/default permissions as needed, CamX/device configuration, the display-HAL-owned legacy DisplayConfig bridge, gralloc/OpenCL integration, and the proven JNI/linker compatibility work unless runtime evidence shows that a stock build does not need a component.

Do not reintroduce broad symlink farms or compatibility libraries preemptively. Start from the smallest stock-compatible integration and add only dependencies proven live by logcat/linker output.

### Correct stock development source

The exact stock APK is the definitive source for a stock-baseline effort.

The current `PocoF3Releases/decompiled_miui_camera:aosp-17` / Library `decoded.zip` tree has eight dex trees and Universal-style code, while the exact stock APK has three dex files. Therefore it must not be treated as byte-for-byte source for a future stock production branch.

If the stock path is pursued, decompile the exact artifact identified above and give that tree its own clear branch/repository identity.

### Recommended isolated experiment

Do not replace the current validated 5.x build immediately. Create an isolated stock-AOSP17 baseline and test the untouched stock APK first, with no Universal 5.x smali patch stack applied.

Initial acceptance matrix:

```text
startup / rear Photo
1x -> 0.6x -> 1x -> 2x
real captures at 0.6x / 1x / 2x
48 MP
front Photo
rear Video
front Video
macro / slow motion where exposed
ExtraPhoto handoff if exposed
```

For the first run, prioritize:

1. fatal exception/native crash/linker failures;
2. permission/SELinux/service failures;
3. camera ID/role selection and capture-session behavior;
4. save/video-record correctness;
5. AF/AE/HDR/image quality;
6. transition timing only after correctness.

Compare the result against the current 5.x validated baseline: logical Photo camera 4 stays open in-session, capability caching is fixed, JPEG JNI is healthy, and warmed SAT handoffs are roughly 250-299 ms (median 262 ms).

Only if the stock baseline proves cleaner/more reliable should it become the primary release camera; until then, treat it as a strong backend-first candidate rather than a completed migration.

## Latest rebuilt-device correction — Photo SAT gate still inactive (2026-09-22 ~13:52)

This section supersedes the earlier current-build claim that Photo logical SAT was already runtime-validated. Keep the older observation as historical evidence only; the newest rebuild/log is authoritative for the current installed image.

Current source checkpoints:

```text
decompiled_miui_camera:aosp-17
c334e3216ec62809d5e0e0206fc75e0435a4c28e
MiuiCamera: alioth: Enable logical SAT photo zoom

device_xiaomi_camera:aosp-17
d928f68b12f46e532a3e4735f4401c99359fdd52
camera: alioth: Use logical SAT camera for photo zoom
```

The decompiled commit was cleaned before push so it contains only the two intended smali changes:

```text
smali_classes7/com/mi/config/DataItemFeature.smali  +11
smali_classes7/com/mi/device/Alioth.smali           +8
```

Generated `build/apk/classes*.dex` files were intentionally removed from that source commit; the production APK must be rebuilt separately.

### New runtime evidence

Latest `camera(8).txt` still exposes the expected lower-layer topology:

```text
role  60 -> camera 4 = [0, 2]
role  61 -> camera 5 = [0, 2]
```

But normal Photo does not use camera 4. On the first logged `1x -> 0.6x` tap:

```text
CAM_ManuallyValueChangeImpl: onDualZoomValueChanged: newValueRatio=0.6
CAM_Camera: onModeSelected from 0xa3 to 0xa3
CAM_PreDataSetup: resetType = 48
CAM_Camera2DataContainer: getActualOpenCameraId: mode=a3, id=0->2
CAM_CameraCapabilities: isSupportReplaceSession: false
CAM_Camera2OpenManager: openCamera: reusable = false
CAM_Camera2OpenManager: cid: 0 -> 2, mid: 163 -> 163, fcc: true
```

The log then tears down camera 0 and opens physical camera 2. Later Photo switching shows the same physical-ID behavior. Thus the current 0.6x lag is not a slow logical-SAT handoff; it is the original full physical-camera reopen path.

Do not optimize camera-2 startup yet. Restoring the logical camera-4 selection is the prerequisite.

### pref_telefix hypothesis ruled out

Universal 5.0 Beta 8.3 checks `UniversalSettings.isDisableTele()` early in `DataItemFeature.E8()`; its `pref_telefix` setting means "Disable SAT lens" and defaults false.

The device was checked directly:

```bash
grep -R -n "pref_telefix" \
  /data/user/0/com.android.camera/shared_prefs \
  /data/user_de/0/com.android.camera/shared_prefs
```

No persisted entry exists. Therefore a stale `pref_telefix=true` is not the reason the current build falls back to physical camera 2.

### Next evidence checkpoint

Before another patch:

1. Compare the installed `/system/priv-app/MiuiCamera/MiuiCamera.apk` with the rebuilt vendor prebuilt by hash.
2. Pull/decompile the installed APK and confirm its dex contains both SAT smali changes.
3. Verify the MiuiCamera RRO is enabled and the effective `pref_camera_dual_sat_enable_default` value is true.
4. If provenance is correct, trace the runtime `DataItemFeature.A` profile class and actual `E8()/CameraSettings.l6()` result. A profile-factory / `instance-of Alioth` mismatch is plausible but **not proven yet**.
5. Apply one patch only after that failing condition is identified.

VideoSAT remains separate; role 62 is absent and must not be remapped while Photo SAT itself is not active.

## Alioth-family variant/profile mapping and Universal deviceCodename cache

Runtime/device-tree identity must distinguish the marketing/mod-device variant from Android's canonical device codename.

From `device_xiaomi_alioth/libinit/libvariant_xiaomi_alioth.cpp`:

```text
POCO F3 Global
  hwc          = GLOBAL
  mod_device   = alioth_global
  name         = alioth_global
  device       = alioth
  marketname   = POCO F3
  model        = M2012K11AG

Mi 11X
  hwc          = INDIA
  mod_device   = aliothin
  name         = aliothin
  device       = aliothin
  marketname   = Mi 11X
  model        = M2012K11AI
```

For MiuiCamera, `Build.DEVICE` is the important fresh-source value: POCO F3 Global should therefore resolve as `alioth`, not `alioth_global`.

Universal 5.0's `com.mi.config.Device.<clinit>` does **not always use Build.DEVICE directly**. It first calls:

```text
ConfigManager.readFromMainFile("deviceCodename")
```

and only if that returns null does it use `Build.DEVICE` and persist it with:

```text
ConfigManager.writeToMainFile("deviceCodename", Build.DEVICE)
```

`ConfigManager.BASE_DIR` is:

```text
/storage/emulated/0/Download/XiaomiCamera/
```

and the main file is:

```text
/storage/emulated/0/Download/XiaomiCamera/general_config.json
```

The device-profile factory constructs `com.mi.device.<CapitalizedDeviceCodename>` reflectively and falls back to `Common` when the class does not exist. Therefore a stale cached `deviceCodename=alioth_global` would attempt `com.mi.device.Alioth_global`, miss the class, and silently fall back to `Common`. That would disable Alioth-specific feature overrides even though libinit correctly exposes `Build.DEVICE=alioth`.

Current direct verification command:

```bash
adb shell 'grep -n -A2 -B2 "deviceCodename" /sdcard/Download/XiaomiCamera/general_config.json 2>/dev/null || cat /sdcard/Download/XiaomiCamera/general_config.json 2>/dev/null'
```

Expected values:
- POCO F3 Global: `alioth`
- Redmi K40: `alioth`
- Mi 11X: `aliothin`

### Mi 11X inheritance

`com.mi.device.Aliothin` is declared:

```text
.class public final Lcom/mi/device/Aliothin;
.super Lcom/mi/device/Alioth;
```

Therefore current Alioth SAT changes already cover Mi 11X:
- an `Aliothin` instance satisfies `instance-of Alioth`;
- it inherits `Alioth.isSupportOpticalZoom() = true`.

Do not add a duplicate `isSupportOpticalZoom()` implementation to `Aliothin.smali` just for parity. Keep shared behavior in `Alioth`; override only if Mi 11X later proves a real device-specific difference.



## VideoSAT on Alioth logical role 60 — Stage 1 implemented, runtime pending

Current 5.x static analysis shows that Alioth did not provide its own VideoSAT overrides and therefore inherited from `Common`:

```text
supportVideoSAT()     -> false
getVideoSATCameraId() -> 62
```

The Universal camera role adapter does not hard-code an actual camera ID. It reads Xiaomi camera-role vendor tags into a role -> actual camera map, then asks `DataItemFeature.getVideoSATCameraId()` which role to use. The per-device profile hook is intentionally overrideable; other Xiaomi profiles select non-default VideoSAT roles.

Alioth runtime already exposes the working main+ultrawide logical camera as:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
role 62 -> absent
```

Therefore the first evidence-driven VideoSAT experiment is app-side reuse of role 60, not creation of fake provider metadata.

Implemented:

```text
decompiled_miui_camera:aosp-17
b07f52816f7a105e9906992717f6705fd1637767
MiuiCamera: alioth: Enable VideoSAT on logical SAT camera

device_xiaomi_camera:aosp-17
433cf879cb10dcf3e682ea515ebc507170c6b3d8
camera: alioth: Use logical SAT camera for video zoom
```

The patch:

- adds `Alioth.supportVideoSAT() = true`;
- adds `Alioth.getVideoSATCameraId() = 60`;
- bypasses stale Universal `ConfigManager` values for those two Alioth-family settings;
- preserves the existing disable-tele gate;
- automatically covers Mi 11X because `Aliothin extends Alioth`;
- does not alter proprietary CHI/provider binaries, camera-role metadata, replace-session, or camera reuse.

Runtime acceptance is intentionally limited to rear 1080p30 first. Video must open logical camera 4, remain on camera 4 during `0.6x <-> 1x` recording handoffs, and save a valid continuous video with audio. If logical camera 4 rejects the recording stream/session, inspect that exact CamX/CHI capability failure before considering lower-layer changes.

Do not manufacture role 62 merely to satisfy the app. The configurable role hook exists specifically to allow device-specific role selection.


### VideoSAT provider evidence from stock Alioth dump

Stock-dump grep adds a useful fallback clue for VideoSAT:

```text
vendor/lib[64]/hw/camera.qcom.so
vendor/lib[64]/hw/com.qti.chi.override.so
```

both contain `VideoSAT` strings, while the exact stock MiuiCamera role adapter explicitly references:

```text
getVideoSATCameraId(): #init() failed, roleId=62
```

Durable interpretation:

- stock Alioth camera code expects a VideoSAT role-62 concept;
- provider-side Qualcomm/CHI binaries contain VideoSAT-related implementation;
- string presence alone does **not** prove role 62 was exposed or required at runtime;
- keep the current first experiment on proven logical role 60 / camera 4 = `[0,2]`;
- if 1080p30 recording on role 60 fails at stream/session creation or VideoSAT metadata negotiation, inspect `camera.qcom.so` and `com.qti.chi.override.so` locally (strings/readelf, then Ghidra/IDA if needed) before synthesizing role 62 metadata or changing CHI blobs.

## Rollback to known-good VideoSAT baseline — 2026-09-23

After later 4K30/60fps experiments regressed camera behavior, active camera state was deliberately restored to:

```text
device_xiaomi_camera:aosp-17
433cf879cb10dcf3e682ea515ebc507170c6b3d8

GitLab vendor_xiaomi_camera:aosp-17
724fcf669cee9cb42f886c672b550f514a4b5c69
```

This is the working Stage-1 role-60 / logical-camera-4 VideoSAT baseline. The later 4K30, 1080p60, 4K60, stale-build-helper, and clean-rebuild artifact experiments are abandoned and intentionally removed from active durable memory.

Future rule: resume only from the Stage-1 baseline and make/test one isolated camera change at a time.

## September 24 baseline update

See [current baseline checkpoint](../today/2026-09-24-repository-baseline-alignment.md) for current branches, mandatory camera dependencies and documentation updates. This supersedes earlier checkout/head routing, not historical test evidence.
