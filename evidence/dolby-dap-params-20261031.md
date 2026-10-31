# Dolby DAP parameter audit and new controls — 2026-10-31

**Source, RE, host build and enforcing temporary device test.** Installed
October 28 ROM with kernel 7d559e9; DAX `DAX3_3.6.1.6_r1` stock service.

## Parameter map

Stock MiSound (V816.0.5.0 dump, `b.b` enum) defines Xiaomi DAP IDs 101-116:
vdhe, vspe, dvle, ieid, deon, geon, iea, dea, ded, gebg, beon, vbon, vssd,
rvse, rvsa, dvla. Stock MiSound itself only exposes on/off, profile and GEQ.
A read-only root probe of the global DAP effect returned all 16 for profile 0
(9 profiles reported), matching `dax-default.xml` values (iea 6, dea 4,
vbon 1 on speaker, vssd 4, rvsa 9, dvla 0). IDs 117+ return 0, not an error,
so readback alone does not prove support.

`libhwdap.so` `dolby::qdspParamIdForParam` (minidebuginfo symbols) maps 67
four-character DAP keys to QDSP IDs, including geon, ieon, vbon, vssd, rvse,
rvsa, dvla, regulator, virtual-bass and hearing-protection keys. Keys are
stored byte-reversed in rodata pairs. Writes are acknowledged asynchronously:
status codes never rejected out-of-range values, so ranges cannot be measured
by write status. A reversible inactive-profile write probe restored profile 3
exactly; do not repeat it as range evidence.

## Decisions

- Added per-profile switches for virtual bass (112, speaker route only) and
  reverb suppression (114); vendor-tuned amounts are untouched.
- Kept stereo widening (113) retired: its tuning tag is
  `headphone-virtualizer-steerer-source-distance` and no range is verified.
- Kept volume-leveler amount (116) unset, as upstream decided from tuning.
- Not added without verified ranges: IEQ amount (107), dialogue ducking (109),
  reverb amount (115).
- frameworks/av `DolbyDapController` already covers the reference controller's
  pregain, I/O handle, audio flag and skip-hard-bypass commands; sound-type
  bypass stays off, matching the reference default without
  `DOLBY_DAP_BYPASS_SOUND_TYPES`. No stock `fade_switch` on Alioth.

## Validation

[hardware_xiaomi 3e77cc0](https://github.com/PocoF3Releases/hardware_xiaomi/commit/3e77cc01266b45539d6fe3ddc62c1c15104322ff)
and Russian strings 3f799c3. XiaomiDolby built cleanly. The persistent app
cannot take a package update, so the test APK was bind-mounted over its
system path (system_file label, Enforcing). Grouped Tone / Voice and loudness /
Surround sections rendered; reverb 0→1→0 and virtual bass 1→0→1 matched
native readback for the active profile and survived process restart.
The mount was removed, the original APK hash `a80121867b3d98de…` verified,
and test-saved preference keys removed. Not covered: audible/acoustic
effect measurement, headphone route, other locales beyond English/Russian.
The next ROM build is needed to ship the changes.
