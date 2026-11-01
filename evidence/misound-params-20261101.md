# MiSound parameters, custom EQ and device check — 2026-11-01

**Source, RE and device-tested (root diagnostic, Enforcing).** November 1 ROM,
kernel `Redline-830fb30`, installed XiaomiParts identical to the build output.

## Native and stock map

`libmisoundfx.so` (`MiSound_command`, Ghidra): set-param IDs 1 headset, 2 EQ
band (string level, bands 0..9), 3 mode, 4 music, 5 movie, 6 per-app exclusion,
7 movie mode, 8 Hi-Fi, 9-14 ear compensation, 15 scenario, 16 surround level,
17 vocal level, 18 movie-scenario restore, 20 3D surround, 21 effect enable,
23/24 SoundID gains/enable, 25 enable. 16/17 have no native range check, and stock
MiSound never calls them; 3D surround is headphone-only on stock Alioth
(`ro.vendor.audio.feature.spatial=7`, speaker spatializer false). Not added.

Stock MiSound scenes (Smart 4, Music 1, Video 2, Voice 3) and its seven-band
presets match Parts, except Classical: stock `-3,-3,-3,-3,0,3,3`, Parts shipped
`0,0,0,0,3,6,6`. Stock DiracEqualizer edits seven bands from -10 to +10 dB in
0.5 dB steps (rank -10..10, level factor 2).

## Change and validation

sm8250-common `e22ff4d` adds the Custom preset/editor and stock Classical with
legacy migration; `0ce6ce8`/`b53a218` (Codex) add draft rollback and translations.
`EffectMiSound` verbose log on the phone: Classical sent -3,-3,-3,-3,0,3,3 (bands
7-9 zero); custom bands reached 9.5 and -10.0 and were saved separately; reselecting
Custom after Classical replayed them; a planted legacy Classical string was
rewritten to the stock curve after process restart and applied. No crash or apply
failure. MiSound was returned to Off with custom keys removed.

## Decision

Dolby and MiSound stay independently switchable (maintainer, November 1), unlike
stock MIUI's single effect choice. Not covered: headphone routes, audible effect.
