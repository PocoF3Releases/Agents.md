# NXP NFC Teardown Regression and Fix (2026-09-22)

## Scope

Target: POCO F3 / `alioth`, Android 17 / Evolution X.

This record captures the NFC log spam discovered while validating the rebuilt MiuiCamera/ExtraPhoto integration.

## Runtime symptom

After boot, the NXP NFC HAL entered a high-frequency error loop:

```text
E NxpHal: NFC client received bad message
```

The captured boot log contained about 183,784 instances. The camera-specific log was also flooded by the same unrelated NFC error, making camera diagnosis difficult.

The loop began during NFC shutdown after otherwise normal NCI traffic and subscription/routing activity.

## Root cause

Upstream LineageOS NXP NFC commit:

```text
ad16c5c95a8613cc7ef8890c243068633e8d2f83
Fix Use-After-Free in NXP NFC HAL timer teardown
```

changed teardown to save the queue ID, clear the global `nClientId`, run timer cleanup, then later release the saved queue.

That protects delayed timer callbacks from dereferencing a freed message queue, but the SNxxx client thread still called:

```cpp
phDal4Nfc_msgrcv(p_nxpncihal_ctrl->gDrvCfg.nClientId, ...)
```

inside its loop.

Once the global ID became zero, receive returned `-1`, while the error branch simply logged and continued, creating an infinite fast loop.

## Implemented fix

Repository:

```text
PocoF3Releases/android_hardware_nxp_nfc
```

Active commit:

```text
8be75516d6d3cfff3a95ca2f249f0b36ceededb9
nfc: nxp: Keep client queue valid during teardown
```

Changed file:

```text
snxxx/halimpl/hal/phNxpNciHal.cc
```

The client thread now snapshots the queue ID before the receive loop and uses the stable local handle for `phDal4Nfc_msgrcv()`.

This keeps the security mitigation intact while allowing the client thread to consume its close-complete message and exit normally.

## Camera finding discovered in the same logs

The rebuilt camera integration proved that the new JPEG utility alias is now found:

```text
/system/priv-app/MiuiCamera/lib/arm64/libcamera_jpegutil_jni.xiaomi.so
```

but loading then failed on:

```text
library "libhidltransport.so" not found
needed by /system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

Although `libhidltransport` exists as vendor/build modules, a vendor copy is not automatically visible in MiuiCamera's system app linker namespace.

Device-camera fix:

```text
9a4cf71fbbbb69e31d20ad158c338bd600a9261c
camera: native: Drop obsolete HIDL transport dependency
```

Changed file:

```text
prebuilts/system/lib64/libcamera_jpegutil_jni.xiaomi.so
```

The obsolete `DT_NEEDED libhidltransport.so` entry was removed while retaining the modern HIDL base dependency.

## Current validation state

A rebuild containing both:

```text
8be75516d6d3cfff3a95ca2f249f0b36ceededb9
9a4cf71fbbbb69e31d20ad158c338bd600a9261c
```

completed on 2026-09-22.

The rebuilt image is being installed / prepared for fresh runtime log collection.

Runtime validation completed for the two immediate fixes:

- **NFC:** the tight `NFC client received bad message` loop is gone.
- **JPEG utility:** the JNI loads successfully without `libhidltransport.so`, initializes, returns image planes, and participates in successful JPEG reprocessing.

The remaining camera performance investigation moved to the independently verified CameraCapabilities cache bug. ExtraPhoto document/ID-card handoff still needs an explicit functional test.

Useful grep:

```bash
adb logcat -d | grep -Ei \
'NFC client received bad message|NxpHal|JpegUtil|jpegutil|libhidltransport|dlopen failed|UnsatisfiedLinkError'
```

## Next steps

1. Collect fresh boot and camera logs from the rebuilt image.
2. Confirm the NFC error loop is gone.
3. Confirm the JPEG utility JNI loads successfully.
4. Re-evaluate the already-verified MiuiCamera capability-cache bug with clean logs.
5. Patch the capability cache only after the new native/runtime state is confirmed.
