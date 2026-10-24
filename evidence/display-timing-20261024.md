# Alioth display timing audit — October 24, 2026

Scope: installed Android 17 user build, Adreno 650 stock V502.0 stack and
kernel b8fc2fc50a5c build 2. Device tests used temporary SurfaceFlinger properties
with SELinux enforcing. No new kernel, DTBO, HAL or complete ROM was flashed.
Raw traces and device dumps remain private under `~/evo/.repo/display-audit-20261024`.

## Panel and source findings

The live K11A 38/08/0A panel node matches the clock, porches and transfer budgets
in the [official Xiaomi panel source](https://github.com/MiCode/kernel_devicetree/blob/alioth-r-oss/qcom/dsi-panel-k11a-38-08-0a-dsc-cmd.dtsi).
Both modes use four 1.1 Gbit/s DSI lanes and DSC 8 bpp. Native modes are 60 and
120 Hz. The [official product specification](https://www.po.co/global/product/poco-f3/)
distinguishes 120 Hz display refresh from 360 Hz touch sampling.
Full-resolution 240 Hz would require 4.977 Gbit/s for active pixels alone,
exceeding the current 4.4 Gbit/s link before overhead. No validated 240 Hz
initialization/calibration exists; historical 90 Hz support was removed for
colour differences. No speculative panel mode or clock change was accepted.

The restored `~/references_code/android-t-qcom` and
`~/references_code/LA.UM.8.12.r1-11900-sm8250.0` were inspected narrowly.
Android 17 already has WorkDuration scheduling; no bulk legacy framework import
is necessary. The generic Qualcomm panel references are not Alioth panel evidence.

## Measured candidate

Use WorkDuration late SF budget 8.333 ms, retaining the original early/GPU
budgets: 15.667 ms at 60 Hz and 12.333 ms at 120 Hz. App budgets remain
16.667/11.667 ms. The common phase-offset properties must be excluded when
this device selects work durations; SurfaceFlinger validates that they do not
coexist. Other common-tree devices retain their original phase-offset properties.

Paired Settings scroll runs used identical alternating 450 ms swipes and balanced
60/120/120/60 order, followed by a fresh baseline using the same flow.

| Mode | Original median / p95 | Candidate median / p95 |
| --- | --- | --- |
| 60 Hz | 32.33 / 32.37–32.46 ms | 25.00 / 25.04–25.27 ms |
| 120 Hz | 24.00–24.02 / 32.27–32.28 ms | 20.00 / 28.25–28.27 ms |

These are app intended-vsync-to-associated-presentation intervals from Perfetto
FrameTimeline, **not physical touch-to-photon latency**. Settings samples per run
were 263–323 at 60 Hz and 628–630 at 120 Hz; fresh baseline 278–323 and 627–630.
The 60 Hz candidate had no Settings late frames; 120 Hz had one per run.
One candidate 60 Hz capture included SystemUI activity; the second clean run
reproduced the gain. Occasional dropped frames remain, including baseline runs.

Launcher/Settings transitions were tested twice with the candidate. No
SurfaceFlinger late-present frame was recorded in either candidate transition
pass, but app/launcher deadline or scheduling misses remain. Transition medians
were essentially baseline-like; do not claim a general animation-speed fix.
Uniformly shortening early/GPU budgets and a middle-budget variant regressed
launcher tails or scheduling and were rejected despite faster scrolling.

Ten forced 60/120 mode transitions and two sleep/wake cycles passed with the
candidate: active mode matched the request, compositor PID remained unchanged,
and SELinux remained enforcing. All temporary properties and refresh preferences
were restored afterward.

## Limits

This validates scoped scrolling, transitions and refresh lifecycle behaviour on
one Alioth panel/build. It does not establish every app/game, power consumption,
physical scanout/input latency or universal absence of jank. A future full ROM
rebuild is separate from the temporary runtime-property acceptance.

## Published implementation and integration checks

- [Common property selection](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/802d6e421bec85f51727c8b1f6d0a1543f65601e)
  preserves all four original phase values by default.
- [Alioth work-duration scheduling](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/42d2f3cedcc0acab152dc5f43604711aa058d89c)
  selects the tested budgets. Both are on `aosp-17`; no recovery-only commits
  were pushed to the ROM branches.

`lineage_alioth-cp2a-user` generated vendor/build.prop successfully with `m -j6`
and the explicit output target. The generated file matches every candidate
property and contains no legacy high-FPS phase properties. Make selection checks
passed for unset/false/true opt-in; unset/false preserve the original phase values.
Git whitespace checks and the existing recovery patch preflight passed.
No production test files or temporary diagnostics were added to either device tree.

A fresh transition baseline confirmed similar latency tails: at 120 Hz, launcher
p95 was 32.28 ms for baseline and candidate; Settings p95 was 40.49/40.45 ms.
At 60 Hz launcher p95 was 65.36 ms baseline versus 48.84 ms candidate in this
repeat; earlier baseline was 48.90 ms, showing run variance. The repeat candidate
still had eight and six launcher late frames at 60/120 Hz; this is not a zero-jank
claim. All 14 temporary properties, three refresh preferences and SELinux enforcing
were verified restored; copied audit traces were removed from the phone.
