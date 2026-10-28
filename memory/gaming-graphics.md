# Graphics, games and parked experiments

**No general game-performance fix or frame-generation port is accepted.** The
maintainer parked donor-driver, Turnip and game-setting experiments. This record
preserves results and avoids repeating unsupported approaches; it is not an
instruction to restart testing. Thermal protection stays enabled.

## Alioth versus OnePlus 9R

Local comparison: shipped SM8250 vendor libraries versus `~/oneplus9r/out/vendor`.
Alioth GLES identifies V@0502.0 (2021-10-04), donor V@0502.46 (2025-06-17).
Compiler versions EV031.32.02.16 / .17. Vulkan/GLES2/GSL/compiler executable
sections differ; EGL/GLES1/helper sections mostly match. Direct dependencies and
export-name sets match; extension-name strings match but are not runtime queries.
A650 GMU/SQE firmware matches; some ZAP artifacts differ.

This is a V502 maintenance donor, not proof of newer Vulkan support or a fixed
GPU fault. Matching ELF dependencies does not verify KGSL ioctls, linker
namespaces, rendering, thermals or FPS. Prior subjective improvement in a game
was not a controlled benchmark. No donor module is a required production fix.

Adreno 650 mainline support uses its own kernel/userspace stack; it does not make
an unrelated newer Adreno proprietary driver interchangeable with Alioth KGSL.
Keep actual loaded driver, firmware, rendering settings, cache state and scene
identical when comparing a newly authorized experiment. Shader compilation or a
loading screen alone cannot prove a recovery-policy success/failure.

## Myron Smart Frame Rate

Recorded myron EEA build OS3.0.302.0.WPMEUXM selects the Novatek dual-DPU backend:
`product/etc/device_features/myron.xml` has `support_dual_dpu=NT`.
Security Center `GameBoxVisionEnhanceUtils` → Joyose
`IGPUTunerInterface.setFrameInsertingOrSuperResolution` → `NovaTekEnhanceContext`
→ FrameMaster/Novatek display services. Native paths include
`setDualDPUMemcState`, `DualDpuHandler::handleGameMemc`, `/dev/vis_display_spidev`
and `odm/etc/dqe` MEMC/game configuration.

The character device and services were observed on Myron; matching integration
was absent from the inspected Alioth dump. This is not a device-tree-only port.
A separate software interpolator would require its own implementation and
performance/latency evaluation. A 120 FPS dashboard does not prove 120 game
simulation frames or independently measured interpolated output. The audit made
no ROM/driver/settings changes and did not measure on/off frame output.

## Turnip and other gaps

Endfield previously loaded stock `vulkan.adreno.so` despite package opt-in.
A shell-domain test succeeding did not prove app-domain selection. If explicitly
reopened, inspect GraphicsEnvironment and package lookup/visibility before
repeating force-queryable patches. No universal Unity/Unreal rootdir flag,
unlocked 120fps/native-resolution solution or game-specific crash cure was
established. Wi-Fi download observations also lacked a controlled LAN throughput
comparison; do not infer a radio-driver fix from WAN download speed alone.

Provenance: local `out/gpu-driver-comparison/REPORT.md` and
`out/myron-frame-audit/REPORT.md`, imported 2026-09-30. This import adds no fresh
device measurement. Source ownership is in the [map](../state/repositories.yaml).

## Production Adreno accounting — October 24

The stock V502.0 stack passed scoped app/native/Khronos checks on both ABIs.
[Validation](../state/validation.md#v-adreno-20261024) and the
[evidence record](../evidence/adreno-audit-20261024.md) separate the installed
baseline from a temporary patched-kernel boot and record remaining limitations.
No donor driver or general game/FPS fix was accepted.

Published kernel changes preserve 64-bit mapping footprints and backport Google's
`gpu_mem_total` emissions, retaining current DMA-BUF cleanup and upstream authorship.
Perfetto now receives real per-process/global memory counters; duplicate-import
accounting, large-footprint and final-global-removal regressions have targeted host fixtures.
[Source-only tools](../scripts/adreno-audit/README.md) stay outside ROM packages.
Vulkan remains 1.1: kernel timeline ioctls do not create a userspace Vulkan extension.
Sparse support remains disabled. Android thermal HAL telemetry is unavailable;
Xiaomi/kernel protection and the normal governor remain enabled.

## Display scheduling — October 24

The [Alioth timing audit](../evidence/display-timing-20261024.md) separates native
60/120 Hz panel support from SurfaceFlinger work budgets. The follow-up retains the original 60 Hz scheduling after GPU stress exposed
small repeatable differences; only the 120 Hz latency reduction remains.
Rendering and video checks are scoped, not a zero-jank or all-games guarantee.
No 240 Hz or speculative panel overclock was accepted.
The restored `~/references_code/android-t-qcom` and Qualcomm vendor snapshot are
reference material, not replacement Android 17 framework dependencies.

## Refresh-switch backlog — October 25

A continuous 120→60 Hz test reproduced a persistent UI buffer queue that paused
or restarted-app tests missed. Kona products now enable Android's existing multi-step
recovery together with its cumulative-delay threshold through the shared system
release configuration. This is normal-ROM policy, separate from recovery UI refresh. The normal 60 Hz budget
and published 120 Hz profile are retained. [Source, build, enforcing device tests
and restoration](../evidence/display-recovery-20261025.md) record the scoped
acceptance; the tested temporary framework was removed afterward. This addresses
transition backlog, not a new steady-state 60 Hz latency budget or every game.

## Cancelled Turnip evaluation — October 25

The newly authorized stable Mesa KGSL experiment did load Turnip in Endfield,
unlike the older package-opt-in attempt. Targeted ABI/LRZ checks passed, but game
frame delivery was substantially slower in the observed captures. Stock scene
loading reproduced 163 page faults; the available Turnip captures do not prove
a general fault cure. [Exact tests, limits and restoration](../evidence/turnip-evaluation-20261025.md).

The maintainer cancelled Turnip. Both stock Vulkan hashes and the empty temporary
autotune property were verified restored; final SELinux was enforcing. No ROM
driver/policy change or production fix was pushed. Do not restart Turnip or repeat
the declined OnePlus donor test without a new request. Adreno 650 is Mesa gen3,
not pre-gen3; do not force another GPU's LRZ profile.
## Kernel GPU audit — October 26

[GPU/dependency evidence](../evidence/kernel-gpu-audit-20261026.md) owns the
current feature links and bounded acceptance. Legacy imports charge actual mapped
size; DMA-BUF user-address classification rejects VMA holes. GMU acquisition
failures unwind and boot initialization remains retryable. SMMU diagnostic timeout
and power cleanup retain lock/register ownership. Typed DRM/ION interfaces preserve
layouts, active heap operations and governor/thermal policy.

Selected W=1 compilation and Image pass; two conditional-SRCU sparse reports remain
visible with balanced source/host paths, not suppressed. Stock graphics remain;
816 app-domain GPU/window checks, sleep/wake and audio/video regressions passed
under a temporary enforcing kernel. Original boot and settings restored. This is
not a new FPS tuning, driver experiment or general historical page-fault cure.

## Refresh-dependent luminance — October 28

[DisplayFeature evaluation](../evidence/displayfeature-evaluation-20261028.md)
records stock framework/native contracts and corrected physical comparisons.
Flat mode did not eliminate the 60/120 Hz luminance difference; no stock HAL or
calibration port was accepted. The published Alioth overlay holds adaptive refresh
at 120 Hz below Android brightness 55 using the existing blocking-zone policy.
Explicit 60 Hz caps and verified Battery Saver behavior remain; thermal protection
was retained. This avoids automatic pumping, not manual-mode optical mismatch.
Runtime-equivalent policy and resource checks passed; the production RRO needs the
next ROM build. Original device state and clean kernel sources/output were restored.

The follow-up compensation audit confirmed the installed stock calibration XML
and core Qualcomm color backend. Alioth's PCC-GABB threshold is zero; the inspected
brightness/CCBB paths do not select 60/120 calibration tables. Stock/current LUT
routines were compared before rejecting an unproven library swap. See the same
evidence record for exact contracts, panel-command comparison and remaining limits.
