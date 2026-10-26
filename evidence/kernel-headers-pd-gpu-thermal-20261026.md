# Kernel header, USB-PD and GPU/display/thermal continuation

Observed **2026-10-26**. `source-checked`, `build-tested`, `host-tested`,
`device-tested` within the limits below. No system-side source or thermal policy
change. This continues the [previous full audit](kernel-full-warning-continuation-20261026.md).

## Published source

Kernel `aosp-17`: [current implementation](kernel-history-map-20261026.json).
Twenty-two separate topic commits include the previously unpublished header/WALT/PD
repairs and seven GPU/display/thermal follow-ups. The push was fast-forward,
verified against the remote; no published history was rewritten.

- [sched: walt: Match status dump formats to native types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e3eae31a51ec513530281e2b53200752fe4fc177)
- [kbuild: Restrict Techpack header exports to selected UAPI trees](kernel-history-map-20261026.json)
- [ASoC: cs35l41: Keep platform headers in the private include tree](kernel-history-map-20261026.json)
- [ASoC: msm: Make calibration UAPI dependencies self-contained](kernel-history-map-20261026.json)
- [fuse: Include Linux types for userspace BPF declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/460e9ac40bc38cdeb4eafcde6d75e50137149a02)
- [devfreq: arm-memlat: Pass bitmap arguments to CPU-list diagnostics](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/61114d61323d693ed0f04f4764ef0ad2ee9f5b21)
- [bus: mhi: Preserve diagnostic arguments and register-read status](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1ef5b6f40367ecb0565ee4c45552ae30645ba17a)
- [soc: qcom: spcom: Supply the invalid-channel diagnostic context](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5c5049ea194ac9ca6c2dac8757c22869c22eb047)
- [media: msm: Match diagnostic instance arguments](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2233e3a1b5b4a42b33cf2e13f9b7f3fc15323903)
- [regulator: qcom-pm8008: Correct bulk and retry diagnostics](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/89d352821310935b3d7c41ca6538bb188ab51d76)
- [power: supply: ti: Correct PD manager diagnostics and local state](kernel-history-map-20261026.json)
- [usb: pd: Share selector and alternate-mode declarations](kernel-history-map-20261026.json)
- [usb: pd: Make denied selections and retries deterministic](kernel-history-map-20261026.json)
- [usb: pd: Validate Xiaomi vendor reply payloads](kernel-history-map-20261026.json)
- [usb: pd: Parse vendor request data with checked bounds](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5c430366113fa8b6accd9c1d9f5c26037f2948ad)
- [thermal: qcom: Preserve LMH MMIO address-space types](kernel-history-map-20261026.json)
- [drm: mi: Include the notifier interface declarations](kernel-history-map-20261026.json)
- [gpu: kgsl: Keep encoded userspace addresses as integers](kernel-history-map-20261026.json)
- [gpu: kgsl: Match kernel-doc to current function parameters](kernel-history-map-20261026.json)
- [drm: dsi: Reject unsupported HBM display commands](kernel-history-map-20261026.json)
- [drm: dsi: Match error interrupt diagnostics to their arguments](kernel-history-map-20261026.json)
- [drm: dsi: Store panel readback words in explicit byte order](kernel-history-map-20261026.json)

## Contracts and regressions

- LMH's three mapped register pointers retain `__iomem` through `readl`/`writel`.
  Its hardware list and mutex have file-local ownership. No trip temperatures,
  current/frequency caps, polling, register writes or IRQ policy changed. The
  CPU limits device is actually bound on the phone; TSENS and `mi_thermald` remain active.
- Xiaomi's display notifier includes its existing interface header. Event values,
  exported prototypes and blocking notifier delivery are unchanged.
- Eleven fixed-width KGSL address fields are integers copied into kernel-owned
  requests, not pointers to dereference. Removing scalar `__user` fixes the
  noderef contract; actual pointer annotations/user-copy boundaries remain.
  ARM/ARM64 API-29 comparisons preserve 62 size/alignment/offset constants.
  A minimal negative sparse fixture still reports a genuine user-pointer dereference.
  Existing KGSL kernel-doc parameter names/delimiters were corrected separately.
- HBM dispatch returns `-EINVAL` for unknown commands instead of an uninitialized
  value. All four supported operations retain forwarding and backend results;
  20 source-extracted ASan/UBSan cases pass. The same-file helper is private.
  Alioth does not establish runtime coverage of other panels' FOD/HBM commands.
- DSI's logging wrapper already supplies the controller index; the redundant
  placeholder was removed without changing interrupt programming. Panel readback
  uses byte pointers and `put_unaligned_be32`, preserving the response byte stream.
  The actual old/new functions agree in 49,600 valid chunk/alignment cases under
  ASan/UBSan; a separate 40,000-case store/guard test passes. Register reads and
  packet selection are unchanged. This does not certify malformed hardware responses.
- WALT diagnostics use native argument types without casts or changing scheduling.
  Source-extracted format/buffer fixtures cover 1/8/64 CPUs. No overflow was proven;
  no speculative dump-loop rewrite was made.
- Techpack exports recurse only into selected UAPI trees, retaining legacy package
  destinations and independent ownership of core/package export directories.
  Header checks resolve package and core includes, including empty/missing/cyclic
  transitive cases. Both Cirrus platform headers moved byte-identically into private
  includes; no private platform structs are exported as userspace ABI. Calibration
  headers gain standalone Linux types/ioctl dependencies; ARM/ARM64 layouts agree.
  FUSE's BPF declarations now include Linux types for userspace too; 74 ABI constants
  across ten structures remain equal on ARM/ARM64.
- MHI/CPU-list/SPCOM/video/regulator/PD-manager diagnostics now match real arguments.
  The MHI assertion wrapper forwards arguments; a failed register read retains its
  conservative pending-reset behavior (16 mocked handler cases). Regulator retries
  and charging policy are unchanged. Logging fixtures check native variadic types.
- USB-PD declarations share the existing public internal header; the duplicate DWC3
  orientation enum was removed before final verification. Denied selections have
  deterministic errors; failed identical PDO requests are retried while successful
  deduplication remains. Counted vendor sysfs parsing retains the 32-byte capacity,
  valid legacy odd-nibble/zero-padding semantics and existing 0/1/4-word sends, while
  rejecting malformed/incomplete input. Vendor receive paths check scalar/vector
  payload lengths and invalid resistance telemetry. Mocked sanitizer tests cover
  parse/send/allocation failures, retries and 44 receive cases. No malformed frames
  were sent to a charger; no adapter-authentication bypass was introduced.

## Build and checker evidence

- Final normal Alioth Image builds with the checkout Clang 21 toolchain and `-j4`.
  The preceding consolidated implementation also passed modules/DTBs; no config or
  DTS changes followed. A new fresh header install/check on the final source passes.
- A separate reusable W=1/C=2 output has the same resolved configuration as normal
  output. The repaired KGSL objects and LMH/notifier objects pass W=1/sparse without
  diagnostics. Real Kona Techpack checking confirms the repaired DSI code errors
  and address-space errors are gone. A pre-existing missing `roi` kernel-doc entry
  remains in the common DSI file.
- **The broader gates remain failing.** The last completed full-kernel audit of the
  preceding consolidated implementation exits 2. Final GPU/thermal and display
  subtree audits also exit 2. Remaining reports include dispatcher lock-context
  contracts, thermal-core/ADC globals, legacy TSENS unused state, and numerous
  other display diagnostics. A3xx/legacy TSENS compilation is not Alioth runtime
  coverage. No lock rewrite or driver removal is justified solely by these reports.
- Checkpatch is not claimed clean: it reports missing human DCO signatures, the
  required project co-author trailer, two long commit-body lines and two continuation
  alignment checks. No human signature/review tag was invented and no warnings were
  disabled. No tests, fixture binaries or Markdown were added to the kernel repo.
- Upstream implementations were searched; no exact narrow replacement for these
  vendor repairs was established. Related older primary Qualcomm/AOSP code was
  compared, rather than importing unrelated newer driver functionality. No human
  authorship was reassigned. Sparse 0.6.4 and a private newer sparse build reproduce
  the same reduced RCU contract reports; upgrading the checker is not a demonstrated
  fix. Exact upstream RCU-annotation candidates remain unapplied pending access review.

## Phone acceptance and restoration

The final published kernel was temporarily booted with the original rooted ramdisk.
The observed kernel suffix matches the published source. No partition was flashed.
SELinux remained **Enforcing** throughout; `mi_thermald`, LMH and TSENS remained active.

- 32/64-bit ordinary-app GPU tests: three fresh processes per ABI at each physical
  60/120 Hz mode, each with 62 native plus six window checks: **816 passes**.
  Actual mode IDs were checked before/after, not inferred from settings. One initial
  60 Hz setup attempt was rejected because the panel still showed 120 Hz; no result
  was counted. Stopping the retained test activity and bounded mode settling allowed
  the final asserted run to pass. This is not an exact-FPS or touch-latency benchmark.
- Three panel sleep/wake cycles passed. Battery stayed below the 45 C test guard;
  cooling devices remained registered. No thermal trip was forced or protection
  disabled; this is not thermal calibration or exhaustive stress qualification.
- A 16 MiB USB push/pull round trip preserved SHA256. Fresh post-marker logs showed
  no new BUG/WARNING, call trace, RCU stall, GPU/SMMU fault or CFI-failure signatures.
- The test APK and owned phone staging files were removed. Normal installed kernel,
  original boot partition hash, 120/120 settings and unset user-preferred mode were
  verified restored. The existing original-kernel shutdown observer and narrow SPU
  unmount live rule were rearmed only for this boot; `initcall_debug` is N. No persistent
  autoload or global permissive rule was added. Intermittent shutdown remains open.

No new real game, external display, headset, charger/DP accessory or inactive-panel
coverage is claimed. Host fixtures do not establish electrical fault handling or
all ABI consumers. A production rebuild is still needed to package the published
source; full strict-audit success is not established.

Private raw receipts/fixtures remain under `~/evo/.repo/kernel-header-walt-20261026`,
`kernel-gpu-display-thermal-followup-20261026`, `kernel-gpu-display-thermal-final-20261026`
and `kernel-gdt-verified-20261026`. They are local evidence, not broken public links;
this record publishes the sanitized source identities, outcomes and limitations.

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
