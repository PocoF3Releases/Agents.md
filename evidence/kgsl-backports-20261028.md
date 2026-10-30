# Qualcomm KGSL maintenance backports

Observation date: 2026-10-28. Kernel-only update for Alioth's existing A650 stack.
The [IQ-8275 comparison](iq8275-research-20261028.md) supplied official Qualcomm
source history; it did not justify replacing Android userspace or GPU firmware.

## Source changes

Base: [previous Redline head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1e45b8cc1cbb9229a464395b5a8e12d8b4bc349c).
Final: [KGSL update](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9edfaf12151fa23329e567b3bad013910121801a), branch `aosp-17`.

| Fix | Applied commit | Original Qualcomm change |
| --- | --- | --- |
| Reject incomplete type-7 draw-state groups | [79446e7](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/79446e7dabc92c50e260f9a9f3e9701d70a0495f) | [Bhaskar Reddy Valluru](https://github.com/qualcomm-linux/kgsl/commit/06f798a179ab38779b5e80e21a31d03504f03c41) |
| Use one captured packet header throughout parsing | [699d4a6](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/699d4a660872968bd630c2189bf38f77b24c9993) | [Scott Bauer](https://github.com/qualcomm-linux/kgsl/commit/3f01c1a6b636b3764d005379592b54d3915eb180) |
| Reject mmap through another address space's KGSL descriptor | [7992aed](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7992aed2f6ac9162eae15822801b5d4aa1aaa6cd) | [Scott Bauer](https://github.com/qualcomm-linux/kgsl/commit/0a145e7671e6fa8e02acc5a4a29f0e2ea9fead01) |
| Stop VMA-open accounting after failed reference acquisition | [d0205f4](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d0205f4abe5237130bf3369240634f99e3f9b9ac) | [Scott Bauer](https://github.com/qualcomm-linux/kgsl/commit/7370c5040d89dba32ce48677c1feab0d53f0b6aa) |
| Remove a kernel virtual address from GMU snapshots | [0774583](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/07745836e21615ea12b7c46e25927d68ef24363a) | [Anil Cheeli](https://github.com/qualcomm-linux/kgsl/commit/98218fb60d15112d6c2c8bc4c2246977144ff3fc) |
| Bound retained legacy groups, indirect packets and load-state table indices | [9edfaf1](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9edfaf12151fa23329e567b3bad013910121801a) | Separate local follow-up |

Original authors, author dates and original sign-offs are preserved. Adaptations
cover the retained type-0/type-3 parser as well as type-7, preserve snapshot layouts,
and balance the process mm reference on allocation failure and destruction.
No defconfig, firmware, userspace, thermal/governor or system-side source changes.
The alignment fix already present was not duplicated; newer IOMMU APIs and Gen7/8
code were not imported into the 4.19/A650 driver.

## Build and host verification

- Full production-config Image: `W=1 KCFLAGS=-Werror`, exit 0; config and source
  unchanged during the build. Two existing kernel-doc warnings about `groupid`
  in `adreno_perfcounter.c` remain; no compiler warning suppression was added.
- All configured KGSL objects: targeted `C=2` sparse, exit 0 with zero reported
  warnings/errors. This is not a whole-kernel sparse claim.
- ASan host fixtures extract actual before/after functions: baseline short-group
  and failed-reference faults reproduce; final malformed/valid packet lengths,
  captured-header behavior and VMA accounting pass.
- Checkpatch: no code errors in the upstream backports. The local follow-up keeps
  existing `uint64_t` style, which triggers two type-style checks. Old checkpatch
  also flags the repository-required coauthor trailer, upstream IDs absent from
  this Git object store, and missing human DCO on the new local commit. No DCO
  was invented or check suppressed.

Image SHA-256: `585ac646507e03b4f3ad7a5580bf4934422b1676e8c8ce2ea5ed5ed95561a248`.
Private fixtures, commands, logs and images:
`~/evo/.repo/research/iq8275-20261028/kgsl-backport`.

## Phone verification and installation

Temporary boot identifies `4.19.325-Redline-9edfaf1-cip136` with SELinux enforcing.
Both 32-bit and 64-bit regressions passed 32 fork/shared-descriptor cycles each:
the old kernel accepts the separate child mmap, the updated kernel rejects it
with EACCES, and own-process mappings/freeing remain functional. The initial
fixture incorrectly accessed a VM_DONTCOPY mapping after fork and faulted on the
old kernel; the corrected fixture explicitly verifies its absence. That test
mistake is not evidence of a kernel defect.

408 app-domain graphics checks passed: 62 native plus six window checks, three
runs on each ABI, with executable ABI, installed APK hash and untrusted-app domain
verified. Three sleep/wake cycles passed. The captured kernel log contained no
GPU fault, kernel panic, BUG or call trace. Xiaomi thermal service remains running;
SELinux stays enforcing and no thermal controls were modified.

The tested kernel was repacked with the phone's existing ramdisk, preserving
Magisk; unpacked ramdisk SHA-256 matches before and after. Active boot partition A
was backed up, its original identity checked, then written and fully read back.
Installed image SHA-256:
`a379d04e4b5fbf79dde83d4b2ea462f3a219d78d09360b5611e9eaa918044961`.
Normal reboot returned to the installed revision with boot completed, root working
and SELinux enforcing. Both ABI mapping tests passed again; Settings opened and
fresh kernel logs showed no matched GPU fault, panic, BUG or call trace. The full
active boot readback still matches the installed image. Kernel commits were pushed
fast-forward and the remote head was verified at the final revision.

This is bounded correctness/security coverage, not an FPS improvement, full GPU
conformance result, resolution of historical game page faults, or a fix for
manual 60/120 Hz optical differences. No deliberate GPU hang/snapshot was induced
on the phone; malformed snapshot parsing and failed-reference paths have host
regression/source coverage rather than live fault injection.

## A6xx register-list follow-up — October 29

Published [0659900](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0659900d8b784b18eaa08d5fc7bdb46ef0d5bef5)
corrects the existing Qualcomm counter-list check: the 16-byte CPU/GPU lock header
is excluded from usable data capacity, shared lengths are checked before traversal,
and appending a complete final pair remains valid. Existing full-list counter
updates and A612 trailing control-register ordering are retained. The original
human-authored bounds commit remains intact; this is a separate follow-up.

Actual before/after function fixtures reproduce the old heap overrun under ASan
at a synthetic capacity boundary; 13 final cases pass, covering malformed/full
lists, existing counter updates, exact-fit append, A612 ordering and lock cleanup.
This does not establish that ordinary Alioth workloads fill the list to capacity.
Full W=1/KCFLAGS=-Werror Image passes. Targeted sparse exits zero with no driver
reports; rebuilding host genksyms emits existing grammar-conflict warnings. The
Image build retains existing trace kernel-doc warnings. Checkpatch flags one
continuation alignment check, an unwrapped commit paragraph, the required coauthor
trailer and absent human DCO; no sign-off was invented or diagnostic suppressed.

Image SHA-256: `23f571cc33c1eaee707c467972e69eb6cb46719388f8c32825bc4ec4f296c037`.
Private follow-up artifacts: `~/evo/.repo/research/iq8275-20261028/kgsl-followup`.
Temporary enforcing boot passed 408 app-domain graphics checks across both ABIs
and three sleep/wake cycles, with no matched GPU fault or kernel crash in fresh
logs. The kernel was installed to the active slot, verified by full readback, and
normal reboot confirmed `4.19.325-Redline-0659900-cip136`, enforcing SELinux and
boot completion. Existing ramdisk/Magisk preserved; source pushed fast-forward.
The user-requested `verifier_verify_adb_installs=0` was verified after reboot;
this affects USB app verification, not Play Integrity attestation.

The broader review found existing equivalents for compound-page unwind,
DMA-BUF metadata cleanup and the original counter-list guard. The newer FastRPC
and Iris changes use different userspace/driver interfaces. Qualcomm's signed
IOMMU-map error handling remains a candidate pending old SMMU call-invariant and
secure-map analysis; no speculative driver/firmware replacement was applied.

## Scatterlist map-error follow-up — October 29

Qualcomm [e8ed003](https://github.com/qualcomm-linux/kgsl/commit/e8ed003c27f1c9352437d51a5eff418ccaa86b09)
is adapted as [a0ee226](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a0ee226f0f514744b07ca46d996c04c60a8e1650),
preserving Lynus Vaz's authorship, author date and original sign-off. The legacy
`_iommu_map_sg_sync_pc` now treats the returned size as signed, rejects negative
results and retains its existing zero-result ENODEV behavior. Power synchronization
is balanced before interpreting every result. No SMMU API or userspace ABI changes.

Alioth's active ARM SMMU callback returns an encoded negative ENODEV when its
page-table operations are absent. The older KGSL zero-only check incorrectly
accepted that value as success. All three callers already propagate failure and
release temporary tables. The secure callback was also inspected for its signed
error return; no unrelated secure-path rewrite is included.

A fixture using the actual helper reproduces baseline false success on a negative
mapping result. Six final zero/error/positive results pass, checking both returned
errors and power-sync balancing. This is source/host evidence of error handling,
not an observed phone mapping failure or a historical GPU-fault root cause.
Checkpatch reports no code error/check; its only warning is the existing coauthor
trailer convention. Full production-config W=1/KCFLAGS=-Werror Image and targeted sparse pass;
no diagnostics appear in the targeted sparse log. Full build retains existing
kernel-doc findings outside the changed helper. The temporary enforcing kernel
passed 408 app-domain graphics checks across both ABIs and three sleep/wake cycles,
with no matched GPU fault or kernel crash in fresh logs. It was installed as the
main active-slot kernel with unchanged ramdisk/Magisk and full readback verified.
Normal reboot confirms `4.19.325-Redline-a0ee226-cip136` and enforcing SELinux.
Source was pushed fast-forward. Failure-result handling is host-tested; no
deliberate SMMU failure was induced on the phone.
Private artifacts: `~/evo/.repo/research/iq8275-20261028/iommu-followup`.

Follow-up Image SHA-256: `591d3617120852d3fea3088b877504f1b07c1abcd2ede88e54f55e6d20762d51`.

## Constraint-state follow-up — October 30

Qualcomm [03dbf72](https://github.com/qualcomm-linux/kgsl/commit/03dbf7267601586fd8b7c9b9f672231478a5313d)
is adapted as [b652bc8](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b652bc8a7d75d02776f5933b92307a463b3629b4),
preserving Kamal Agrawal's authorship/date and original sign-off. The older
interface has no owner timestamp argument; its existing timeout already uses
jiffies, so neither newer timestamp plumbing nor millisecond conversion is copied.
The unused cached-level union is removed after checking all references.

The old cached effective level can prevent a MIN-to-MAX constraint transition
after sysfs limits change. The adapted helper selects by constraint subtype and
refreshes matching ownership/expiry. The thermal-limited `_adjust_pwrlevel` remains
unchanged. An extracted-function host fixture reproduces the old transition failure
and passes priority, ownership, expiry, null-input and thermal-boundary cases after
the fix. Host compilation uses `-Wall -Werror`; adding `-Wextra` diagnoses existing
signed comparisons in the unchanged adjustment helper. No kernel diagnostic flag
is weakened. Checkpatch has no code errors/checks; only the coauthor convention.
Full W=1/KCFLAGS=-Werror Image and targeted sparse pass. Temporary enforcing
boot passed 408 app graphics checks across both ABIs and three sleep/wake cycles;
mi_thermald remained active and fresh logs contained no matched GPU fault/panic.
The active-slot image was written and fully read back, preserving ramdisk/Magisk.
ADB and fastboot disappeared after reboot; restarting Windows ADB recovered
the connection. Normal boot then confirmed `4.19.325-Redline-b652bc8-cip136`,
boot completion and enforcing SELinux. Source was pushed fast-forward.
The specific stale-constraint sequence has host coverage; phone coverage is
normal rendering/lifecycle regression, not direct sysfs-limit fault injection.

Other screened changes: SVM overflow protection already exists; the rounddown-zero
UBSAN fix targets another page-size implementation. New IRQ-index, VMA-array,
OPP/ICC and kernel-7 fence changes do not match Alioth's retained driver paths.
The firmware symlink-depth workaround targets the newer distro lookup sequence;
no matching Alioth failure is established. They are not imported speculatively.
Private artifacts: `~/evo/.repo/research/iq8275-20261028/constraint-followup`.
