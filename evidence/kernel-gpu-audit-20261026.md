# Kernel GPU and dependency audit

Observation: 2026-10-26. **source-checked, host-tested, build-tested, device-tested**
within the limits below. Target: Alioth's stock Adreno 650/KGSL stack. No donor
userspace driver, Turnip, MIUI optimization, overclock or thermal bypass.

## Source and verification scope

Repository: [kernel_xiaomi_sm8250](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250),
branch `aosp-17`. Eighteen final feature commits follow the
[previous verified series](kernel-techpack-eos-gem-20261026.md). Only unpublished
assistant changes were consolidated; prior authorship/history remain intact.
No warning suppression, configuration, Android system-source, UAPI or vendor
prebuilt changes. Regression fixtures remain outside the kernel repository.

| Selected build path | C-source checks |
| --- | ---: |
| drivers/gpu, including KGSL and DRM support | 113 |
| drivers/iommu | 14 |
| drivers/devfreq | 20 |
| drivers/dma-buf | 7 |
| drivers/staging/android/ion | 13 |
| techpack/display | 135 |
| drivers/thermal/devfreq_cooling | 1 |
| Total | 303 |

These are configured source checks, including compiled support for other
hardware, not 303 physically bound drivers. Runtime hardware coverage is Alioth.
Unselected configurations and external display/legacy GART hardware are not
certified by compilation.

## Real defects corrected

- Legacy DMA-BUF accounting now charges actual mapped size, matching destruction
  and avoiding counter imbalance when the userspace length differs. Existing
  64-bit footprints and gpu_mem_total emission behavior are preserved.
- User-address import requires the address to belong to the VMA returned by
  find_vma; an address in a hole cannot borrow the following DMA-BUF mapping.
  Existing GUP rejection and supported contained offsets remain.
- Command-queue state checks and marker exits now expose actual held-lock flow
  directly. No lock annotations or warning masks were used to hide diagnostics.
- GMU clock failures reverse-unwind acquired clocks; all startup states check
  regulator/clock results before IRQ/firmware access. Failed reset suspension
  propagates. Cold microcode initialization is marked complete only after success.
- ECATS busy timeout restores SCTLR; lock/IRQ ownership stays in the caller.
  Failed second capture-power acquisition releases the first reference.
- ION nested prefetch pointers retain userspace provenance and correct stride.
  Two unexported, unreferenced CMA entry points were removed; active heap, pool
  worker and shrinker operations remain.
- Typed DRM RAM/MMIO access, opaque compat tokens and little-endian table entries
  retain layouts and behavior. AUX diagnostics consume successful complete reads
  before printing, avoiding stale/uninitialized bytes. Linkage, value formats and
  kernel-doc contracts were corrected without changing bandwidth/governor policy.

## Host and build results

Extracted actual-function ASan/UBSan cases cover legacy accounting (12), VMA
selection (9), AUX diagnostic reads (7), GMU state/acquisition failures and retries,
boot initialization retry, ECATS lock/IRQ/register cleanup and capture-power
ownership. ION tests cover pointer stride, EFAULT, region limits and empty input.
DRM internal map layout matches 32/64-bit size/member offsets. Actual conditional
SRCU entry/exit tests balance six acquisitions and six releases.

Configured W=1 compilation passes. ARM64 sparse uses `CHECK="sparse --arch=arm64"`:
this installed checker otherwise retains host x86 macros despite `__aarch64__`.
A preprocessor fixture verified the target correction; no warning option was disabled.
The final source check retains exactly two reports in drm_drv.c:

- drm_dev_enter: different lock contexts for basic block.
- drm_dev_exit: unexpected unlock.

The existing API acquires SRCU only on successful entry, then releases through
exit. This old declaration/checker combination does not convey the conditional
pairing; source analysis and bounded actual-function tests show balanced paths.
No unconditional annotation or synthetic acquire/release was added. These reports
remain visible, so this is **not a zero-sparse-warning claim**.
[Kernel context-analysis documentation](https://docs.kernel.org/dev-tools/context-analysis.html)
explains conditional acquisition contracts; broad compiler machinery was not
backported merely to silence the old checker.

Strict cumulative checkpatch: zero errors, warnings or CHECKs; diff checks pass.
Normal production Image builds with zero compiler warnings/errors and unchanged
warning policy. WSL restarted during an earlier run: incomplete receipts were
rejected, malformed outputs preserved and regenerated, and final checks rerun.
No source or warning workaround was applied for damaged build artifacts.

Final Image SHA-256:
`fe68049ae394926bf4272614e1500288977fc81ece1ceff5fb400feb90f345cb`.

## Phone checks and restoration

Exact final Image/source temporarily booted with the installed ramdisk preserved.
SELinux enforcing, stock graphics libraries loaded in both ABIs, mi_thermald active.
All four installed GLES/Vulkan binaries match the unchanged stock build inputs.

- 816 ordinary app-domain native GPU/window checks: 32/64-bit, 60/120 Hz, repeated
  process launch/close; refresh preferences restored and probe app uninstalled.
- Five screen sleep/wake cycles; this does not certify every GMU hardware state.
- Six Qualcomm AVC/HEVC decode/AVC encode cycles, generated 640x360 content,
  300 frames; 19 PCM capture/playback cases, no microphone content saved.
- Fresh marked logs contain zero critical warning/fault/stall matches.

Original installed kernel restored, boot partition hash unchanged and exact task
staging removed. Windows ADB needed a server restart after the restoration
reboot; this audit does not claim that recurrent USB transport issue is fixed.
No partition flashed and no new ROM/recovery release declared.
Raw identifiers, network information, memory maps and logs remain private.

## Limits and open work

No live regulator/clock/ION allocation failure or ECATS timeout was forced on the
phone: these are host-tested failure paths. Fixtures do not replace kernel
sanitizers or concurrency stress. External display and legacy GART endpoints were
unavailable. This does not establish a general game/FPS improvement or resolve
all historical GPU page faults; stock userspace is unchanged.

The earlier whole-atomic-commit runtime-PM failure design remains open, as do
legacy late-LSM-generation limits in prior records. No speculative local return-
type redesign, stopped thermal protection or universal bug-free claim is included.

## Published feature commits

- [drm/msm: Charge legacy imports by their actual mapped size](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7b7aa5a0b67a20cc93342519f443d63bd0dff71b)
- [drm/msm: Require user addresses to belong to the matched VMA](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/763998ed98aec945bae14cd77731969b9a030fa5)
- [drm/msm: Make command queue lock flow explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3147a3022a5e9928c085e4bb70faa5df07a342c2)
- [drm/msm: Unwind failed GMU power acquisitions before startup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4f56eda10b09f49306e163710bf9525c221ae36a)
- [drm/msm: Mark GMU microcode initialized only after success](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8784fe939589170e0ef08aa1b9266d5dfda537b9)
- [PM / devfreq: Correct governor linkage and value contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3739b2c32e96fef3670897f4223e9ce11a9c5de7)
- [iommu/arm-smmu: Correct interface and diagnostic value contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/809f5a5f0f715bff410d7381e4e903b37cde1e68)
- [iommu/arm-smmu: Restore ECATS state on busy timeout](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/885a11b624c480b75406a67f84a8e2d5353b28f1)
- [iommu/arm-smmu: Balance failed capture interrupt power votes](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/26c4b9d4e3efdee57a112a5de4b2de40fea323df)
- [iommu: Make fast DMA allocation failure cleanup explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0a946a278f3ec4856b8d3ad3e441b978c475a9a0)
- [drm: Keep legacy RAM, MMIO and opaque token types distinct](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/72defc4b0fdc0129f7a4a46234fa4c9450bbbca4)
- [drm/dp: Consume MST transfer results before diagnostic output](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0992d106e990e7bb0b0cc15b6da04e22f40465b0)
- [drm: Preserve little-endian GART table entry types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/779841bef0ac3423523ba4f00677e4f2ac4c38d2)
- [drm: Remove unused mode and plane calculation state](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9271fb9107f663bc742b588d05a46d6f22a87e0b)
- [drm/bridge: Keep LT9611 implementation helpers private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/13325a55aa90eeff6e90fbdd376f6c8ad38d7207)
- [drm/iommu: Document graphics and mapping API contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4afca18f366b552da34cbab551c83f0c3ecd147a)
- [staging: ion: Correct allocator linkage and pointer contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/30378917707ee76c8068b0ea64be9edebf90a6f0)
- [staging: ion: Remove unreachable secure CMA entry points](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7b0c889d08add642d9022ac87288356030e65d29)
