# Alioth AW8697 haptics

Checkpoint: 2026-09-30. Source implementation is pushed; latest target compilation and host tests were recorded. The maintainer cannot reconnect the device yet and will rebuild, install, root and test later. Do not describe this checkpoint as device-accepted. [V-HAPTICS](validation.md#v-haptics) owns acceptance scope; [source map](repositories/TRACKED_HEADS.yaml) owns current full refs.

## Production ownership

- `hardware/xiaomi:cnb` dd9b48e: `vibrator/aw8697/` owns the standalone AIDL V2 service, waveform/scale/buffer helpers and tests.
- `kernel/xiaomi/sm8250:aosp-17` 0dea12dc: `drivers/input/misc/aw8697_haptic/` owns stock-driver compatibility, direct RAM gain and bounded custom RTP transport.
- Common tree 070778f and Alioth 551ee94 provide opt-in packaging, node permissions and SELinux. Inspect their exact changes before modifying policy.
- Module `android.hardware.vibrator-service.xiaomi_aw8697`; init `vendor.aw8697.vibrator`; Binder `android.hardware.vibrator.IVibrator/default`; device test `xiaomi_aw8697_vibrator_test`.

Final product works without root. Rebuild matching kernel/HAL/device integration; a temporary root deployment is only a test. Keep hardware/xiaomi standalone. Do not apply the Alioth mapping to every SM8250 phone without its hardware/firmware evidence.

## Verified stock foundation

Driver reference: [MiCode Alioth kernel](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/tree/alioth-r-oss/drivers/input/misc/aw8697_haptic), local `~/alioth-r-oss`. DTS reference: [MiCode kernel_devicetree](https://github.com/MiCode/kernel_devicetree/tree/alioth-r-oss), local `~/kernel_devicetree_alioth-r-oss`. Alioth stock replaced the earlier dagu/psyche-derived driver mixture. PMIC qcom haptics bindings are not automatically AW8697 bindings: trace the actual driver property reader before copying DTS fields.

Stock `~/miui/out/vendor/firmware/aw8697_haptic.bin` matches the shipped `vendor/xiaomi/alioth/proprietary/vendor/firmware/aw8697_haptic.bin`: 3622 bytes; SHA-256 `7e31b22b591d5f45dcf262529b71fd2b5b3277f98553414b54d3b69d7255d4c4`. The public [firmware tools](https://github.com/kde-yyds/aw8697-firmware-tools) provided matching reference data. Header checksum is big-endian 0xe010, sum of bytes from offset 2; RAM base 0x0800. Four-byte inclusive start/end descriptors begin at offset 5; first waveform data begins at offset 49. Eleven sample lengths: 381,443,304,252,681,243,437,169,217,304,142. Zero-based waves 2 and 9 match; wave 10 is a calibration sine. The audit tool is read-only.

Stock `vendor/lib64/libaachaptics.so`: 56344 bytes; SHA-256 `9d70e1d5337f3494ea359eb7532112a0af48fc563c352d5ff816ef7d8f0dd54a`. Analysis identified AAC 1.0.7_20210722, 24 kHz processing, 256/512/1024 frames, one/two-byte samples and nonlinear intensity handling. Its tuning/model internals do not supply an Android measured acceleration map. Empty named RTP placeholders do not establish missing firmware. RAM F0 calibration and RTP oscillator calibration differ: replaying RAM bytes as RTP is not physically equivalent.

No runtime RichTap SDK/library dependency is integrated. Option B means retaining verified stock behavior and implementing compatible missing transport/contracts. Earlier generated RichTap-style templates caused weak/indistinguishable effects and were abandoned; do not resurrect them on the assumption that the brand proves correctness. The Xaga 5.10 driver is comparative reference, not Alioth certification.

## Kernel and HAL interface

Find the input event node by EVIOCGNAME `aw8697_haptic`, not a fixed event number. Observed sysfs base: `/sys/devices/platform/soc/a8c000.i2c/i2c-2/2-005a/`.

- `gain` accepts decimal 0..128. Positive Android amplitude rounds to at least one driver unit.
- Read `f0_value` for cached resonance in tenths of Hz; reading `f0` triggers calibration. Cached resonance alone is not Q factor or FOAM.
- Custom wave ABI 2: 512-byte period, 8192-byte ring, custom effect ID 193. Service waits up to ten seconds for delayed RAM firmware before publishing capabilities, which Android caches.
- Optional `ram_gain_abi=1`: fourth short `0x4700 | gain`, gain 0..128, input custom length eight bytes; legacy payload remains six bytes. Tagged gain is limited to RAM effects, not arbitrary RTP IDs. Older kernels retain the legacy path.
- RTP writes are bounded to 3584 bytes per chunk, period-aligned except final partial data; append a zero sample for an exact period multiple. Prefill reaches 2048 bytes or EOF; subsequent refill respects actual available space, deadlines and cancellation.
- Kernel publishes EOF after payload; release/acquire ordering protects ring data/indices. Reader checks EOF before the tail snapshot. Wait conditions use actual free space/cancellation rather than a lost-wakeup-prone flag. Invalid lengths are rejected.

## Android behavior and current limits

`perform` retains stock LIGHT/MEDIUM/STRONG drive 30/64/128. Double click is two stock clicks separated by 80 ms; texture tick uses a softer stock tick. Composition RAM primitives use CLICK ID 0, LIGHT_TICK ID 2 and THUD ID 3.

Additional primitives are explicit software RTP waveforms, not proven stock Android calibrations:

| Primitive | Internal ID | Active duration | Current shape |
| --- | --- | --- | --- |
| SPIN | 103 | 100 ms | Sine envelope, varying carrier |
| QUICK_RISE | 104 | 50 ms | Rising amplitude/frequency |
| SLOW_RISE | 105 | 120 ms | Longer rise |
| QUICK_FALL | 106 | 50 ms | Falling amplitude/frequency |
| LOW_TICK | 108 | 12 ms | Short 130 Hz pulse |

Waveforms use signed 8-bit 24 kHz samples, peak bound 96, 2 ms tapers and an 8 ms guard. Existing full-scale samples are preserved. Earlier user-selected multipliers (spin .65, slow rise .60, quick rise/fall .95) are subjective tuning, not frequency-response measurements. `Waveforms.h` is authoritative for exact construction.

dd9b48e maps composed RAM and RTP scale 0 to the same nonzero software baseline `(30 + 98*scale)/128`. This is an initial stock drive bound, not a measured per-primitive minimum. Raw zero-amplitude generation stays silent; NOOP stays silent. Physical thresholds still require testing.

Completion callbacks are exactly once on normal termination, cancellation, replacement or asynchronous failure, outside the worker mutex. Completion is a terminal notification, not proof of physical success; errors remain logged. This supersedes the earlier failure-callback suppression in d90f299. `setAmplitude` persists across `on()` requests until `off()`, and does not mutate `perform`/`compose`. Advertise amplitude only when its node is available; advertise complete composition only with the required RTP backend.

PWLE, frequency control, Q and FOAM are not advertised without trustworthy measured actuator data. Do not fabricate a frequency/acceleration table to expose a checkbox. Android contracts: [haptics implementation](https://source.android.com/docs/core/interaction/haptics/haptics-implement), [haptics assessment](https://source.android.com/docs/core/interaction/haptics/haptics-assess-hardware). Device-local AIDL and VTS sources are the exact build contract.

## Reproduce checks and resume

Source tests in `hardware/xiaomi/vibrator/aw8697/tests`: PrimitiveScaleTest.cpp, WaveformsTest.cpp, RtpBufferTest.cpp, test_hal_host.py, test_firmware_audit.py and device VibratorTest.cpp. Kernel tests: `drivers/input/misc/aw8697_haptic/tests/ram_gain_test.c` and test_ringbuffer.py. Read each test's runner/header rather than guessing command-line arguments.

Recorded checks: HAL target compile/link and device test compilation with r596125; kernel object compilation with r563880c against existing configuration; exhaustive RAM tag handling (65536 words, 129 accepted); production ring-buffer ASan/UBSan host stress over 200000 bytes; real HAL-worker tests with Binder stubs/syscall mocks for callbacks, reentrancy, cancellation, failure, capability fallback, amplitude lifetime and zero-scale RAM/RTP. These establish software behavior, not physical feel or a complete ROM build.

After the maintainer's rebuild, identify actual installed kernel/HAL/firmware and remove ambiguity from any temporary mounts. Check capability discovery after service/framework restart, then Tremor predefined effects, every primitive at several scales, toggle on/off, keyboard/back, double-click separation, sine/envelope variation and cancellation. The earlier reports of missing low tick, weak heavy click and single-feeling double click remain regression cases. Record subjective acceptance separately from logs and API completion. Tune only the implicated waveform after a controlled comparison; do not globally boost gain or expose unverified capabilities.
