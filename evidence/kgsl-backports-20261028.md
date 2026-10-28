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
