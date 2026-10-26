# Shutdown fixes: upstream provenance review — October 25, 2026

This is an upstream-replacement audit, separate from the earlier
[phone acceptance](shutdown-investigation-20261025.md). The published kernel
branch now contains the applied, build-tested and temporarily device-tested
replacement series through [ee8cd976d579](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ca1a538b314b791b28bbe4e318be4f338cc21005).
The maintainer authorized the history rewrite; an explicit expected-head lease
protected the push and a local backup preserves the former published stack.

## Accepted mainline replacements

| Original upstream commit | Author | Replacement scope |
| --- | --- | --- |
| [becef184dfe9](https://github.com/torvalds/linux/commit/becef184dfe9bfef522c80501d22a5e02efba8d8) | Luc Van Oostenryck | Replaces the complete local generic per-CPU fallback declaration implementation with the simpler upstream typeof(pcp) pointer spelling. |
| [43b9e4febc66](https://github.com/torvalds/linux/commit/43b9e4febc66b98d83cc1560196d56ac7fef3c32) | Mukesh Ojha | Replaces the two perf PMU per-CPU member-declaration hunks of the local cleanup. |
| [d00dbd298142](https://github.com/torvalds/linux/commit/d00dbd29814236ad128ff9517e8f7af6b6ef4ba0) | Ben Dooks | Uses the original static-inline cgroup stub fix instead of locally removing the unused stub. |

All three original patches apply without adaptation to the pre-fix source.
The applied commits preserve their original authors, dates, messages and
trailers, with upstream commit references. Their stable patch IDs match the
original patches. Unchanged imports receive no invented assistant attribution.

The final tree differs from the published tree only in five generic
pointer declarations and restoration of the unused static-inline stub. Its
remaining local cleanup is kept separate from the three upstream patches; the
timer repair remains unchanged. Independent source/provenance review found no
blocking issue in that series.

Both the upstream-compatible variant and restored published source completed
ARM64 W=1/sparse checks across the enabled kernel/events objects without perf
source diagnostics. Pre-existing host Genksyms grammar notices are unchanged.
LLVM dumps differ in source-line-derived/debug metadata and were not treated as
proof of byte-identical linked kernels. The subsequent applied series completed a fresh Image build and the separate
phone checks below; earlier acceptance was not reused as its runtime evidence.

## SPU policy precedent

The January 10, 2025 community device patch
[b2e34aefdade](https://github.com/wshamroukh/device_xiaomi_cas/commit/b2e34aefdade171b97dfbddec059651cfcde7eda)
by wshamroukh adds exactly the init-to-vendor_spunvm_file filesystem unmount
permission, with the same permission-denied/unmount-timeout symptom. Its other
mount/relabel permissions are already inherited by our tree; importing unrelated
policy is unnecessary. Our validated one-permission delta is functionally the
same. This is independent device-tree precedent, not an officially merged
Lineage fix or proof of the separate kernel stall's cause.

## Timer and remaining local cleanup

The inspected Lineage kernel
[7646fd34cc76](https://github.com/LineageOS/android_kernel_qcom_sm8250/blob/7646fd34cc76f1ff57f020aaa67b8e6a813db723/kernel/events/core.c)
retains the Qualcomm cancellation under the callback lock. The related human
mainline fixes [272325c4821f](https://github.com/torvalds/linux/commit/272325c4821f052092c41feac21f4a1a46f0ad48)
and [4cfafd3082af](https://github.com/torvalds/linux/commit/4cfafd3082afc707653aeb82e9f8e7b596fbbfd6)
are already ancestors of our kernel and predate the Qualcomm hotplug change.
They address timer forwarding/restart synchronization, not this later
cancellation lock cycle. Re-picking them is not a replacement.

No verified drop-in upstream replacement was identified for our timer stop gate
and failed-CPU-down rollback handling, or for the residual RCU/lock-contract
cleanup. The latter is largely checker/type-contract maintenance and must not be
presented as an independently reproduced runtime shutdown fix. Modern perf core
rewrites are not small compatible substitutes for this vendor hotplug design.

The three exact upstream patches are now imported separately. Retain explicit
local provenance for the rest and keep the intermittent hang open until causal
runtime evidence establishes the failing path.

Private originals, application checks, patch-ID receipts, compiler logs and
prepared-series mapping are under `~/evo/.repo/upstream-shutdown-review-20261025/`.

## Applied source and fresh phone acceptance

The public replacement commits preserve original authorship:

- [a1925f97b4b5](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2c2ac210b4d1476e58b542a7b7437767418f6a8c): Luc Van Oostenryck's generic per-CPU fix.
- [14f8da1a63ff](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d02e7a86b2443567af8b54eb1f473f2d44b4dfd2): Mukesh Ojha's PMU declaration fix.
- [d6914617fbe8](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/daf3b2adf2e6206df25c7314ffd85f25f1c3b19f): Ben Dooks's static-inline fix.
- [ee8cd976d579](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ca1a538b314b791b28bbe4e318be4f338cc21005): remaining local ownership contracts.

The independent [timer repair](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1a8f7faa9d86c864ad81f598c71af7466eb62fcf)
is preserved unchanged. No approved feature, configuration or production policy
was dropped. No test modules, fixtures or Markdown were added to the kernel.

Build-tested: final ee8cd Image and enabled perf W=1/C=2 checks pass. Private
modules also pass W=1/C=1. Inherited host Genksyms grammar notices are unchanged.
The tested Image SHA-256 is
`f522895c06f8ce4ae2a898327df9ca615649226cb77d49bd9f4854a8cc22460e`.

Device-tested: temporary ee8cd kernel, original rooted ramdisk, SELinux enforcing.
Raw counters opened/multiplexed all 96 events with zero failures before and after
CPU7 offline/online recovery. Both sampling runs produced 118 samples, one fork,
one exit and zero malformed records. The bounded actual-PMU lock probe captured
a fresh remote callback while holding its lock: try_cancel=-1, 12 running events,
ret=0. It never calls blocking cancellation under the held lock. Its initial
permission denial required only a current-boot kernel perf_event cpu permission;
that diagnostic rule is not a production policy change and disappeared on reboot.

Restart under 96 retained kernel counters reached the observer immediately before
perf with eight active mux timers across eight contexts. Perf and the remaining
notifier tail returned in about 11 ms; hardware warm reset followed. SPU unmount
succeeded without its former permission-denied retry. No new warning/BUG/RCU
stall appeared in the targeted interval. Private out-of-tree modules taint the
kernel normally; that is separate from a production warning.

A separate Power off under the same counter load reached charging animation,
confirmed by the maintainer, who then booted Android. Charger startup overwrote
the candidate's Power off console; this is user-confirmed behavior, not a saved
candidate driver-teardown trace. The boot partition hash remained unchanged.
The phone returned to installed d2c680, enforcing, CPU0-7 online and initcall_debug=N.
Temporary upstream probe/image artifacts were removed. Only the original-kernel
observer and narrow SPU live rule are rearmed for the current boot; no persistent
autoload or global permissive policy was installed.

## Remaining shutdown investigation

The old long-uptime stall still has no captured blocking task stack. These passes
do not establish that every intermittent shutdown failure is fixed. Normal
priority notifier completion and perf completion now have separate markers in
the private candidate observer, so a recurrence can distinguish those phases.

Source review followed ESOC into MHI's suspend completion, runtime resume and
worker teardown. The inherited human MHI pm_lock release fix is already present;
PM_POST_SUSPEND completion is emitted on normal and aborted suspend paths. No
causal stack establishes a missing completion here. NPU's NOTIFY_DONE condition
is inherited from its human vendor change; SYS_RESTART skips that locking branch,
so its last log line alone cannot identify it as the restart blocker. No speculative
timeout, NPU semantic change or thermal bypass was added. Obtain the observer's
stack on an actual recurrence before selecting the next production repair.

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
