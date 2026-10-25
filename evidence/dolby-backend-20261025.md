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
production policy passed. The candidate and installed APK signing certificates
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
