# Alioth ExtraPhoto Integration (2026-09-22)

## Scope

Integrate the stock Alioth `ExtraPhotoGlobal` companion required by MiuiCamera 5.x document, ID-card and refocus editing flows without importing unrelated MIUI applications or the older miatoll external-library stack.

## Why it is needed

MiuiCamera 5.x explicitly launches Xiaomi ExtraPhoto actions including:

```text
com.miui.extraphoto.action.EDIT_DOCUMENT_PHOTO
com.miui.extraphoto.action.EDIT_IDCARD_PHOTO
```

Alioth stock provides the companion as:

```text
/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
```

Use the Alioth stock package instead of the older miatoll `MiuiExtraPhoto.apk`.

## MiuiGallery is not required

The Alioth ExtraPhoto package contains MiuiGallery integration hooks, but MiuiGallery is not a hard package dependency for the Camera -> ExtraPhoto workflow.

Do not add MiuiGallery solely for ExtraPhoto.

Gallery-specific cloud/editor integration may be unavailable without MiuiGallery, but the ExtraPhoto entry points used by MiuiCamera are provided by `com.miui.extraphoto` itself.

## Hard Java shared-library dependency

ExtraPhoto declares:

```text
gson.jar
```

Alioth stock supplies:

```text
/system_ext/framework/gson.jar
```

and declares it as:

```xml
<library name="gson.jar"
         file="/system_ext/framework/gson.jar" />
```

Verified Alioth stock identity:

```text
SHA-1 4e7699dde5290f45810a6aafb2e9ffd21db3be57
```

A dedicated AOSP declaration is used instead of importing the entire stock `platform-miui.xml`.

## Native-library strategy

`ExtraPhotoGlobal.apk` already embeds its large arm64 document/refocus native stack.

Do not externalize the old miatoll set such as:

```text
libdoc_photo*
libgallery_arcsoft_*
libgallery_mpbase
libmibokeh_gallery
librefocus*
```

and do not duplicate Alioth's existing `libSNPE.so`.

Several embedded files deliberately use alternate filenames while preserving the SONAME expected by their dependent libraries. Treat the APK as the canonical ExtraPhoto native payload unless runtime proves a missing external dependency.

## Device-tree implementation

Checkpoint:

```text
423ae8e4a44f2bf2ef99807179c27f4624689c18
camera: extraphoto: Add stock Alioth companion app support
```

Added extraction section:

```text
# ExtraPhoto
product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
system_ext/framework/gson.jar;MAKE_COPY_RULE_ONLY
```

Added device-owned declarations:

```text
configs/permissions/product/privapp-permissions-extraphoto.xml
configs/permissions/system_ext/gson.xml
```

The old `com.miui.extraphoto` privileged-permission block was removed from the system MiuiCamera allowlist and moved to the product partition, matching the app's stock placement.

Final intended layout:

```text
/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk
/product/etc/permissions/privapp-permissions-extraphoto.xml

/system_ext/framework/gson.jar
/system_ext/etc/permissions/gson.xml
```

## Section-only extraction

Known-good command:

```bash
cd ~/evo17/device/xiaomi/camera
./extract-files.py --section ExtraPhoto ~/miui/out
```

The section name is exactly:

```text
ExtraPhoto
```

This copies only the selected blobs and avoids normal full vendor cleanup.

## Generated vendor result

Current generated vendor checkpoint:

```text
c7c62f25992309ca3c4c4fdd46a782665496e7a2
camera: extraphoto: Import stock Alioth companion app
```

Parent:

```text
be17b6743bde5b3f230a66098841f7d4d9474b2e
```

Generated packaging is:

```text
android_app_import {
    name: "ExtraPhotoGlobal",
    ...
    certificate: "platform",
    privileged: true,
    product_specific: true,
}
```

Gson is **not** a Soong module. The generated vendor makefile copies the exact stock prebuilt directly:

```make
vendor/xiaomi/camera/proprietary/system_ext/framework/gson.jar:$(TARGET_COPY_OUT_SYSTEM_EXT)/framework/gson.jar
```

There must be no `dex_import gson` and no `PRODUCT_PACKAGES += gson`.

Current ExtraPhoto LFS object committed by that extraction:

```text
oid sha256:614c7c27ddf5cf14b5c7ae61c799643e6639d82a344e46c83200266efa3c1451
size 227197486
```

This is the exact ExtraPhoto object from the active Alioth Global Android 13 stock dump (`V816.0.3.0.TKHMIXM`). The matching stock SHA-1 is:

```text
938f03ceb4641ed3a492b8fffe1e9358fdae73cb
```

Do not replace it with the `eb8089...` object seen in another dump revision.

## Important extract-utils behavior

`--section ExtraPhoto` filters blob extraction, but generated package/module lists are not section-filtered.

The tool still regenerates the complete:

```text
vendor/xiaomi/camera/Android.bp
vendor/xiaomi/camera/camera-vendor.mk
```

As a result, the ExtraPhoto commit showed large apparent changes for:

```text
libOpenCL_system
libcameraimpl
libopencl-camera
```

Those were **generator ordering changes only**.

The module definitions were compared against parent `be17b674` and were byte-for-byte identical:

```text
libOpenCL_system  identical
libcameraimpl     identical
libopencl-camera identical
```

Their sources, shared dependencies, partition flags and multilib settings did not change.

Do not interpret this generated diff noise as an OpenCL/runtime-layout regression.

## Current camera checkpoints

GitHub device tree:

```text
423ae8e4a44f2bf2ef99807179c27f4624689c18
camera: extraphoto: Add stock Alioth companion app support

63594546455453b7749556f9ff1679be00eb981e
camera: native: Add MiuiCamera JPEG utility JNI

852e10c242a949bc2e03923fa0ec70e0c11417c5
camera: native: Restore stock camera runtime layout
```

GitLab generated camera vendor:

```text
c7c62f25992309ca3c4c4fdd46a782665496e7a2
camera: extraphoto: Import stock Alioth companion app
```

## Remaining validation

After the next build/flash:

1. verify `ExtraPhotoGlobal` package installation;
2. verify `gson.jar` appears in the shared-library list;
3. capture a document and launch the document editor;
4. test ID-card handoff;
5. test refocus paths as available;
6. check logcat for missing Java shared-library or native-loader errors.

No MiuiGallery installation is required as a prerequisite for this test.
