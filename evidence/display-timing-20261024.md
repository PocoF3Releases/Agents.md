# Alioth display timing audit — October 24, 2026

**Follow-up:** the initial shorter 60 Hz budget below is superseded. GPU stress
review found a repeatable small deadline-miss increase; intermediate budgets did
not pass every check. The final profile restores the original 60 Hz scheduling
and retains only the verified 120 Hz latency improvement. See the follow-up below.

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

## Initial candidate — 60 Hz result superseded

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
- [Alioth work-duration scheduling](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/7c7229bdb805456900b817ebf023aab69bcb94a8)
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

## GPU and playback follow-up

Source review retained the common conditional property fragment: non-opted-in
devices keep the same four phase properties. On Alioth, all fixed global duration overrides are removed. Period-derived
defaults give the original 60 Hz app/SF offsets and budgets, while explicit
120 Hz overrides retain the 8.333 ms late SF budget and original early/GPU budgets. This sacrifices
the experimental 60 Hz latency gain rather than accepting a possible gaming
regression. No claim of a final 60 Hz latency improvement remains.

Tests used private, temporary normal-app APKs with SELinux enforcing. No games
were installed and the maintainer specified no particular title. The workloads
cover relevant rendering/presentation APIs, not every commercial game:

- Continuous fullscreen GLES rendering, shader compilation and error checks.
  Initial 60 Hz GPU deadline misses were 6/6 baseline versus 10/10 with the
  shorter 8.333 ms budget; frame-time tails also increased slightly. These
  small samples are not statistical proof of a universal regression, but were
  insufficient non-regression evidence for production. The 120 Hz runs recorded
  52 compositor late frames in both profiles; this is not a zero-jank claim.
- Intermediate 10 ms and 12.333 ms 60 Hz budgets were investigated. The former
  retained higher stress miss counts; the latter produced an extra queued frame
  in one repeated Settings scroll capture. Neither is included in the final source.
- Vulkan Android FIFO swapchains on both app ABIs exercised acquisition,
  command submission, per-image presentation semaphores and teardown. All
  baseline/initial candidate checks completed without API errors. The clear-only,
  queue-idle workload is a functional test, not a game-FPS benchmark.
- Local deterministic 1080p AVC clips at 24/30/60 fps and HEVC at 60 fps used the
  real Qualcomm OMX decoders. Both original profiles at both refresh rates
  rendered all 4,176 submitted frames with EOS and ordered timestamps. Codec
  frame-render callbacks are not proof of physical scanout or A/V synchronization.
  Steady playback compositor late-frame counts were essentially baseline-like
  (e.g. 60 fps AVC at 120 Hz: 9 versus 10; HEVC: 11 versus 11).

No HDR, protected/DRM video, streaming network behaviour, audio/video lip sync,
physical touch latency or sustained thermal/power certification is claimed.
Raw reports, sources, assets and traces remain private in
`~/evo/.repo/display-review-20261024`, outside production source repositories.

The final property set has seven entries: the WorkDuration factory flag and six
120 Hz overrides. A host fixture extracts the checkout's actual `constructOffsets`
body and passes under ASan/UBSan for 20/24/30/40/60 Hz defaults and the exact
120 Hz budgets. These are host configuration checks, not physical support for
extra panel modes. A pre-animation sample during a request for 120 Hz showed 20 Hz-derived
compositor budgets. Its physical panel state was not retained in that failed
check, so it does not prove a native 20 Hz panel mode or steady idle cadence.
Final timing checks sample active rendering and verify both requested modes.

The generated vendor property target rebuilt successfully and was checked for all
seven values, absence of fixed global budgets and absence of legacy phase conflicts.
The common implementation needed no additional changes. No production test files,
APK assets, clips, native probes or temporary diagnostics are part of the fix.

Final-configuration 60 Hz checks retained all rendered AVC/HEVC frames and completed
32/64-bit Vulkan presentation without errors. The later warm Settings capture
returned the original ~32.33 ms median; an initial cold capture still showed an
extra queued frame (~48 ms). This review does not establish a fix for every cold
transition or the originally reported general 60 Hz lag, and does not claim zero
jank. Keeping the original 60 Hz timing avoids shipping the shorter-budget trials
as a verified improvement.

## Final published fix and restoration

[Limit work-duration tuning to 120 Hz](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/7c7229bdb805456900b817ebf023aab69bcb94a8)
is published on `aosp-17`. The main branch contains only the display fix, without
local recovery-only commits. The common property-selection commit remains unchanged.
Both source worktrees are clean and the recovery patch preflight passes.

The final seven-property set was tested after a clean compositor restart.
On-device active 60 Hz offsets/durations exactly match the original configuration;
active 120 Hz values exactly match the prior tested 120 Hz candidate. Final GLES
runs and 32/64-bit Vulkan swapchain runs at both modes completed without API errors.
Ten further mode switches and two wake cycles matched requested modes, with the
compositor PID unchanged. These are bounded checks, not universal game compatibility.

Original timing properties and three refresh preferences were verified restored,
SELinux was enforcing and Android boot complete. Both owned diagnostic APKs and
copied on-device traces were removed after hash checks. No new tombstones or GPU
fault candidates were found in the final matrix's observation window. No firmware,
HAL, kernel, DTBO or full-ROM image was flashed. A production ROM rebuild remains
separate from these runtime-property and generated-vendor-property checks.

The exact final seven-property set also completed a fresh eight-play video matrix:
AVC 24/30/60 fps and HEVC 60 fps at both 60/120 Hz. Qualcomm hardware decoders
rendered **2,088 of 2,088 submitted frames**, with EOS, ordered timestamps and no
decoder error. Original properties/preferences were rechecked after this replay,
Android was booted/enforcing, and the reinstalled owned APK and traces were removed.

Current link targets consolidate the two original timing commits without changing
the final tree. Measurements retain their original October 24 scope.
