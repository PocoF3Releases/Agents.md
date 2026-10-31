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
- Parameter 113 is `headphone-virtualizer-steerer-source-distance`, now
  exposed as virtual speaker distance with its verified range (below).
- Kept volume-leveler amount (116) unset, as upstream decided from tuning.
- Ranges were later verified from the shipped `libswdap.so` public setters
  (clamp immediates, lower bound `max(x, 0)`): `dap_cpdp_ieq_amount_set` and
  `dap_cpdp_de_amount_set`/`de_ducking_set` 0..16,
  `dap_cpdp_headphone_virtualizer_steerer_source_distance_set` 4..64,
  `dap_cpdp_volume_leveler_amount_set` 0..10, `surround_boost_set` 0..96.
  All tuned values lie inside. No public reverb-amount setter exists.
- [Slider commit](https://github.com/PocoF3Releases/hardware_xiaomi/commit/540bd0e7cc2ac1e09bb7cc0e4bd9381451858d3b) adds
  per-profile sliders: IEQ amount (107, shown with an IEQ preset), background
  ducking (109, under dialogue enhancer) and virtual speaker distance (113,
  headphone virtualizer). Dialogue strength keeps the upstream 1..12 subset.
- Still unexposed: volume-leveler amount (upstream decision) and reverb
  amount (115, no verified setter).
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
and test-saved preference keys removed. Slider test (same method): IEQ amount reached native 0 and 16, ducking 8 and
16; native values, `profile_0.xml` hash and APK were restored afterwards.
Not covered: audible/acoustic effect measurement, the headphone-only
distance slider (no headset), other locales beyond English/Russian.
The next ROM build is needed to ship the changes.
