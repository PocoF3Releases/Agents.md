# Kernel build finalization

Observed **2026-10-26**. `source-checked`, `build-tested`, `host-tested`,
`device-tested` within the exact scope below. Continues the
[previous accepted batch](kernel-headers-pd-gpu-thermal-20261026.md).

## Current request and source

The maintainer explicitly requested finalization after the extended audit:
remove warning-as-error enforcement and provide a build-ready product. The
open-ended warning-only audit was stopped. This supersedes the earlier instruction
to make every strict warning gate green before preparing this build; it does not
mean every reported warning or every possible kernel bug was fixed.

Published `aosp-17`: [final branch head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/428dc4e97f724e388347ecd400630bbb87fdb046).
The normal Image and phone tests use [this production implementation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/727bd1c2def4b20a0f0eb896fd3ce7da93b9d473). The only subsequent source delta is removal of fatal-warning flags
from six standalone test recipes; no kernel executable source, production build
rule or hardware configuration changed after the accepted build. The push is
fast-forward and the published ref was checked. System-side sources are unchanged.

- [thermal: Keep internal sensor and ADC state file-local](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/14ce8bd660d91368bb422d52e1e3ef281fe2cdf4)
- [thermal: tsens: Remove unused threshold intermediates](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a55ffe2b4546086234f11e30b69aab66c1cbafbf)
- [drm: dsi: Include existing catalog operation declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4c93edc6177a6eb28a9be242d94029d874d3593f)
- [drm: dsi: Initialize remove status with an integer zero](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/31613894087f4c9b6ce27b4b7672b4ee32b6fe6c)
- [gpu: kgsl: Describe the context queue wait lock contract](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2cd7bc2523cfa22a69121a49c3ef9ce7e91a1244)
- [sched_domain: Annotate RCU pointers properly](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/32f3373da14b2d9e3ea51deff4aea1d3e2c48c60)
- [rcuwait: Annotate task_struct with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/462744695205809d5d87f7666e43ef3a72690157)
- [tasks, sched/core: With a grace period after finish_task_switch(), remove unnecessary code](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4f54cba4039317c7300d35683eec203b6ba73a28)
- [sched/core: Annotate curr pointer in rq with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2a696b8142037ee48532fda986fe999d1822bb86)
- [gpu: kgsl: Correct dispatcher parameter documentation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a2b6d10f89367377f5d7f2bc7f5a86772b4a3a11)
- [gpu: adreno: Keep the A3xx protection table private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5730fe0fb2a822eabf60e8c4eb7970df283c2635)
- [tasks, sched/core: RCUify the assignment of rq->curr](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/411794600b95575fa94c34cab00cccc7cae3f892)
- [sched: trace: Match formats to native trace field types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/95cbdc1c9cab42b23fc9ff2036a4db00e1a8f623)
- [sched: walt: Keep trace window formatting private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6c6994a7237fcc0cb26c011b0ab3c2c3c616b4f4)
- [sched: Traverse domain links through the existing RCU accessor](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/043957b913c8540e2e5d1c99450c0ad0d52b9763)
- [drm: dsi: Bound Xiaomi panel receive buffers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/24c347785234e6e474afff2ac5764a8b34eea1f8)
- [drm: dsi: Validate and commit panel calibration updates atomically](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/33cfbb6530b8c9f420f1b5359f0c352f1daee78b)
- [sched: Use address-only accessors for current-task comparisons](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0c0c69e84c91b1a0d5fbd4b2651b80776c382422)
- [sched: walt: Protect remote rotation task snapshots with RCU](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4a64432f0e2b62dd8912abb673dd8666600ba84e)
- [drm: dsi: Document the command stream region parameter](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c81aeb13b82e9d02cec3e60ac5c3c26d28e5c109)
- [kbuild: Keep production compiler warnings nonfatal](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/26e5ace53c8a03298bcb7f1a972268791f452441)
- [arm64: configs: Regenerate Xiaomi warning policy](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/727bd1c2def4b20a0f0eb896fd3ce7da93b9d473)
- [tools: Keep standalone test compiler warnings nonfatal](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/428dc4e97f724e388347ecd400630bbb87fdb046)

## Warning policy and configuration

- Removed blanket/per-warning fatal enforcement from kernel, driver, Techpack and
  host-tool build rules. Corresponding warnings remain enabled. Removed the global
  `CC_WERROR` option and Qualcomm base-fragment selections.
- Regenerated all twelve Xiaomi defconfigs with `scripts/update_defconfig`, using
  the checkout Clang toolchain and `-j4` for configuration work. The generated delta
  is only removal of `CC_WERROR`. Resolved Alioth configuration likewise changes
  only that option; no thermal, clock, hardware or security settings change.
- Removed `-Werror` from standalone selftest/JPEG regression recipes too. Existing
  runtime assertions remain. Only capability/feature probes retain strict compiler
  checks, because accepting unsupported options would break feature detection;
  documentation/comments are not executable flags.
- **4,356 saved compile/link commands** from the final normal build contain zero
  warning-as-error flags. Final normal compiler output had no warnings or errors.
  The separate strict/sparse audit remains incomplete/failing and is not relabeled
  as passing because build policy changed. No further warning-only work is part of
  this finalization request without a new instruction.

## Retained reviewed repairs

Five human upstream RCU fixes retain their authorship, original messages/trailers
and upstream provenance: domain annotations, rcuwait annotation, removal of the
superseded task helper after its existing lifetime prerequisite, curr annotation
and publication assignments. Two context adaptations are documented; no new
hot-path release barrier was invented. Local traversal accessors and address-only
comparisons express the actual RCU contracts without force casts.

WALT rotation uses explicit RCU task snapshots during remote scans, carries CPU
IDs out of read sections and takes task references under the existing double-rq
lock. Selection thresholds, reservations and worker reference ownership remain.
No use-after-free was reproduced; implicit interrupt/RCU guarantees were not used
as a substitute for an explicit reader contract. Heuristic fields are not claimed
coherent. **40,000** source-extracted sanitizer scenarios preserve stable selection
and validate lock-boundary replacement/reference ownership.

Thermal globals/ADC list become file-local. Legacy TSENS drops only unused
computed state, retaining every tested register read/write, barrier, temperature
result and threshold-state update. **19,033** old/new comparisons pass ASan/UBSan.
The GPU queue helper's existing held-lock contract is annotated; no lock operations
change. Sparse does not enforce missing caller acquisition in the negative fixture,
so caller correctness remains separately reviewed. Its unbalanced-helper negative
control does diagnose. Dispatcher kernel-doc and private A3xx linkage are corrected.

DSI implementations include existing catalog declarations; the accidental imaginary
zero initializer becomes integer zero. Trace formats match stored native types;
trace field layouts and scheduling policy remain unchanged.

Panel reads reject zero/oversized lengths and missing command descriptors before
I/O. Calibration validates indices and payloads, stages gamma bytes, attempts key
cleanup after a successful enable on error paths, and commits only after all reads
and cleanup succeed. Failures leave the table untouched and completion false.
Valid byte arithmetic and command order remain. No inactive feature, calibration
value or panel timing was enabled/changed. Exact-source sanitizer fixtures cover
all command/read failure positions and stale completion; **65,536** arithmetic
cases and **56** common-reader cases pass. Host sequence checks are not hardware
timing measurements or inactive-panel certification.

## Build and phone acceptance

- Final normal Alioth Image: **PASS**, checkout Clang 21, `-j8`; no installclean or
  ROM rebuild was launched. Modules/DTBs and fresh header install/check: **PASS**.
- Temporary boot of the accepted Image with original rooted ramdisk: **PASS**.
  Runtime kernel identity matched the built production revision. SELinux remained
  **Enforcing**; TSENS/LMH and `mi_thermald` remained active. Thermal protection and
  CPU isolation were not disabled.
- Native task-exit/affinity probe: **1,024 children, zero failures** across eight
  workers. Actual CPU coverage mask was `0x6f`; this is not all-core certification.
  The baseline probe initially wrongly assumed online CPUs were never isolated.
  Live isolation plus the scheduler's explicit isolated-target rejection explained
  that test assumption; the final probe respects isolation and reports skips/retries.
- GPU app checks at confirmed physical 60/120 Hz: 32/64-bit ordinary-app processes,
  three runs per ABI/mode, **816 checks passed**. A keyguard-mode setup attempt was
  rejected without counting results; dismissing the boot keyguard established the
  correct display precondition. Actual modes were checked before/after, with saved
  120/120 settings and unset preferred mode restored. No exact FPS claim.
- Fresh post-marker logs showed no new BUG/WARNING, call trace, RCU stall, GPU/SMMU
  fault or CFI-failure signature during accepted tests. This is bounded regression
  evidence, not proof that every possible bug is absent.
- Test APK, native probes and owned phone staging files were removed. The original
  installed kernel and unchanged boot partition hash were verified after reboot.
  The existing original-kernel shutdown observer/narrow SPU live rule were restored
  only for the current boot; `initcall_debug` is N. No partition was flashed and no
  persistent diagnostic autoload was added.

The source is prepared for the maintainer's normal ROM rebuild. A new full ROM OTA
was not built or installed by this finalization. The intermittent shutdown report
and remaining broad static-analysis findings are not declared universally resolved.
Private receipts remain under `~/evo/.repo/kernel-next-audit-20261026` and
`~/evo/.repo/kernel-finalization-20261026`; raw device logs/identifiers are not published.
