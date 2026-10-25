# Alioth audio integration audit — October 25, 2026

## Reverse-engineered scope

The shipped 32-bit Qualcomm primary HAL, MiSound, DAP, Game DAP and VQE were
inventoried against product properties, effect registrations, resource files,
current Parts/Dolby wrappers and existing framework DAP integration. All 20
libraries in the common audio_effects.xml resolve in the 32-bit build output.
This is dependency coverage, not proof that every registered effect is active.
Raw libraries, disassembly, decompiled code and device logs stay private.

MiSound library SHA-256:
`8a8cb2b953d296697db7ff3024661126e0c4932920b0e13778fbd016aa9c00d6`.
MiSound_command is ELF VA 0x7ef0 (Thumb symbol 0x7ef1); Ghidra adds 0x10000.
Its SET_PARAM case 2 accepts band IDs 0..9 and calls strtof on the supplied
ASCII value. Parts now includes the C-string NUL terminator. Headset parameter 1,
music parameter 4, scene parameter 15 and enable parameter 25 remain unchanged.
MiSound_saveEQ at ELF VA 0x6b38 persists only for session zero; the native probe
used a separate nonzero session, avoiding the global saved EQ. Negative, zero and
positive gain were confirmed through native readback using the production wrapper.
A separate scene-restore decompilation was incomplete and is not used to infer
new controls. No unverified ear-compensation or sound-ID UI is exposed.

VQE setConfig (ELF VA 0x11d170) requires matching input/output rates and formats.
VqeProcess::configure (0x11d9fc) accepts PCM format IDs 1/3/5, matching mono/stereo
channel masks 1/3, and rates 8/16/32/48 kHz. It is not an arbitrary universal insert
for every modern capture/playback path. Existing registration is preserved;
no blanket VQE insertion or unverified tuning is enabled.

## Integration decisions

| Area | Result |
| --- | --- |
| DAP and DMS | Existing registered libraries, service, endpoint tuning and opted-in lifecycle ownership retained. |
| Native game processing | Explicit qcom-qdsp contract retained; unsafe route/mode changes clear immediately and activation rechecks live eligibility. |
| Game DAP library | Already registered; presence alone does not establish an additional safe automatic attachment policy. |
| MiSound | Fix NUL-terminated EQ transport; keep ten-band native writes, seven-band saved presets, headset names, scenes, tile and approved UI. |
| Hi-Fi | Existing hardware capability gate retained; no claim of an additional DAC or unverified endpoint. |
| Capture | Existing AEC/NS registration retained; no outgoing calls, microphone capture or private audio collected. |
| Karaoke/voice changing | Native hooks require application/session/routing contracts; do not force them globally. |
| MediaTek | Work was cancelled by the user; no MTK property, binary or tuning was integrated. |

## Validation

The production MiSound wrapper passes host encoding/invalid-input checks and
native isolated-session EQ readback at -1.5, 0 and +1.5. Both XiaomiParts and
XiaomiDolby incremental module builds pass. Original preferences and approved
feature controls are retained. The source changes contain no test fixtures or
proprietary decompilation.

The updated Dolby APK was exercised through a temporary overlay with SELinux
Enforcing. An active game was confirmed before entering MODE_IN_COMMUNICATION;
game state was false/off after 700 ms, then true/on after returning to MODE_NORMAL.
No microphone or outgoing call was used. Three game/Home cycles and a forced
persistent restart while active passed. Four silent 48 kHz stereo PCM runs each
rendered 180480 frames with zero underruns; the crash buffer was empty and there
were no matching controller command/acknowledgment failures in captured logs.

The original installed Dolby and Parts APK hashes were verified after restoration.
The module, test preference, diagnostic APKs and probes were removed; game/backend
properties returned to their original absent state. Android boot completed and
SELinux remained Enforcing. The installed full ROM still predates these fixes.
Tested Dolby APK SHA-256:
`a80121867b3d98de284975202aaa9bf395a5ca4594b296a1eb24e8e49d98be9a`.
Tested Parts APK SHA-256:
`ded629e43b01f8d25b8487f528571e898bc5ccdef69cce9eb889d1cc3ef592c1`.
The Parts APK supplied the production effect class to an isolated native probe;
it was not installed over the phone's Parts package.

## Consolidated sources

- [Qualcomm backend](https://github.com/PocoF3Releases/hardware_xiaomi/commit/6ea372a7ac473bcf96aede8b1fe8fd22446423c1).
- [Persistent owners](https://github.com/PocoF3Releases/hardware_xiaomi/commit/628f5eff494edad989bfebc73ce8c6ba8d3ddf2a).
- [Product selector](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/44c50c27882a1324a9bf06910d038d5fbca91025).
- [MiSound EQ transport](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/58cf1a749473496bc4130d0bdc68016dfe5f1d5f).

The recent backend refinements are consolidated into the implementation, with
persistent-owner initialization and the Parts fix kept separate. Recovery
patches remain local overlays, outside the ROM public branches. These APK tests
are not full OTA acceptance, subjective listening or physical headset validation.

## Independent final review

A separate GPT-6.1-Sol agent using low reasoning reviewed the cumulative hardware
backend/lifecycle changes and the Parts transport fix, with no actionable findings.
This was static review, not an additional build or device test. Recovery patch
preflight reports zero pending patches for frameworks/base and both Xiaomi device
trees after consolidation.
