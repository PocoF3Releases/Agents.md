# Kernel audio error and packet-boundary fixes — 2026-11-02

`source-checked`, `host-tested`, `build-tested`. Follow-up to the
[whole-kernel W=123 audit](kernel-w123-20261102.md), with two focused fixes on
`aosp-17`. No production config, thermal/security setting, system-side source,
public header, warning flag or device installation changed.

## Final commits

- [ADM calibration failure reporting](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/400d43198c824b2ac0e74dbc2e523684a12d12de):
  return `adm_set_pp_params()` status through `send_adm_cal_block()`. Previously,
  allocation/APR/timeout/DSP rejection failures returned success and
  `send_adm_cal_type()` marked the calibration used. The existing caller now
  avoids that false mark. Successful uploads and the legacy Dolby topology
  bypass retain their behavior.
- [In-band parameter packet bounds](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3d374cb35915256513a2dbccb921d9fbf1259c4b):
  ADM, ASM and AFE V2/V3 now validate the payload against the 16-bit APR packet
  length minus its fixed header before addition/allocation/copy. The old
  32-bit addition could wrap allocation size or truncate the packet length.
  The three in-band packing wrappers validate data sizes before adding a
  parameter header. Header-only requests allocate only their header and retain
  valid 32-bit parameter-size fields; out-of-band limits remain unchanged.
  The AFE pack-size local matches the shared packer's `u32 *` output contract.

The bounds follow `struct apr_hdr.pkt_size` and the actual packet structs;
this does not introduce a new hardware packet-size capability or claim that all
wire-representable sizes are accepted by firmware. Generic packing used for
out-of-band calibration remains unchanged. Original human authorship/history is
preserved; Fixes trailers identify the checked ADM/ASM/AFE instance-ID commits.
The new Codex trailers are recognized by GitHub.

## Host regressions

Actual before/final functions, packet structs and the common parameter-packing
implementation were extracted from the checkout. Dependency stubs exercise
legacy and instance-ID modes under AddressSanitizer/UBSan:

- **227 cases, 856 assertions: original 140 failures, final zero.**
- **125 requests accepted by both versions have identical complete captured
  packet bytes**, including ordinary in-band/out-of-band/header-only traffic.
- Boundary cases include zero, small data, exact APR maximum, one byte beyond,
  16-bit/32-bit extremes and allocation overflow candidates. Allocator spies
  safely stop huge original requests before unsafe copies; no malicious packet
  was sent to a phone. These tests demonstrate the arithmetic/validation path,
  not exploitability of a particular userspace entrypoint.
- Calibration checks inject allocation, transport, timeout and DSP failures and
  verify the used mark, lock balance and frees. The deliberate legacy Dolby
  bypass still skips upload. No sanitizer reports in the modeled cases.

The extracted host compilation retains three pre-existing warnings (unused
arguments and a packed-member warning); the original has one additional pointer
signedness warning. These are separate from the strict kernel compiler result.
Tests and synthetic packet captures stay private; no test/tool files were added
to the production kernel commits.

## Kernel validation

- Strict **W=1/Werror Image, modules and DTBs passed**, zero compiler diagnostics.
  Kernel-doc baseline reports remain. Release: `4.19.325-Redline-3d374cb-cip136`.
- **W=123** through `techpack/audio/` compiled 142 audio C objects. The three
  modified files introduce no new diagnostics after accounting for the moved
  calibration-call argument; three existing AFE diagnostics disappear.
- **C=2 sparse** through that parent target executed 142 audio checks plus two
  preparation checks, with no diagnostics. Replaying the exact parent-context
  sparse commands on the three original files also produces no diagnostics.
- Both patches pass strict checkpatch with zero errors, warnings and checks;
  `git diff --check` passes. Only three DSP C files change.

Audio checks must enter **`techpack/audio/`** so its Makefile includes
`konaauto.conf`/`konaautoconf.h`, Elliptic/MiUS includes and the proper module
identity. Direct leaf-object checks omit that context, including Cirrus code,
and are not sufficient backend coverage. Initial leaf checks were replaced by
the parent-context checks above. Compiler capability probes remain strict;
only private W=123 object collection makes global Werror nonfatal, preserving
all warning messages and production flags.

Config SHA-256 unchanged: `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`.
Strict Image SHA-256: `f5a9b756f76791494dfc0904ab88382acc48486ec31bb8b87c9b05df872cf61e`.
[Sanitized machine-readable result](kernel-audio-boundaries-20261102.json).

## Scope and remaining limitations

The earlier 150,176-warning whole-tree inventory remains an unclassified broad
baseline; it was not recounted and is not claimed fixed. No whole-kernel sparse
rerun, listening test or execution of this new kernel on the phone occurred.
Byte/control-flow host checks and compilation do not certify DSP firmware,
physical endpoints, every audio mode or device-level recovery behavior.

Both commits were pushed normally and the remote head verified. Private source
snapshots, host stubs/captures, original/final regressions, per-object stderr,
parent Kbuild commands and build receipts live in
`~/evo/.repo/kernel-audio-boundaries-20261102/`. Earlier Images were preserved;
normal ROM output is untouched.
