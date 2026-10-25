# Shutdown fixes: upstream provenance review — October 25, 2026

This is an upstream-replacement audit, separate from the earlier
[phone acceptance](shutdown-investigation-20261025.md). The published kernel
branch remains unchanged. A reviewed local replacement series is prepared at
`review/upstream-shutdown-20261025`; it is not published or device-tested.

## Accepted mainline replacements

| Original upstream commit | Author | Replacement scope |
| --- | --- | --- |
| [becef184dfe9](https://github.com/torvalds/linux/commit/becef184dfe9bfef522c80501d22a5e02efba8d8) | Luc Van Oostenryck | Replaces the complete local generic per-CPU fallback declaration implementation with the simpler upstream typeof(pcp) pointer spelling. |
| [43b9e4febc66](https://github.com/torvalds/linux/commit/43b9e4febc66b98d83cc1560196d56ac7fef3c32) | Mukesh Ojha | Replaces the two perf PMU per-CPU member-declaration hunks of the local cleanup. |
| [d00dbd298142](https://github.com/torvalds/linux/commit/d00dbd29814236ad128ff9517e8f7af6b6ef4ba0) | Ben Dooks | Uses the original static-inline cgroup stub fix instead of locally removing the unused stub. |

All three original patches apply without adaptation to the pre-fix source.
The prepared commits preserve their original authors, dates, messages and
trailers, with upstream commit references. Their stable patch IDs match the
original patches. Unchanged imports receive no invented assistant attribution.

The prepared final tree differs from the published tree only in five generic
pointer declarations and restoration of the unused static-inline stub. Its
remaining local cleanup is kept separate from the three upstream patches; the
timer repair remains unchanged. Independent source/provenance review found no
blocking issue in that prepared series.

Both the upstream-compatible variant and restored published source completed
ARM64 W=1/sparse checks across the enabled kernel/events objects without perf
source diagnostics. Pre-existing host Genksyms grammar notices are unchanged.
LLVM dumps differ in source-line-derived/debug metadata and were not treated as
proof of byte-identical linked kernels. No phone operation or new full-image
acceptance was performed during this audit. Earlier phone acceptance belongs
to the published tree, not automatically to the prepared series.

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

Prefer the three exact upstream patches when adopting the prepared series.
Retain explicit local provenance for the rest and keep the intermittent hang
open until causal runtime evidence establishes the failing path. No published
history was rewritten by this audit.

Private originals, application checks, patch-ID receipts, compiler logs and
prepared-series mapping are under `~/evo/.repo/upstream-shutdown-review-20261025/`.
