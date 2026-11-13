# Kernel correctness follow-up — 2026-11-02

`source-checked`, `host-tested`, `build-tested`, `device-tested`; **five local findings fixed**, installed and subsequently published with the user's explicit authorization. Continues the [first two IOMMU fixes](kernel-correctness-20261102.md), retaining their exact upstream authorship. The original at-most-five-finding scope is now filled; this is not a claim that every kernel bug or validation limitation has disappeared.

## Source identity

Baseline remains aosp-17 3d374cb (historical `3d374cb35915256513a2dbccb921d9fbf1259c4b`). Published head: aosp-17 1cfe734 (historical `1cfe734008290c228abf15a8f8ae67a03d52fc1e`). The published tree retains exactly the tested C-file bytes. Tested baseline-to-final patch SHA-256: `422ea99ccfeadabb24113d4f0a589dfd25b3d9aabe6aa79120da63f70c5afc0c`.

Only three C files change: `drivers/iommu/iommu.c`, `drivers/gpu/msm/kgsl.c`, `drivers/iommu/dma-mapping-fast.c`: **14 insertions, 4 deletions**. Five independent private patches replay onto baseline files and reproduce all three worktree files byte-for-byte. No source change preceded its old-code counterexample. No ABI/declaration/config/security/thermal or system-side source change, warning suppression, documentation-only kernel patch, new boot parameter or production debugging flag was introduced.

## Additional demonstrated findings

### F3 — KGSL reports success after worker creation fails

**Reachability:** `CONFIG_QCOM_KGSL=y` runs `kgsl_core_init()`. Earlier registration and workqueue allocations succeed, leaving `result == 0`, but `kthread_run()` returns `ERR_PTR(-ENOMEM)` or another thread-creation error such as `-EAGAIN`. Kernel thread creation can fail allocating the task/resources; this requires no invalid ioctl or off-configuration GPU.

**Invariant/consequence:** an initializer which tears its resources down after a required worker fails must return the failure. The old error branch jumps to cleanup without updating `result`, returning zero and marking failed initialization successful. This is a false-success error-propagation defect, not a claim that returning an error alone prevents every independent built-in initcall from running.

**Alternatives checked:** `kthread_run()` does not assign `result`; successful earlier calls leave it zero. `kgsl_core_exit()` does not change the local return variable. No replacement worker is created on this path. Set only `result = PTR_ERR(kgsl_driver.worker_thread)` before the existing log and error jump. Successful startup and the original error value are preserved.

**Regression:** source-extracted actual init/exit functions, inject two thread-creation error values after successful preceding steps and assert the exact negative return. Both cases fail in old code and pass with only F3; F4's tests still fail in that independent variant.

### F4 — KGSL loses ownership of its worker on teardown

**Reachability:** worker creation succeeds, then `kgsl_drawobjs_cache_init()` fails allocating a cache. The same exit function also serves core teardown. Current Alioth is built-in; the concrete production failure is an unreaped live worker after late initialization failure, not an observed module-unload exploit.

**Invariant/consequence:** every created worker must be drained and stopped while resources used by its callbacks remain alive. The old exit destroys workqueues and caches but never flushes or stops `kgsl_driver.worker_thread`. The worker remains alive. The dispatcher producer has its own close/flush path; the fix does not modify normal scheduling or queue submission.

**Alternatives checked:** the worker loop exits only when stopped, and no other call site stops this task. The global worker object is embedded, so `kthread_destroy_worker()` must not be used because it frees the worker allocation. Copy the existing target-tree teardown sequence from `kernel/kthread.c`: flush the embedded worker, stop its valid task, then clear the task pointer. Do this before existing workqueue destruction. NULL/error handles acquired on earlier failure paths are never flushed or stopped. No active-path producer, priority, frequency or thermal policy changes.

**Regression:** the actual init/exit functions run against finite ownership stubs; cover failures before the task exists, task creation failure, late cache failure, normal init/exit, optional memfree-list allocation failure, pending-work drain ordering and two task-creation errnos. Old GPU suite: **8 failures / 20 cases**; F3-only: 6; F4-only: 2; combined and actual worktree: **0**. Flush/stop order is modeled by state/counters, not real callbacks or concurrent scheduling.

### F5 — Failed atomic pool permits sleeping fast-DMA allocation

**Reachability:** `CONFIG_ARM64_DMA_USE_IOMMU=y`, `CONFIG_IOMMU_IO_PGTABLE_FAST=y`, `CONFIG_IPA3=y`. Kona's `ipa_smmu_ap` is `fastmap` and DMA-coherent; `ipa_smmu_ap_cb_probe()` installs that device as `ipa3_ctx->pdev`. WAN GSI channel setup selects `GFP_ATOMIC`; `ipa_gsi_setup_event_ring()` passes it to `dma_alloc_coherent()`. Header and routing-table code supplies additional atomic DMA callers. The fast allocator's `atomic_pool_init()` can return `-ENOMEM` at arch init, leaving its pool NULL while boot/probing continues. DMA ops setup does not require that pool to exist.

**Invariant/consequence:** a nonblocking DMA request must never enter sleeping page-array/remap paths. The old condition `atomic_pool && !gfpflags_allow_blocking(gfp)` bypasses atomic handling when the pool is absent. It then reaches `__fast_smmu_alloc_pages()`, whose pointer-array `kzalloc()` uses `GFP_KERNEL`, or the generic contiguous/remap path. Thus the caller's atomic allocation constraint can be violated, with possible sleep-in-atomic warnings or locking/progress failure. No phone occurrence is asserted.

**Alternatives checked:** this pool is distinct from the ARM64 allocator's own pool; failure of its initcall does not stop boot or fastmap setup. The explicit return on a missing pool is safer than introducing a new successful allocation type on an untested edge path. Preserve every pool-present atomic branch and every blocking branch; return NULL with the already-set DMA error handle when the nonblocking pool is unavailable. No fabricated per-call missing-domain check was added.

**Regression:** extract actual dispatcher, atomic allocator, page-array allocator and contiguous helper. Vary pool presence, coherent/noncoherent route, `GFP_KERNEL`/`GFP_ATOMIC`/`GFP_NOWAIT`, contiguous attribute, one/two-page sizes and backing-allocation failure. Track entry into blocking primitives and returned handles. Old: **32 failures / 96 cases**; fixed and actual worktree: **0**. Tests prove dispatch/context/handle behavior. They do not execute `fast_smmu_free()`, real IOVA/map/remap failures, live memory pressure or hardware DMA.

## Provenance and independent patch boundaries

Published as five independent commits; no history rewrite or force-push:

| Finding | Published fix | Authorship |
| --- | --- | --- |
| F1 | iommu: Remove duplicate ida_free in iommu_group_alloc (historical `38c65b4986b8457ce101f1e4e86f808e1444e974`) | Yuan Can; upstream backport |
| F2 | iommu: Fix error unwind in iommu_group_alloc() (historical `7e1964203e1ab2b78e13c01bcae3fa9420990ecf`) | Jason Gunthorpe; unchanged upstream fix |
| F3 | msm: kgsl: Return worker creation failures (historical `3bf6863fd0d30c149077134abe5533e3ad213680`) | Local fix |
| F4 | msm: kgsl: Stop the owned worker before core teardown (historical `631598f0a1b10c711b052777e1955f81c4f64b76`) | Local fix |
| F5 | iommu: fast: Reject atomic allocations without a pool (historical `1cfe734008290c228abf15a8f8ae67a03d52fc1e`) | Local fix |

F1/F2 retain Yuan Can and Jason Gunthorpe's upstream patch metadata as recorded in the first audit. For F3–F5, matching exact upstream/vendor fixes were searched but not established; they remain local fixes, not falsely attributed human backports. The existing Qualcomm implementation and its original authorship are untouched. F4 follows the existing kernel helper's flush/stop semantics without freeing the embedded worker. No upstream architecture replacement or wholesale new driver was imported.

## Verification

- **130 actual-worktree host cases pass:** IOMMU 14, GPU 20, fast DMA 96. Each suite retains pinned baseline failures, independently applied candidates and a separate actual-worktree variant. Host Clang `-Wall -Wextra -Werror`, ASan and UBSan pass with empty sanitizer stderr. These are finite source-extracted models.
- **Complete incremental Image/modules/DTBs build passes:** checkout Android Clang 21.0.0 r563880c, `-j4`, `W=1`, `KCFLAGS=-Werror`, existing `CONFIG_CC_WERROR=y`. There are zero compiler diagnostics. Twelve kernel-doc parameter/member warnings occurred in this incremental invocation; earlier affected-directory checks had eleven. Neither count is a whole-tree documentation recount. No doc-only fixes or suppressions were added.
- Config SHA-256 remains `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`. Existing ROM output and the previous strict output are preserved; work ran in the private audit output, without installclean.
- **Unlimited ARM64 Sparse**, matching the historical architecture/limit settings: `C=2 CHECK="sparse --arch=arm64 -fmax-warnings=unlimited"` completes **59 translation units** across GPU, IOMMU, the ARM64 DMA setup caller and preparation units, with **zero diagnostics**. This does not clear the historical 2,954-warning whole-kernel backlog.
- **Database-backed Smatch** runs the same 59-unit scope with no analyzer failures. The earlier `kgsl_core_init()` missing-error report is gone. Other reports remain; none was suppressed to obtain a count. Initial cross-function SQL coverage and tool pin remain as recorded in the first audit.
- **Coccinelle** report-only `kfree` checks complete for GPU and IOMMU. The existing speed-bin pointer-value report remains, without demonstrated dereference-after-free. Strict checkpatch and `git diff --check` pass with zero findings.
- Fresh read-only GPT-6.1-Sol adversarial review found no Required/Critical defect in F3–F5. It specifically verified error propagation, embedded-worker ownership/order and preservation of pool-backed/blocking DMA branches. Its test limitations are retained here, not described as runtime acceptance.

## Linked build artifacts

| Artifact | SHA-256 |
| --- | --- |
| `arch/arm64/boot/Image` (55,586,840 bytes) | `f997de4c0f8578a7b1309443513b4cbc40152b579697d4b69c75b22ba76550be` |
| `vmlinux` | `6780b60a57ff897a475d188ffbebb519a5c0a094e616f93d8edc3831a10d9ee3` |
| `kona.dtb` | `0acfbc2011af41aad96c38aa753499db1a3b8c227a4244c145afac79dd463ef3` |
| `alioth-sm8250-overlay.dtbo` | `926d1bc64e28d035593c6d115dd7d52c65d900d6403973fe692145e8087ac82b` |

The kernel was later packaged and flashed with explicit authorization as recorded below; this is not a complete ROM release. Five separate patches, source baselines, per-check commands/results and hashes remain at `~/evo/.repo/kernel-correctness-20261102/` (`continuation/` for this follow-up).

## Exact-image phone acceptance

The user subsequently authorized flashing the connected phone for final rechecks. This superseded the earlier device/flash restriction. After these tests, the user separately authorized committing and pushing the five fixes; publication did not rewrite existing history.

- Active **slot B** was checked before writing. Its original boot partition was read into a private host backup and device/host SHA-256 matched. Only `boot_b` was written; no command wrote the other slot, DTBO, vendor_boot or user data.
- Repacked the strict-built raw Image using the installed Magisk boot tooling and the phone's original boot image. Extracted kernel SHA-256 equals the linked Image above; decompressed ramdisk SHA-256 is unchanged: `f900d3b07a7554f287249c80849a7fe6cf224a8bf8a5f5c12f17256427b504ab`.
- Installed boot image/partition SHA-256: `c18cec755e4c7ef079a6f27b0aeba0070a84792b89305f16a70a18f44554f6b4`. Hash verified before reboot and after both subsequent boots. Runtime release: `4.19.325-Redline-3d374cb-dirty-cip136`; `dirty` identifies the then-uncommitted build. Its C-file bytes match the subsequently published five-commit tree; the phone was not rebuilt or reflashed merely to change Git/version metadata.
- `/proc/config.gz` SHA-256 matches the production config above exactly. Both boots complete normally with SELinux **Enforcing**, taint **0**, CPUs **0–7** online, battery **Good**, and thermal/audio services running. No diagnostic configuration, thermal override or live SELinux policy was used.
- **Six ordinary-app GPU runs**, three per actual arm64/arm app process, each pass **62 native + six window checks**. The installed APK hash and `app_process64`/`app_process32` identity are verified; each process runs in its ordinary `untrusted_app` domain. This is 408 functional checks, not FPS/game certification.
- **19 PCM cases** pass: MIC/CAMCORDER/VOICE_RECOGNITION/VOICE_COMMUNICATION capture at 16/48 kHz with repeated stop/release, plus three playback cycles. Captured samples are not retained. This is not headset/VoIP endpoint or subjective sound-quality certification.
- Owned **4 MiB** storage write/copy/compare passes; **eight of eight** initial network pings return. **Three** sleep/wake cycles return Awake. Connectivity returns after the final normal reboot, and Windows ADB reconnects without a permanent USB workaround.
- Initial, post-functional and post-reboot dmesg checks contain no new critical BUG/panic/lock/CFI/UBSan/atomic-sleep/GPU/SMMU-fault signature. These are bounded log-signature checks, not a claim that every kernel message is classified or every race is excluded.
- Known test APKs and owned device staging are removed. Private host boot backups, package hashes and raw logs remain under the audit directory. No user file, saved audio setting or partition beyond active boot was changed by the tests.

The first GPU install timed out at Play Protect verification, not kernel execution. The prior ADB-only verifier value was temporarily changed for test installation and then restored. The user subsequently explicitly requested **Disable Google Play Protect**: selected permanent Disable rather than Pause in the official UI, verified both scanning and unknown-app submission switches OFF, and set ADB install verification OFF. The same off states were verified after reboot. This is a requested device preference, not a ROM/kernel change or a requirement for future testing. [Google's control documentation](https://support.google.com/googleplay/answer/2812853?hl=en).

## Remaining reports and acceptance limits

All 32 earlier IOMMU Smatch rows have an explicit private disposition:

- Three kobject-initialization reports: actual initializer establishes the release type before its registration failure; analyzer modeling limitation.
- Fourteen possible-ERR_PTR DMA reports: a valid initialized domain/cookie is required before fast ops installation and throughout driver DMA lifetime. No in-contract counterexample was demonstrated; teardown-client correctness is not universally certified.
- Three GFP reports: generic DMA caller takes its blocking branch first; the fast helper's missing-pool exception is fixed by F5.
- Three idempotent/defensive/ownership branches: already-initialized domain returns success; group NULL check is redundant but safe; foreign/absent fwspec rejection owns nothing to unwind.
- Two IRQ-mismatch reports require malformed/mismatched DT/hardware description rather than proven Alioth preconditions. Seven optional debugfs reports concern partial optional instrumentation/error detection; they were not promoted into production fixes merely to clear diagnostics. These are retained follow-ups, not a claim that their code is ideal.

GPU timestamp reports were checked against context-ID allocation below `KGSL_MEMSTORE_MAX`, fixed aligned memstore fields and context references retained by event users; no valid-context failure was demonstrated. FastRPC map/output construction and fds/maps initialization likewise provide important caller invariants; no speculative NULL-guard patch was added. This review does not prove absence of every race or external misuse.

**Still unverified:** forced real GPU-worker teardown/failure injection, live pool-init/OOM behavior, exhaustive DMA allocate/free/unwind and concurrency, whole-kernel/new-configuration correctness. Normal-path exact-image device acceptance above closes the earlier no-device-test gap; it does not turn finite host error-path models into hardware fault-injection proof. These limits are retained rather than masked by production debug/configuration changes. The five source fixes are now pushed to `aosp-17`; the remote head was verified. Original upstream authorship is preserved, and GitHub recognizes Codex on the four commits carrying its trailer. This publication does not certify the unchanged baseline findings or the fault-injection limitations above.

## Cross-repository integration

After the user's integration/push request, checked all **43 GitHub build inputs**
selected from the two PocoF3Releases organizations, the **GitLab camera input**,
and the canonical recovery local-manifest repository against their published
selected heads. Forty GitHub inputs and the GitLab input match directly. For the
other three, replaying the approved four recovery patches on current published
bases reproduces the actual frameworks/base, Alioth and common-device trees
exactly. Equivalent device commits have different IDs because of patch placement;
no source implementation is missing, so no rebase or synthetic source fix was made.

The deployed recovery XML, runner, series and four patches match the canonical
published repository byte-for-byte. Actual runner preflight reports zero pending
patches in all three projects. A single generated `.pyc` was preserved privately
outside the Alioth Git checkout to clear its dirty-worktree rejection; tracked
source files and user data were unchanged.

The kernel diff has no UAPI, DT, config, ABI-documentation, Makefile or version-script
changes. `scripts/update_defconfig --check -j4 alioth` passes. The existing ROM kernel
`.config` and strict-tested config have the same recorded SHA-256. Real
`lineage_alioth-cp2a-user` product resolution passes and selects this kernel source,
`alioth_defconfig`, Clang r563880c, raw Image with DTB inclusion, separate DTBO,
Virtual A/B, boot header v3 and the existing 120 Hz recovery request; there is no
prebuilt-kernel or prebuilt-header override. No new HAL, fstab or SELinux adaptation
is required by these five internal error-path fixes.

This is source/manifest/configuration acceptance, **not a fresh complete ROM build
or additional phone test**. The exact-image phone acceptance above remains its
own evidence. Private integration receipts are at
`~/evo/.repo/kernel-integration-20261102/`. Source repos were already published;
only this verification record needed a new push.
