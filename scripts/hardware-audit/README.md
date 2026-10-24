# Alioth hardware checks

Source-only development tools for an already built Android 17 / SDK 37 checkout.
Use `ANDROID_BUILD_TOP` to override `~/evo`. No Gradle, ROM rebuild or proprietary
binary is bundled. These tools do not establish that every hardware feature works.

```bash
python3 build_apk.py
python3 build_native.py
# Optional camera-only APK using the existing vendor auxiliary-camera allowlist:
python3 build_apk.py --aux
```

The normal package is `org.pocof3.hardwareaudit`. Grant only CAMERA and RECORD_AUDIO,
then launch `.MainActivity` while the screen is awake and the app is visible.
It keeps camera/microphone samples in memory and writes only measurements to its
private `files/result.txt`. Ordinary app execution is separate from any existing
root used to retrieve reports. No photographs, video clips or audio files are saved.
Audio playback is silence: advancing counters are not acoustic-quality proof.

The optional package is `org.lineageos.aperture.dev`; **install it only when that
package is absent**, never over an existing developer camera or user data. Its
normal positive matrix excludes private IDs 4/6/7. `--ez cameraOnly true` skips
non-camera tests; `--es cameraId N` explicitly selects one camera and overrides
that exclusion. IDs 6/7 can crash an unpatched stock provider: those are deliberate
negative tests, not ordinary positive capture tests. On the guarded blob, the
recorded generic request is still unsupported; success means a normal error with
the provider staying alive, not working VTCam capture. ID 4 requires vendor session
controls; its generic-session failure does not invalidate a tested MiuiCamera path.

`guard-regression` runs nine ARM64 cases against the actual extractor payload,
covering valid/empty/realtime inputs and missing arrays/descriptors. It performs
no camera operations. `storage-canary` exclusively creates its own fixed audit
file under `/data/local/tmp`, writes/fsyncs/reopens/verifies 8 MiB, then removes it.
It refuses an existing path and does not simulate power loss or benchmark storage.

Camera checks cover YUV timestamps/planes, in-memory JPEG decoding and main
1080p AVC output packet timestamps/keyframes. They do not certify optical quality,
all recording modes, HDR or 4K60. Display samples are Choreographer callback timing,
not a measurement of every displayed frame: a 60-Hz app can run on a 120-Hz panel.
PCM client formats do not prove the final DSP/codec format. Sensors receive an
initial finite sample; haptics check capabilities and request/cancel a short pulse.
Calls, Bluetooth/USB audio, NFC tags/payments, GNSS and tactile/acoustic quality
need their actual endpoints and remain outside this run.

Remove only the two diagnostic packages and audit-created files afterward. HAL
replacement is intentionally not automated here; temporary testing must restore
the original binary and normal boot. [Evidence](../../evidence/hardware-audit-20261024.md)
records source identity, rejected experiments, limits and restoration.


## Camera mode recheck without copying footage

`python3 build_clipcheck.py` builds a small `app_process` checker. Deploy the jar
under `/data/local/tmp/codex-camera-review-clipcheck.jar`; supply only the exact
`/sdcard/DCIM/Camera/VID_*.mp4` files created for an authorized test:

```bash
CLASSPATH=/data/local/tmp/codex-camera-review-clipcheck.jar app_process /system/bin org.pocof3.camerareview.ClipCheck /sdcard/DCIM/Camera/VID_TEST.mp4
```

The command runs **on the phone**. MediaExtractor checks sample timestamps and
sizes; MediaCodec decodes to buffers that are released immediately. Only dimensions,
rate, packet/frame counts and decoder identity are reported. No raw frames or
video packets are written or transferred. Require decoder EOS and an output frame
for every video sample. This does not inspect optical quality or decode audio.
Keep test clips on-device and delete only their exact MediaStore entries afterward;
never select existing personal videos implicitly. Restore camera settings from the
pre-test snapshot. [Mode recheck](../../evidence/camera-review-20261024.md).

The guard fixture also asserts unchanged valid-input x0 and balanced stack state,
including the valid non-realtime/zero-input case. Diagnostic outputs and recordings
are not source artifacts and must not be committed.
