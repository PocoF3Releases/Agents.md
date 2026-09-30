# Alioth AW8697 haptics

**Final stock-backed production design.** The maintainer chose this over generated
primitives. The corrected HAL passed device checks and received subjective
acceptance on 2026-09-30. [V-HAPTICS](../state/validation.md#v-haptics) distinguishes
the installed baseline from the temporary accepted correction.

## Ownership and interfaces

Current heads: [source map](../state/repositories.yaml). Code:
`hardware/xiaomi:cnb/vibrator/aw8697/`, Alioth's stock driver under
`kernel/xiaomi/sm8250:aosp-17/drivers/input/misc/aw8697_haptic/`, and device/common
packaging, DAC and SELinux. Hardware stays standalone; final playback needs no root.

Module `android.hardware.vibrator-service.xiaomi_aw8697`; init
`vendor.aw8697.vibrator`; Binder `android.hardware.vibrator.IVibrator/default`.
Find input by `EVIOCGNAME=aw8697_haptic`, never a fixed event number. Observed
sysfs base: `/sys/devices/platform/soc/a8c000.i2c/i2c-2/2-005a/`.

- Linux FF uploads/erases effects with `EVIOCSFF`/`EVIOCRMFF`; `EV_FF` starts/stops.
- Read-only `custom_wave` checks RAM readiness and optional `ram_gain_abi=1`.
  Service waits for firmware before registration because Android caches capabilities.
- Tagged RAM gain: fourth short `0x4700 | gain` (0..128), eight-byte custom payload;
  legacy ABI is six bytes. Negotiate support; do not send tagged gain to arbitrary RTP IDs.
- `gain` updates timed `on()` amplitude. Predefined effects own their gain separately.
- Read `f0_value` (tenths of Hz) for cached resonance. **Reading `f0` triggers calibration.**

## Effects and stock strength

| Android effect | Zero-based RAM ID | Scheduled duration |
| --- | ---: | --- |
| CLICK | 0 | 20 ms |
| DOUBLE_CLICK | 0 twice | 20 + 80 gap + 20 = 120 ms |
| TICK | 2 | 20 ms |
| THUD | 3 | 20 ms |
| POP | 4 | 28 ms |
| HEAVY_CLICK | 8 | 20 ms; MIUI mesh-heavy |
| TEXTURE_TICK | 5 | 20 ms; MIUI mesh-light |

Hardware RAM slots are one based. Filename numbers are not Android enum IDs.
In particular, stock mesh-heavy uses 8; the light mesh waveform uses 5.

Stock `sys.haptic.infinitelevel=true` activates `VibrateUtils` →
`VibratorExt::configStrengthForEffect` → `InputFFDevice::playEffect`.
Light/medium/strong factors **0.375 / 0.625 / 1.0** yield gains **48 / 80 / 128**.
The old native fallback 30/64/128 was not the active stock UI path. The final
HAL uses the active values; `TEXTURE_TICK` has no extra half-gain multiplier.
At medium it matches `sys.haptic.mesh.light=5,1`.

Android gesture-threshold-deactivate and toggle-off fall back to TEXTURE_TICK
when primitives are absent. The earlier RAM-2 half-gain choice compounded weak
feedback. Long press uses HEAVY_CLICK; gesture activate/toggle-on use TICK.
Trace the actual `HapticFeedbackVibrationProvider` for future Android versions.

Timed amplitude, long-request splitting, cancellation and exactly-once terminal
callbacks are supported; callbacks occur outside the worker lock. Completion
alone does not measure physical strength. Capabilities are `0x87`: on/perform
callbacks, amplitude control and cached resonant frequency. **No composition
primitives, PWLE, frequency control, FOAM, external control or vendor effects.**

## Kernel and firmware

Alioth's [stock driver](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/tree/alioth-r-oss/drivers/input/misc/aw8697_haptic)
and [stock DTS](https://github.com/MiCode/kernel_devicetree/tree/alioth-r-oss)
replace the former dagu/psyche mixture. Live drive/overdrive 73/73 and boost
`0x11` match stock; compensation arithmetic and legacy gain floor are unchanged.
The tagged gain path preserves low timed amplitudes and fades. Do not raise a
global minimum to compensate for a wrong effect mapping or Android intensity setting.

| Shipped `/vendor/firmware/` file | Size | Actual consumer |
| --- | ---: | --- |
| `aw8697_haptic.bin` | 3622 bytes | `aw8697_ram_update`: ten effect slots plus slot 11 constant loop |
| `aw8697_rtp_1.bin` | 120000 bytes | Boot `aw8697_rtp_update` preload and explicit oscillator-calibration sample |

Both match stock; hashes and device evidence are in the
[portable verification record](../evidence/haptics/2026-09-30.md). RTP preload
is not proof oscillator calibration ran. Ordinary Android effects use RAM.
Numbered MIUI/game/ringtone banks and `vibrator_firmware_aidl` duplicates are
not shipped; extended MIUI IDs and RichTap streaming have no production caller.
The large firmware-catalog commit was removed; source README documents actual dependencies.

RAM bank: checksum `0xe010` equals sum(bytes[2:]) modulo 65536; base `0x0800`;
four-byte inclusive descriptors start at offset 5, data at 49. Eleven sample
lengths: 381,443,304,252,681,243,437,169,217,304,142; waves 2 and 9 match.
These digital samples do not provide measured actuator acceleration.

## Retired approaches and limits

Generated RichTap-like primitives, synthetic RTP envelopes, arbitrary strength
multipliers and their tracked test helpers were removed from production.
Stock `libaachaptics.so` identifies AAC 1.0.7_20210722 / 24 kHz processing, but
its filters/tuning do not supply an Android primitive or FOAM calibration map.
RAM uses F0 trim while RTP uses oscillator trim; replaying RAM bytes as RTP is
not equivalent. Xaga/Myron data is comparative evidence, not Alioth calibration.
Do not restore these retired features to satisfy a capability checkbox.

For an explicitly requested regression check, identify installed artifacts and
temporary mounts first. Test the implicated effect/strength through Android,
then cancellation and logs as relevant. Root may install a temporary candidate;
ordinary app playback must remain in the production UID/domain with enforcing
SELinux. No further campaign is automatically pending. Exact HyperOS perceptual
parity and measured acceleration remain unestablished.
