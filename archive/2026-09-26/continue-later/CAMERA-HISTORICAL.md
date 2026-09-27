> CLOSED historical rollback record. Not a continuation plan. See [finalized camera](../memory/miuicamera.md).

# Camera continuation pointer

The user resumed camera work on September 23. Start from the
[latest validation checkpoint](../today/2026-09-23-camera-video-validation.md), not the old rollback below.
The tested current delivery heads are recorded there.

## Historical paused checkpoint (superseded)

# Continue Later — MiuiCamera / POCO F3 Camera Baseline

> **Paused work. Read this only when camera development is explicitly resumed.**
>
> This file preserves the last known-good VideoSAT rollback baseline after later 4K/60 fps experiments caused regressions. Camera is not an active task. Do not continue from those abandoned experiments unless the user explicitly reopens that work.

Last refreshed: **2026-09-23**

## Active source of truth

```text
GitHub
PocoF3Releases/device_xiaomi_camera:aosp-17
433cf879cb10dcf3e682ea515ebc507170c6b3d8
camera: alioth: Use logical SAT camera for video zoom
```

```text
GitLab
johnmart19/vendor_xiaomi_camera:aosp-17
724fcf669cee9cb42f886c672b550f514a4b5c69
camera: alioth: Update MiuiCamera for VideoSAT
```

Readable Stage-1 source reference:

```text
PocoF3Releases/decompiled_miui_camera
b07f52816f7a105e9906992717f6705fd1637767
MiuiCamera: alioth: Enable VideoSAT on logical SAT camera
```

The live `decompiled_miui_camera:aosp-17` branch may contain later abandoned experiment history. For the active baseline, use the exact Stage-1 commit above rather than assuming branch HEAD is authoritative.

## Verified VideoSAT topology

```text
role 60 -> logical camera 4 = physical [0,2]
role 61 -> logical camera 5 = physical [0,2]
role 62 -> absent
```

Alioth VideoSAT intentionally uses **role 60 / logical camera 4**.

Do not manufacture role 62 merely because generic Universal camera code has a role-62 default.

## Stage-1 implementation

The working implementation does four things:

1. `Alioth.supportVideoSAT()` returns true.
2. `Alioth.getVideoSATCameraId()` returns role 60.
3. `DataItemFeature.vb()` bypasses stale cached `supportVideoSAT=false` for Alioth/Aliothin.
4. `DataItemFeature.getVideoSATCameraId()` bypasses stale cached role 62 and returns role 60 for Alioth/Aliothin.

`Aliothin` inherits from `Alioth`.

Relevant role override:

```smali
iget-object v0, p0, Lcom/mi/config/DataItemFeature;->A:Lcom/mi/device/Common;

instance-of v0, v0, Lcom/mi/device/Alioth;

if-eqz v0, :alioth_video_sat_role

const/16 v0, 0x3c

return v0
```

`0x3c == 60`.

## Runtime result

The Stage-1 implementation was validated at **1080p30**:

```text
quality = 6
profileSize = 1920x1080
getActualOpenCameraId: mode=a2, id=0->4
```

Verified behavior:

- logical camera 4 remained open through the tested zoom loop;
- the app drove 0.6x on camera 4 without reopening physical camera 0/2;
- CHI/ArcSoft performed real SAT master handoffs between the physical members;
- eight completed `sat_switch_162_0` samples measured 233..327 ms;
- median handoff time was 252 ms.

The old validation did **not** conclusively prove final encoded-file/audio continuity because the supplied trace did not show a complete real recording start/stop cycle.

## Current rule

The restored baseline is the end of the active implementation.

Do not reintroduce the abandoned 4K30, 1080p60, 4K60, or clean-rebuild-helper experiment unless explicitly requested again from this known-good base.

If future VideoSAT work resumes:

1. first confirm the restored 1080p30 baseline still opens camera 4;
2. change only one behavior at a time;
3. test immediately;
4. do not batch multiple quality modes or packaging changes into one step;
5. only investigate CHI/provider behavior after the app actually opens logical camera 4 and a concrete session/stream failure occurs.

## Settled points

- `alioth_global` handling is already resolved by the Alioth profile path; do not reopen it without new evidence.
- role 60 / camera 4 is the working VideoSAT baseline.
- role 62 is absent from the proven runtime topology.
- stock Alioth camera is a provider/compatibility reference; MiuiCamera 5.x behavior remains the app-side feature reference.
- the known-good integration commit is **433cf879**.
- the known-good packaged APK commit is **724fcf66**.
- later 4K/60fps experiment commits are abandoned and must not be treated as active state.
