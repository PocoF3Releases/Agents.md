# Audio route compatibility — 2026-11-02

## Published device-tree correction

[fc61c32](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/fc61c32444f435031bbd6f86ce84aec644e9a895),
`alioth: Route GSM mode requests to the RX codec control`, changes exactly two
control names in `audio/mixer_paths.xml`: the default OFF value and `gsm-mode`
ON value now address `RX_GSM mode Enable`.

**Source/binary checked:** the shipped primary HAL handles `call_type=GSM` in
`voice_extn_set_parameters` and calls `platform_set_gsm_mode`. Its named route
used `GSM mode Enable`, which is absent from the live mixer. The registered
Bolero provider is `RX_GSM mode Enable` (`rx-macro.c`), with OFF/ON selecting
bit 2 of the RX BCL VBAT register. The missing control was skipped by the route
loader, leaving a route that reported success without changing the GSM bit.
The stock dump has the same stale name; this is an inherited integration defect,
not evidence that recent kernel correctness fixes broke the ABI.

Independent review found no blocker in the two-name correction. No calibration,
DSP tuning, Dolby/MiSound preference, route topology, security/thermal policy or
kernel source was changed. Tests remain private; no tests or documentation enter
the device-tree commit. GitHub recognizes both project and Codex authors.

## Verification scope

**Device-tested:** isolated minimal XML was extracted from the actual default
and GSM path. The fixture loaded the phone's production 32-bit
`libaudioroute-v34.so` and `libtinyalsa.so` against its real mixer:

- Five old apply/reset cycles returned success but left GSM mode OFF.
- Five corrected cycles enabled the bit, then reset it to OFF. Final state OFF.
- The 19-case PCM fixture passed four capture sources at 16/48 kHz and three
  generated-playback cycles. Capture samples were discarded in memory.
- Three built-in speaker/earpiece duplex pairs passed, six route switches total.
  Mode 0 was restored; audioserver and mi_thermald PIDs remained unchanged.
- Running kernel: `4.19.325-Redline-7285847-cip136`, SELinux Enforcing, taint 0.
  No new critical kernel message matched the marked PCM test window. Task staging
  was removed; no call, modem request, settings reset, flash or policy relaxation.

This proves route/control transport and bounded PCM regression coverage, not
cellular-call acoustics or a modem-driven GSM call. The complete revised mixer
XML is **not persistently installed**: the phone comparison used an isolated
fixture, and the production change will enter the next ROM rebuild.

**Build-tested:** `m -j4 out/target/product/alioth/vendor/etc/mixer_paths.xml`
passed under `lineage_alioth-cp2a-user`. Artifact equals source, SHA-256
`92966cb38a93410f205e1ab05e570bf85337304753e6a470841297d210273ad0`.
All six Alioth audio XML files parse; diff checking passes. There is no changed C
object requiring another kernel W=1/Sparse build. The unchanged running kernel's
strict build is recorded in [platform acceptance](platform-recheck-20261102.md).

**Composition checked:** the public source commit excludes recovery overlays.
Local integration head `d3ce37193743309e4b5c0fae90316de728c26b90` retains them. Applying all four
manifest-listed recovery patches to the current public framework/device bases
reproduces all three local Git trees exactly. The normal patch runner's
`--check` reports zero pending patches. Manifest branches/checksums need no edit.
Private receipts: `~/evo/.repo/audio-route-followup-20261102`.

## Remaining generic routes

The [earlier inventory](kernel-contract-plan-20261102.md) is a pinned historical
checkpoint; its residual GSM entry is superseded by this correction. Remaining
limits are not silently classified as working or removed just to reduce counts.

| Contract | Finding and disposition |
| --- | --- |
| Handset sidetone | Actual handset caller is reachable. The generic path contains an absent WSA sidetone control despite Alioth's Cirrus receiver. Correct replacement and acoustic behavior remain unproven; do not invent AFE routing or an empty override. |
| Headphone HiFi | Shipped native HiFi gate can select a path whose `CLS_H_HIFI` enum is unavailable and falls back to `CLS_H_INVALID`. Current Parts feature opt-in is false; retain it. No headphone endpoint is available for verification. |
| Two generic defaults | V34 loader maps unknown `ZERO` to enum index 0: `RDAC3_MUX` becomes RX1 and `ADC2 MUX` becomes INP2. No new incorrect reset behavior demonstrated; unchanged. |
| Liquid DMIC | Unsupported DEC7 selection confirmed; Alioth activation not established. No guessed replacement. |
| DisplayPort voice | Generic DP1 names differ from registered `DISPLAY_PORT_RX1_Voice` names. External endpoint/support and end-to-end behavior remain unverified; deferred. |
| MMAP | Framework/product policy 1 means NEVER, including app override attempts. Do not enable it to exercise dormant generic paths. |
| FM capture | Runtime extension feature flag is true; kernel RADIO_IRIS is disabled. Physical FM endpoint is not established, so feature availability alone is no runtime acceptance. |
| Other amplifier/VBAT routes | Alioth's overlay and explicit feature gates remain authoritative. Do not enable other amplifier/protection topologies to satisfy generic XML. |

The paused touch boundary task remains skipped. Broader kernel-to-consumer
compatibility work remains incomplete; this one fix does not certify every
proprietary path or all downstream commits.
