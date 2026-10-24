# Camera commit recheck — 24 October 2026

**source-checked · ARM64-tested · temporarily device-tested**.
The existing [device extractor](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/8c41b46ac69847a68cbb3717851f3546e8acca39)
and [vendor HAL](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/a9e382360adc8124f71f96590ff823b1fc688413)
need no further production change after this review. Their remote heads were
rechecked. The device commit changes only the extractor hook/helper; the vendor
commit changes only `camera.qcom.so`. The local recovery overlay was not published
or modified. No full ROM build or partition flash was performed.

## Source and ABI review

Extractor output exactly matches the vendor blob; a second application is
idempotent and corrupted/unknown input is rejected. The guard still resumes the
original prologue for valid data, uses caller-saved scratch registers and changes
no IDs, tuning, dependencies or relocations. Its descriptor checks cover only the
non-realtime layout consumed by the original initializer. Valid zero-input
pipelines are accepted. The strengthened native fixture executes nine cases of
the actual payload and asserts unchanged valid-input x0 and balanced stack state.
It passed on Alioth; tests remain workhub tools, outside ROM device/vendor sources.

The provider's **mapped backing file** was hashed through `/proc/PID/map_files`
on the phone before accepting camera results. It matched the exact published
patched SHA-256:
`2e116c44ed926e8a787615fa9cf3cf8ec53b396612d99ff3adf04c862be42497`.
Android remained SELinux enforcing. Existing root was used for diagnostics and the
temporary HAL replacement, not to bypass the production camera application's API.

## Approved mode matrix

MiuiCamera itself recorded six short test clips. Each selected mode/lens was
checked in the UI; camera preferences were backed up before changes. Output was
inspected **on the phone** using MediaExtractor and decoded to discarded buffers
with `OMX.qcom.video.decoder.avc`. No raw video/frame data was copied to the PC.

| Case | Output | Measured rate | Decoded frames |
| --- | --- | ---: | ---: |
| Main 4K30 | 3840×2160 | 30.03 fps | 180 |
| Main 4K60 | 3840×2160 | 60.04 fps | 270 |
| Ultrawide 1080p30 | 1920×1080 | 30.05 fps | 138 |
| Ultrawide UI 1080p60 | 1920×1080 | 30.05 fps | 135 |
| Ultrawide → 4K30 guard | 3840×2160 | 30.03 fps | 138 |
| Final main 4K60 | 3840×2160 | 60.04 fps | 278 |

All 1139 frames decoded through EOS, one output frame per video sample, with
strictly increasing timestamps. Main 4K30/60 and ultrawide 1080p retain the
[previous accepted behavior](../state/validation.md#v-camera). Ultrawide's 60fps UI
setting still produces about 30fps; this known limitation was not relabeled as
true 60fps. Selecting 4K from ultrawide restores 1× and hides 0.6×; the resulting
clip is valid 4K30. No new Java/native fatal, illegal-zoom, DSX/MNDS failure
signature was found in the captured test interval.

This does not expand acceptance to every camera mode, optical quality, HDR,
long-duration thermal behavior or private VTCam capture. The earlier
[hardware audit](hardware-audit-20261024.md) separately covers physical-camera
YUV/JPEG capture and malformed VTCam rejection. No speculative camera or shared
system-side change was made merely to produce another commit.

## Cleanup and reusable checks

Automatic approval review rejected copying raw recordings to the PC because they
could contain sensitive footage. The safe replacement was on-device metadata and
hardware decoding. Only numerical results and diagnostic text were retained.
[Source-only checker](../scripts/hardware-audit/README.md#camera-mode-recheck-without-copying-footage)
and stronger guard fixtures were built with the existing checkout's JDK/LLVM.

All six exact test MediaStore entries were deleted; pre-existing camera files were
preserved. Every backed-up camera preference file matched its original content
after restoration. The temporary HAL was detached and the provider restarted;
its mapped backing file again matched the original installed HAL hash
`21e4bb61dcd9bdef97d2d38fcfae1a59be15a6d951fc73b9fe785de86d027388`.
Eight cameras and SELinux enforcing were verified afterward. Only audit-created
helper files were removed. The installed build is unchanged; the published camera
fixes still require the normal production rebuild to be packaged.
