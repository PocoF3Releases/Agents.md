# Full configured techpack acceptance — October 26, 2026

## Source and boundaries

[Final source](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4662499db59d9c7b743021a2ce90e27e18531a72), branch `aosp-17`.
[21 feature-separated commits](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/compare/3700906827419979ef7d0812827443680972e29e...4662499db59d9c7b743021a2ce90e27e18531a72)
continue the [earlier repair series](kernel-techpack-errors-20261026.md).
They were pushed as a fast-forward; existing upstream/human history is retained.
Local style fixups were folded into their owning commits before publication.

No system-side source, configuration, thermal limit, panel timing or MIUI policy
was changed. Kernel-owned ARM64 checksum typing is the only touched path outside
techpack. No diagnostic suppressions, warning-policy changes, production test
files or Markdown files were added to the kernel repository. Private fixtures,
logs and images remain outside production Git.

## Coverage and builds

| Configured subtree | Fresh C compilation units | Final W=1/C=2 |
| --- | ---: | --- |
| audio | 142 | zero diagnostics |
| camera-xiaomi | 131 | zero diagnostics |
| display | 135 | zero diagnostics |
| video | 24 | zero diagnostics |
| data | 11 | zero diagnostics |
| stub | 1 | zero diagnostics |
| Total | 444 | zero diagnostics |

The initial fresh audio pass exposed two malformed narrative documentation
headers; they were repaired and rechecked. Final combined `techpack/` checks
cover all 444 selected units with zero warnings/errors. Normal strict kernel
Image builds successfully with zero emitted warnings/errors. Original fatal
warning settings remain enabled. Checkpatch reports zero errors, zero warnings
and 204 vendor-style CHECK notes; no waivers were used.

Image SHA-256: `1f8b550a780d88b655a03bc4e12985aa8e554bc64680b5e60ae34fb50bda0d1b`.

This covers the complete resolved Alioth techpack configuration, not every
possible Kconfig combination. Shared fixes were source-reviewed across camera,
camera-bengal, camera-xiaomi, camera-xiaomi-cas and camera-xiaomi-tablet; the four
unselected variants were not force-built or hardware-tested. The final unselected
K81 DSP source also compiles using the selected codec's exact compiler/include
context. No universal optional-codec or other-device certification is implied.

## Real defects repaired

- Camera: fuse mapping leaks; coherent-RAM firmware copy primitive; concurrent
  subscription handle allocation; unmatched IRQ unsubscribe dereference; invalid
  poll error masks and buffer ownership. Existing register values/modes remain.
- Audio: LSM allocation-failure and transcode lookup lock leaks; oversized
  host-voice queue-node reclamation; unmatched ultrasound cleanup unlocks;
  userspace buffers consumed directly by ultrasound/DSP/FIFO paths.
- Cirrus: user-controlled native/compat header sizes, unchecked allocations,
  transport packet-size bounds, ignored backend errors, truncated reply handling
  and callback/response-buffer lifetime. Valid smaller replies retain the existing
  zero-padding ABI. Calibration/routing controls are preserved.
- DSP formats: unaligned TFA partial-update bitmap stores, raw Cirrus endian
  contracts and packed-name bounds; voice/echo-reference sample widths now use
  16/24/32-bit conversion rather than ALSA format enum numbers.
- Display: installed fence descriptors were incorrectly treated as unused fd
  reservations on user-copy failure; register word bounds and MMIO dump access;
  29 failed PM acquisitions plus the PM-disabled completion guard/reference.
- Packet/video ownership: preserve flow-hash bytes and TCP/fragment byte order,
  make existing lock ownership explicit, keep private state local and declare
  exported/shared objects in their owner headers. No codec capability was removed.

The PM fixes use the [documented failed-get usage-count contract](https://docs.kernel.org/power/runtime_pm.html).
This 4.19 tree retains its existing APIs rather than importing an unsupported
resume-and-get helper or changing generic PM policy.

## Host verification

Private strict-warning ASan/UBSan fixtures passed actual changed code for:

- All five camera variants' process/IRQ event traces, invalid handles, NULL
  controllers and handle wraparound.
- 60,000 original/new IPv4/IPv6 flow-hash input tuples.
- 65,536 TFA partial-update masks and a two-block unaligned bitmap.
- 18,432 display copy-failure branches; 221 register length/offset pairs and
  131 dump lengths per IO implementation; explicit 32-bit reads and byte tails.
- PM vote/accounting success, failure, nested votes and exact unwind branches.
- LSM allocation failure, host-voice bounds, APR session/lock combinations,
  mapping retirement/late callbacks and stale other-client response ownership.
- Cirrus native/compat ioctl errors, bounded/truncated/short valid replies and
  concurrent request/callback lifetimes; ultrasound usercopy/allocation failures.

These fixtures mock kernel services; they do not prove real hardware fault
injection. LSM's unchanged legacy wire token cannot distinguish generations of
successive requests by the same client. A firmware token-echo extension was not
assumed. PM-enabled failed-resume propagation through void prepare/complete
callbacks remains unverified; the fixed disabled-PM guard is narrower.

## Phone acceptance and restoration

The exact final source Image was temporarily booted with `fastboot boot`;
SELinux stayed enforcing and mi_thermald remained active. Passed:

- 40 actual Cirrus malformed-ioctl rejection cases, 20 each in native64 and
  compat32. Invalid headers/pointers/lengths are rejected before DSP commands;
  these tests did not trigger calibration or send arbitrary DSP parameters.
- 19 PCM cases: MIC, CAMCORDER, VOICE_RECOGNITION, VOICE_COMMUNICATION at 16/48 kHz,
  repeated start/read/stop, plus three playback cycles. No microphone data saved.
- Six hardware codec cycles using generated 640x360 content: AVC/HEVC decode
  and AVC encode twice each, totaling 300 frames. Codec identities are Qualcomm.
- 816 app-domain GPU/native/window checks across 32/64-bit and 60/120 Hz.
- Rear, front and ultrawide JPEG capture, checked on-device by dimensions only.
  No image content exported; only the three test captures were deleted.

Fresh logs show no critical kernel warning splats, GPU/SMMU faults, RCU stalls,
CFI failures or kernel panic. Battery health, Wi-Fi connectivity and audio/thermal
processes were checked. This is bounded functional acceptance, not every camera
mode/resolution, physical audio-quality assessment, live-call certification,
performance guarantee or full-device VTS.

Original kernel restored; boot partition SHA-256 unchanged. Refresh preferences
restored, test app uninstalled and exact task staging removed. Raw serials,
network details, media paths and device logs remain private. No ROM/recovery
partition was flashed and no new ROM release is declared by this record.

## Published feature commits

- [arm64: csum: Preserve the checksum accumulator type](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b190c0a5c2259156a65c9581cfd602b39f74f309)
- [media: vidc: Correct private state and pointer contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7318f2ef850f06b7fd7cedba2f7ec066d7597839)
- [net: rmnet: Make packet byte order and lock ownership explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2693e03b6f453e583c202e8012b8995b50f40bc3)
- [media: camera: Release feature-fuse mappings after use](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/753713938a129c645b93408f313155d5f32edd92)
- [media: camera: Copy firmware into coherent RAM with memcpy](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/89d3a92648c9d4abaee75fda37b008b784a6e958)
- [media: camera: Serialize IRQ subscription handles and invalid-handle cleanup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1f7ba2d8c1d9b5a5951ada29d01ff7b63240f41c)
- [media: camera: Correct internal access and ownership contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b6d9df13cc3e54cb66520414d010a91390120796)
- [drm/msm: Close installed fence descriptors when user copies fail](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ed54af445feb7248de2c361dc61c13e9b7b926d0)
- [drm/msm: Bound register access and dump MMIO through accessors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/20d08e56c4d3d899a5d11c5acbc048b03b26339b)
- [drm/msm: Correct display access, encoding and ownership contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/afeea24c5dce5ab169b82de0b43ee964b3ccfb58)
- [drm/msm: Balance failed runtime power acquisitions](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/05fe85e0a6ff3dd7db00f3baed4c574a79fbee53)
- [ASoC: cs35l41: Preserve DSP wire types and bounded firmware names](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e44894aa848a660b73241e69ca21ff2353a7829b)
- [ASoC: tfa98xx: Pack partial-update masks without unaligned stores](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/297d2315f97cea86214f50299d9685e208606bee)
- [ASoC: lsm: Release event locks and stage sound-model user data safely](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c00d9d231610912506a52dbc629ffeba1b82a822)
- [ASoC: host-voice: Reclaim oversized playback nodes before returning](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3c15328c46ac75783fdbc29631d232d9706f9af1)
- [ASoC: transcode: Unlock failed runtime lookups](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/26a603a6c88698d5ddbc311df8b15eb162ebc3ac)
- [ASoC: cirrus: Bound control messages and protect DSP reply lifetime](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7db2acf33a34c266c4d87f3a1cb2cfe93303e06e)
- [ASoC: ultrasound: Stage userspace payloads before DSP and FIFO access](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ce5bc5f119051a889e013c4c1cd1142dde67ea04)
- [ASoC: qcom: Keep PCM formats distinct from sample widths](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8f4dcae25859f09c9d85d23a24764318e5ab6503)
- [ASoC: q6: Make APR session and mapping ownership explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5d11ad475d0cfae8380516112d1e17307aa9630a)
- [ASoC: Correct internal access and state ownership contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4662499db59d9c7b743021a2ce90e27e18531a72)
