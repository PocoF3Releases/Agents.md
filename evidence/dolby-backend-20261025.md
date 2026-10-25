# Alioth Dolby backend audit — October 25, 2026

## Shipped contract

The audit uses Alioth's shipped ARM32 `audio.primary.kona.so` and DAX3.6
hardware/software DAP, Game DAP, VQE, DMS service/implementation and parameter
storage libraries. Direct Dolby dependencies and runtime-library build outputs
are present. Existing DMS init/VINTF registration and product opt-ins are retained.
No codec/HAL version transplant, ACDB edits or gain changes were justified.

The primary HAL SHA-256 and private disassembly are retained in the local audit;
no proprietary decompilation or APK is copied into this documentation repository.
At ELF VA 0x72ff4, platform_set_parameters accepts native effect/mode switches
with on/off values and a package name (32-byte buffer). Its effect handler
writes vendor.audio.game.sound.effect and vendor.audio.game.effect.enable.
The Ghidra project rebases addresses by 0x10000; ELF VAs above exclude that base.

The old app sent AURISYS/FPSOP parameters while the generic product feature flag
was true. That does not identify a supported four-control protocol. Generic HAL
success can accept unknown keys; it is not proof of processing or feature support.

## Alioth implementation

An explicit Alioth product selector chooses native Qualcomm commands. The app
checks both HAL-written state properties before recording success, clears stale
startup state, restores media mode on exit and bypasses communication. Native
speaker/headphone mixer names and game calibration mappings already exist in
Alioth's tree (speaker 10024, headphone/USB 10022); they are not retuned.

Qualcomm keeps OEM tuning. The four FPSOP sliders/help are shown only for an
explicit FPSOP backend; saved preferences and that code remain. Long package
names are excluded according to the native buffer bound, without truncation or
parameter injection. Other products are not automatically opted into this ABI.

Persistent-process recreation also needs initialization independent of boot
broadcasts. A dedicated Application starts the existing singleton owners;
existing idempotent start guards prevent duplicate observer registration.

## Verification status

Changed Kotlin/Compose compilation, the complete XiaomiDolby APK build, native
protocol/capability host regressions and property_info_checker against the
production policy passed. The vendor/build.prop target also built successfully
and contains exactly one alioth-qdsp backend selector. The candidate and installed APK signing certificates
match. Existing system_app vendor-audio property read access covers state checks;
no permissive policy or broad new allow rule is added.

A rooted diagnostic on the enforcing phone started in MODE_NORMAL with no music
active and both game properties absent. Enable returned status 0 / true / on;
disable returned status 0 / false / off. The original absent properties were
restored. This establishes native command handling, not acoustic quality.

On the enforcing phone, the candidate ran as system_app (UID 1000). Selecting
Settings as a temporary game target enabled true/on; leaving it disabled false/off.
Killing the persistent Dolby process recreated it and acknowledged the native
backend without a new boot broadcast or reopening Dolby settings. Silent 48 kHz
stereo PCM playback rendered 180480 frames with zero underruns in each baseline
and native-enabled run. This does not certify audible quality, physical headset
routes, game latency or all games.

The temporary APK module, game preference fixture and diagnostic files were
removed. The original APK hash and absent preference/property state were restored,
Android boot completed and SELinux remained Enforcing. The currently installed
full ROM predates these fixes; a new incremental ROM build is required.

## Published source

- [Native Alioth transport](https://github.com/PocoF3Releases/hardware_xiaomi/commit/8195f7379646fa554fb2059897663db2583a0f99).
- [Persistent owner initialization](https://github.com/PocoF3Releases/hardware_xiaomi/commit/ba2cd983e2af1f524aa62e926d40fdef4b9b65e6).
- [Alioth backend selector](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/6e6eb8c97475aea4d94912b5640456a2192823b3).

Runtime acceptance used the built APK from these source trees through a temporary
Magisk overlay, not a full OTA. Recovery overlays remain separate from ROM public
commits. Private native dumps and test fixtures are not published.

## Final Qualcomm naming and cleanup review

The shared backend is named `qcom-qdsp` / `QcomGameEffect`; the exact property
enum and device selector change together. Only the verified product opts in;
Qualcomm naming is not a claim that every Qualcomm HAL implements this ABI.
The native wire commands, route allowlist, OEM calibration, saved preferences,
Dolby profiles, equalizer controls and persistent-process initialization remain.

A communication-state callback failure now schedules immediate reconciliation;
the existing fail-closed live query clears game processing if querying still
fails. Reconciliation also reuses package validation. The unused old
Alioth/FPSOP summary is removed from 79 default/localized resource entries;
the visible compact summary and approved icons are unchanged.

Production helper/capability host regressions, resource XML parsing and the exact
property-context policy check pass. Earlier enforcing phone acceptance above
covers the unchanged native commands; this review does not claim a fresh phone
installation or fault-injection test of callback query failure.

The final XiaomiDolby APK and vendor/build.prop incremental build passes; the
generated selector is exactly `qcom-qdsp`. No full ROM or new phone deployment
was performed for this cleanup. Final public heads:

- [Qualcomm cleanup](https://github.com/PocoF3Releases/hardware_xiaomi/commit/25a1e35be9ce87196f26d11db93b9222cc0b69cc).
- [Matching product selector](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/488009ad6e8108ecee8cb6c103ceba6e8f08931a).

## Final Qualcomm APK phone acceptance

The final APK built from hardware_xiaomi 25a1e35be9ce87196f26d11db93b9222cc0b69cc
was tested through a temporary Magisk overlay with the qcom-qdsp selector.
APK SHA-256: `3861022c49d4e4ec1f4f3f49768e1893471d1b1330415bbc034ff6779c78199c`.
Package inspection confirmed DolbyApplication, UID 1000 and system_app; SELinux
remained Enforcing. No permissive policy or production preference change was used.

- Three selected-foreground/Home cycles acknowledged true/on then false/off.
- A forced persistent-process restart while active recreated Dolby and restored
  true/on without opening Dolby settings or sending a boot broadcast.
- A second restart on Home recreated Dolby and retained false/off.
- Four silent 48 kHz stereo PCM game-usage runs passed before, during and after
  switching/restart, each rendering 180480 frames with zero underruns.
- A separate normal media-usage PCM run passed with the same frame/underrun result
  after game processing was off. AudioService requested/actual mode was MODE_NORMAL.
- The captured crash buffer was empty; captured logs contained no matching native
  command acknowledgment failures or Dolby/game property SELinux denials.

The first diagnostic process did not exit after successful playback because of
Android runtime threads; its host timeout stopped the sequence. Explicit probe
exit after releasing AudioTrack corrected the harness. The complete corrected
sequence passed; this was not a production audio fix.

The test-only game preference was verified unchanged against its fixture before
removal. The original package-cache entry was restored, the temporary module and
all device diagnostic files were removed, and Android rebooted successfully.
The original installed APK SHA-256 was restored exactly:
`20e2e5175630eb83d6f6c7a0e5c69e14bc89b894145f408c44b9ab4cda6d50b0`.
Backend/game properties returned to their original absent state and SELinux
remained Enforcing. No production source correction was needed.

This establishes playback/control/lifecycle smoke acceptance of the final APK,
not subjective listening quality, physical Bluetooth/wired/USB endpoint coverage,
all games or a full OTA. Permanent inclusion still needs the next ROM build.
