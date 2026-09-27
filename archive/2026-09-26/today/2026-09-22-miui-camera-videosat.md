# MiuiCamera VideoSAT — Alioth Stage 1

## Scope

Move from Photo SAT work to the first isolated VideoSAT implementation for POCO F3 / Redmi K40 / Mi 11X on the Universal 5.x camera stack.

## Current state

Stage 1 code is implemented and pushed. Runtime validation on a rebuilt device is pending.

Known runtime provider topology:

```text
role 60 -> camera 4 = [0,2]
role 61 -> camera 5 = [0,2]
role 62 -> absent
```

## Static findings

Universal Camera builds its camera role table from Xiaomi CameraCharacteristics vendor tags:

```text
com.xiaomi.cameraid.role.cameraIds
com.xiaomi.cameraid.role.cameraId
```

Its VideoSAT path resolves a configurable role through `DataItemFeature.getVideoSATCameraId()`, rather than requiring actual camera ID 62.

Relevant VideoSAT capability tags present in newer Xiaomi Camera code include:

```text
com.xiaomi.camera.videomultisat.enable
com.xiaomi.camera.videosat.zoomRange
com.xiaomi.videosat.supportedRange
```

The current Alioth profile had no VideoSAT overrides. It inherited from `Common`:

```text
supportVideoSAT()     = false
getVideoSATCameraId() = 62
```

That creates two independent app-side blockers before any recording session is attempted.

Other Xiaomi profiles prove `getVideoSATCameraId()` is designed for per-device role selection, so using a non-default role is supported by the app architecture.

## Implemented change

Readable source:

```text
PocoF3Releases/decompiled_miui_camera:aosp-17
b07f52816f7a105e9906992717f6705fd1637767
MiuiCamera: alioth: Enable VideoSAT on logical SAT camera
```

Build integration patch:

```text
PocoF3Releases/device_xiaomi_camera:aosp-17
433cf879cb10dcf3e682ea515ebc507170c6b3d8
camera: alioth: Use logical SAT camera for video zoom

patches/alioth-video-sat.patch
```

Behavior:

1. `Alioth.supportVideoSAT()` returns true.
2. `Alioth.getVideoSATCameraId()` returns role 60.
3. `DataItemFeature.vb()` returns true for Alioth/Aliothin after the existing disable-tele/debug gates, before reading a stale cached false.
4. `DataItemFeature.getVideoSATCameraId()` returns role 60 for Alioth/Aliothin before generic Universal/cached role selection.
5. `Aliothin` inherits the implementation from `Alioth`.

No provider/CHI binary, role metadata, Video module, replace-session, or reusable-camera changes were made.

## Why role 60 first

Role 60 is already proven at runtime to resolve to logical camera 4 backed by physical cameras 0 and 2. This makes it the smallest testable route to a seamless main/ultrawide video session.

Adding synthetic role 62 metadata would be a broader lower-layer intervention without proof that role 62 needs a distinct provider usecase on Alioth.

## Runtime checkpoint

First test only rear 1080p30.

After rebuilding, begin a recording and exercise:

```text
1x -> 0.6x -> 1x -> 2x -> 0.6x -> 1x
```

Collect a focused camera log.

Stage 1 PASS requires:

- Video mode resolves/open camera 4;
- no physical camera `0 -> 2` / `2 -> 0` CameraDevice reopen during recording;
- recording does not stop or restart across zoom handoffs;
- saved file is playable and has continuous audio/video/timestamps;
- no fatal app/native/camera-device failure.

If camera 4 opens but recording-session creation fails, capture the exact stream configuration / CamX / CHI error. That failure decides whether VideoSAT needs provider capability/usecase work.

If camera 4 works for 1080p30, only then test higher-risk combinations such as EIS, 4K30, and 4K60.

## Future-agent rule

Do not reopen Photo SAT or manufacture provider role 62 before the Stage 1 VideoSAT result unless new runtime evidence requires it. Keep one patch/test checkpoint at a time.


## Stock-dump / provider binary evidence

Additional evidence from the Alioth stock dump was collected after the Stage 1 app-side role-60 patch was pushed.

A recursive grep from the extracted stock dump reports the literal `VideoSAT` in both 32-bit and 64-bit provider-side camera binaries:

```text
vendor/lib/hw/camera.qcom.so
vendor/lib/hw/com.qti.chi.override.so
vendor/lib64/hw/camera.qcom.so
vendor/lib64/hw/com.qti.chi.override.so
```

The exact stock MiuiCamera smali also contains extensive VideoSAT plumbing. Relevant call sites include:

```text
CameraZoomAnimateDrawable.mVideoSATZoomSpline
HardwareCapabilities -> getVideoSATCameraId()
ComponentConfigVideoQuality -> getVideoSATCameraId()
UserRecordSetting.isInVideoSAT()
VideoModule -> supportVideoSATForVideoQuality() / getVideoSATCameraId()
BaseModule.isInVideoSAT()
CameraSettings.isSettingsVideoSATEnable()
CameraSettings.supportVideoSATForVideoQuality()
```

Most importantly, the stock role adapter contains the explicit diagnostic:

```text
Warning: getVideoSATCameraId(): #init() failed, roleId=62
```

### Interpretation

**Verified static fact:** stock Alioth MiuiCamera is architected to request VideoSAT role 62, and the stock Qualcomm/CHI provider binaries contain VideoSAT-related code/strings.

**Not yet verified:** the presence of those strings does not prove that role 62 was actually exposed in the stock runtime topology, nor that role 62 is required for successful VideoSAT recording on the current AOSP stack.

The current Stage 1 experiment therefore remains unchanged:

```text
Alioth supportVideoSAT() = true
Alioth getVideoSATCameraId() = 60
role 60 -> logical camera 4 = [0,2]
first runtime test = rear 1080p30 recording
```

Role 60 is still the smallest evidence-driven test because it is already proven to expose the required main+ultrawide logical camera. Do not manufacture role 62 before this runtime result.

### Provider-side fallback if Stage 1 fails

If logical camera 4 opens but Video recording/session creation fails, or the HAL reports missing VideoSAT capability/usecase metadata, investigate the provider binaries before applying another app-side workaround.

Priority binaries:

```text
/vendor/lib64/hw/camera.qcom.so
/vendor/lib64/hw/com.qti.chi.override.so
```

Recommended local analysis against the stock dump/current vendor copies:

```bash
strings -a vendor/lib64/hw/camera.qcom.so | grep -i -E 'videosat|multisat|role|cameraid'
strings -a vendor/lib64/hw/com.qti.chi.override.so | grep -i -E 'videosat|multisat|role|cameraid'
readelf -Ws vendor/lib64/hw/camera.qcom.so | grep -i -E 'sat|multi|role'
readelf -Ws vendor/lib64/hw/com.qti.chi.override.so | grep -i -E 'sat|multi|role'
```

If strings/symbols are insufficient, use Ghidra/IDA to locate the VideoSAT string references and the role/usecase-selection logic. Compare stock-dump provider binary hashes against the current `vendor_xiaomi_alioth:aosp-17` copies before assuming behavior differs.

Current vendor-tree static groundwork remains:

```text
multiCameraEnable=TRUE
enableSensorHWSync=1
multiCameraFrameSync=1
com.qti.node.dummysat
libarcdualcamsat
libarcmulticamsat
```

This makes a provider-specific VideoSAT path plausible, but still unproven until the Stage 1 recording test supplies runtime evidence.
