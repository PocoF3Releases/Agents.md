# Techpack repair acceptance — October 26, 2026

## Source and scope

23 feature-separated kernel commits; no system-side edits, configuration changes,
thermal-limit changes or MIUI policy imports. Human upstream history/authorship
is unchanged. Private harnesses and logs remain outside production kernel Git.
No warning suppressions or relaxed fatal-warning flags were added.

[Complete source comparison](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/compare/a7a655ccadb22fe516b7f0c84063b8f93a29ee95...3700906827419979ef7d0812827443680972e29e).

## Implementations

- [ASoC: Resolve in-tree audio headers from the kernel source root](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cd69e6f09675dc7ce7c6b9bf2332c470935f52ac)
- [media: camera: Correct stale internal include directories](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/eb53255d2697dfa7a9e158c60d19c64e6b6200a4)
- [drm: sde: Balance failed secure MISR transitions](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/eed57ac2f91ce9a1fdfde56ebddf1ff30d8dc146)
- [drm: sde: Bound VBIF memory-type table population](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f4feb16baf5c142225ee6a845d994189d39a51d3)
- [drm: msm: Retry teardown lock deadlocks correctly](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/dd301090c5dfb4806f2d7acafcf2e3a6acd4a6ec)
- [media: camera: Preserve initialization and stop failures](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/717bb1a55c27cac182a581f03c087b275655f95c)
- [media: camera: Preserve the VFE170 CAMIF register map](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/fc6ff3b8187093d4b10fb2f2f5eb485594588247)
- [ASoC: cs35l41: Preserve profile state when fast switching fails](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7ea84348e2dd536fa36ce7d65785951a108db08d)
- [ASoC: tfa98xx: Bound userspace profile name copies](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2bc5a7c56f3b2c48d1f4dd5b2f0dcced661bebb0)
- [ASoC: wcd: Return component and ADC configuration errors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/703fd60ca3d0796332373fcabba1658be1c32bdb)
- [ASoC: q6adm: Preserve calibration and parameter diagnostics](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c2af7729824af478c511f5b4a62a491230cfd0de)
- [ASoC: ultrasound: Bound operation-mode sysfs output](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/80227259a4014124db9f89d3b2bfaecf92c8c8b7)
- [net: rmnet: Balance RCU on missing endpoint cleanup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ea7156f7fb36fdb9b17b4c9559a51763aa49906f)
- [media: vidc: Preserve callback and MMIO types in HFI](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/06e38c66b171e6db9712107e0e433ab430c59762)
- [drm: rotator: Initialize format packing once](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3267f0a43610cb53a88f2ff18d4f79b13fd6dab1)
- [net: rmnet: Annotate shared SHS hooks for RCU](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a33a14ae95c944559601108f11e4a8dd7097f1ad)
- [media: vidc: Preserve userspace pointer types in private ioctls](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0031c8c98aa384847ff3a6d21b00f0b78dcbb6cd)
- [ASoC: Share backend interfaces and scope private helpers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bbb5c93bfcf9824a0402a0ac69b1b80f741f2058)
- [media: camera: Scope internal callbacks and correct diagnostics](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/580ed27accd6065aba95fffa6eef568ddfd7b553)
- [net: rmnet: Scope internal helpers and remove unused bookkeeping](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8165af1ccbd989e80190544fbfe3d4ef031882c1)
- [drm: msm: Scope callbacks and remove inert display work](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/86b130b86e8ca86f5274f11c6677e3ff1ccee805)
- [media: vidc: Scope private callbacks and discard unread aliases](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1d17cbdde4d7da2576ef72c4d31d506a38d0a6e3)
- [net: rmnet: Publish initialized SHS state with release ordering](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3700906827419979ef7d0812827443680972e29e)

## Build and host verification

The configured Alioth techpack target passes W=1 C=2, including a serial diagnostic
pass. Normal kernel Image also builds successfully with the existing strict
warning policy and no emitted compiler warnings/errors. This does not mean sparse
is warning-free: nonfatal NULL, endian, user-pointer and lock-context diagnostics
remain. The wider kernel audit is still open.

Final Image SHA-256:
`e0f0d94b77edaa076821eadc53ba3e6f37738aa07915ef91bbd145a3992960b1`.

ASan/UBSan host fixtures exercise actual changed functions/macros: six DRM
teardown outcomes; HFI void/integer callback fallbacks and absent-call argument
handling; 648 VBIF count/index combinations plus injected helper failures;
MISR PM/XIN acquisition failure and successful cleanup; CAMIF v2/v3 IRQ-failure
cleanup across DSP/diagnostic combinations. These bounded fixtures are not a
replacement for hardware error injection. Checkpatch reports zero errors;
existing vendor style checks and one diagnostic-string warning remain.

## Phone acceptance

The [first 22 commits](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1d17cbdde4d7da2576ef72c4d31d506a38d0a6e3)
were temporarily booted with SELinux enforcing. Tests passed:

- 816 app-domain GPU/native/window checks across 32/64-bit and 60/120 Hz.
- 16 PCM capture start/read/stop cases across MIC, CAMCORDER,
  VOICE_RECOGNITION and VOICE_COMMUNICATION at 16/48 kHz; three playback cycles.
- Rear, front and ultrawide JPEG capture, checked through on-device dimensions
  only. No camera image content was exported. This does not certify every mode.
- Fresh kernel logs contained no new warning splats, GPU/SMMU faults or RCU stalls.

The final SHS release-publication patch was separately temporarily booted with
SELinux enforcing: Android completed boot, audio server ran, Wi-Fi reached
COMPLETED and SHS parameters were present. No kernel warning splats, GPU/SMMU
faults or RCU stalls appeared. The full 816-case suite was not repeated for this
single publication-ordering change. This is not an isolated cellular SHS stress
or race-reproduction test.

Both temporary boots used fastboot boot, without flashing a partition. The
original installed kernel was restored and its boot partition hash matched the
pre-test hash. Task probes/captures were removed and changed refresh settings
restored. Raw device identifiers, network details and logs stay private.

Playback fixture corrections (stream priming and standalone VM exit) were harness
issues, not claimed as kernel fixes. Other suppliers, unselected configurations,
all camera modes and the intermittent shutdown failure remain outside acceptance.
