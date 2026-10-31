# Replacement-battery thermistor reading — 2026-10-31

**Device-tested; kernel fix installed.** Measurements were read-only root diagnostics. Installed October 28
user build, Redline f503c8d, Enforcing, charging near full at about 0.43 A. FG Gen4
selected `K11A_custom` (battery ID about 98.8 kΩ, authentic=1).

## Observation

`bms`/`battery` temperature moves with the board but at about one third of its
rate, so this is not a fixed offset or a stuck value (0.25 °C steps observed).

| State | quiet_therm °C | battery °C | Resistance implied by FG model | Stock NTC at board temp |
| --- | ---: | ---: | ---: | ---: |
| Rest, charging | 28.5 | 14.5 | 168 kΩ | 85 kΩ |
| Cooling | 32.0 | 16.2 | 154 kΩ | 72 kΩ |
| After 4-core load | 39.1 | 18.0 | 141 kΩ | 52 kΩ |

Model: every Alioth profile (FMT, GY, sun, custom) uses identical 100 kΩ,
β 4250, 100 kΩ pull-up thermistor coefficients. Inverting that model gives a
near-constant **~85 kΩ excess** in series with a stock-like NTC; a different NTC
alone would need β ≈ 1600. Assumes the pack is near quiet_therm temperature;
it is inferred, not a direct pack measurement.

## Consequence

Software JEITA (`qcom,sw-jeita-enable`, step-chg-jeita) and the health/thermal
`bms` zone consume this value. Extrapolated, a real 60 °C pack reads about
23.5 °C, so pack over-temperature current/voltage reduction is effectively
blind; at room temperature the 101–150 range caps FCC at 3536 mA. Board
thermistors and mi_thermald still respond. FG hardware hot/cold thresholds use
the same raw domain.

## Fix constraints

The FG coefficient encoding is proprietary (`BATT_THERM_COEFF_WORD`, generated
offline), so do not hand-edit coefficients. Every unidentified pack selects
`K11A_custom`, so a fitted per-pack resistance correction would mis-report
correctly built packs. A board-sensor floor only raises the reading, so it is
safe for those packs and needs no per-device setting or root; FG hardware
thresholds remain in the raw pack domain. Genuine replacement packs are no
longer manufactured. `smb1390_therm` reads about 405 °C but backs no thermal zone
on this charge-pump (BQ2597x) phone.

## Implemented fix — kernel 7d559e9

The maintainer confirmed a non-stock pack; genuine packs are no longer made, so
pack thermistor data is not relied on. [7d559e9](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7d559e98d4d948a94c2cc68cefa0e2a4ba5afb6b)
reports at least the hottest valid zone in `qcom,replacement-batt-temp-zones`
(alioth: `quiet_therm`, `charger_therm0`) only while the replacement fallback is
active. It feeds POWER_SUPPLY_PROP_TEMP (software JEITA, healthd), the `bms`
thermal zone and the soc-monitor low-temperature cutoff, and notifies the battery
supply on 1 °C moves. Identified profiles, FG internal algorithms, FG hardware
thresholds and `fake_temp` keep the pack reading. Zones outside -40..120 °C or
failing reads are skipped; `bms`/`battery` names are rejected.

Trade-off: charger IC heat can lower fast-charge current earlier; a warm board
can mask a colder pack only during use. Cold-ambient readings remain cold.

Validation: ROM-identical config, clang r563880c, full `W=1 KCFLAGS=-Werror`
Image and DTBs, checkpatch clean. The new DTBO differs from the ROM DTBO only by
this property. Temporary fastboot boot (Enforcing, taint 0): bms/battery and
healthd followed charger_therm0 (31–37 °C) instead of about 15 °C. Persistent
install: `boot_a` repacked with the unchanged ramdisk/Magisk
(ramdisk `9a64d35c…`), image `49b07284780c2e0b074af314a7db3c8ab6cee4a7b47aa86c626ee68aa9ba6c27`
read back; `dtbo_a` written with `c9fd94c99ac822b9e3f7aaede869a0b819116434f8a6fa5b93672f5c6f7586c5`
(first 462848 bytes) and read back. Normal reboot: `4.19.325-Redline-7d559e9-cip136`,
Enforcing, taint 0, root intact, battery 31.3 °C beside 31.0/31.3 °C board zones.
Originals kept privately on phone and host (`boot_a` `3481afa7…`, `dtbo_a` `3c53f2b4…`).
Not covered: charger FCC/FV votes (no debugfs on user build), long charging/thermal
sessions. The DTBO and kernel need the next ROM build to ship.

## Device-tree consumer recheck

Source/device read-only, after installation. Consumers of the floored value:
default healthd path (`android.hardware.health-service.alioth` only rescales
current), framework `config_shutdownBatteryTemperature` 680 (AOSP default),
software JEITA, the `bms`/`battery` thermal zones and mi_thermald, whose strings
show a `battery` zone lookup plus capacity/current/voltage reads. No device-tree
init/script writes battery temperature or `fake_temp`. The next ROM build takes
the DTBO from this kernel source (`BOARD_KERNEL_SEPARATED_DTBO`); inactive slot B
keeps the previous kernel/DTBO until an OTA replaces it.
