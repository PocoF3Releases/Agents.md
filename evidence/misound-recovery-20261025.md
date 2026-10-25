# MiSound communication recovery verification

Observation: 2026-10-25. Source-checked, build-tested and device-tested.

A higher-priority MiSound client set native music state to zero and released control.
The persistent owner regained control, but normal playback callbacks and reopening
MiSound failed to restore requested processing. Cached state was stale.

[2147d20](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/2147d20b731be3400255925b14cd5de40ecc3176)
reconciles framework enable, native enable and music state on refresh and callbacks.
Requested Off and Pause during calls remain authoritative. No tuning or UI changed.
[Translations remain separate](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b653ae1cbb59c26410eae3b1b22e0029781d254a).

Two independent internal agents reviewed Dolby and MiSound; follow-up review found
no actionable issue in this correction. No natural Dolby failure was reproduced.
XiaomiParts module build passed. Tested APK SHA-256:
810f96391cefa913e4993f9b81da7e43b5ca4f0ec25c2aa16591c726dc8d3ff9.

Phone tests reproduced native drift and verified repair through playback callbacks
and activity refresh. Read-only effect observers never took control. Three scenarios
passed: On with pause, requested Off, and On without pause. Each covered MIC and
voice recognition capture, communication capture/playback without mode changes,
eight rapid recording pulses, five rapid playback pulses, communication duplex,
actual earpiece/speaker selection and normal-mode restoration. Dolby recovered and
MiSound respected preferences. Capture buffers were discarded; playback was silent.
No calls or messages were made. SELinux stayed enforcing.

Original APK and exact preference hashes were restored after temporary module removal
and reboot. This is temporary APK/native-state verification, not flashed ROM or
acoustic acceptance. Bluetooth/USB endpoints and individual messaging apps remain
outside this test scope. The next ROM build must include the fix.

Local recovery overlays were preserved with an identical final tree. Recovery
preflight reports zero pending patches in all three projects.
