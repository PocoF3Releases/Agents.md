# Kernel build finalization

Superseded policy: the maintainer subsequently rejected warning relaxation.
See [strict restoration and consolidation](kernel-history-cleanup-20261026.md).

Observed **2026-10-26**. `source-checked`, `build-tested`, `host-tested`,
`device-tested` within the exact scope below. Continues the
[previous accepted batch](kernel-headers-pd-gpu-thermal-20261026.md).

## Current request and source

The maintainer explicitly requested finalization after the extended audit:
remove warning-as-error enforcement and provide a build-ready product. The
open-ended warning-only audit was stopped. This supersedes the earlier instruction
to make every strict warning gate green before preparing this build; it does not
mean every reported warning or every possible kernel bug was fixed.

Published `aosp-17`: [final branch head](kernel-history-map-20261026.json).
The normal Image and phone tests use [this production implementation](kernel-history-map-20261026.json). The only subsequent source delta is removal of fatal-warning flags
from six standalone test recipes; no kernel executable source, production build
rule or hardware configuration changed after the accepted build. The push is
fast-forward and the published ref was checked. System-side sources are unchanged.

- [thermal: Keep internal sensor and ADC state file-local](kernel-history-map-20261026.json)
- [thermal: tsens: Remove unused threshold intermediates](kernel-history-map-20261026.json)
- [drm: dsi: Include existing catalog operation declarations](kernel-history-map-20261026.json)
- [drm: dsi: Initialize remove status with an integer zero](kernel-history-map-20261026.json)
- [gpu: kgsl: Describe the context queue wait lock contract](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0700ad4ad92aee2e70d9c7d35b2f2917a51f49c0)
- [sched_domain: Annotate RCU pointers properly](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4ee3ce35e91db864e722e4daeed0be0561376079)
- [rcuwait: Annotate task_struct with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/306ee36b6823fa537346e14d9a68d63f81b93277)
- [tasks, sched/core: With a grace period after finish_task_switch(), remove unnecessary code](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c56cce401cfe01ce1e8d4cb413941ae6cf91c70f)
- [sched/core: Annotate curr pointer in rq with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/259064bb349449d7783025e4ea830ed1917068f6)
- [gpu: kgsl: Correct dispatcher parameter documentation](kernel-history-map-20261026.json)
- [gpu: adreno: Keep the A3xx protection table private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/48b61193671bcc485af6d608c9c60a771cff7cd6)
- [tasks, sched/core: RCUify the assignment of rq->curr](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/36ac625d89c65f1f30990c53f03d15cffee52548)
- [sched: trace: Match formats to native trace field types](kernel-history-map-20261026.json)
- [sched: walt: Keep trace window formatting private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c20164351ec724734136068bf53233b3cd8c5caa)
- [sched: Traverse domain links through the existing RCU accessor](kernel-history-map-20261026.json)
- [drm: dsi: Bound Xiaomi panel receive buffers](kernel-history-map-20261026.json)
- [drm: dsi: Validate and commit panel calibration updates atomically](kernel-history-map-20261026.json)
- [sched: Use address-only accessors for current-task comparisons](kernel-history-map-20261026.json)
- [sched: walt: Protect remote rotation task snapshots with RCU](kernel-history-map-20261026.json)
- [drm: dsi: Document the command stream region parameter](kernel-history-map-20261026.json)
- [kbuild: Keep production compiler warnings nonfatal](kernel-history-map-20261026.json)
- [arm64: configs: Regenerate Xiaomi warning policy](kernel-history-map-20261026.json)
- [tools: Keep standalone test compiler warnings nonfatal](kernel-history-map-20261026.json)

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

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
