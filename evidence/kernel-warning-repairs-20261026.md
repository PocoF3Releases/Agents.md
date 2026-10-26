# Power-reset and USB warning repairs

Date: 2026-10-26. Base: edb46ba397834c339d4341bb8664935c1fdcbf4b.
Scope: configured Alioth kernel, checkout Clang 21, W=1 and C=2 sparse at -j4.
No warning suppressions, configuration changes, thermal changes or system-side
source edits. No imported patch is relabeled with assistant authorship.

## Separate source changes

- [Qualcomm IMEM mapping contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a2c4e490a5dbeb2bce42e6dd388e3698a637c4c7): retain `__iomem` through mappings and register accesses, release acquired OF-node references after mapping, and keep the SCM helper private. Register values, barriers and power-off/restart sequencing are unchanged. This is not a demonstrated fix for the intermittent shutdown hang.
- [xHCI secondary event-ring contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/fb3f44ae35d4637cc6857fcf45a90de613d27494): decode the saved event flag as little-endian before deriving its cycle bit, matching the subsequent comparison. Five same-file helpers become static; allocation parameter documentation is completed. Public secondary-interrupter interfaces remain unchanged. No performance benefit on little-endian Alioth is claimed.
- [USB-core unused locals](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1ee79a4383f5bab1feca922a986f5f02eeea858f): remove an unused parent lookup and unread suspend result storage, retaining all feature requests, masks and return paths. This is source cleanup, not new suspend error handling.

The matching Qualcomm downstream and mainline USB event handling were reviewed;
no exact drop-in human patch for this vendor combination was established. These
are own scoped changes; all existing upstream author attribution remains intact.

## Reproduction and acceptance

The four-object baseline fails with fatal missing-prototype/unused-variable
warnings plus sparse MMIO/endian diagnostics. After repair, those four objects
pass W=1 compilation with fatal-warning policy intact. Power-reset, USB driver
and xHCI memory objects have no sparse diagnostics. The hub object retains the
pre-existing `hub_port_connect` lock-context warning: cleanup conditionally unlocks
according to its earlier `retry_locked` state. That report is not suppressed and
this batch does not restructure enumeration locking merely to satisfy analysis.
Full-kernel W=1/sparse completion is not established.

Private exact-source host fixtures built with `-Wall -Wextra -Werror` and ASan/UBSan:

- `map_prop_mem`: missing-node and failed/successful mapping combinations verify return values and OF-reference release. The old helper fails the release assertion; the final helper passes. Mocks establish reference-ownership flow, not hardware MMIO validity or a measurable leak on Alioth's static OF configuration.
- Actual xHCI cycle expression: 131,072 simulated little/big-endian cases pass; the baseline fails a big-endian expectation. This tests decoding, not a physically attached secondary-interrupter device.

Strict checkpatch: zero errors, warnings or checks. Git whitespace check passes.
Final normal configured Image build passes with fatal-warning policy intact and
no compiler warning/error diagnostics. Image SHA-256:
`71c2577e8fd2319d682437ff1ee117b0679126a60cf389bc4817836868c6f99f`.

No phone flashing or runtime test was performed for this batch. Earlier device
acceptance cannot certify a new image. Raw commands, before/after logs and mock
fixtures remain private under `~/evo/.repo/kernel-warning-repairs-20261026/`.
