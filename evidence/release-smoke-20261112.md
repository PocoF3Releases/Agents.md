# Installed release smoke check — 12 November 2026

**Device-tested:** the installed Android 17 / SDK 37 v12.4 user build, with Magisk and
SELinux Enforcing, passed this bounded release smoke check. No production source,
APK, policy, security setting or thermal limit was changed. No new build or flash
was performed. This is not certification of every endpoint or absence of bugs.

## Identity

`EvolutionX-17.0-20261112-alioth-12.4-Unofficial.zip`, 3,157,240,414 bytes,
independently streamed SHA-256:
`2a9488829885a362277b3d9c5948266fb1484ff4254544b85347e9d0619fd88a`.
It matches the sidecar and local OTA metadata. Phone version/timestamp 1794507125,
SDK 37 and five installed APK hashes match the completed output. A spoofed
fingerprint was not treated as OS/source identity. The ZIP has no embedded full
source manifest; current heads alone do not establish every build input.

| Matched installed artifact | SHA-256 |
| --- | --- |
| XiaomiParts | `e2c8c43712063d30b81b4528d45da45f7d9f7aa5da93107c68def067693f305e` |
| XiaomiDolby | `69ae91a066c5ddfdcf3d39b5cc5d22438efe2b32c2b215a14ed9f6a0bb4248ed` |
| audioserver | `edefe5b5558d650de77ae3e0d0b0488b33c5772129f290adae62f4697bb6760f` |

SystemUIGoogle, SettingsGoogle, MiuiCamera and the stock MiSound/DAP libraries also
match their output files. Kernel reports `4.19.325-Redline-cd1f8df-cip136`, build #8.
Source references: [framework](https://github.com/PocoF3Releases/frameworks_base/commit/53e0061d824e3c6c571aebe95fb7bfa83258b3e6),
[AudioFlinger](https://github.com/PocoF3Releases/frameworks_av/commit/6b8c30f24b18f50bc28f6d9f24f98c33ec6e7e07),
[Parts](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/6f6fa1ceb7cee6a01c98d643453158801e491bcc),
[Dolby](https://github.com/PocoF3Releases/hardware_xiaomi/commit/b533e52319d6a3ad59a85e61999fc4f6aa2a66a0),
[kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cd1f8df56f66a012ad4a8b25f3d7a99cc6a5ddce).
The effective framework checkout additionally contains the existing local recovery
overlay; its presence is not a new recovery runtime test.

## Results

- Seven owned recordings saved with strictly increasing packet timestamps and
  clean complete H.264/HEVC decoding using the native time base. Six bounded
  scenarios cover maximum/normal, Keep blur and low quality; the seventh is the
  first extended capture after a test-driver stop-tile lookup failed. The final
  physical 60-Hz test verified display mode 1 and encoder request 60 FPS; physical 120-Hz
  selected 120 FPS. Earlier 60-Hz-labelled attempts still had active 120 Hz and are not 60-Hz
  acceptance. These variable-rate clips do not certify sustained FPS. Blur stayed
  available with Keep blur, otherwise disabled while active and restored on stop.
- Thirteen ordinary-UID/SDK 37 audio cases: two silent-media controls, eight MIC
  and 36 simulated voice-communication duplex cycles, including zero-gap re-entry.
  All completed with frame progress, zero underruns, clean cleanup, MODE_NORMAL,
  no callback/timing drops and no bounded Dolby/AudioFlinger error lines.
- Original-state and MiSound-On matrices each retained owner preference bytes.
  After the On test, non-owning GETs confirmed native/framework gates=1; restoring
  the original Off through UI returned all gates=0. Eleven stream/device volume
  maps and all saved tuning survived. Only an explicit default
  `misound_enable=false` key was added. Headphone-only controls were gated without
  headphones; all three capability properties were verified through authorized
  root reads (shell visibility is restricted).
- Real Sound Settings opened MiSound; Dolby reported enabled for media. Thermal,
  display, refresh, touch and Clear Speaker screens opened without starting the
  cleaning tone. A diagnostic touch client completed 27 GETs and zero setters;
  this does not prove normal-domain setter access. Camera rear preview streamed.
- A normal reboot completed in 24.5 seconds. Wi-Fi was validated, USB configured
  with functions applied, battery present/healthy; saved audio gates recovered.
  Pre/post crash buffers were empty and reviewed kernel fatal-signature searches
  had zero hits. This is narrower than an all-warning or all-subsystem audit.

Own helpers, diagnostic scratch and seven exact MediaStore files were removed.
Recording/display defaults and stay-awake=0 were restored; SELinux and thermal
protection stayed enabled. Raw logs, identifiers, preferences and clips are private
under `~/evo/.repo/release-verification-20261112`.

## Release delta and limits

Maintainer confirms 04.11.2026 as published. The semantic comparison uses the
immutable pre-refresh 5 November source snapshot as a conservative proxy; the exact
published ZIP manifest is unavailable. Replayed/equivalent commits and old banner
topics were excluded. [Long](../state/telegram-20261112-full.md) and
[short](../state/telegram-20261112-short.md) drafts group new system personalization,
audio/Parts, recording-blur restoration, Mini Google apps and distinct kernel
cleanup. No new camera, refresh/FPS, haptics or battery-life claims. USBPD teardown
fixes do not certify physical power-outage/role-swap recovery; Dagu-only PS5169 is
excluded. No current download URL was supplied; none was invented.

Physical headphones/Bluetooth/OTG/NFC transactions, acoustic benefit, new DSP
execution, every camera mode, fresh wipe/sideload/recovery and long-duration
gaming/shutdown/outage tests were not repeated. Parked investigations remain
parked. No Telegram post or release upload was performed; 12 November is a tested
candidate, not a declared published baseline.
