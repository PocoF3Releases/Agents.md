# Deferred sparse review — October 28, 2026

## Frozen baseline

The [accepted kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1efb0bf8d7a52abc450285c470bb34c28ad57dfd)
passes strict W=1/Werror and targeted phone checks. Its full unlimited C=2 run
still emits **2,954 warning reports and zero errors** after the sixteen errors
and five requested contexts were fixed. [Acceptance](kernel-sparse-errors-20261028.md).

The [complete backlog](kernel-sparse-backlog-20261028.json) preserves all 2,954
unique primary diagnostics, exact source locations, available expected/got type
context, stable W-identifiers and immutable GitHub source links. Every row is
**unreviewed**. Counts reflect checker reports, not distinct root causes or
confirmed bugs. Repeated header reports are deduplicated by the same
path/line/column/level/message key as acceptance; type-context variants remain.
One report names generated `kernel/config_data.h`, which has no tracked blob
and intentionally has no broken GitHub file link.

## Review order

1. Audit lifetime, user/MMIO/RCU address-space and lock-context contracts in
   active paths. Confirm ownership, access rules and teardown before editing.
2. Check packet/storage byte order and restricted representations against the
   actual ABI and hardware. Prefer compatible accepted upstream fixes.
3. Review remaining linkage, NULL representation and other reports by affected
   caller/configuration. A lower initial priority is not a safety finding.

Categories below are mechanical navigation aids. No report is waived or
suppressed. Future fixes require root-cause evidence, feature-separated changes,
strict compiler/sparse regressions and relevant phone checks. Compare by source
and context after rebases; never clear a row merely because its line moved.
This record schedules no build or device operation.

| Category | Reports |
| --- | ---: |
| pointer address space | 724 |
| restricted type or representation | 682 |
| lock context | 493 |
| declaration or linkage | 463 |
| null pointer representation | 371 |
| byte order | 172 |
| other | 49 |

| Source area | Reports |
| --- | ---: |
| drivers | 1764 |
| kernel | 387 |
| net | 240 |
| fs | 139 |
| mm | 129 |
| include | 101 |
| sound | 79 |
| init | 53 |
| security | 32 |
| arch | 16 |
| lib | 8 |
| block | 6 |

Private complete logs/commands remain under
`~/evo/.repo/kernel-sparse-errors-20261028/`; Android Clang r563880c and
0.6.4 (Ubuntu: 0.6.4-5ubuntu3) were used. The installed-image acceptance above is separate
from the later Redline branding change. No kernel-doc review is claimed here.
