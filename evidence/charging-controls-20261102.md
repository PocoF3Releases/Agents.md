# Charging control audit — 2026-11-02

## Published input-validation correction

[1846f92](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1846f927ad7ca1e32d9b2c478b667de17d95791e),
`power: supply: qcom: Reject unrepresentable restricted currents`.
One guard in `drivers/power/supply/qcom/battery.c`, independent of fast-charge
policy or bypass proposals. The source parent is
[7285847](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7285847f4a2af70e52e7b41a22485307d6a018c9).

**Source-checked:** `restrict_cur_store` parses `unsigned long`, then assigns an
`int restricted_current` and passes that integer to `vote`. On arm64,
2147483648 narrows to a negative value; 4294967296 becomes zero. The old write
reports success and retains the changed value, even when restriction is currently
disabled and can be enabled later. Negative FCC callback inputs are ignored;
this is not a faithful application of the requested current.

The new `val > INT_MAX` check rejects unrepresentable values before state or
votes change. Valid 0 through INT_MAX and existing syntax-error behavior are
unchanged. This is a representability bound, not a new hardware current ceiling.
No claim of unprivileged exploitability or observed hardware damage is made.
A bounded upstream search found the legacy implementation still unbounded;
a newer, differently structured QTI charger implementation was not transplanted.
Original history/authorship is unchanged; this is a new independent correction.

## Verification

**Host-tested:** actual kernel parser and store bodies, mocked class/vote
transport, Clang Werror plus ASan/UBSan. Thirty-two executions per version,
covering valid values, unsigned/signed boundaries, syntax errors and enabled/
disabled restriction. Old code fails eight out-of-range executions; fixed code
passes all 32. Explicit state/vote assertions detect narrowing; sanitizers alone
would not prove this implementation-defined conversion is wrong. No malformed
current was written to the old phone kernel.

**Build-tested:** affected object W=1/Werror and Sparse pass without diagnostics.
Full production-config Image/modules/DTBs pass W=1 with compiler Werror.
Twelve unchanged kernel-doc diagnostics in tracing remain; no warning flags or
checks were weakened. Strict code-hunk checkpatch has zero findings. The legacy
full-commit checker flags the required Codex co-author trailer as nonstandard;
the trailer is retained and GitHub recognizes both authors.

Configuration SHA-256 remains
`6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`.
Toolchain remains Clang r563880c. No system/device-tree source, defconfig, thermal
threshold, charging voter, debug mode or SELinux change accompanies this fix.

**Device-tested and installed:** temporary boot passed before active-slot B
installation. Running version is `4.19.325-Redline-1846f92-cip136`; root ramdisk
contents and boot metadata were preserved using the existing Magisk boot tool.
Installed boot-partition SHA-256 equals the tested image:
`8ff5bf67adfb3b8c5328f5732cc7eea8bae724c6b039696698c4762e95e16e22`.

- Eight invalid writes return EINVAL and leave the stored current unchanged.
- A same-value valid write succeeds. Limit remains 1000000 µA, restriction off.
  Large but representable valid values were tested only on the host, not hardware.
- The same rejection test passes after persistent installation and reboot.
- All 19 bounded PCM capture/playback cases pass. Battery is present with Good
  health; the four earlier F2FS statistics still return numeric values.
- SELinux stays Enforcing, taint 0 and mi_thermald runs. Audioserver/thermal PIDs
  are unchanged across the input test; no new critical kernel match occurs in
  that marked window. Task phone staging is removed; no wipe/settings reset.

Private build/host/device receipts and local boot backups:
`~/evo/.repo/charging-audit-20261102/restricted-current` and the preceding
`~/evo/.repo/platform-recheck-20261102/test.img`. No private images, raw logs or
tests enter the production commit.

## Fast-charge policy findings remain separate

Both `usbpd-pm` and `cp-qc30` are bound on Alioth. The board uses standalone
BQ2597x, not the generic Qualcomm charge-pump topology. PC USB remains 5 V,
PD inactive, pump disabled; these observations validate neither PPS nor QC
active charging. Bypass remains disabled and no new control is exposed.

Zero FCC from USER is already reflected in the night-charge getter. Stronger
independent cases are `RESTRICT_CHG_VOTER` with zero current and zero
`BATT_PROFILE_VOTER` through `constant_charge_current_max`. The generic callback
looks up `charge_pump_master`/`cp_slave` and does not directly disable BQ2597x.

- **PPS:** an active tuning pass retains positive static limits when FCC becomes
  zero. The private late guard preserves all existing fault/taper dispositions
  and returns before the next tuning request. Its 40,965 extracted-tail host
  cases pass, and both baseline/candidate compile under the exact strict target
  flags. It remains unpublished: caller/EXIT latency, flash-entry voting races
  and active adapter behavior are not device-verified.
- **QC:** zero FCC creates a zero numeric bus target, but current 1–310 mA can
  cause no downward pulse and a successful return while the pump stays enabled.
  A TUNE-only guard would allow repeated re-entry through SW_LOOP. A complete
  correction needs signed snapshots, entry/intermediate/recovery gates and
  preserved fatal-fault priority, with full transition regressions and a real
  QC charger. No QC policy candidate was installed or published.
- A missing FCC votable and unsigned error wrapping are plausible defensive
  cases; their occurrence during a normally initialized charging session is
  not established. Do not present them as an observed phone failure.

Independent adversarial review confirmed these distinctions. Do not infer true
charging bypass or complete fast-charge protection from the bounded input fix.
The [broader compatibility plan](kernel-contract-plan-20261102.md) remains open;
the paused touch boundary task remains skipped.
