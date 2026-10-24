# Alioth hardware audit — 24 October 2026

**source-checked · host/ARM64-tested · temporarily device-tested**. This is a bounded
hardware/API check of the installed Android 17 / SDK 37 user build, not certification
that every mode, accessory or service works. GPU findings remain in the separate
[Adreno record](adreno-audit-20261024.md). No full ROM rebuild or partition flash
was performed. Raw dumps, crash records and executable/proprietary artifacts remain
private. [Source-only tools](../scripts/hardware-audit/README.md) reproduce the
bounded checks with existing checkout tools.

## Useful production correction

- [Device extractor](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/8c41b46ac69847a68cbb3717851f3546e8acca39).
- [Matching vendor HAL](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/a9e382360adc8124f71f96590ff823b1fc688413).

The local device tree includes its existing recovery overlay; the published ROM
commit excludes that unrelated patch. No shared system-side source, camera ID,
tuning, user setting or advertised camera capability was changed.

**Seen:** generic 1280×720 YUV configuration on private VTCam ID 6 independently
crashes the provider with a null read at offset `0x20`. The original
`camera.qcom.so` has build ID `634f550df725646612f373893718f14e`, SHA-256
`21e4bb61dcd9bdef97d2d38fcfae1a59be15a6d951fc73b9fe785de86d027388`.
Its compressed ELF debug symbols identify `CamX::Session::Initialize`; at ELF
virtual address `0x85aef8`, `ldr w17,[x22,#0x20]` executes with x22 null.

A diagnostic late guard reached another null access in `Session::Destroy` /
`Mutex::Lock`, because initialization had not created its mutex. That candidate
was removed and **is not published**. The final guard validates relevant input
stream arrays/descriptors at `CHISession::Create` entry (`0x79d3b8`), before
allocation. Missing input returns NULL through the caller's existing failure path.
Non-realtime pipeline layout and branch destinations were checked against the
actual function disassembly; valid input resumes the displaced original prologue.
Only caller-saved scratch registers/flags are used.

The 92-byte payload occupies verified zero RX padding at `0x8c0640`; the RX segment
is extended within its existing page, before the next segment at `0x8c1000`.
File size, dynamic dependencies and relocations are unchanged. Extraction accepts
only exact original/patched hashes, is idempotent and rejects unfamiliar input.
Patched SHA-256:
`2e116c44ed926e8a787615fa9cf3cf8ec53b396612d99ff3adf04c862be42497`.

Eight **actual ARM64** fixture cases execute the same guard payload: valid empty,
realtime and two-stream data; missing create data, pipeline array, stream array,
second stream and second-pipeline stream. The fixture makes no camera calls.
This is not an exhaustive memory-safety or proprietary-HAL audit.

## Phone results

Tests used normal app permissions and an existing camera-allowlisted developer
package that was verified absent before installation. Existing root was used only
for diagnostics and the temporary HAL mount; Android remained SELinux enforcing.

| Area | Observed result | Limits |
| --- | --- | --- |
| Camera | IDs 0/1/2/3/5 each deliver 20 valid timestamp-monotonic YUV frames and an in-memory decoded JPEG; main AVC 1080p30 delivers 67–68 output packets and three keyframes in the short run | No saved images/clips; not optical quality or all camera modes |
| VTCam rejection | Generic requests on IDs 6/7 return unsupported errors instead of provider death; three repetitions each keep the provider alive; main YUV/JPEG still pass afterward | Rejection is a negative-test success, not functional VTCam capture |
| MiuiCamera | Active vendor-session preview on logical ID 4 observed with the guard loaded | Generic ID-4 session needs private controls; no new 4K60/ultrawide acceptance |
| Display | 121 Choreographer callbacks per requested rate; median about 16.51 ms at 60 and 8.26 ms at 120 | Panel remains at 120 during the 60-Hz app case; an app-rate override is not a panel-mode failure or proof of every presented frame |
| Audio | PCM 16-bit, packed 24-bit, 32-bit and float clients write 4,800 stereo frames at 48 kHz and playback positions advance on the speaker route | Silent samples test the API/route; no acoustic-quality or final DSP-format claim |
| Microphone | 24,000 mono PCM16 samples at 48 kHz; nonzero finite aggregate levels | Samples discarded; not acoustic calibration, calls or every microphone |
| Sensors | Accelerometer, gyro, magnetometer, light and proximity register and return finite initial samples | No pressure sensor; near/far transitions and calibration not exercised |
| Haptics | Present/amplitude capability and click/tick/heavy-click support; short request/cancel accepted | No human tactile confirmation or new PWLE claim |
| Storage | Exclusive 8-MiB canary write, fsync, close, reopen and complete readback pass; own file removed | Not power-loss testing, endurance or a throughput benchmark |
| Connectivity/power | Wi-Fi validated state, Bluetooth on/disconnected, NFC off; normal reboot retains battery-present state | No paired Bluetooth/USB audio, NFC tag/payment, GNSS or call test |

The first float-PCM attempt incorrectly used AudioTrack's byte-array API, which
this checkout explicitly rejects for float PCM. The corrected float-array call
passes; no framework patch was justified. One camera run was invalid after the
phone entered Dozing and camera access was disabled by policy. The positive rerun
required an awake/visible activity and passed. One provider-restart attempt queried
too early; tests awaited all eight cameras before accepting results.

The unsigned source APK and installed MiuiCamera APK have different whole-file
hashes; the primary DEX matches the source. Platform signing can change the APK
hash, so this comparison was not treated as proof of an app-code regression or of
full ZIP-entry identity.

## Cleanup and release boundary

Both diagnostic packages and only the audit's own device files were removed.
The temporary HAL overlay was detached and normal Android rebooted; the original
HAL hash and eight-camera enumeration were checked again under SELinux enforcing.
No camera mode or global audio/display preference was changed. The existing
USB-install scan-prompt setting remains as requested.

Windows retained an ADB USB interface but its ADB server temporarily listed no
device after reboot. Restarting that Windows server restored the connection;
Android boot was then confirmed. This is transport recovery, not a proven kernel
USB fix. No extra ten-reboot campaign was repeated.

The installed build retains its original HAL/kernel. The published source changes
need the normal production rebuild to be packaged. Private SAT/VTCam feature modes,
4K60, HDR, protected media, calls, Bluetooth/USB endpoints, GNSS, NFC payments and
human acoustic/visual/tactile quality remain outside this scoped acceptance.
