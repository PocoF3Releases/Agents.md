# MiuiCamera — finalized

Camera is completed with accepted limits, not paused. No optimization experiment or test campaign is planned; only a new explicit request reopens it.

## Canonical delivery

Both `PocoF3Releases/device_xiaomi_camera:aosp-17` and GitLab `johnmart19/vendor_xiaomi_camera:aosp-17` are required. [The source map](../state/repositories.yaml) owns observed heads. Final implementation checkpoint: device `6c25fe9babca33dfc37813be7a92f5bbbe4d6319`; later device documentation head `1335f9ada0a7b9450f3f10658154300fc795c64c`; vendor `f13797ef3d93508756e06a4a185c9208dbc3ee88`.

Use the vendor prebuilt `proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk`, installed under `/system/priv-app/MiuiCamera/`. Accepted APK: **223517496 bytes**, SHA-256 `29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`. It is for ROM platform signing, not a newly signed ordinary user-install APK. MiuiCamera 5.x defines feature/ABI requirements; Alioth stock 4.x is a compatibility reference, not replacement delivery authority.

## Final behavior and boundaries

Logical VideoSAT is role 60 / Android camera 4. Do not invent role 62 or confuse vendor ArcSoft master ID 3 with Android physical camera ID 3. The 60fps patch preserves non-EIS session `0xf010` instead of overwriting it with `0x803c`. The ultrawide guard removes sub-1x choices in 4K and clamps stale toolbar selection before rebuilding controls; intermediate failure was `Illegal zoom ratio: 0.6, zoomRatios = [1.0, 2.0]`.

Main 4K30/60 and ultrawide 1080p were accepted. Ultrawide UI 1080p60 measured about 30fps; do not advertise true ultrawide 60fps. Unsupported 0.6x 4K selection is blocked and resolution changes safely restore 1x. The IMX355 pipeline failure showed DSX error 67108866 / MNDS DS16 errors; this is not proof every hypothetical software-upscale pipeline is impossible. [V-CAMERA](../state/validation.md#v-camera) owns the exact six-clip matrix, packaging checks and temporary-install limits.

## Retained implementation lessons

Current integration includes runtime/JNI/capability-cache and Xiaomi compatibility work. Preserve native library/partition ABI, permission/SELinux ownership, JPEG utility, ExtraPhoto and cache evidence. CameraX vendor-extension and unused MiSys integrations were removed; do not restore them because old notes mention them. Maintain the existing apktool patch flow in the device tree and ready-to-use APK in the vendor tree, rather than rebuilding from an old decompiled/Stage-1 rollback experiment.

Earlier HEIF notes report direct HeifWriter lifecycle/planar-input fixes and JPEG-versus-HEIF chroma comparisons; those are historical validation, not a fresh acceptance of every current camera mode. Old native audits, failed patches, exact binary identifiers and alternative designs remain intact in [camera history](../archive/2026-09-26/memory/miuicamera-history.md) and [dated camera evidence](../archive/2026-09-26/today/2026-09-23-camera-video-validation.md). Retrieve only the relevant section for a provenance question. The [closure record](../archive/2026-09-26/today/2026-09-24-camera-finalized.md) supersedes all old continuation plans. Already announced camera changes belong to the release baseline, not the next delta.
