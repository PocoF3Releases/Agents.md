# Kernel correctness audit — 2026-11-02

`source-checked`, `host-tested`, `build-tested`; **historical first-phase checkpoint**. Later device acceptance and publication are owned by the follow-up below.

This records the first two findings. The [follow-up](kernel-correctness-followup-20261102.md) owns the final five fixes, complete kernel build, phone acceptance and publication.

## Identity and scope

Audited [aosp-17 source 3d374cb](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3d374cb35915256513a2dbccb921d9fbf1259c4b), tree `ed5849318f3d1c18892b17326d2f29b6562ede8d`. Workhub started at [afd9047](https://github.com/PocoF3Releases/Agents.md/commit/afd9047f3d90e3c67d00f5c5e13227f2195e4a5c). The source was clean and the remote kernel head matched before investigation. Current changes are uncommitted; these links identify the baseline, not a published fix.

Production config copied from the prior isolated strict build: SHA-256 `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`. `CONFIG_IOMMU_API=y`, `CONFIG_IOMMU_SUPPORT=y`, `CONFIG_ARM_SMMU=y`, `CONFIG_CC_WERROR=y`. Toolchain: checkout Android Clang 21.0.0, r563880c, build 14054515, LLVM revision `5e96669f06077099aa41290cdb4c5e6fa0f59349`. Source and toolchain commands ran inside Linux. Existing ROM output and previous isolated output were preserved.

The supplied audit brief and current [audio checks](kernel-audio-boundaries-20261102.md), [W=123 discovery](kernel-w123-20261102.md), [Sparse backlog](kernel-sparse-backlog-20261028.md) and [prior Sparse acceptance](kernel-sparse-errors-20261028.md) were read first. W=123 was used only as the existing discovery inventory, not a new acceptance standard. This audit selected **two** findings, below the five-finding limit. Warning reduction was not an acceptance criterion.

## Demonstrated findings

### F1 — IOMMU group ID released twice after registration failure

- **Path and preconditions:** the configured ARM SMMU device-group path can call `generic_device_group()` → `iommu_group_alloc()`. ID allocation succeeds, but `kobject_init_and_add()` fails, for example allocating a sysfs name/directory under memory pressure. That function initializes the kobject and installs `iommu_group_ktype` before attempting registration.
- **Invariant:** the allocated ID has one owner and must be released exactly once. The old branch calls `ida_simple_remove()` and then `kobject_put()`. Final kobject release invokes `iommu_group_release()`, which removes the same ID again. In this tree `ida_simple_remove` aliases `ida_free`.
- **Consequence:** a redundant IDA release is certain on this injected error path. Without interleaving, IDA detects an unallocated ID; if an independent allocator reuses the ID between calls, the second removal can remove its reservation. The latter is a legal modeled interleaving, not a phone-observed corruption or a proven exploit. SMMU grouping has a per-SMMU mutex; this does not establish global serialization of the shared IDA across independent callers.
- **False-positive alternatives checked:** registration failure does not bypass `kobject_init()`, and putting this initialized object does call the group release method. This is not a memory double-free claim. The successful allocation branch is untouched.
- **Minimal regression:** fail kobject registration after successful ID allocation; count one removal through the real extracted group release function. Repeat with deterministic reuse immediately after the first ID removal and verify the other owner's reservation survives. Original: two failing cases; ID-only fix: both pass.
- **Smallest fix/provenance:** remove only the early ID removal, retaining `kobject_put()` and the original errno. Backport of Yuan Can's [bf75eb44](https://github.com/torvalds/linux/commit/bf75eb44e11bcdb1edda3305dc7292b605c25172). Adaptation is only the existing `ida_simple_remove()` spelling; the API is not migrated. Original author, message and trailers are retained in a separate private patch file, with a backport note. No commit was created.

### F2 — IOMMU group leaked when either sysfs attribute fails

- **Path and preconditions:** group ID, group kobject and child `devices` kobject are allocated successfully. Creating `reserved_regions` or `type` fails (the underlying kernfs/sysfs allocation can return an error).
- **Invariant:** an allocation function returning `ERR_PTR` must release the resources it still owns. The group transfers lifetime to the child's parent reference and drops its own original kobject reference. The old attribute-error branches return without putting the child's initial reference; callers cannot recover the inaccessible group from the error pointer.
- **Consequence:** the group, child, ID reservation and any already-created sysfs attribute remain allocated after failure. Repeated failed grouping/probe attempts accumulate resources. No user-visible steady-state performance claim is made.
- **False-positive alternatives checked:** `sysfs_create_file()` does not consume or put either object. The group's initial parent reference has already been dropped, but the child's initial reference remains. Putting the child deletes its sysfs node and drops the parent reference; the parent's release removes a previously created attribute and frees the group/ID. No second parent put is needed.
- **Minimal regression:** independently fail the first and second attribute creations, retain the original errno, and verify zero live group/child/attributes and exactly one ID removal. Original: four failing cases (with/without reuse); sysfs-only fix: all four pass. Ordinary success and caller `iommu_group_put()` also pass.
- **Smallest fix/provenance:** put `group->devices_kobj` immediately before both existing error returns. Exact code backport of Jason Gunthorpe's [4daa8611](https://github.com/torvalds/linux/commit/4daa861174d56023c2068ddb03de0752f07fa199), whose upstream test used `iommufd_fail_nth`. This 4.19 tree does not thereby gain that newer test infrastructure. The upstream patch, authorship and trailers remain separately archived; no fabricated attribution or commit was added.

## Source evidence

The final kernel diff changes only `drivers/iommu/iommu.c`: **6 insertions, 3 deletions**. Patch SHA-256: `64946cb576a683567183725de21bfdbadd29a6e3814ab530f5e831b43565d734`.

A private gate receipt records clean-source identity, baseline bytes and old/new failure results before either source patch was applied. Each patch was checked and applied independently. There are no header/UAPI/export declarations, structure layout, Kconfig/defconfig, security, thermal, success-path or system-side source changes. The rebuilt object's 75 defined global name/type entries equal the previous strict-build object's entries; this is a symbol check, not complete ABI certification.

## Host and static evidence

- Extracted the **unchanged actual allocator, release and group-put functions** into a host harness; only kernel primitives are stubbed. The archived baseline is asserted byte-for-byte against the pinned Git source. The current worktree is tested as a separate variant, so re-running cannot silently replace the old baseline.
- Faults cover group allocation, ID allocation, group registration, child allocation and each attribute; include normal success and caller release, plus an ID-reuse schedule. Results across 14 cases: **old 6 failures; ID-only 4; sysfs-only 2; combined 0; actual worktree 0**. Every variant compiles with Clang `-Wall -Wextra -Werror` and AddressSanitizer/UndefinedBehaviorSanitizer; sanitizer stderr is empty. Parent references are released before child release, matching target kobject cleanup order.
- These are source-extracted host ownership tests. They do not execute real kernfs, scheduler interleavings, memory pressure or device hardware. ASan/UBSan passing is not proof of kernel-wide sanitizer cleanliness.
- Smatch maintainer source pinned at `5189e3fb018b783a26dcb45c02c114c1d1aad290`. First pass analyzed **101 configured translation units** in `drivers/char/`, `drivers/gpu/msm/`, `drivers/iommu/` and ION, including Kbuild preparation units. Built a current-source cross-function database (102,502 caller-info and 71,952 return-state rows), then ran the same 101-unit database-backed pass. All analyzer invocations completed. This is scoped coverage, not whole-kernel or all-config coverage.
- Post-fix database-backed Smatch checked **16 units** (14 IOMMU plus two preparation units). Its **32 IOMMU reports are unchanged after line-number normalization**. They are not automatically confirmed defects or a clean Smatch result. In particular the kobject-initialization warning cannot see the full initializer contract; source inspection establishes initialization before the error branch. Fast-DMA mapping ERR_PTR warnings and other unproven reports remain in raw evidence for later caller/attachment analysis. No warning was suppressed to change these counts.
- Coccinelle 1.3 report-only `kfree` rules checked GPU, ION and IOMMU; GPU iterator rule also ran. Post-fix IOMMU `kfree` pass completes with no report. The GPU speed-bin report passes a freed pointer value to `PTR_ERR_OR_ZERO` without dereferencing it; it was not treated as a demonstrated use-after-free. Two KGSL fence puts also have separate acquired references; no speculative refcount patch was applied.
- Existing Sparse **0.6.4** checked all 16 affected/preparation units after the fixes, with **no diagnostics**. The historical **2,954-warning / zero-error** backlog remains historical and unrecounted; this local result does not clear it.

Private tools were built/extracted inside the audit directory; the stock Smatch kernel wrapper was not run because it cleans its build directory and writes source-side artifacts. An unsupported `--param-mapper` preparation attempt failed explicitly; final passes omit that unsupported option. Analyzer options, per-TU command receipts, SQL input/database, package versions and raw logs are retained. No analyzer success-forcing option was used.

## Build evidence

Forced recompilation of **14 affected IOMMU C units** in a separate output tree passes with `W=1`, `CONFIG_CC_WERROR=y`, `KCFLAGS=-Werror`, checkout Clang and `-j4`. There are **zero compiler diagnostics**. Eleven pre-existing kernel-doc warnings remain (one `iommu_trigger_fault` argument and ten `msm_iommu_map` members); no documentation-only edits or warning suppressions were made. This was the affected directory target, not a newly linked whole Image or DTB build. Config SHA-256 is unchanged. `git diff --check` and strict checkpatch pass (zero errors/warnings/checks).

## Adversarial review and limits

A fresh read-only GPT-6.1-Sol reviewer checked tests first, exact baseline/candidate bytes, both upstream patches, target `kobject_init_and_add`, `kobject_cleanup`, `kobject_del`, group release, IDA and actual SMMU callers. No Required/Critical issue was found. Review prompted making the modeled parent/child cleanup order exact; the final five-variant suite and archived result hashes were then rechecked by the reviewer without source edits. Approval is limited to these two fixes and their stated evidence.

Other Smatch candidates were not patched merely to clear reports. GPU timestamp output reports still require proof of a reachable invalid memstore/context state; FastRPC nullable-output warnings require their map/output/caller invariants; KGSL initialization-error reporting warrants a separate bounded follow-up. This audit is not a certification that the remaining kernel has no defects.

## Device and publication boundary

**At this first-phase checkpoint**, no new device operation, boot, flash, runtime acceptance, full ROM build, history rewrite, commit or push had occurred. The source branch still pointed to the original baseline, pending the user's publication/deployment scope. This restriction was subsequently superseded by explicit authorization recorded in the follow-up. No phone result from earlier tasks is attributed to this diff.

Raw source/build/host/static evidence and two author-preserving patches are private at `~/evo/.repo/kernel-correctness-20261102/`; no proprietary dumps, device identifiers or unrelated source changes were published.
