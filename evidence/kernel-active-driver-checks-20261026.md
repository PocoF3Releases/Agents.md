# Active driver follow-up — October 26, 2026

This continues the [configured audit](kernel-subsystem-audit-20261026.md).
Baseline b544d9ee5fe2; final source 6ab769d4a561. Scope is the existing Alioth
configuration and seven selected built-in objects, not a whole-tree clean bill.
No system-side source, configuration, warning flags, thermal limit, charging
profile, retry limit or firmware was changed. Host fixtures and temporary kernel
modules remain private, outside production sources.

## Separate source changes

- [scsi: ufs-qcom: Make request-end lock ownership explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/dfac40ccb015620d09e0e0f6407a8696dc031912).
- [scsi: ufs-qcom: Read diagnostic registers with explicit access size](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7444bf7653b900f2f1dfbc8eabb869c66569c8f1).
- [usb: dwc3: debug: Check non-standard control requests](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/10bd8f40681ff128f9e7f0507b6eb229cd11d3e0).
- [power: supply: qcom: Define private and shared battery state](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/fa1f502b41d4eed3272e3d10b48f498923737515).
- [Bluetooth: qcom: Keep private power and SLIMbus helpers local](kernel-history-map-20261026.json).
- [Bluetooth: qcom: Propagate exhausted SLIMbus read errors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/58fb3e3bbe152920f2176afde036c638ea0d80d9).

The UFS register strategy comes from Marc Gonzalez's
[d67247566450](https://github.com/torvalds/linux/commit/d67247566450cf89a693307c9bc9f05a32d96cea).
The existing vendor callback receives words rather than bytes and can run before
its no_sleep guard, so the backport uses kmalloc_array/GFP_ATOMIC and explicit
32-bit readl accesses before printing normal memory. Prefixes, groups and word
counts remain. Allocation failure skips only that diagnostic bank. No normal
storage request path or QoS policy was changed.

UFS request-end locking now has separate caller-held and self-locking branches,
with the same completion helper called once. Documentation describes the real
arguments; the operations-variable overview is no longer falsely described as a
struct definition. No lock annotation or cast hides the ownership warning.

The DWC3 change backports Thinh Nguyen's
[b6155eaf6b05](https://github.com/torvalds/linux/commit/b6155eaf6b05e558218b44b88a6cad03f15a586c)
into the existing driver-local decoder. Nonstandard requests no longer receive
standard request descriptions merely because bRequest values overlap. Generic
output uses CPU-order values and the existing 500-byte trace buffer, eliminating
the old restricted-endian arithmetic. Standard request handling, trace fields and
USB transfer paths are unchanged. Both backports retain original authors/dates
and explicitly describe adaptations; broad newer driver refactors were omitted.

Private battery instance state, retry counters and read-only tables now have
internal linkage. The genuinely shared off-charge flag retains external linkage
and gains a common declaration in the existing small battery header. Importing
the large SMB5 header into FG was rejected after its DEBUG_BOARD_VOTER collision;
the minimal header resolves the interface without macro suppression. Charging,
authentication retries, profile selection and all thermal protections remain.

Bluetooth cleanup retains generic SLIMbus read/write interfaces and removes only
four unreferenced, unexported wrappers. Private class/reset/delay state is local;
regulator diagnostics print their index rather than passing a pointer to %d.
Separate functional repair returns an exhausted SLIMbus read error before logging
destination data. Existing callers handle negative results; normal success,
transport selection, transfer locking and three-attempt retry behavior remain.
No matching drop-in upstream repair was identified for that vendor read defect.

## Compiler and host evidence

The final serial W=1/C=2 checks pass for battery.o, smb5-lib.o, qpnp-fg-gen4.o,
ufs-qcom.o, DWC3 trace.o, bluetooth-power.o and btfm_slim.o with **no source
warnings or errors**. Existing host Genksyms grammar conflict notices remain
outside these driver objects. No warnings were disabled. Cumulative strict
checkpatch reports zero errors, warnings and checks. A full normal Image build
of the final source passed with the checkout's Clang 21 at -j6; no installclean
or full ROM build was performed.

Private ASan/UBSan tests cover USB routing/CPU-order values and all 65,536 request
type/code pairs. The old decoder fails the vendor-request assertion. Extracted
UFS functions cover caller-held/self-held/null paths, all current register bank
sizes, alignment/count rejection and allocation failure. The emitted LTO wrapper
contains explicit i32 MMIO loads; LLVM-dis emits numbered files for this
multi-module object. A missing unnumbered output was not treated as evidence.
Bluetooth fault injection covers immediate success, retry recovery and exhausted
read failure; the original helper fails the exhaustion assertion. Host mocks do
not establish physical controller behavior or force hardware faults.

## Phone acceptance

The temporary candidate identifies 6ab769d4a561, boot completes and SELinux stays
enforcing. Raw Image SHA-256:
`91ff5ec891446d25cec48d5ae6d9642c645b1b1e15aa2ed057b4fb1da446b536`.
Repack round-trip verifies its kernel and unchanged installed rooted ramdisk.
No partition is flashed.

- A uniquely created 16 MiB file passes fsync and aligned O_DIRECT readback with
  exact word verification, then is deleted. No global cache drop is used.
- A 16 MiB random payload passes USB push/pull SHA-256 comparison.
- Battery stays present, healthy and charging, with valid SOC/voltage/temperature.
- Bluetooth disable/STATE_OFF and enable/STATE_ON all succeed; its original ON
  setting is restored. Wi-Fi remains enabled and COMPLETED afterward.
- No new WARNING, BUG, call trace or RCU stall appears after the runtime marker.

No headset is available: A2DP/HFP playback and physical SLIMbus fault injection
are not certified. UFS hardware error injection/register dump invocation was not
forced. USB decoder formatting is host-tested; USB bulk data is device-tested.
No claim of universal hardware correctness or resolved intermittent shutdown
causality follows from these bounded checks.

All six commits are pushed on the public kernel aosp-17 branch through
6ab769d4a561. Retained pstore identifies this candidate's successful restart:
normal-priority callbacks returned, perf teardown took about 7 ms and hardware
warm reset followed. This is a bounded healthy test, not proof of the historical
intermittent hang's cause.

The phone returned to its installed d2c680 kernel, enforcing, with its original
Bluetooth ON state and unchanged boot-partition SHA-256. Windows ADB server
refresh restored the transport after boot; no extra phone reboot was needed.
Owned phone probe/image/USB staging, Windows temporary image and host bulk-data
fixtures were removed. The baseline observer and narrow SPU unmount live rule
are rearmed only for the current boot; initcall_debug=N. No persistent diagnostic
module or permissive policy was installed.
Private raw logs, fixtures, IR and receipts are under
`~/evo/.repo/kernel-subsystem-followup-20261026/`.

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
