# Replacement-battery thermistor reading — 2026-10-31

**Device-tested (read-only, root diagnostic), unresolved.** Installed October 28
user build, Redline f503c8d, Enforcing, charging near full at about 0.43 A. FG Gen4
selected `K11A_custom` (battery ID about 98.8 kΩ, authentic=1). No source, image
or setting change.

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
`K11A_custom`; a global profile correction would mis-report correctly built
packs. A correction must be opt-in per device, map both reported temperature and
hardware thresholds, and work without root. Physical pack replacement remains
the direct remedy. `smb1390_therm` reads about 405 °C but backs no thermal zone
on this charge-pump (BQ2597x) phone.
