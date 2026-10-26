# Hub locking investigation and MTP boundary repairs

Date: 2026-10-26. Base: `1ee79a4383f5bab1feca922a986f5f02eeea858f`.
Source-checked and host-tested; configured kernel build result below. Kernel-only
changes: no system-side sources, thermal protection, defconfigs or warning policy
were changed. Existing upstream commits and authorship remain untouched.

## Hub warning: preserve the upstream locking fix

`hub_port_connect` includes Mathias Nyman's existing
[upstream locking repair](https://github.com/torvalds/linux/commit/6cca13de26eea6d32a98d96d916a048d16a12822).
The early enumeration failure paths retain port/address0 locks until cleanup;
the later paths already released them and clear `retry_locked`. Cleanup releases
the pair only for the former paths. Allocation failure releases both before
`done`; successful enumeration returns after releasing both. Port-before-address0
acquisition order is retained. No actual imbalance was found in these paths.

An exact-function host harness runs 420 scenarios across allocation, address
assignment, reset/init, status, bus-powered hub and new-device failure stages,
retry counts, terminal errors, connection presence and speed selections. Mock
assertions check lock order, cleanup ownership and balanced exits. Strict Clang
plus ASan/UBSan passes. A negative control that removes the conditional unlock
fails. Exact extracted function SHA-256:
`0fd72a4a7f3f03090abab89a29f00660ec0da5803904b6aa1b1d9e64dc54a875`.

The surviving sparse context-join report is consistent with its inability to
preserve the correlation between earlier unlocks and the cleanup flag here.
No production lock restructuring, annotation waiver or diagnostic suppression
was added. These mocked sequential paths are not a concurrency proof or a test
of physical hub enumeration. The warning remains visible, with no demonstrated
locking defect requiring a source fix.

## Separate kernel repairs

- [usb: gadget: mtp: Include shared function declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9636c9ad918b1a30b04491ba0c302c30c457c2d1).
- [usb: gadget: mtp: Use kernel-buffer file I/O in workers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3f7db875bbb6787a532f54be701b55b0d9298b2a).
- [usb: gadget: mtp: Safely parse debug statistics writes](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1d7f78b6a0b2658c72e821bd2549679afbcf5223).
- [usb: gadget: mtp: Release compat event lock after copy failures](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8aa39d2adb865c1e86208dd3873dfe40ab58d2bc).
- [usb: pd: Keep QPNP IRQ gating helper private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8e2446567f2636b2afe17c66725d415e9f7949d6).
- [usb: dwc3: Test reset lookup as a pointer](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/214c6de5d610070ddd93c10de46fd4e350feda2f).

MTP/PTP factories use their existing shared header; they remain callable from
f_ptp.c. Only same-file parameters/debug state become private. File workers use
kernel_read/kernel_write for their kernel request buffers; the local API wrappers
retain the VFS operation and offset contract while saving/restoring address limits.
Debug writes use bounded userspace copying and reject copy/parse/nonzero-command
errors before clearing stats. Compat event copies now release ioctl_excl even on
EFAULT, matching native ioctl cleanup. QPNP's same-file IRQ helper becomes private;
DWC3 uses a pointer test without changing host-reset timing or controller selection.

## Verification and remaining diagnostics

The baseline MTP/PTP and PD PHY checks fail fatal W=1 prototype diagnostics. Final
MTP/PTP, QPNP PHY, DWC3, policy engine and unchanged hub objects pass W=1 compiler
checks with C=2 sparse enabled. Fixed user/kernel I/O, direct debug-user access,
private-state/helper and DWC3 integer-NULL reports are gone. Remaining visible
reports include the analyzed hub context join, MTP descriptor/endian/plain-NULL
and event-pointer annotation diagnostics, plus DWC3 kernel-doc parameter reports.
This is not a whole-kernel W=1/sparse-clean claim.

Exact-handler host regressions:

- Debug reset: baseline fails on a one-byte nonterminated zero at a guard-page boundary; fixed handler passes. Additional cases cover four zero spellings, nonzero/malformed/empty/overflow input and injected EFAULT without changing stats.
- Compat ioctl: baseline fails the assertion that a failed event copy releases exclusion. Fixed code passes failed-copy/retry, event-submission error, busy rejection, all three bulk-command translations, bulk-copy failure and unknown command. External copy/USB boundaries are mocked.

The compat fixture uses strict Clang, Wextra and ASan/UBSan; the exact debug
handler uses Wall/Werror plus sanitizers. Strict patch checking has zero errors,
warnings or checks. Git whitespace checks pass. No temporary fixtures are added
to kernel production sources. No phone flashing/runtime acceptance was performed.

Normal strict configured Image build passes with no compiler warning/error
diagnostics. Raw Image SHA-256:
`ba7923f21c5c5c00827a743f19c6eb19ff65a5083a3b9bf7850e15d1610e3082`.

Private commands, fixtures and logs: `~/evo/.repo/kernel-hub-audit-20261026/`.
