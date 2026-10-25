# Alioth audio prebuilt audit and consolidated recovery

Observation: 2026-10-25. Source-checked, build-tested and device-tested within the scope below.
Proprietary copies, disassembly, pseudocode and raw logs remain private.

## Consolidated MiSound implementation

[0de236a](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/0de236a93b3dc7dbb59e16219d234e7141c6bd87)
combines native-state reconciliation and control-listener recovery in one commit.
Both the public final tree and the local tree including recovery overlays are
identical to their pre-consolidation equivalents. The native EQ string fix remains
a separate existing change; translations/resources stay in
[b653ae1](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b653ae1cbb59c26410eae3b1b22e0029781d254a).

Independent internal agents rechecked cumulative MiSound lifecycle and Dolby
interaction. No additional controller change was justified. Fresh phone checks
passed prolonged control loss, startup during contention, three audio-server
restarts, non-flat EQ recovery and rapid recording/playback/VoIP with actual
earpiece/speaker transitions. Exact saved preference hashes were unchanged.
The earlier requested-Off and pause-disabled acceptance remains applicable to the
identical final implementation.

Tested Parts APK SHA-256:
8d4daaeaeb784e5a04eabb3ffcaced87540ef35acb78c87667e3cfcaed7f1da6.
Dolby remained unchanged. Temporary APK deployment was removed; original APK,
preference and backed-up audio-property hashes/values were restored, Android boot
completed and SELinux remained enforcing. This does not establish inclusion in a
flashed ROM; the next ROM build is required.

## Reverse-engineering coverage

The inventory uses both vendor extraction lists, audio/codec/effect configuration,
ELF imports/exports, embedded dynamic-library names and same-ABI dependencies.
It covers current proprietary Alioth/common inputs, not every historical MIUI
binary or source-built Android library. Thirteen source-built support/effect
modules were identified separately, rather than treated as missing blobs.

The first 65-entry ELF sweep was incomplete. A follow-up added 22 dynamic/helper
paths, including FCSAM, HDMI/HFP, compressed capture, sound-monitor, ADPCM,
mu-law, DSD and sound-trigger graph helpers. All 87 distinct paths are indexed.
Four had prior partial pseudocode; all other 83 were imported and processed with
Ghidra, including four Hexagon DSP programs. MiSound was also reprocessed, and
targeted primary-HAL voice/recording/audiozoom routines were newly decompiled.

ARM Thumb context was corrected from ELF function metadata before analysis.
This recovered previously truncated MiSound scene and audio-cloud mutation bodies.
The initial pass identified 21,387 functions and produced 21,380 bodies. Targeted\nretries recovered two more; five remain unresolved/timed out.\nGhidra completion is not semantic proof: timeouts, bad-instruction bodies,
unresolved indirect calls and private ABI uncertainty remain explicitly recorded.
Calibration and firmware data are inventoried rather than falsely disassembled
as ARM code. The sanitized [coverage index](audio-prebuilt-coverage-20261025.json)
owns per-input identities and decompiler limits.

## Confirmed contracts

- MiSound manual scene setters already apply/save native state. Scene restore
  reads the configured scenario support gate and persistent scene/restore values;
  the separate restore-switch default does not prove manual scenes are broken.
- Native VoIP rate/DTX controls match existing mixer controls. Recording,
  communication and incall helpers do not justify a second Parts controller.
- Ultrasound uses the existing audio seqpacket socket. Some native APIs return
  success despite transport failure, so a return code alone is not acceptance.
- Audio-cloud mutations, region overlays and dynamic logs already have native
  wiring or optional fallbacks. No MIUI whitelist was imported.
- Generic Qualcomm speaker protection is hardware/property gated. Its presence
  does not justify enabling it for the different shipped amplifier.
- Sound-trigger callback/version exports, wrappers and configuration exist.
  Bluetooth session providers enforce negotiated session/codec contracts.
- Legacy OMX binaries are distinct from the advertised codec stack and HAL
  compressed-offload path. Blob presence alone does not justify registering
  obsolete components. Recognition stages retain their configured 16 kHz paths.

## Real packaging gap: FCSAM

The existing 32-bit primary HAL dynamically loads the stock FCSAM plugin, whose
Open function requires FM_CAM.bin. Both shipped FCSAM ABIs exactly match the
provided stock dump; the matching 3164-byte stock payload was absent from our
vendor inputs. On the phone, isolated 32-bit initialization returned 116 without
the file and zero with it. The file is unchanged, SHA-256:
5493b05bf10d5f768a1511e521a9d69820d4c592953562d7901b948cb3cbad5a.

[Vendor payload](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/3b312ac9d0a32daaff6785ee45d9f3a3715475f7) and\n[extraction entry](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/d6c19893590c1004e0a579c0ca9182b2ef2594c3)\nadd only this stock payload, its extraction entry and the generated
copy rule. No flags, gains, calibration values, UI or new consumer are enabled.
An independent sweep of 845 shipped vendor ELFs found only the 32-bit primary HAL
referencing FCSAM; no 64-bit caller was identified. A synthetic direct 64-bit probe
crashed after loading the data. Its private ABI/behavior remains unresolved; this
is not labeled a production failure or fixed by enabling a 64-bit audio stack.
No 64-bit migration was made.

## Limits

Native enable/readback and initialization are not acoustic quality proof.
Bluetooth/USB endpoints, phone calls, full recognition, all codec streams and
individual third-party VoIP applications were not comprehensively exercised.
DSP firmware/tuning semantics remain incompletely decoded. No global VQE,
speaker tuning or experimental route changes were added.

## Packaging and publication

The scoped vendor/etc/FM_CAM.bin build target passed. Its output checksum exactly
matches the stock payload and vendor source file. No full ROM build or flash was
performed. All three source branch tips were read back after publication; recovery
overlay preflights remain clean. Temporary native probes and phone files were
removed. Workhub structural, fixture and whitespace checks passed.
