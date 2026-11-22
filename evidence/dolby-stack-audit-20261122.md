# Dolby stack audit against stock HyperOS — 2026-11-22

**Source, decompilation, module build and temporary enforcing phone checks.**
Published: hardware_xiaomi `cnb` `e26f4c0` (amended Dolby topic; previous tip `3f9c1f1`).
Phone: Nov 12 user build, root via Magisk, SELinux Enforcing. Installed
XiaomiDolby APK SHA-256 `69ae91a066c5ddfdcf3d39b5cc5d22438efe2b32c2b215a14ed9f6a0bb4248ed`
(the final [Nov 12](dolby-voip-reentry-20261112.md) tested APK). Stock input:
the HyperOS alioth dump in `~/miui/out`. Decompiled output is private scratch.

## Stock components compared

| Area | Stock alioth | Ours | Result |
| --- | --- | --- | --- |
| Effect libraries/UUIDs | `audio_effects.xml`: dap, gamedap, vqe, misoundfx | identical entries | parity |
| Dolby properties | dax.support, surround, version, ds2 off | same plus app/AudioFlinger opt-ins | parity |
| Decoders | AC-3, E-AC-3, E-AC-3 JOC, AC-4 OMX | same include; AC-4 already [V-AC4](../state/validation.md#v-ac4) | parity |
| Profiles | `dax-default.xml` 0-3 and 8 default, 4-7 mobility | Dynamic, Movie, Music, Voice, Custom | stock MiSound exposes fewer |
| Tuning selection | system_server `DolbyEffectController`, gated by `vendor.audio.dolby.control.support` (unset on alioth) | app policy with same IDs/ports | ours is an addition |
| MiSound Dolby controls | on/off, profile, mean-centred GEQ on all profiles | all DMS IDs 101-116 per profile | superset |

Stock `DeviceId`/`DolbyEffectController` (miui-services.jar) use the same IDs and
ports as `DolbyEndpointPolicy`: speaker 0 `default_internal_speaker` (an alias of
the landscape tuning), wired 3, Bluetooth 4, USB 5. Rotation only selects
spatializer IDs, so stock never selects `speaker_portrait` on this device.

The stock primary HAL (`adev_set_parameters`, ARM code) handles `dolby_mode` by
setting `persist.vendor.audio.dolby.switch` and calling `select_devices` for each
active use case; no stock vendor component reads that property. Not sending it
loses no processing. `dolby_video_tool_enable` only feeds the HAL scenario path.
`libdovi_omx`/`libdolbyottcontrol` look for a `dolby_vision.cfg` that the alioth
image does not ship and no Dolby Vision codec is declared: dormant MIUI code.

## Runtime state on the phone

DMS (`vendor.dolby.hardware.dms@2.0-service`) runs; DMS logs show only profile and
parameter events from the app's restore. AudioFlinger's DAP controller reports
`support=1 control=qdsp version=DAX3_3.6`, captured on I/O 13, offloaded, attached
and enabled, with the app holding control at priority 100. All Dolby/game
properties are set (the shell domain cannot read `vendor_dolby_config_prop`;
root can). The only audio denial since boot was the HAL opening `/dev/diag`.

## Fix

`SummaryProvider` showed the live `activeState`, whose defaults (`enabled=false`,
empty name) apply until the engine publishes its first snapshot or after a failed
transaction. It now falls back to the saved enable preference and saved profile
name. The window is short in practice (two fresh-process queries already read the
loaded state); the fallback covers failed initialization. `XiaomiDolby` built;
the APK (SHA-256 `8fe46d89c2ae14184a88307323a48c722690808c350059a3b869b8cb37a4875a`)
was bind-mounted temporarily: summary `On (Dynamic)`, DAP control regained, no
crash. The original APK, mounts and preferences were restored and re-verified.

No other defect was found in the reviewed engine, controller, effect wrapper,
endpoint policy, game controller, boot/tile/summary classes, SELinux policy or the
native DAP pregain path. Headphone/Bluetooth/USB routes, acoustic effect and an
installed-ROM check remain unverified (no accessories attached).

## Tooling

jadx 1.5.6 was reinstalled under `~/tools/jadx-1.5.6` from the official release
(asset digest verified); `~/.local/bin/jadx*` now point there. The Ghidra links in
`~/.local/bin` still point at the removed `~/evo/.repo/host-tools` copy.
