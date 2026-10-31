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
- [Final commit](https://github.com/PocoF3Releases/hardware_xiaomi/commit/78334404dfa794f7f1c7d139acc1d2d87d166891) completes
  101-116: GEQ enable (106) switch, reverb amount (115) and leveler amount
  (116) sliders. The QDSP `capi_v2_dap_cpdp.so` (Hexagon, decompiled with
  Ghidra) clamps `rs_amount` 0..16 and leveler amount 0..10, but the DAX
  service keeps reverb writes above 9 at 9, so that slider is 0..9. IDs 117+
  log "param id not supported" in the DMS ParameterAdapter.
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
Final test: GEQ 1->0->1, reverb amount 0/1/4/8/9 (10-14 read back 9),
leveler 0 and 10; all 13 native values, preferences and APK restored.
Not covered: audible/acoustic effect measurement, the headphone-only
distance slider (speaker-route probes read the speaker endpoint and stayed
4), other locales beyond English/Russian.
The next ROM build is needed to ship the changes.

## Deeper recheck — speaker route

[UI commit](https://github.com/PocoF3Releases/hardware_xiaomi/commit/ab7a012708621560b1fa480b98d5f025f1924423) adds an
Equalizer-tab notice while the GEQ switch is off (with Turn on), one shared
check/cross switch on every tab and a Games section heading.

Same enforcing bind-mount method, speaker only (no BT/USB headset):
- With the app paused (SIGSTOP), toggling IEQ preset, dialogue, reverb and
  leveler never reset their amounts, so restore order cannot clobber them.
  While the app runs, foreign probe writes are erased: on regaining control it
  resets the profile and replays its saved keys. Earlier probe "restore" writes
  therefore only matched because the tuning defaults equal the baseline.
- Leveler amount 6 persisted across Movie/Dynamic switches (Movie keeps its
  own 0) and process restart; Reset current profile returned it to 0 and
  cleared the key. Reset and custom profiles cover all new keys.
- GEQ notice appeared at native 0 and cleared after Turn on (native 1).
Original APK, `profile_0.xml` (hash, owner, label) and all native values were
restored. Not covered: headphone-only distance and game audio (need headset).
