# MiuiCamera — retained integration

The accepted integration and mode limits are retained. The explicit October 24
hardware recheck added the bounded CamX guard below; it does not reopen speculative
mode tuning or establish new camera-mode acceptance.

## Canonical delivery

Both `PocoF3Releases/device_xiaomi_camera:aosp-17` and GitLab `johnmart19/vendor_xiaomi_camera:aosp-17` are required. [The source map](../state/repositories.yaml) owns observed heads. Historical implementation heads remain in the dated evidence; use the source map for current identities.

Use the vendor prebuilt `proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk`, installed under `/system/priv-app/MiuiCamera/`. Accepted APK: **223517496 bytes**, SHA-256 `29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`. It is for ROM platform signing, not a newly signed ordinary user-install APK. MiuiCamera 5.x defines feature/ABI requirements; Alioth stock 4.x is a compatibility reference, not replacement delivery authority.

## Final behavior and boundaries

Logical VideoSAT is role 60 / Android camera 4. Do not invent role 62 or confuse vendor ArcSoft master ID 3 with Android physical camera ID 3. The 60fps patch preserves non-EIS session `0xf010` instead of overwriting it with `0x803c`. The ultrawide guard removes sub-1x choices in 4K and clamps stale toolbar selection before rebuilding controls; intermediate failure was `Illegal zoom ratio: 0.6, zoomRatios = [1.0, 2.0]`.

Main 4K30/60 and ultrawide 1080p were accepted. Ultrawide UI 1080p60 measured about 30fps; do not advertise true ultrawide 60fps. Unsupported 0.6x 4K selection is blocked and resolution changes safely restore 1x. The IMX355 pipeline failure showed DSX error 67108866 / MNDS DS16 errors; this is not proof every hypothetical software-upscale pipeline is impossible. [V-CAMERA](../state/validation.md#v-camera) owns the exact six-clip matrix, packaging checks and temporary-install limits.

## Retained implementation lessons

Current integration includes runtime/JNI/capability-cache and Xiaomi compatibility work. Preserve native library/partition ABI, permission/SELinux ownership, JPEG utility, ExtraPhoto and cache evidence. CameraX vendor-extension and unused MiSys integrations were removed; do not restore them because old notes mention them. Maintain the existing apktool patch flow in the device tree and ready-to-use APK in the vendor tree, rather than rebuilding from an old decompiled/Stage-1 rollback experiment.

Earlier HEIF notes report direct HeifWriter lifecycle/planar-input fixes and JPEG-versus-HEIF chroma comparisons; those are historical validation, not a fresh acceptance of every current camera mode. Old native audits, failed patches, exact binary identifiers and alternative designs remain intact in [camera history](miuicamera.md) and [dated camera evidence](miuicamera.md). Retrieve only the relevant section for a provenance question. The [closure record](miuicamera.md) supersedes all old continuation plans. Already announced camera changes belong to the release baseline, not the next delta.

## Final native and companion packaging

Preserve the system_ext camera OpenCL bridge: libcameraimpl depends on
libopencl-camera; libOpenCL_system is separate. Private libyuv/JPEG/C++ libraries
must retain their required symbols/versions and app-namespace visibility.
APK-local aliases resolve camera_algoup_jni.xiaomi, camera_mianode_jni.xiaomi and
camera_jpegutil_jni.xiaomi. The JPEG utility obsolete libhidltransport dependency
was removed; native initialization/SurfaceImage planes were verified September 22.
Do not restore a broad vendor-HIDL symlink workaround.

ExtraPhotoGlobal belongs in product with its product permission allowlist.
Its gson.jar shared-library declaration/copy belongs in system_ext; use
MAKE_COPY_RULE_ONLY rather than a Soong gson module. MiuiGallery is not a hard
prerequisite. Keep the APK's embedded native stack rather than old miatoll blobs.
Reference APK: Alioth Global V816.0.3.0.TKHMIXM, 227197486 bytes, SHA256
`614c7c27ddf5cf14b5c7ae61c799643e6639d82a344e46c83200266efa3c1451`.
Section extraction filters copied blobs but still regenerates full vendor modules;
ordering changes alone do not establish a library-layout regression.

## Final cache and device identity lessons

Recorded September 22 cache validation initialized eight IDs once rather than
104 repeated calls; subsequent tested switches did not reconstruct capabilities.
Keep the persistent cache lifecycle. Physical lens switches still close/open;
unsupported replace-session reuse must not be forced. Historical switch timings
are not a current benchmark.
Universal camera reads cached deviceCodename from
Download/XiaomiCamera/general_config.json before Build.DEVICE. Stale alioth_global
can select Common instead of Alioth. Use alioth/aliothin; Aliothin inherits Alioth
and does not need duplicate shared SAT overrides.


## CamX descriptor validation — October 24

A requested hardware audit reproduced a camera-provider crash from generic YUV
configuration on the private VTCam IDs 6/7. The missing input stream descriptor
reaches `Session::Initialize`; its partial-init destructor is also unsafe. Reject
that descriptor before `CHISession::Create` allocates an object. The Alioth extractor
and paired vendor HAL carry an exact-hash/idempotent guard; valid processing and
camera IDs are unchanged. Do not replace it with a late initializer return.

[Hardware evidence](../evidence/hardware-audit-20261024.md) records five positive
YUV/JPEG IDs, 1080p AVC output, MiuiCamera's vendor-session preview and repeated
malformed-request rejection without provider restart. The negative request remains
unsupported; do not advertise VTCam compatibility or new 4K/60fps acceptance.
The test was a temporary enforcing HAL replacement, then the installed blob was
restored. Public source heads belong to the repository ledger.


[Final commit recheck](../evidence/camera-review-20261024.md) repeats the approved
six-clip MiuiCamera matrix with the mapped guarded HAL identified by hash. All
frames decode on-device; main 4K60 remains about 60fps, ultrawide UI 60 remains
about 30fps, and switching ultrawide to 4K returns to 1×. Camera preferences and
the original installed HAL were restored. No further production patch was needed.
