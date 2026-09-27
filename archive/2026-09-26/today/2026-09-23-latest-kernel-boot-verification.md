# Latest kernel boot verification — 2026-09-23

## Current installed state

Verified through ADB/Magisk after the user rebuilt and rebooted:

- Kernel: `4.19.325-cip136-st20-perf-g10f8a106de65`, built 2026-09-23 15:42:15 EEST.
- Android 17 user build; boot completed; SELinux Enforcing; root available.
- Initial new-kernel capture began about 50 seconds after boot, followed by a later settled-boot capture.
- Live config: WIL6210 disabled; DMABUF_SYSFS_STATS and FUSE_BPF disabled. Do not restore the reverted DMA-BUF option just to silence missing-backend messages.

This supersedes the earlier same-day installed-kernel observation of `78d5b0cd5d26`. That earlier boot used a kernel preceding the fixes despite current vendor init files. The deployment/build-cache cause was not established; the latest boot confirms the expected revision is now installed.

## Before / after boot-log comparison

| Signature | Earlier kernel | Current kernel |
|---|---:|---:|
| WiGig parent PCIe enumeration failed | 53 | 0 |
| Invalid ASoC routes (AUDIO_REF_EC_UL30, MultiMedia23/24/25) | 4 | 0 |
| White LHBM b2 / 1000-nit parameter reads failed | 2 | 0 |
| Cirrus amplifier PDN failed | 2 | 2 |

These counts are from complete captured dmesg/initial logcat snapshots, not equal-duration performance measurements. Disappearance of the first three signatures confirms those boot regressions are resolved in this observation; it is not blanket hardware validation.

## Remaining issues

- Both Cirrus amplifiers still report `PDN failed` during startup. Audio service registration does not prove the power-down sequence is correct.
- Sensor HAL continues `ERROR: Fix ultrasound sensor so it does not return error from poll()` in initial and later logs.
- A later `dumpsys meminfo --oom` query reproduced system_server errors for `/sys/fs/bpf/dmabuf/prog_dmabufIter_iter_dmabuf` and `/sys/kernel/dmabuf/buffers`. No periodic background rate is inferred from diagnostic-triggered messages.
- Other optional-interface/debugfs and vendor startup warnings remain; do not turn missing optional interfaces into broad permission grants.

## Healthy observations and limits

No fatal Java/native crash or ANR signature was found in captured current-boot logs. No restarting service was reported by property checks. Existing tombstones predate this boot. USB functions are applied/configured, NFC is on, the audio HAL is registered and 62 sensors are enumerated. Thermal status was 0.

These checks do not validate audio quality, microphone capture, proximity behavior in calls, camera recording, Bluetooth accessories, NFC transactions or fast-charger speed. No production-readiness claim follows from this boot audit alone.

## Evidence and actions

Local raw captures (not uploaded because they contain device/network/account information):

- `~/evo17/out/boot-audit-20260923-153036/` — earlier kernel.
- `~/evo17/out/boot-audit-20260923-160357/` — current kernel; `identity.txt`, `dmesg.txt`, `logcat.txt`, `health.txt`, `services.txt`, `late.txt`, `REVIEW.md`.

All diagnostics were read-only. No rebuilds, flashing, source changes, policy changes, service restarts or debugfs reads were performed by the agent.

## Next focused work

Investigate ultrasound polling and Cirrus PDN independently with functional evidence. Reconcile the current libmeminfo source and installed library before deciding how to handle unsupported DMA-BUF accounting. Preserve user-build and standalone hardware/xiaomi ownership constraints.
