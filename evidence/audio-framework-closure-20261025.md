# HyperOS audio framework closure — October 25, 2026

**Static analysis and separately scoped installed-phone tests.** This closes the
specific Java decompiler gaps from the [previous audit](audio-subsystem-followup-20261025.md).
It does not claim reconstructed buildable HyperOS source or acoustic equivalence.

## Java gaps resolved from actual bytecode

Input identities match the earlier stock extraction: MiSound APK SHA-256
`5367a89f6f0c65f79d52ce8134d040e1e309919dac89e2092402cc6c9937373c`;
miui-services JAR `048763a871c0de03a361bf167749a80c6233fa91409e5f093adcaeccec1d167e`.

JADX simple/fallback output was cross-checked with complete offset-annotated
baksmali disassembly, raw method signatures, instruction ranges and callers.
[Per-method dispositions](audio-java-closure-20261025.csv) distinguish:

- Services: 12 aggregate errors corresponded to seven hard-error methods. Only
  `DolbyEffectController.acquireDolbyDeviceIdForSpatializer` concerns audio.
  The recovered selector uses rotation, volume and available/enabled platform
  spatializer state, with existing private parameter 4 transport. Current Dolby
  transport matches. The source spelling `speaker_spatilizer_*` is an ABI detail,
  not a typo to silently correct. It does not establish Alioth spatial support.
- Other audio warning sites concern audio-button analytics, cloud retrieval/file
  download and Bluetooth identity parsing. Their bytecode was also examined;
  these do not establish missing PCM or effect control.
- MiSound: 15 aggregate errors are not 15 missing audio methods. Eleven textual
  stubs include support-library synthetic methods; the malformed Dolby enum
  initializer adds a twelfth recovery target. Every target has a bytecode/caller
  disposition. The enum confirms DAP IDs 101–116 and 20-band gains at ID 110.
  Remaining stubs are calendar/UI/window/fragment/constraint routines.
- Simple Java generation still fails on unrelated edge-suppression/support code.
  Exact instructions and targeted semantics close the investigation; do not
  relabel original JADX errors as a successful whole-source reconstruction.
  MiSound fallback completed successfully. The 39,275 DEX declarations include
  native/abstract declarations; they were not all manually semantically reviewed.

## Native framework expansion

[Native coverage](audio-native-framework-closure-20261025.csv) includes 45 newly
decompiled ABI-specific libraries plus the previous five: 32,379 discovered
functions. All 22 initial timeouts completed on targeted 90-second retries;
selected assembly was retained alongside the retries. No reported decompiler
failure remains in this selected set. This is not complete instruction coverage,
manual understanding of every function, or semantic/runtime proof. Private output
includes ELF hashes, dependencies, symbols and corrected ARM Thumb metadata.

The expanded filename inventory contains 170 system/system_ext/product audio
libraries. Additional generic helpers and generated interfaces received scoped
metadata/export/string checks, not blanket semantic decompilation. The two Dolby
OTT-control libraries are Dolby Vision/video, not Atmos. Broad JNI-owner checks
found OZO MediaRecorder bindings in libmedia_jni; no matching private Dolby/MiSound
markers in libandroid_runtime is a search result, not proof of universal absence.

## Integration decisions

FX4 is real client-side filtering, separately gated by `vendor.audio.lowpower`
(default false), a fixed 27-package video allowlist, eligible linear PCM at
44.1/48 kHz, output flags and speaker routing. Its device state is populated from
AudioTrack route callbacks; it is not a missing prerequisite for the session-zero
MiSound effect already owned by Parts. Both that property and the ULL opt-in are
unset on the checked phone. No duplicate processor or old private AudioTrack
layout was imported into Android 17.

Stock DlbVqeCallback forwards non-fast track notifications to an existing DMS
service; initialization creates no processor. A separately registered VQE
consumer is still required. Current QDSP lifecycle and global MiSound ownership
remain independent. MIUI karaoke, app routing, cloud policy, UID/16-kHz game
voice changing, OZO and shooting detection are distinct opt-in paths; their
presence does not justify global activation or guessed controls.

The deeper follow-up found two configured stock capabilities absent from current
Parts: headphone 3D (parameter 20) and personalized SoundID (23/24). The former
requires the stock spatial feature bit, appropriate headphone route and no
superseding framework Spatializer. SoundID requires real per-headset calibration:
six saved gains are padded to nine indexed writes, with index 8 committing the
block. Native setters and actual stock UI/boot/device-change callers exist.
Earlier broad conclusions must not be read as establishing full stock-feature
parity. Movie surround/vocal/movie-mode reflection handles remain uninvoked in
this APK; support properties alone do not make them active integrations.

The maintainer has no headphones for acceptance. These optional features were
not newly enabled, exposed, or represented as verified fixes. No reproducible
behavioral defect in the approved implemented paths was established by the newly
recovered methods. [Comment cleanup](https://github.com/PocoF3Releases/hardware_xiaomi/commit/f70f79506831bf55b064974ca5a69a4c3bea3d8f)
removes the obsolete incomplete-decompilation explanation for preserving speaker
spatializer tuning. Runtime mapping, capability defaults and translations are
unchanged. No proprietary code or library was copied into ROM sources.

## SoundID profile search

The provided dump has no user-data or persistent-property partition; its
`system_root/data` is empty. No candidate `soundIdData`/shared-preferences profile
was found. APK assets contain six tones and four music samples, not calibration
results. Native restore defaults are nine zero gains and disabled SoundID.
Stock profile records live in app-private `soundIdData.xml`, associate a selected
profile with a headset and include calibrated gains/test data/name. Stock restore
services disable SoundID if no selected profile exists. A firmware dump cannot
establish whether the former user had a profile; factory defaults are not a
replacement. Current-phone gain/state properties are also absent. No personal
calibration values were collected or published.

## Fresh phone verification

The connected rooted phone remained enforcing. Installed-build probes passed
saved Dolby On / MiSound Off readback, rapid capture/playback communication
bypass/recovery, duplex and actual earpiece/speaker route acknowledgments, AAC/Opus
in-memory voice-message encoding and eight recording restarts. Test buffers were
discarded. Exact preference hashes and all six recorded audio properties match
before/after. The original audioserver remains installed; no new prebuilt was
deployed or persistent overlay installed, and the owned test directory was removed.

These tests do not establish remote-call acoustic quality, physical external
Bluetooth/USB/headset behavior or execution of the optional stock processors.
Existing accepted features and separate translation history are preserved.
Headphone-only 3D/SoundID remain incomplete optional feature ports, pending a real
endpoint and, for SoundID, a calibrated profile or properly validated calibration
workflow. This audit closes the specified decompiler gaps, not those feature ports.
The previous combined module readiness check remains applicable: the only new
ROM-source change is a comment, so no redundant compilation was requested.

Private artifacts remain in `~/evo/.repo/audio-framework-closure-20261025/`;
raw proprietary code, recordings and device identifiers are not published.
