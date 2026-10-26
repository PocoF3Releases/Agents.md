# Active-driver fixes and main-kernel installation — October 27, 2026

**Source/build/host/device checked; full W=1 gate failed.** This continues
[the prior active-driver series](kernel-active-driver-fixes-20261027.md).
Five separate local feature commits preserve all prior history and human
upstream authorship. Only kernel source files changed; Android system-side
sources, production config, warning flags and thermal policy are unchanged.
No warning suppressions or production test files were added.

## Final changes

- Qualcomm service-notifier QMI tables assign the terminal TLV field once and
  have private linkage. The prior duplicate array_type assignment used another
  zero constant. All nine tables / 26 elements remain field-for-field equal,
  including offsets, type/length fields and nested-table presence.
- Service-notifier unregister rejects ERR_PTR handles with IS_ERR before
  accessing the notifier-list member. Pointer comparison against integer zero
  did not implement that contract. Valid unregister and NULL handling remain.
- GPI DMA keeps actual register pointers typed as MMIO through register tables
  and EE base adjustment. Private callbacks/state stay local. Unread descriptor
  conversions are removed, and debug-only strings follow their existing logging
  consumer's configuration. Coherent ring memory is not relabeled as MMIO.
- NCM converts the little-endian setup version before extracting its bytes.
  This preserves Alioth's existing little-endian behavior.
- Four UAC1 configfs volume/mute readers return -ENODATA for an absent control
  instead of formatting an uninitialized local. Bound successful values and
  unbound empty reads retain their prior behavior.

These are local repairs, not claimed exact human-authored upstream imports.
Existing human commits and trailers were not rewritten.

## Checks and strict-build limitation

Affected service-notifier, GPI, NCM and UAC1 objects pass W=1/C=2 with checkout
Clang clang-r563880c and sparse 0.6.4: no diagnostics in the final scoped log.
Strict checkpatch finds no code/style issue; missing human DCO and this old
checker's unsupported Co-authored-by trailer remain. No sign-off was invented.

Host ASan/UBSan fixtures extract the actual functions. The baseline notifier
fails the invalid-handle assertion; the fixed version rejects error handles
and preserves a successful unregister. Baseline UAC1 fails the missing-selector
assertion; the fixed functions pass 20 unbound, missing-selector/control/getter
and valid-result checks. Host fixtures stay outside the source repository.

An isolated GPI debug-enabled config compiles with W=1; its sole config delta
is QCOM_GPI_DMA_DEBUG n to y. Sparse still reports MMIO pointer loss in that
variant's existing debug-log records; generated host parser conflicts also
remain visible. This alternate config is not the production image or a claim
of globally clean sparse output.

The **full Image W=1 target was run again at the final source** with the
unchanged production CONFIG_CC_WERROR policy. It exits **2**, with **1,138
parsed compiler diagnostics across 352 files**. Core syscall tables, ARM64,
IPA and Wi-Fi are among the remaining owners. This is an attempted full-target
build, not a successful strict Image, exhaustive diagnostic count, or proof
that all these warnings are runtime bugs. No error policy was lowered to pass.
The broader [whole-audit limits](kernel-whole-warning-audit-20261026.md), including
the SPS mixed-memory FIFO contract, remain open.

The normal production Image and matching private test modules pass. **The
installed artifact is this normal build, not a successful W=1 build.** Its
configuration SHA-256 remains
`6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`.
Image SHA-256:
`9e031e623b78259d82dffefcb3306a3a1fd819f05a442a80baff29614f8165fd`.

## Phone acceptance and persistent deployment

The tested source is [a028da5feaa0](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a028da5feaa05034c7cf8d3956cf36c94f25a961).
The existing Magisk ramdisk was preserved; the candidate kernel and unpacked
ramdisk hashes were checked before boot. On-device acceptance passes:

- Six hardware video decode/encode and 19 PCM capture/playback cases.
- 21 crypto/library cases and a generated 4 MiB storage round-trip; the private
  module and generated data are removed.
- Four invalid notifier-handle checks invoke the actual exported kernel API;
  the private test module is unloaded afterward. No subsystem crash or restart
  was injected, and valid registration lifetime is not exhaustively tested.
- Wi-Fi gateway ping receives four of four packets; USB ADB operates and GPI
  driver binding is observed. Battery health is Good, SELinux Enforcing and
  mi_thermald/audio services remain running. Thermal protection stays enabled.
- Fresh post-test logs have no matched critical kernel fault signatures.

After these tests, the package was **flashed to the active boot slot**. The
written boot-image prefix hash matches the tested package. Android boots on
`4.19.325-cip136-st20-perf-ga028da5feaa0`, then survives an additional reboot
with the same installed image, four-of-four Wi-Fi ping, Good battery health,
Enforcing SELinux and the thermal daemon running. Task-owned device staging is
removed. The original boot backup remains private for emergency recovery;
**the previous kernel was not restored**. The newest verified kernel is the
maintainer's development baseline, unless a real regression requires rollback.

A broad final boot-log filter initially also matched the substring in PMIC
"debug" status and early userspace console/linker/debugfs/capability notices.
Those raw messages and the failed filter result are retained privately. The
final classification distinguishes kernel BUG/WARNING splats, stalls, panics,
CFI and GPU/SMMU faults from these notices; no matching kernel fault is found.
This is not a claim that early userspace notices were fixed or logs are empty.
No source warning or compiler flag was suppressed for log classification.

Physical USB-audio/MirrorLink endpoints, rare concurrent teardown and all
external peripherals are not certified. The intermittent shutdown investigation
and full W=1 backlog remain open. No new full ROM ZIP was built or installed by
this task, and this record is not a complete production-release sign-off.

## Feature commits

- [soc: qcom: service_notifier: correct private QMI descriptors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/39d91cd07829d0dfaec2df700dd09dc90c4d6765)
- [soc: qcom: service_notifier: reject error handles on unregister](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/45c179303f5698decfbf27e9fa4ec4b6d8873964)
- [dma: qcom: gpi: preserve register address-space contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bd9508d660c4dfaa9ca4d1b285ea73e69fb13669)
- [usb: gadget: ncm: decode MirrorLink version in CPU byte order](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/8566844c80d5960ee7e92dbad5778b4c4c3d2e8a)
- [usb: gadget: uac1: reject missing controls in configfs reads](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a028da5feaa05034c7cf8d3956cf36c94f25a961)
