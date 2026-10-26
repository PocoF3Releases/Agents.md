# MTP wire/pointer contracts and DWC3 diagnostics

Date: 2026-10-26. Base: `214c6de5d610070ddd93c10de46fd4e350feda2f`.
Source-checked, host-tested and build-tested. Kernel sources only; no system-side
sources, defconfigs, thermal policy or diagnostic flags changed. Existing upstream
authorship is preserved. No phone flashing or runtime test occurred in this batch.

## Separate changes

- [usb: gadget: mtp: Preserve descriptor endian types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/279d55e34b11e22927397392292d4a3e3697b178).
- [usb: gadget: mtp: Validate event payloads without narrowing](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1c2bef7c6c1be6fdfc52edb028bbf42f2f317899).
- [usb: gadget: mtp: Use typed null request pointers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9d16ee99a6ce8db9d256df56a006c662992d4e62).
- [usb: gadget: mtp: Reject overflowing container lengths](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/551f22ba6901e59d692952d8766d5771c527211b).
- [usb: dwc3: Correct Qualcomm DBM and GSI documentation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/90971a36383ff107cff55c7b37001eb6283d036b).

The Microsoft descriptor version now has its actual __le16 wire type. Container
length selection happens in CPU order before conversion to __le32; saturation to
0xffffffff is retained. These type corrections preserve the observed wire bytes.

Event length stays size_t until validated against the 28-byte interrupt buffer.
Previously a native length such as 0x100000004 could truncate to four and pass.
The event payload carries __user through native and compat handling; the header
exporter removes this annotation without changing the userspace interface. Typed
NULL initializers replace integer request/debugfs pointer constants.

The worker separately rejects transfer lengths whose added 12-byte container
header would overflow its signed 64-bit counter. Representable large transfers
keep their existing wire sentinel. Negative lengths keep their existing rejection.

DWC3 fixes correct 27 kernel-doc function/parameter/return contracts against the
actual MMIO, DBM and GSI implementations, including the boolean doorbell argument
and void callbacks. Existing controller operations are unchanged: a lexer comparison
preserving C string/character literals verifies identical executable/preprocessor
tokens before and after the comment edits. No comments or diagnostic checks were
deleted to hide the reports.

## Verification

- Configured Alioth MTP, PTP and Qualcomm DWC3 objects pass W=1 plus C=2 sparse with checkout Clang 21 at -j4, with zero warning/error diagnostics. Fatal compiler warnings stay enabled.
- The tree-local kernel-doc checker reports 51 warnings for baseline DWC3 and zero after correction. Strict checkpatch and Git whitespace checks pass without errors, warnings or checks.
- Exact event-handler sanitizer fixture: baseline fails oversized-length rejection; final passes lengths 0..28, oversized native lengths, queue failure, copy failure, offline and timeout cases. External queue/copy boundaries are mocked.
- Exact header-preparation sanitizer fixture: baseline reports signed overflow; final passes negative, zero, large and signed-maximum boundaries with/without the header. Invalid additions return EINVAL without producing a counter.
- Exported UAPI compiled for aarch64, armv7, aarch64_be and armeb: before/after sizes, field offsets and all four ioctl values are identical. The exported event is 16 bytes on 64-bit and 8 bytes on 32-bit; its pointer offset remains 8/4 respectively. MTP file-range size remains 32 bytes on these targets.
- Exact descriptor/length-expression cross-compilation for all four ARM targets: the 40-byte Microsoft descriptor and eight representative container headers match expected little-endian bytes before and after the type cleanup. Large-file saturation remains unchanged; no baseline byte-order regression is invented.
- Normal configured kernel Image and fresh exported-header checks pass, with no compiler warning/error diagnostics.

Image SHA-256:
`226512a0c9f76a0a6235e606ee5b1297041d807f63214c1d1df8e9970ce5aab3`.

These scoped passes do not establish whole-kernel W=1/sparse completion or physical
MTP interoperability. The separately analyzed USB hub context report remains
visible; [its investigation](kernel-hub-mtp-audit-20261026.md) is unchanged.
Raw commands, sanitizer fixtures, compiled ABI/wire data and logs remain private
under `~/evo/.repo/kernel-mtp-dwc3-contracts-20261026/`; no temporary tests were
added to production kernel sources.
