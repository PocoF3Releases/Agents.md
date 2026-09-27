# MiuiCamera 5.x on Alioth — Final Integration State (2026-09-22)

## Scope

Target: POCO F3 / `alioth`, Android 17 / AOSP-17, Evolution X.

The shipped MiuiCamera 5.x mod is the feature and ABI source of truth. Alioth stock MiuiCamera 4.x and the stock HyperOS dump are compatibility/provider references only.

## Final architecture

- Canonical MiuiCamera APK lives in the generated vendor tree and is tracked with Git LFS.
- No build-time APK reconstruction.
- No `MiuiCamera-compat.apk`.
- No APK patching genrule for the final library integration.
- No native-payload externalization.
- Soong directly imports the canonical APK with `android_app_import`.
- Final ROM output is re-signed with the target ROM platform certificate.

Expected Soong shape:

```bp
android_app_import {
    name: "MiuiCamera",
    apk: "proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk",
    certificate: "platform",
    privileged: true,
    dex_preopt: {
        enabled: false,
    },
}
```

## Embedded compatibility libraries

Four verified libraries are physically embedded in `lib/arm64-v8a/`:

| Library | Size | SHA-256 | Purpose |
|---|---:|---|---|
| `libmialgo_ai_vision.so` | 239328 | `212d7402541b556a83109347b92a62ab1e8840d1ec3a2e38f06fc42b4d15a999` | MiAlgo saliency / AI vision dependency |
| `libxmi_slow_motion_mein.so` | 29548840 | `51c7d73938188405557f1f1277bf191cf2478af362cc2d3a9f9678b0096fe6fa` | Slow-motion MEIN runtime |
| `libmialgo_utils.so` | 132872 | `fa6203f8cbc8da471a9dac3d36899e82353b4794ecee2d16b6e96c0a82d09785` | Slow-motion utility dependency; Alioth stock-compatible copy |
| `libmpbase.so` | 5296 | `a1391e697699e2a87d9d46dc91589fe64521d08b4079f6643d6ed71ba5e01144` | Hand-gesture dependency; Alioth stock-compatible copy |

The final APK contains 42 arm64 shared libraries.

## Source APK alignment

The canonical LFS source APK was explicitly 16 KiB aligned with the AOSP-built `zipalign`:

```bash
zipalign -f -P 16 -v 4 MiuiCamera.apk MiuiCamera.aligned.apk
zipalign -c -P 16 -v 4 MiuiCamera.aligned.apk
```

Verification result:

```text
Verification successful
```

Current aligned Git LFS object:

```text
oid sha256:bc6b8cfb1f179d742156e2f3b29133524db749166d2e0c9324438cf1ab733bd7
size 223417444
```

Alignment adds padding compared with the unaligned archive; that size increase is expected.

## Final ROM APK verification

The built APK under `out/target/product/alioth/system/priv-app/MiuiCamera/MiuiCamera.apk` was verified to:

- pass `zipalign -c -P 16 4`;
- contain all 42 arm64 libraries;
- contain all four added compatibility libraries;
- verify with APK Signature Scheme v3;
- use the same platform certificate as SystemUI.

The source APK must not be replaced with the already platform-signed `out/` APK. The public vendor prebuilt stays the canonical build input; Soong signs each ROM build with that ROM's own platform key.

## OpenCL / camera runtime layout

Keep the stock Alioth partitioning:

```text
/system_ext/lib/libOpenCL_system.so
/system_ext/lib64/libOpenCL_system.so
/system_ext/lib64/libcameraimpl.so
/system_ext/lib64/libopencl-camera.so
/vendor/lib64/libOpenCL.so
```

Important dependency:

```text
libcameraimpl.so -> DT_NEEDED libopencl-camera.so
```

Do not relocate `libcameraimpl.so` or `libopencl-camera.so` into `/system/lib64`.

## APK-local JNI aliases

The original static audit identified two required app-local JNI aliases:

```text
/system/priv-app/MiuiCamera/lib/arm64/libcamera_algoup_jni.xiaomi.so
    -> /system/lib64/libcamera_algoup_jni.xiaomi.so

/system/priv-app/MiuiCamera/lib/arm64/libcamera_mianode_jni.xiaomi.so
    -> /system/lib64/libcamera_mianode_jni.xiaomi.so
```

**Runtime update:** later device testing proved that `libcamera_jpegutil_jni.xiaomi.so` is also directly loaded during a real mode switch and is currently missing. The earlier "only two" conclusion is superseded. See [mode-switch regression](2026-09-22-miui-camera-mode-switch-regression.md).

Removed app-private aliases should remain removed unless runtime evidence proves a namespace problem:

- `libmicampostproc_client.so`
- `maintainer@example.com`
- `libOpenCL_system.so`
- `libmqsas.so`
- `libcameraimpl.so`
- `libopencl-camera.so`

## Current repository checkpoints

GitHub device tree `PocoF3Releases/device_xiaomi_camera`, branch `aosp-17`:

```text
852e10c242a949bc2e03923fa0ec70e0c11417c5
camera: native: Restore stock camera runtime layout
```

GitLab generated vendor tree `vendor_xiaomi_camera`, branch `aosp-17`:

```text
be17b6743bde5b3f230a66098841f7d4d9474b2e
MiuiCamera: Align native libraries to 16 KiB boundaries

b223378dde272a44c447e8314a6c15ebded7041e
MiuiCamera: Embed required native compatibility libraries

4a26262b081c4b45e16d7e66cbebd6cb3581ebfb
camera: native: Restore stock camera runtime layout
```

## Remaining validation

Static APK packaging/signing/alignment is complete, but runtime testing has now exposed additional camera integration problems. See [mode-switch regression](2026-09-22-miui-camera-mode-switch-regression.md).

Remaining device validation includes:

- normal photo;
- video;
- front video;
- 48 MP QCFA;
- macro;
- slow motion;
- hand gesture;
- document/OCR;
- night/portrait;
- native-loader/linker/OpenCL/SNPE logs.

Do not add more native libraries based only on static name references. Require a real loader/symbol failure or a proven ABI dependency.
