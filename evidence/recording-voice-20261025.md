# Alioth recording and voice audit — October 25, 2026

## Native contracts and integration

Two independent GPT-6.1-Sol agents using low reasoning audited shipped recording
and voice processing. Private decompilation and symbols remain outside public
sources; only contract evidence and test results are recorded here.

The primary HAL's cin_read (ELF VA 0x92140) expects compress_read to return the
entire requested byte count. in_read (0x5a8b8) zero-fills the request on failure.
This confirms the existing [tinycompress correction](https://github.com/PocoF3Releases/external_tinycompress/commit/eacefe332464fbb2f55f12d70b2e60fb244e05ca)
as a genuine legacy capture dependency. The installed 32-bit library matches the
current build artifact exactly (SHA-256
`7ca2bc349338a9c3274df327e74ba6a498000bfc61c210de1c3275debef73ac0`).
Normal AudioRecord tests do not by themselves prove compressed capture coverage.

add_remove_audio_effect (0x5c4a0) recognizes the standard AEC and NS type UUIDs,
tracks their attachment and updates native processing/routes. The Qualcomm
preprocessing wrapper is a hardware-tunnel effect, not another software AEC/NS
processor. Current voice_communication preprocessing already attaches both and
Alioth's platform configuration supplies the corresponding module mappings.
No missing global insertion was found. The installed Qualcomm preprocessing
library also matches the built 32-bit output exactly (SHA-256
`af949afb3fe57bd1f8cb422d0b84854fd99ae19124a4e109288257b341135e45`).

PCM VoIP capability (0xa4ee0) accepts PCM16 mono at 8/16/32/48 kHz and uses
vendor.voice.path.for.pcm.voip. The product flag is already true on the phone and
in source, and voip_tx policy matches those limits. Registered VQE remains subject
to the [previously established format/session constraints](alioth-audio-integration-20261025.md);
no unverified global VQE, gain, ACDB, voice-changing or karaoke activation is added.

## Phone validation

The installed user build was tested with authorized root diagnostics and SELinux
Enforcing. Audio buffers were processed in memory and discarded; no recording
file was saved and no outgoing call or SMS was made.

| Target | Passed |
| --- | --- |
| Microphone PCM16 | 16 kHz mono; 48 kHz stereo |
| Voice recognition PCM16 | 16 and 48 kHz mono |
| Voice communication PCM16 | 8, 16, 32 and 48 kHz mono; AEC and NS creation/enable/readback passed |
| Packed PCM24 capture | 96 kHz stereo |
| Float capture | 48 kHz mono; 96 kHz stereo |
| Simultaneous voice playback/capture | 48 kHz mono capture with AEC/NS, silent voice playback; 139200 rendered frames and zero playback underruns |

Capture returned frames and valid timestamps in the PCM16 cases. These are API,
format-negotiation and lifecycle checks, not acoustic echo-cancellation/noise-
reduction quality, bit-perfect high-resolution capture or physical headset
certification. Twelve capture runs passed across the matrix and duplex case.
The crash buffer was empty. All sessions/effects were released, requested/actual
audio mode returned to MODE_NORMAL, SELinux remained Enforcing and all device
diagnostic files were removed. No package, preference or product property was
changed. No new recording source defect was established, so no speculative
production fix was introduced.

## Separate resource history

The user-requested hardware/xiaomi history split has an identical final source
tree to the previously built/tested head. Independent review and mechanical tree
comparison confirm no behavior change:

- [Qualcomm native implementation](https://github.com/PocoF3Releases/hardware_xiaomi/commit/6d8191fc778289e315d011171d64ce4dc27b5c73) contains no translation/resource changes.
- [Unused summary translations](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b653ae1cbb59c26410eae3b1b22e0029781d254a) removes only 79 unused game_effect_summary entries, with no remaining references.
- [Persistent initialization](https://github.com/PocoF3Releases/hardware_xiaomi/commit/6429de66995b8083ff348bc2a2957ead3b833d4d) stays separate.

The branch was pushed with an explicit expected-head lease and read back. No
redundant APK/ROM rebuild was needed for a tree-identical history change. Earlier
[Dolby/MiSound artifact acceptance](alioth-audio-integration-20261025.md) and its
limits remain applicable; these source fixes still need the next full ROM build
for permanent installation.
