# MiuiCamera Repository, History, LFS, Signing and Packaging (2026-09-22)

## Public-tree design

The public build flow is:

```text
Git LFS source MiuiCamera.apk
        ↓
android_app_import
        ↓
Soong processing / JNI handling / alignment
        ↓
certificate: "platform"
        ↓
final ROM MiuiCamera.apk
```

Do not copy the already platform-signed APK from `out/` back into the vendor repository.

Each downstream ROM should sign the imported APK with its own platform certificate.

## GitHub device-tree cleanup

Two earlier runtime-layout commits were rewritten into one coherent final commit.

Current `PocoF3Releases/device_xiaomi_camera:aosp-17` checkpoints:

```text
423ae8e4a44f2bf2ef99807179c27f4624689c18
camera: extraphoto: Add stock Alioth companion app support

63594546455453b7749556f9ff1679be00eb981e
camera: native: Add MiuiCamera JPEG utility JNI

852e10c242a949bc2e03923fa0ec70e0c11417c5
camera: native: Restore stock camera runtime layout
```

The final change:

- restores stock `system_ext` placement for `libOpenCL_system`, `libcameraimpl`, and `libopencl-camera`;
- keeps the proven algoup/mianode aliases and later adds the runtime-proven JPEG utility JNI alias;
- removes stale `PACKAGE_USAGE_STATS` from the MiuiCamera privileged allowlist;
- removes unused OpenCL build-default/header experiments.

No `xiaomi_camera_opencl_defaults` remains in the active tree.

## GitLab vendor-tree cleanup

Generated vendor history was similarly consolidated.

Current relevant sequence:

```text
be17b6743bde5b3f230a66098841f7d4d9474b2e
MiuiCamera: Align native libraries to 16 KiB boundaries

b223378dde272a44c447e8314a6c15ebded7041e
MiuiCamera: Embed required native compatibility libraries

4a26262b081c4b45e16d7e66cbebd6cb3581ebfb
camera: native: Restore stock camera runtime layout
```

The APK integration commit changes only the APK LFS pointer. The runtime-layout commit changes the generated prebuilt locations/Soong metadata.

## Git LFS

Canonical path:

```text
proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk
```

Current source object:

```text
version https://git-lfs.github.com/spec/v1
oid sha256:bc6b8cfb1f179d742156e2f3b29133524db749166d2e0c9324438cf1ab733bd7
size 223417444
```

Downstream clone sanity checks:

```bash
git lfs install
git lfs pull
git lfs ls-files | grep MiuiCamera.apk
file proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk
```

The checked-out APK should be a ZIP/APK, not the small ASCII LFS pointer.

## 16 KiB alignment

Use the AOSP-built/new enough `zipalign`, because older Build Tools 34-era `/usr/bin/zipalign` supports `-p` but not `-P 16`.

Known-good command:

```bash
ZIPALIGN=out/host/linux-x86/bin/zipalign
"$ZIPALIGN" -f -P 16 -v 4 MiuiCamera.apk MiuiCamera.aligned.apk
"$ZIPALIGN" -c -P 16 -v 4 MiuiCamera.aligned.apk
```

Expected:

```text
Verification successful
```

## Final build signing

The final ROM APK verified with:

```text
Verified using v3 scheme (APK Signature Scheme v3): true
Number of signers: 1
```

MiuiCamera and SystemUI reported the same platform-certificate SHA-256 digest in the tested build, confirming correct platform signing.

v1/v2/v3.1/v4 or SourceStamp absence is not a blocker for this privileged system-image APK when v3 verification succeeds.

## Rebuild policy

The existing `out/` APK was already verified aligned and platform-signed before source pre-alignment was committed.

A rebuild is not required solely to repair that already-generated output.

A rebuild is useful only as reproducibility confirmation for the newest repository state or as part of the next full ROM build.

## Do not regress to abandoned architectures

Do not reintroduce:

- `MiuiCamera-compat.apk`;
- APK-generating genrules;
- donor native payload directories beside the APK;
- custom extraction callbacks that mutate the vendor output tree;
- extraction from `vendor/xiaomi/camera` into itself;
- broad app-private symlink farms.

The final approach is intentionally simpler: canonical APK + verified embedded compatibility libs + stock platform/vendor providers.


## ExtraPhoto generated-tree checkpoint

The stock Alioth ExtraPhoto companion was added with:

```text
c7c62f25992309ca3c4c4fdd46a782665496e7a2
camera: extraphoto: Import stock Alioth companion app
```

It adds:

```text
proprietary/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
proprietary/system_ext/framework/gson.jar
```

`gson.jar` is installed through a generated `PRODUCT_COPY_FILES` rule only. It must not be represented as a `dex_import` or listed in `PRODUCT_PACKAGES`.

The APK is Git-LFS tracked and matches the active stock dump:

```text
oid sha256:614c7c27ddf5cf14b5c7ae61c799643e6639d82a344e46c83200266efa3c1451
size 227197486
SHA-1 938f03ceb4641ed3a492b8fffe1e9358fdae73cb
stock build V816.0.3.0.TKHMIXM
```

### Generated-file diff rule

A section extraction:

```bash
./extract-files.py --section ExtraPhoto ~/miui/out
```

does not clean the whole vendor directory and only extracts matching blobs, but it still regenerates the complete generated makefiles.

Therefore `Android.bp` and `camera-vendor.mk` can reorder existing modules.

A superseded intermediate commit `723671f6` demonstrated this behavior: its apparent moves of:

```text
libOpenCL_system
libcameraimpl
libopencl-camera
```

were verified to be ordering-only; their complete module definitions are identical to parent `be17b674`.

Do not rewrite working OpenCL definitions merely to eliminate this generator diff noise.
