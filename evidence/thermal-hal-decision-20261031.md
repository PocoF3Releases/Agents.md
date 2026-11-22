# Android Thermal HAL decision — 2026-10-31

**Decision: do not add a Thermal HAL.** mi_thermald stays the only thermal
authority; Android thermal status/headroom reporting remains unavailable, as on
stock. Source/RE/read-only device checks; no source, image or device change.
Follows the gap in the [integration audit](integration-audit-20261030.md).

## Device observations (installed October 28 user build, Redline f503c8d, Enforcing)

- `dumpsys thermalservice`: HAL Ready false, status 0, nine registered
  event/status listeners. SoC ID 356 (Kona).
- mi_thermald reads only zone `temp`/`type` (strings); it programs no trip
  points. It publishes its own estimate at
  `/sys/class/thermal/thermal_message/board_sensor_temp` (VIRTUAL-SENSOR).
- Kona `*-usr` zones (CPU, GPU, NPU) and `cpu_therm`/`quiet_therm` use the
  `user_space` policy with no bound cooling devices; kernel cooling is on `*-step`
  zones. `xo-therm-adc` reads -40000 (invalid); `skin-msm-therm-usr` does not exist.

## Stock HAL reverse engineering

Stock V816.0.5.0.TKHMIXM `vendor/bin/hw/android.hardware.thermal@2.0-service.qti`,
140088 bytes, SHA-256 `05031fcf68231360394b5dded8003eb13ce5ea5d1cf84f2e1063fe9e7b5ffcd2`.
Ghidra 12.2 decompilation of `_GLOBAL__sub_I_thermalConfig.cpp` (0x10ce68):
SoC 0x164 maps to a common vector allocated with 0xd8 bytes = three 0x48-byte
entries (CPU, `gpuss-0-usr`, `gpuss-1-usr`, 95000 thresholds), plus a four-entry
specific vector. **Xiaomi's Kona table has no SKIN entry**; the binary's "skin"
labels belong to other SoC tables. Stock Android therefore had no skin
temperature or headroom from this HAL either.

## Why no HAL

Android headroom uses SKIN sensors only. LineageOS
`hardware/qcom-caf/thermal-legacy-um` (07a34951c4a8, builds cleanly) would expose
only 95 °C junction thresholds, so status would effectively stay NONE while
adding a running root service and trip writes. A useful skin mapping would need
thresholds absent from both stock HAL and inspected sources; mi_thermald
configs are encrypted. Do not invent severity/headroom values, enable
thermal-engine, or revive `TARGET_USE_QTI_THERMAL_SERVICE` without a new
source of Xiaomi skin limits and paired throttling tests.

Unaffected: kernel/mi_thermald protection. Known consequence: JobScheduler
thermal deferral, ART thermal cutoff and app headroom APIs see NONE.

## Separate battery finding

The replacement-pack temperature lead is now measured in
[battery thermistor evidence](battery-thermistor-20261031.md).

Private scratch only: decompile and disassembly were not retained or published.
