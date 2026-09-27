# MiuiCamera 5.x Native-Library Audit (2026-09-22)

## Audit baseline

Latest final MiuiCamera base APK:

- 42 arm64-v8a shared libraries.
- Four compatibility libraries added directly into the APK.
- Static ELF graph, dynamic-load strings, DEX references, Qigsaw split metadata, and Alioth provider availability were reviewed.

## Closed dependency chains

### Slow motion

```text
libcamera_video_mein_algo_jni.so
 ├─ libxmi_slow_motion_mein.so   [APK]
 └─ libmialgo_utils.so           [APK]
```

`libxmi_slow_motion_mein.so` additionally uses Qualcomm/Xiaomi runtime providers such as `libOpenCL.so`, `libcdsprpc.so`, and `libSNPE.so`.

### MiAlgo saliency

```text
libmialgo_saliency_jni.so
 └─ libmialgo_saliency.so
      ├─ libmialgo_ai_vision.so  [APK]
      ├─ libOpenCL.so            [vendor/public]
      └─ libcdsprpc.so           [vendor/public]
```

### Hand gesture

```text
libcamera_arcsoft_handgesture.so
 ├─ libhandengine.arcsoft.so     [APK]
 └─ libmpbase.so                 [APK]

libhandengine.arcsoft.so
 └─ libmpbase.so                 [APK]
```

## External DT_NEEDED set

After resolving APK-local libraries, remaining external dependencies are ordinary Android/platform/vendor libraries:

```text
libEGL.so
libGLESv2.so
libGLESv3.so
libOpenCL.so
libOpenSLES.so
libSNPE.so
libandroid.so
libc.so
libcdsprpc.so
libdl.so
libjnigraphics.so
liblog.so
libm.so
libmediandk.so
libstdc++.so
libz.so
```

Key proprietary providers are present and publicly exposed in the current device trees:

- `libOpenCL.so`
- `libcdsprpc.so`
- `libSNPE.so`

Do not embed these into the APK.

## Duplicate SONAME finding

Only one duplicate SONAME exists among the 42 libraries:

```text
libcamera_handgesture_mpbase.so  -> SONAME libmpbase.so
libmpbase.so                     -> SONAME libmpbase.so
```

The two binaries have matching runtime code/data and export API, but use different filenames.

Keep both for now:

- consumers use `DT_NEEDED: libmpbase.so`, so the correctly named `libmpbase.so` is the reliable loader target;
- the renamed `libcamera_handgesture_mpbase.so` may still be referenced by a Xiaomi feature loader.

The space cost is negligible compared with the regression risk.

## Dynamic dependencies not visible in DT_NEEDED

### `libion.so` and `libdmabufheap.so`

These are not dead weight. The slow-motion runtime dynamically loads allocation backends and resolves APIs such as:

```text
CreateDmabufHeapBufferAllocator
DmabufHeapAlloc
MapDmabufHeapNameToIonHeap
ion_open
ion_alloc_fd
ion_close
```

Keep both bundled compatibility libraries.

### `libOpenCL-pixel.so`

This is a candidate in a broader OpenCL loader list, not a hard requirement. Alioth already supplies the standard vendor `libOpenCL.so` implementation.

Do not add `libOpenCL-pixel.so`.

### `libtbbmalloc.so`

Used as an optional TBB scalable allocator backend. The document-processing runtime has fallback behavior.

Do not add it unless runtime proves a hard failure.

### `libneuralnetworks.so`

Barhopper probes NNAPI. Alioth/Android exposes `libneuralnetworks.so` publicly.

No APK import needed.

### `libunwind.so`

xCrash dynamically probes it for enhanced unwinding. It is not a hard base dependency.

Do not import it solely because the name appears in native strings.

## DEX-only native names

DEX contains references to:

```text
libcamera_ispinterface_jni.xiaomi.so
libcamera_jpegutil_jni.xiaomi.so
```

These are known Xiaomi camera libraries from other device/platform families. They are not present in Alioth stock and are not declared as base native requirements in this APK.

Treat them as universal-camera cross-device branches unless runtime on Alioth proves otherwise.

## Qigsaw / dynamic feature modules

The APK advertises on-demand Qigsaw modules including:

```text
mimojifu
mimojifu2
milive
panorama
ambilight
mimojias
vlog2
clone
videosky
movielens
```

These are marked `builtIn: false` and `onDemand: true`.

Libraries referenced by those feature catalogs must not be bulk-imported into the base APK merely because they are absent from the base archive.

## Compatibility libraries that must remain bundled

### C++ runtimes

Both `libc++.so` and `libc++_shared.so` are used by different dependency groups. They are not interchangeable cleanup targets.

### JPEG runtimes

Both `libjpeg.so` and `libturbojpeg.so` are actively referenced with different APIs/versioned symbols. Do not replace them with arbitrary system copies.

### `libyuv.so`

The MiuiCamera 5.x binary requires APIs including `ABGRToNV21`. Alioth's available older/system copy must not be substituted without a complete symbol compatibility check.

## Static-audit conclusion

No additional base-library import is justified at this point.

Future additions require one of:

1. `dlopen failed` / `library not found`;
2. unresolved symbol failure;
3. proven ABI mismatch;
4. a reproducible feature failure traced to a missing native provider.

Recommended runtime log filter:

```bash
adb logcat -d | grep -Ei 'dlopen|linker|nativeloader|UnsatisfiedLinkError|cannot locate|library.*not found|mialgo|mein|SNPE|OpenCL|cdsprpc|dmabuf|libion|mpbase|handgesture|miocr'
```
