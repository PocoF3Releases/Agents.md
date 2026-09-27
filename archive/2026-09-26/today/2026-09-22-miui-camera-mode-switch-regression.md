# MiuiCamera Mode-Switch Regression Investigation (2026-09-22)

## Scope

Target: POCO F3 / `alioth`, Android 17, MiuiCamera Universal 5.0 Beta 8.3.

This record captures runtime findings after the static APK/native-library packaging work.

## Symptom

Camera mode switching is noticeably problematic. MiuiCamera repeatedly reports mode-switch performance timeouts and rebuilds camera capabilities while changing modules.

Example transition:

```text
mode change, mCurMode = 163, newMode = 171
onModeSelected from 0xa3 to 0xab
```

The transition later reports:

```text
trackModeSwitchCost: 1283
Event: SWITCH_MODULE_171_0 takes 1282 ms
Event: SWITCH_MODULE takes 1282 is more than 1000
Action: [HAL]startPreview2firstFrame_171_0 takes 638 ms
```

## Finding 1 — missing JPEG utility JNI

### Verified runtime evidence

During the real `0xa3 -> 0xab` switch, a pending JPEG reprocess completes and MiuiCamera tries to load:

```text
libcamera_jpegutil_jni.xiaomi.so
```

The device log shows:

```text
nativeloader: Load libcamera_jpegutil_jni.xiaomi.so using class loader ...
dlopen failed: library "libcamera_jpegutil_jni.xiaomi.so" not found

CAM_JpegUtil: couldn't find libcamera_jpegutil_jni.xiaomi.so
CAM_JpegUtil: getPlanesExtra: inited = false
```

This disproved the earlier static assumption that this JNI name was only an unused cross-device branch.

### 5.0 Beta 8.3 behavior

The shipped/decompiled code contains:

```text
System.loadLibrary("camera_jpegutil_jni.xiaomi")
nativeClassInit()
```

When available, the JNI helper accesses extra planes from:

```text
android.media.ImageReader$SurfaceImage
```

Consumers include the Qualcomm/MIVI reprocessing path.

### Implemented device-tree fix

The device tree now ships a pinned Xiaomi JPEG utility prebuilt and exposes it through the MiuiCamera app-local native-library directory:

```text
63594546455453b7749556f9ff1679be00eb981e
camera: native: Add MiuiCamera JPEG utility JNI
```

Source identity:

```text
TOCO Global V13.0.4.0.SFNMIXM
SHA-1 d159aebabed57516153a2d203d6104c80b4c1a95
```

Layout:

```text
device/xiaomi/camera/prebuilts/system/lib64/libcamera_jpegutil_jni.xiaomi.so

/system/lib64/libcamera_jpegutil_jni.xiaomi.so

/system/priv-app/MiuiCamera/lib/arm64/libcamera_jpegutil_jni.xiaomi.so
    -> /system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

This prebuilt is intentionally device-tree-owned; it does not need to live in the generated camera vendor repo.

First runtime validation after the JPEG utility integration found the library successfully by its app-local alias, but load then failed because its donor ELF still declared the obsolete dependency `libhidltransport.so`.

Follow-up compatibility commit:

```text
9a4cf71fbbbb69e31d20ad158c338bd600a9261c
camera: native: Drop obsolete HIDL transport dependency
```

The dependency was removed from the JPEG utility prebuilt rather than exposing the vendor-side legacy library to MiuiCamera's system app namespace.

A rebuild with this follow-up fix completed on 2026-09-22. Runtime validation on the newly installed build is pending.

## Finding 2 — capability cache is destroyed during initialization

### Verified code structure

In:

```text
smali_classes2/d/c/a/q6/t8/b/q.smali
Camera2CompatAdapterRole
```

the async camera-capability initializer recreates the shared capability `SparseArray` while iterating camera IDs.

In:

```text
smali_classes2/d/c/a/q6/t8/b/o.smali
Camera2CompatAdapter
```

`initCameraCapabilitiesByCameraId()` also creates a new shared `SparseArray` and then inserts only the requested camera.

This means repeated initialization can discard previously cached camera capabilities.

### Runtime evidence

After asynchronous initialization of available cameras, the log reports:

```text
mCapabilities.get(id)=null id=0
mCapabilities.get(id)=null id=1
mCapabilities.get(id)=null id=2
mCapabilities.get(id)=null id=3
mCapabilities.get(id)=null id=4
mCapabilities.get(id)=null id=5
mCapabilities.get(id)=null id=6
role: 101 (...) <-> 7
```

During a later module switch, the app rebuilds multiple IDs again:

```text
E: initCameraCapabilitiesByCameraId(): 5
X: initCameraCapabilitiesByCameraId(): 5

E: initCameraCapabilitiesByCameraId(): 0
X: initCameraCapabilitiesByCameraId(): 0
```

### Independent reference

MiuiCamera 6.2 uses persistent camera-capability caches and updates them with `put()`:

```java
capabilities.put(cameraId, capability);
characteristicsCache.put(cameraId, characteristics);
```

It does not replace the entire capability cache for each camera.

### Patch attribution

Current active `device_xiaomi_camera` APK patches do not modify the async capability initializer.

Therefore this cache bug is not attributed to the recent OpenCL/symlink cleanup.

Status: **fix #2 implemented and rebuilt into the vendor MiuiCamera prebuilt; runtime validation is pending**.

## ExtraPhoto is a separate integration

Alioth's `ExtraPhotoGlobal.apk` is required for the complete document/ID-card/refocus editing workflow, but it is not the root cause of the capability-cache mode-switch regression.

The integration was added separately in:

```text
423ae8e4a44f2bf2ef99807179c27f4624689c18
camera: extraphoto: Add stock Alioth companion app support
```

See [ExtraPhoto integration](2026-09-22-miui-camera-extraphoto-integration.md).

## Important sequencing

1. Collect fresh logs from the rebuild containing camera commit `9a4cf71f...` and NFC commit `8be75516...`.
2. Confirm JPEG utility JNI now loads without the obsolete `libhidltransport.so` dependency.
3. Confirm the unrelated NXP NFC tight log loop is gone so camera logs are readable.
4. Patch the capability cache so all camera IDs persist.
5. Re-test mode switching and compare switch timing/log behavior.
6. Validate ExtraPhoto document/ID-card handoff.
7. Only then investigate residual CamX/HAL errors.

Do not restore all previously removed camera symlinks as a blanket workaround.


## Fresh rebuilt runtime validation

The rebuild containing NFC commit `8be75516d6d3cfff3a95ca2f249f0b36ceededb9` and JPEG utility commit `9a4cf71fbbbb69e31d20ad158c338bd600a9261c` was installed and retested.

### NFC

The old `NFC client received bad message` tight loop is gone from both the new boot and camera logs.

### JPEG utility

The JPEG JNI now loads successfully:

```text
Load /system/priv-app/MiuiCamera/lib/arm64/libcamera_jpegutil_jni.xiaomi.so ...: ok
```

Native initialization succeeds and the app reports:

```text
CAM_JpegUtil: getPlanesExtra: inited = true
```

Multiple JPEG reprocess operations successfully returned SurfaceImage planes and continued into JPEG save processing. The old `libhidltransport.so` failure is gone.

### Capability cache — reproduced

Startup initializes camera IDs 0 through 7, but immediately after the asynchronous pass:

```text
mCapabilities.get(id)=null id=0
...
mCapabilities.get(id)=null id=6
role: 101 (72.3) <-> 7
```

Only the final camera survives in the shared cache.

The fresh run contained 104 actual `E: initCameraCapabilitiesByCameraId()` calls. Camera IDs 0, 2 and 5 were reconstructed repeatedly. One `0xa3 -> 0xab` mode switch alone triggered 15 capability initializations.

Measured mode-switch examples:

```text
0xa3 -> 0xa2:
  SWITCH_MODULE ≈ 2172 ms
  HAL startPreview -> first frame ≈ 335 ms

0xa3 -> 0xab:
  SWITCH_MODULE ≈ 1270 ms
  HAL startPreview -> first frame ≈ 580 ms
```

The large gap between total switch cost and HAL first-frame time strongly supports app-side setup/cache churn as a material contributor.

### Implemented cache fix

```text
4ba629723586315e06905b9c1b5d5104a1286a82
camera: capabilities: Preserve initialized camera cache
```

New patch:

```text
patches/camera-capabilities-cache.patch
```

The patch removes two incorrect whole-cache reallocations:

1. the per-camera allocation in `Camera2CompatAdapterRole.N()`;
2. the per-lookup allocation in `Camera2CompatAdapter.K()`.

It preserves the one cache allocation already performed by `Camera2CompatAdapterRole.init()` and lets `K()` append capabilities with `SparseArray.put()`.

Only two direct callers of `K()` exist in this 5.0 build: the role async initializer and the initialized capability getter. Both operate after the role adapter has allocated the cache.

The corrected apktool tree was rebuilt locally from `~/evo17/out/camera-capabilities-cache/decoded`, the resulting APK was 16 KiB aligned using the AOSP `zipalign -P 16` flow, and the canonical MiuiCamera prebuilt under `vendor/xiaomi/camera` was replaced with that rebuilt artifact.

This advances the cache fix from source-only to packaged-prebuilt state. Runtime validation is still pending: after the next build/install, confirm that camera IDs 0 through 7 remain resident after async initialization and compare `initCameraCapabilitiesByCameraId()` counts and mode-switch timings against the previous 104-initialization baseline.

### Secondary observations to revisit after the cache fix

- `CAM_ModuleUtil: ... invalid module: destroyed|alive` appears repeatedly during module teardown/switching. Treat it as secondary until cache churn is removed.
- A single early `surfaceTexture unavailable` warning occurs, but preview later starts and frames arrive.
- Several unsupported-role warnings remain; do not suppress them broadly without proving an Alioth feature needs those roles.
- No MiuiCamera FATAL EXCEPTION, native fatal signal, UnsatisfiedLinkError, or camera-specific `dlopen failed` remains in this fresh run.


### Decompiled-tree verification of cache lifecycle

A full decompiled working tree was pushed to:

```text
PocoF3Releases/decompiled_miui_camera
```

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

The decompiled repo was corrected to this canonical state:

```text
99da18c1fc7d6657b847a2306b8903676e8d26c8
MiuiCamera: Keep capability cache allocation in init
```

Do **not** add constructor cache initialization or a broad post-reset lazy allocation in `K()`. A stale async initializer should not be allowed to silently recreate cache state after a reset.

## Post-fix runtime validation — capability-cache regression closed

A fresh boot plus camera-session log from the rebuild containing the packaged capability-cache patch validates the fix.

### Installed artifact freshness

The boot log rejects stale MiuiCamera ART artifacts because the dex checksum no longer matches the installed `/system/priv-app/MiuiCamera/MiuiCamera.apk`, then performs a fresh `boot-after-ota` dex2oat pass for `com.android.camera`. This is consistent with the rebuilt MiuiCamera package being installed rather than re-testing the previous APK.

Current source heads were rechecked and have not drifted:

```text
PocoF3Releases/device_xiaomi_camera:aosp-17
4ba629723586315e06905b9c1b5d5104a1286a82

PocoF3Releases/decompiled_miui_camera:aosp-17
99da18c1fc7d6657b847a2306b8903676e8d26c8
```

### Capability-cache acceptance result

The role initializer reports camera IDs `[0, 1, 2, 3, 4, 5, 6, 7]`. The complete camera log contains exactly one `E: initCameraCapabilitiesByCameraId()` call for each ID, for 8 actual initializations total. There are no later capability rebuilds and no `mCapabilities.get(id)=null` lines.

Compared with the 104-call pre-fix baseline, capability initialization churn dropped by 92.3%.

Result: **commit `4ba629723586315e06905b9c1b5d5104a1286a82` is runtime-validated fixed**.

### Runtime safety / linker regression check

The camera-session log has no MiuiCamera fatal exception, native fatal signal, `UnsatisfiedLinkError`, camera-device fatal error, or camera-specific `dlopen failed`. The only `dlopen failed` entries in the camera-session log belong to an unrelated Pixel device-personalization text-classifier process.

JPEG utility behavior remains correct:

```text
Load .../libcamera_jpegutil_jni.xiaomi.so ...: ok
CAM_JpegUtil: getPlanesExtra: inited = true
```

### Mode-switch timing after the cache fix

Seven completed deliberate mode switches after initialization:

```text
163 -> 171 : 1118 ms
171 -> 173 :  694 ms
173 -> 254 :  598 ms
171 -> 163 :  691 ms
163 -> 162 : 1144 ms
162 -> 186 :  706 ms
186 -> 167 :  686 ms
```

Median: **694 ms**. Five of seven completed below the app's 1000 ms warning threshold.

For the two slower completed cases:

```text
163 -> 171:
  HAL startPreview -> first frame = 639 ms
  total = 1118 ms

163 -> 162:
  cameraOpened -> createCaptureSession = 365 ms
  HAL createCaptureSession = 193 ms
  switch_module_setup = 545 ms
  HAL startPreview -> first frame = 253 ms
  total = 1144 ms
```

The same named pre-fix examples were approximately 1270 ms for `163 -> 171` and 2172 ms for `163 -> 162`. This is not a controlled benchmark, so do not attribute every timing difference solely to the cache fix.

### Remaining investigation

The capability-cache regression is closed and should not be reopened unless future logs show renewed cache loss/churn.

Residual unsupported-role warnings, module-teardown messages, and CamX/CHI messages are secondary unless tied to a reproducible feature failure. For performance, repeat `163 -> 171` and `163 -> 162`; if they remain visibly slow, inspect their mode-specific capture-session/HAL setup. Do not restore broad camera symlink or compatibility-library workarounds from this log.

## Photo lens-switch stress run

A second follow-up log was captured after repeatedly tapping Photo-mode zoom/lens controls.

### Scope correction

This run does **not** repeat the two slower module transitions `163 -> 171` and `163 -> 162`. It exercises same-mode Photo reselection:

```text
onModeSelected from 0xa3 to 0xa3
```

The user action alternates physical lenses through the zoom UI:

```text
0.6x -> physical camera ID 2
1x/2x -> physical camera ID 0
```

### Stress results

22 completed same-mode lens switches were parsed from `trackModeSwitchCost`:

```text
n       = 22
median  = 854 ms
mean    = 861 ms
minimum = 732 ms
maximum = 961 ms
>=1 s   = 0
```

Direction split:

```text
camera ID 2 / 0.6x:
  n = 11
  total median = 917 ms
  total mean   = 913.7 ms
  range        = 858..961 ms
  preview->first-frame median = 451 ms

camera ID 0 / 1x-2x:
  n = 11
  total median = 823 ms
  total mean   = 808.2 ms
  range        = 732..850 ms
  preview->first-frame median = 382 ms
```

The slower 0.6x direction is primarily explained by its longer HAL preview-to-first-frame interval. Session creation and module setup are broadly similar between the two directions.

### Cache stress result

The full file contains 16 actual capability initializations because it contains two separate MiuiCamera processes. The first process initializes IDs 0..7 once, is later killed by ActivityManager because its task is removed, and the replacement process initializes IDs 0..7 once again.

After the second initialization pass, all 22 lens switches complete without any additional `initCameraCapabilitiesByCameraId()` call and with zero `mCapabilities.get(id)=null` messages.

This strengthens the runtime conclusion: the persistent-cache patch remains correct under repeated physical-camera switching.

### Physical-camera reopen behavior

Switching 0.6x <-> main-lens zoom is not a lightweight in-session zoom change on this configuration. MiuiCamera resolves camera ID 2 for 0.6x and camera ID 0 for main-lens zoom, then reports:

```text
isSupportReplaceSession: false
openCamera: reusable = false
```

and performs a real close/open for each physical camera change.

Do not enable replace-session or reuse paths speculatively. The current behavior is consistent and all stress switches remained below the application's 1000 ms warning threshold.

### Instrumentation limitation

All 22 same-mode switches log:

```text
Event: SWITCH_MODULE has no start time, ignore this stop event as take 0 ms
```

while `trackModeSwitchCost` records valid costs. This is a performance-instrumentation mismatch for same-mode lens reselection, not a functional switch failure.

### Native RefBase warning

The stress interval contains 2040 occurrences of:

```text
RefBase: Explicit destruction, weak count = 0
```

with call-stack logging unavailable. The Android warning states that weak-count-zero explicit destruction can leak the `weakref_impl` bookkeeping object.

There is no PSS/RSS sampling, OOM, crash, ANR, or clear progressive switch-time degradation in this log, so this is **not yet a proven material memory leak**. Keep it as a low-priority native/vendor compatibility observation. A future long-duration test should pair repeated lens switching with periodic `dumpsys meminfo com.android.camera` before changing code.

### Remaining performance task

The previous focused module-switch question remains open: repeat `163 -> 171` and `163 -> 162` if their >1 s behavior is still user-visible. This lens-switch stress run must not be used as evidence that those two module transitions are below threshold.

## Seamless SAT feasibility investigation

The user asked whether Alioth can be changed from ~0.8-0.9 s physical camera switching to modern seamless 0.6x <-> 1x behavior, including video.

### New vendor evidence

`PocoF3Releases/vendor_xiaomi_alioth:aosp-17` already enables:

```text
multiCameraEnable=TRUE
enableSensorHWSync=1
multiCameraFrameSync=1
```

and packages Qualcomm/Xiaomi SAT components:

```text
com.qti.node.dummysat
libarcdualcamsat
libarcmulticamsat
```

This materially changes the feasibility assessment: the platform is not missing all multi-camera support.

### Current missing layer

MiuiCamera repeatedly requests a VideoSAT role and fails to resolve it:

```text
getVideoSATCameraId(): #init() failed, roleId=62
```

Current Photo lens switching still chooses physical camera ID 2 for 0.6x and ID 0 for main-camera zoom, with replace-session and reuse disabled. That forces a full close/open and explains why the measured cost is hundreds of milliseconds rather than a few frames.

### Architecture target

Preferred target:

```text
MiuiCamera
  -> one logical rear SAT CameraDevice/session
     -> physical ID 2 (ultrawide) below crossover
     -> physical ID 0 (main) at/above crossover
  -> CONTROL_ZOOM_RATIO / Xiaomi SAT vendor metadata
  -> HAL switches active physical sensor without closing the logical device
```

Because POCO F3 has no telephoto sensor, 2x remains digital crop on camera ID 0. The seamless physical transition problem is only 0.6x ultrawide <-> main.

### Next proof required

Before modifying app logic, inspect provider metadata and determine whether a logical rear camera already exists and includes physical IDs 0/2. If yes, map MiuiCamera VideoSAT role 62 to it and test in-session zoom. If no, investigate CHI/CamX logical camera/usecase configuration and role metadata.

Do not force `isSupportReplaceSession` or `reusable` true on the current separate physical-camera path; that does not create a logical multi-camera pipeline.

## Source-role correction — decompiled_miui_camera is stock Alioth camera

User clarification plus repository/archive verification establishes that:

```text
PocoF3Releases/decompiled_miui_camera:aosp-17
Library /decoded.zip
```

are the **stock Alioth MiuiCamera decompiled reference tree**.

They are not the authoritative source tree for the Universal 5.x mod currently shipped in the ROM. Earlier session text that referred to this repo as the decompiled mod source is superseded by this correction.

The production 5.x mod remains a separate patched prebuilt/worktree integrated through `PocoF3Releases/device_xiaomi_camera:aosp-17`.

Use the stock repo/archive for:

- Alioth-specific camera-role and capability behavior;
- stock provider/metadata expectations;
- device-specific compatibility logic;
- comparison against the 5.x mod;
- reconstructing stock-supported paths when porting them into the mod.

Never assume a stock smali implementation exists in the 5.x mod without independently checking the mod APK/worktree.

## Logical SAT Photo fix implementation

The provider topology from runtime is sufficient for Photo SAT without HAL reconstruction:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
VideoSAT role 62 -> absent
```

Current 5.x APK analysis found `pref_camera_dual_sat_enable_default=true`, so the missing gate was optical-zoom support. Alioth implements `isSupportedOpticalZoom() = true`, but `DataItemFeature.E8()` calls the differently named `isSupportOpticalZoom()`, inherited as false from `Common`. `modify.ConfigManager` then persists that computed false value in `Download/XiaomiCamera/<device>.json`.

Implemented in:

```text
PocoF3Releases/device_xiaomi_camera:aosp-17
36fbb1d503d7c23f17e0daf73efc020ed5ffa0d0
camera: alioth: Use logical SAT camera for photo zoom
```

The patch adds the correctly named Alioth profile method, bypasses the stale generated false cache for Alioth after Universal Settings overrides, and keeps dual SAT enabled by default through the RRO.

Static result: normal Photo selection now satisfies `F3 && l6`, `J6` is false for Alioth's >=3-lens topology, and `Camera2DataContainer.D()` resolves role 60 -> logical camera 4.

Runtime validation is pending. A passing log must show camera 4 remaining open across repeated 0.6x/1x/2x changes instead of physical 0<->2 reopen events. Only after that should timing be compared against the old 854 ms median / 961 ms max stress baseline.

VideoSAT is intentionally not changed because role 62 is absent.

## Staged rebuild/test plan

User requested an explicit one-step-at-a-time workflow because long multi-part investigations can time out and, more importantly, later decisions depend on real device behavior.

### Stage 1 — current

Apply/build/test:

```text
36fbb1d503d7c23f17e0daf73efc020ed5ffa0d0
camera: alioth: Use logical SAT camera for photo zoom
```

Acceptance:

- Photo opens logical camera ID 4 (role 60, physical `[0,2]`);
- repeated `0.6x <-> 1x <-> 2x` no longer causes physical `cid: 0 -> 2` / `2 -> 0` reopen;
- collect a focused camera log and compare timing with the old 854 ms median / 961 ms maximum.

Stop after this runtime test.

### Stage 2 — pending Stage 1 result

If camera 4 stays open, inspect whether zoom changes remain within the existing capture session or still rebuild the session. Only then decide whether an additional app/session patch is needed.

### Stage 3 — pending healthy Photo SAT

Investigate VideoSAT separately. Alioth runtime exposes roles 60/61 but no role 62. Do not remap video to role 60 without a dedicated patch and rebuild/test checkpoint.

### Stage 4 — pending stable behavior

Optimize remaining transition latency toward ~100-250 ms only after the correct logical-camera/session architecture is proven on device.

Rule: do not research/implement later stages ahead of the current user rebuild result unless the user explicitly asks to skip the staged workflow.

## Canonical SAT execution plan — exact current checkpoint

This section supersedes shorter earlier SAT stage notes where they conflict.

### Canonical source state

```text
device_xiaomi_camera:aosp-17
d928f68b12f46e532a3e4735f4401c99359fdd52
camera: alioth: Use logical SAT camera for photo zoom
```

Earlier temporary SHAs `36fbb1d...` and `a336a285...` were superseded by history cleanup.

Current decoded mod tree:

```text
~/evo17/out/camera-capabilities-cache/decoded
```

Last confirmed result is a clean dry-run against:

```text
smali_classes7/com/mi/config/DataItemFeature.smali
smali_classes7/com/mi/device/Alioth.smali
```

The user has not yet reported actual patch application or rebuilt-device runtime.

### Stage 1 — apply/rebuild/test Photo logical SAT

Apply:

```bash
cd ~/evo17/device/xiaomi/camera
git pull --ff-only origin aosp-17
cd ~/evo17/out/camera-capabilities-cache/decoded
patch -p1 < ~/evo17/device/xiaomi/camera/patches/alioth-logical-sat.patch
```

Verify:

```bash
grep -n -A12 -B4 "alioth_optical_zoom_cache" smali_classes7/com/mi/config/DataItemFeature.smali
grep -n -A8 -B2 "isSupportOpticalZoom" smali_classes7/com/mi/device/Alioth.smali
```

Build and 16 KiB-align:

```bash
apktool b . -o ../MiuiCamera-logical-sat-unaligned.apk
~/evo17/out/host/linux-x86/bin/zipalign -P 16 -f -v 4 ../MiuiCamera-logical-sat-unaligned.apk ../MiuiCamera-logical-sat.apk
cp -f ../MiuiCamera-logical-sat.apk ~/evo17/vendor/xiaomi/camera/proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk
```

Then rebuild/install the ROM normally.

Capture:

```bash
adb logcat -c
adb logcat -v threadtime > sat-photo.txt
```

Exercise Photo:

```text
1x -> 0.6x -> 1x -> 2x -> 0.6x -> 1x
```

Stage 1 pass criteria:

- role 60 still maps to logical camera `4 = [0,2]`;
- Photo actually opens camera 4;
- `0.6x <-> 1x` no longer causes physical `cid: 0 -> 2` / `2 -> 0` reopen;
- no camera fatal/device/linker regression;
- timing is recorded but not considered solved until session behavior is known.

### Stage 2 — branch on Stage 1 runtime

**Outcome A — camera 4 and capture session both stay alive**

- measure zoom-request to physical handoff / first stable frame;
- confirm true in-session SAT;
- only then tune residual latency toward ~100-250 ms.

**Outcome B — camera 4 stays open but capture session is recreated**

- trace the same-mode `163 -> 163` zoom UI path;
- identify why zoom still triggers module/session reconfiguration;
- patch SAT zoom to update the existing repeating request/session;
- make one patch, rebuild, retest.

**Outcome C — app still opens physical 0/2**

- inspect `CameraSettings.l6()` / `DataItemFeature.E8()` runtime state;
- verify installed RRO `pref_camera_dual_sat_enable_default=true`;
- inspect Universal Settings / `modify.ConfigManager` persisted override state;
- do not change CamX yet.

**Outcome D — camera 4 opens but session/preview fails**

- collect exact stream/CamX/CHI failure;
- compare role 60 and role 61 semantics;
- do not blindly switch roles or force replace-session/reusable flags.

### Stage 3 — Photo SAT stability

- stress 50-100 handoffs;
- verify actual capture at 0.6x/1x/2x;
- check AF/AE/HDR crossover behavior;
- confirm no cache regression or camera-device errors;
- compare against old physical-switch baseline: median 854 ms, max 961 ms.

### Stage 4 — VideoSAT

Known topology:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
role 62 -> absent
```

Plan:
1. Trace current 5.x `supportVideoSAT()` and `getVideoSATCameraId()`.
2. Compare stock/other Xiaomi profiles that enable VideoSAT.
3. Determine role/usecase from evidence; do not assume role 60.
4. Make one isolated VideoSAT patch.
5. First test 1080p30 while recording across `0.6x <-> 1x`.
6. Verify recording continuity, audio, timestamps, preview, and no reopen/crash.
7. Only then test EIS/4K.

### Stage 5 — unrelated real mode switches

Retest `163 -> 171` and `163 -> 162` separately after SAT work. Do not mix those results with lens handoff.

### Stage 6 — optional RefBase/memory follow-up

If RefBase warnings remain after camera teardown is reduced, run a long switch test with periodic:

```bash
adb shell dumpsys meminfo com.android.camera
```

Only investigate native leakage if memory growth is actually demonstrated.

### Workflow rule

One patch + exact apply/rebuild/test instructions per stage, then stop for the user's runtime result. Do not pre-implement later stages.

## Stage 1/2 runtime validation — logical SAT works in-session

Runtime inputs:

```text
camera log: 2026-09-22 ~11:02
boot log:   2026-09-22 ~11:00
source:     device_xiaomi_camera:aosp-17 @ d928f68b12f46e532a3e4735f4401c99359fdd52
```

### Stage 1 — PASS

Photo now resolves to logical camera 4. The opening path reports `id=0->4`, `cid: -1 -> 4`, then the same-mode setup reports `cid: 4 -> 4`, excludes camera 4 from close, and says camera 4 is already open.

Across the complete camera log there are only six Camera2OpenManager transitions:

```text
-1 -> 4   160 -> 163   initial Photo
 4 -> 4   163 -> 163   Photo same-mode setup
 4 -> 0   163 -> 162   intentional Photo -> Video
 0 -> 0   162 -> 162   Video same-mode setup
 0 -> 4   162 -> 163   intentional Video -> Photo
 4 -> 4   163 -> 163   Photo same-mode setup
```

There is no Photo physical-camera `0 -> 2` or `2 -> 0` reopen.

### Stage 2 — PASS, Outcome A

The Photo capture session survives the zoom loop. `createCaptureSession` is seen only at Photo/Video module setup boundaries, not during repeated Photo zoom taps. The zoom path calls `setZoomRatio`, updates the existing request and resumes preview on `cameraId=4`.

CHI/CamX then changes the internal SAT master. The first cold ultrawide activation starts with `active_map=0x2`, grows to `0x3`, and then both rear pipelines remain available in the logical session.

Measured Photo zoom data:

```text
Photo toggle actions:            20
completed sat_switch_163_0:      18
durations (ms):                  288,309,299,288,355,435,403,458,304,280,303,283,298,274,299,250,270,254
median:                          299 ms
mean:                            314 ms
range:                           250..458 ms

first Photo run:                 14 samples, median 301 ms, mean 327 ms, range 274..458 ms
second/warmed Photo run:          4 samples, median 262 ms, mean 268 ms, range 250..299 ms
```

Twenty Photo taps but eighteen completed timing records is consistent with quick/overlapping UI updates being coalesced; do not invent missing timings.

Cold/warm internal-master observations from timestamp correlation:

```text
first  1x -> 0.6x: click -> logged master 2->1 ≈ 617 ms; active_map 0x2 -> 0x3
second 1x -> 0.6x: click -> logged master 2->1 ≈ 306 ms
0.6x -> 1x: early logged master 1->2 edges ≈ 105/117 ms; first cold return briefly bounces
```

Use `sat_switch` as the safer app-visible handoff metric; the first internal-master metadata edge is not necessarily the fully settled preview.

### Regression checks

- no MiuiCamera `FATAL EXCEPTION`, native `Fatal signal`, `UnsatisfiedLinkError`, or app-specific linker failure;
- capability cache still performs exactly eight real camera-capability initializations and does not rebuild during zoom;
- JPEG utility JNI remains initialized;
- vendor handoff emits some nonfatal buffer notifications/fallback messages; no code change is justified from those messages alone.

### Boot-time dual-camera calibration warning

Before provider registration, CHI logs missing dual-camera persist calibration for camera role 0. The provider then loads/registers and cameraserver enumerates it normally.

Current source already creates `/mnt/vendor/persist/camera` and grants the camera HAL read access, and this boot log has no camera SELinux denial. Keep this as an unresolved quality/alignment risk rather than adding guessed calibration data.

### Stage 3 — CURRENT

No rebuild or code patch is needed for the next checkpoint. Collect one focused long Photo run:

```bash
adb logcat -c
adb logcat -v threadtime > sat-photo-stage3.txt
```

During capture:

```text
- perform 50-100 handoffs, prioritizing 1x <-> 0.6x
- sprinkle 2x taps
- take real photos at 0.6x, 1x and 2x
- test autofocus, exposure changes and HDR
- watch for visual jump/alignment/color/exposure mismatch at the 0.6x <-> 1x crossover
```

Also collect the actual persist-camera inventory:

```bash
adb shell 'ls -laZ /mnt/vendor/persist/camera; find /mnt/vendor/persist/camera -maxdepth 2 -type f -print 2>/dev/null'
```

If RefBase warnings remain relevant during the long run, take memory snapshots before/after with:

```bash
adb shell dumpsys meminfo com.android.camera
```

Only after this Stage 3 evidence should another Photo SAT patch be considered. VideoSAT remains Stage 4 and still must not be mapped speculatively because role 62 is absent.

## Latest rebuild correction — current Photo SAT test fails Stage 1

Newest runtime input:

```text
camera(8).txt
captured 2026-09-22 ~13:52
```

This runtime supersedes the earlier current-build PASS entry above.

Provider topology is still present and correct:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
```

However the first Photo `1x -> 0.6x` action follows the legacy physical-camera path:

```text
newValueRatio=0.6
onModeSelected 0xa3 -> 0xa3
resetType = 48
getActualOpenCameraId: mode=a3, id=0->2
isSupportReplaceSession: false
openCamera: reusable = false
cid: 0 -> 2, mid: 163 -> 163
```

The camera module is destroyed, physical camera 0 is closed, and physical camera 2 is opened. Later Photo switches repeat the same behavior. This directly explains the user's report that launching 0.6x still lags heavily.

The current issue is therefore **not** residual logical-SAT handoff latency. The installed build is not taking the intended camera-4 SAT branch.

### Preference check

A direct device grep found no persisted `pref_telefix` entry under either Camera shared-preferences directory. That removes the leading Universal Settings override hypothesis.

### Current one-step investigation

Do not make another camera behavior patch yet. First verify:

```text
A. installed MiuiCamera APK hash == rebuilt vendor prebuilt hash
B. installed dex contains the DataItemFeature.E8() Alioth bypass
C. installed dex contains Alioth.isSupportOpticalZoom() = true
D. MiuiCamera RRO is enabled and dual-SAT default resolves true
E. if A-D pass, inspect actual runtime device-profile class and E8()/l6() result
```

Only after the exact failing gate is found should the next single patch be made. Do not touch VideoSAT, CamX replace-session, or reusable-camera behavior in this checkpoint.

## Alioth Global / Mi 11X profile routing clarification

The product variant name is not necessarily the Camera device-profile name.

Current libinit mapping:

```text
POCO F3 Global:
  mod_device/name = alioth_global
  device          = alioth

Mi 11X:
  mod_device/name = aliothin
  device          = aliothin
```

So on a fresh configuration POCO F3 Global should instantiate `com.mi.device.Alioth`, while Mi 11X should instantiate `com.mi.device.Aliothin`.

`Aliothin` extends `Alioth`, so the current logical-SAT patch is already shared with Mi 11X by inheritance. No duplicate Aliothin smali patch is needed.

However Universal Camera persists its own `deviceCodename` in:

```text
/storage/emulated/0/Download/XiaomiCamera/general_config.json
```

and reads that value before `Build.DEVICE`. A stale `alioth_global` cached value would make the reflection factory search for a nonexistent `com.mi.device.Alioth_global` and fall back to `Common`, which is now a leading explanation for the latest physical-camera 0 -> 2 runtime.

Next single device check:

```bash
adb shell 'grep -n -A2 -B2 "deviceCodename" /sdcard/Download/XiaomiCamera/general_config.json 2>/dev/null || cat /sdcard/Download/XiaomiCamera/general_config.json 2>/dev/null'
```

Do not patch further until this value is known.

