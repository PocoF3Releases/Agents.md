# Active bus, Wi-Fi and SPS warning repairs — October 27, 2026

> Kernel links were updated to the [finalized history](kernel-history-map-20261027.json). Recorded test identities and measurements remain historical; corresponding rewritten commits are not claims of testing those hashes.

**Source/build/host/device checked.** Thirteen separate commits extend
[the previous tested head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7f23a5259ac1064b488a20875098a3f1189e2fe2)
to [the published tested head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f462c99f563ccdd84c561137593579ea59b82951).
System-side sources, production configuration, warning flags and thermal policy
are unchanged. No suppression attributes, force casts, test files or Markdown
were added to the production kernel. Original authorship/history is retained;
these are local repairs, not claimed human-authored upstream cherry-picks.

## Two actual bandwidth-report defects

`bw_show()` advanced its output pointer but passed PAGE_SIZE on every append.
Enough active clients or long labels could write beyond the sysfs page. Every
append now uses PAGE_SIZE minus the used length. An exact-function ASan/UBSan
fixture reproduces the original heap overflow, then passes empty, single-client,
128 long-client truncation, termination and absent-node cases.

A separate review found registration can increment num_lnodes and reallocate,
copy and free lnode_list under the arbitration mutex while the sysfs reader
accesses it unlocked. Move formatting into an internal arbitration helper
holding the existing mutex across list, label and totals reads. Keep the lock
private and preserve page bounds. The fabric attribute is a small wrapper.
Kernfs active-read draining protects the node during device teardown; no
arbitration-mutex-held removal of this sysfs attribute was found.

A second fixture uses the actual final formatter and a controlled pthread
writer following the allocation owner's mutex contract. The unprotected but
already page-bounded baseline fails its writer-blocked assertion; the fixed
reader blocks registration until formatting completes and passes ASan/UBSan.
This is a host synchronization model, not kernel lockdep or exhaustive races.

The originating [bus snapshot](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a26573f591650e3ddc0262496fd2124d715857b7)
is identified in both Fixes trailers. A comparison with the public
[Qualcomm RPMh source](https://android.googlesource.com/kernel/msm.git/+/faa225852f6b36e9ae0a3d04ff6af5f27216e7f4/drivers/soc/qcom/msm_bus/msm_bus_fabric_rpmh.c)
retained the full-size append pattern; no exact upstream replacement was found
in the checked material. The fixes use existing 4.19 APIs, without importing a
new sysfs framework or altering bandwidth votes.

## Other scoped repairs

- CNSS2 debugfs callbacks follow the existing CNSS2_DEBUG registration guard;
  all features remain available when enabled. Generic-netlink definitions use
  their existing shared header. The debugfs parent uses NULL.
- Bus helpers/state with only local users become private. Encoded DT vectors
  retain `__be32` through existing endian conversion. Remove unread counters
  while preserving division, command generation, failures and vote ordering.
- Rule-engine prototypes move to their common owner header. The notifier-head
  membership comparison uses the RCU access helper under existing serialization.
- SPS directly assigns two already-typed MMIO pointers rather than stripping
  `__iomem`. Accurate parameter/caller/locking documentation resolves 77 SPS
  and 12 bus kernel-doc warnings without deleting documentation blocks.
- SCM QRKS helper linkage and diagnostic types match their actual use.
  Secure-buffer mutex bookkeeping stays local and its unread response copy
  is removed. Existing transport-return and firmware argument policy is kept;
  no new secure-world response interpretation is claimed.

## Build and review evidence

- Normal production ARM64 Image and matching private crypto test module pass
  with checkout Clang `clang-r563880c`.
- Production config remains
  `6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`.
- Image SHA-256: `f93d5fc3e0c5a09116a31e38f73e843a1406bb3b685b97e47e0c778f4a9ff734`.
- Complete configured Qualcomm bus directory plus changed CNSS/SCM/secure-buffer
  and SPS objects: W=1/C=2 exit 0, **17 source checks**, no compiler or sparse
  parser/type errors. Exactly **two SPS FIFO address-space warnings remain**.
  That FIFO API mixes coherent RAM and ioremapped storage; casting them away
  or blanket annotations would misrepresent its allocation contract.
- Separate CNSS debug-enabled output also passes W=1/C=2, with no driver
  diagnostics. Its sole config difference is CNSS2_DEBUG n to y. Production
  config was never changed for that check; debug functionality was not booted.
- Kernel-doc checks pass for the corrected files. Read-only agent reviews found
  no introduced blocker, including the new lock's teardown/order paths.
- Checkpatch retains missing human DCO and the old tool's co-author warning;
  limited inherited alignment/type-style observations remain. No human sign-off
  was invented. This is not a claim of globally clean checkpatch output.

The prior [whole-kernel strict audit](kernel-whole-warning-audit-20261026.md)
still owns broader unresolved diagnostics and coverage limits. Its 1,218
compiler-diagnostic count is a historical baseline, not a newly measured count
after this series. The full-kernel Image strict gate was not repeated here;
**the entire kernel is not claimed W=1/sparse clean**.

## Phone acceptance

The temporary boot ran kernel `39febeb4e337` with the installed ramdisk
preserved, SELinux Enforcing and mi_thermald/audio services active.

- **1704 real bandwidth reads** over 213 attributes in eight rounds,
  maximum 2038 bytes, pass. They overlap the media process for
  approximately 9.9 seconds. No bus state was written or client faults injected.
- Six hardware video encode/decode and 19 PCM capture/playback cases pass.
- 21 crypto/library cases and a generated 4 MiB storage round-trip pass.
  The private module is unloaded and storage fixtures removed.
- **816 graphics checks** pass across 32/64-bit app domains at 60/120 Hz;
  refresh preferences are restored and the private app removed. No new FPS,
  latency, gaming-quality or complete graphics-conformance claim.
- Wi-Fi gateway ping returns 4/4 packets; USB ADB works. Battery health reports
  Good. Thermal protection and its daemon remain enabled.
- Fresh marked logs have no matched BUG/WARNING/panic/RCU stall/CFI or GPU/SMMU
  fault signatures. Raw identifiers, client labels and logs remain private.

The first bandwidth checker used wc's seekable-file size shortcut and observed
4096-byte inode sizes rather than formatter output. That failed harness was
replaced with actual cat-to-pipe reads and rerun concurrently with media;
only the corrected result is accepted. Kernel sources were unchanged for
this harness correction.

Original installed kernel is restored, its slot and boot-partition hash match
the baseline, and exact task staging is removed. A stale Windows ADB transport
after reboot recovered by restarting its server, without another device reboot;
this does not establish a general kernel USB diagnosis. Tests are bounded, not
fault-injected kernel concurrency, external peripheral or secure-firmware
certification. Old GPU/display/shutdown and other driver limits remain open.

## Feature commits

| Commit |
| --- |
| [soc: qcom: msm_bus: bound bandwidth report appends to the page](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a4cbad68ca91be95ec2a8677aa26e0513bb4de84) |
| [net: cnss2: match debug callbacks to their feature configuration](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e4b0f813a2b0870ae3e9f04f188d4a6fdca0170c) |
| [net: cnss2: include the shared generic-netlink declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e143ec5f43258a7322bb832db7a177d4909dffd3) |
| [platform: msm: sps: preserve the BAM MMIO address space](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/749bcd3bf0d1e5ddcd758538d169ee84092f432e) |
| [platform: msm: sps: document BAM function parameters and callers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ec7575faa0e005cc5589bfd1593198462c1da0c9) |
| [soc: qcom: scm: correct private boot-notification contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cc2be2b85f6bfa4f6336bb60d341f74871781804) |
| [soc: qcom: secure_buffer: keep private bookkeeping local](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f3bbfc16b6104c1f921838f2b802e70731a183e3) |
| [soc: qcom: msm_bus: keep implementation callbacks and state private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/93ee18d5453ca8c99c122399cba6b39b8a7a8232) |
| [soc: qcom: msm_bus: remove unread vote bookkeeping](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ce4ab23d4a18951f2ea5f9f5602f278221b552a2) |
| [soc: qcom: msm_bus: type device-tree cells as big endian](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/57f3f3213af693b2e559047af31b84af2a370e91) |
| [soc: qcom: msm_bus: share rule-engine type contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/67766f559528414f47187434e3a757812c2dcca5) |
| [soc: qcom: msm_bus: document bus helper parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9d78e459f6e15ce6c7dbe7c1b408c6ae27e4be72) |
| [soc: qcom: msm_bus: serialize bandwidth reports with client updates](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f462c99f563ccdd84c561137593579ea59b82951) |
