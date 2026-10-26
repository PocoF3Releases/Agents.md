# Full-kernel warning continuation — October 26, 2026

Baseline eb8826a50995; final source a2be591af2b4. The configured Alioth kernel
received a complete `make -k -j6 W=1 C=2 Image` pass before and after these
repairs. Both full strict passes **fail**; this is progress on the audit, not a
whole-kernel clean bill or release certification. No system-side sources,
configuration, thermal policy, firmware or userspace drivers changed.

## Separate fixes

- [fuse: Correct BPF reply argument contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/265cd8a21635b229a4e1968e48bd55dadae94d2b).
- [net/sysctl: remove leftover __user annotations on neigh_proc_dointvec*](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6914d230b94b0bf48a21615a8213a59581e68bc6).
- [net: Declare the shared zerocopy iterator helper](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/dd1dd07e0460e35fe48d8c047004f42d38738484).
- [bpf: Declare global calling-convention test targets](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/80e487c1a6a438bf090aaa90321dd4a364dd497c).
- [qcacmn: Properly abstract the Linux bottom half interfaces](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2d2981a5b93d3d929e693e1336f736ea87a9dd91).
- [wifi: cnss2: Correct event and QMI diagnostics](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/75d9915589cbe980ad21de3bdc399c93afb71756).
- [drm: msm: rotator: Match private callback contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/320ff8c31ed53381fc362da1be117657f55cea2c).
- [drm: msm: pll: Validate retained DFPS tables before use](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c3935abdcb21ca7831626ea2984d0ae0a52930ef).

The neighbour declaration patch is Christoph Hellwig's exact
[c7388c1f8fb6](https://github.com/torvalds/linux/commit/c7388c1f8fb6d8687403e9554c873f9df4512797),
following the existing kernel-buffer sysctl backport. Its stable patch ID and
original author/date/trailers are preserved. Existing cross-function neighbour
lock-context warnings remain separate; no lock behavior was changed.

Jeff Johnson's Qualcomm
[acc4c1baae73](https://github.com/LineageOS/android_kernel_sony_sm8450-modules/commit/acc4c1baae736a4ad4effe6290dc706c2aed9004)
replaces an incompatible tasklet callback cast with a typed QDF adapter. It
preserves callback/argument identity and uses the existing tasklet API, with
source-context adaptation, comment spelling and export spacing recorded.
Original authorship is retained. QDF public wrappers already return void; direct
HIF tasklets use other types. This kernel enables CFI, so signature correctness
matters; no general firmware or Wi-Fi performance fix is inferred.

The FUSE BPF STATFS initializer advertised an 8-byte pointer rather than the
80-byte native reply. It now describes the full object and has one output-count
initializer. Pointer finalizers return NULL explicitly. No exact narrow human
upstream replacement was established; a broad newer FUSE API rewrite was omitted.

CNSS logging now supplies the missing MAC-response error argument, prints the
registration error value and uses native unsigned-long formats. Event flags keep
gfp_t. A private IMS helper and unused pure country getter are cleaned up;
regulatory filename selection, retries and recovery policy remain unchanged.

BPF global noinline calling-convention targets retain their signatures/visibility
and gain an internal declaration header; the old GCC-only warning suppression is
removed. The exported zerocopy iterator helper gains its shared declaration,
without data-path changes. Rotator polling uses __poll_t and two same-file helpers
are private. No hardware mode or request-cleanup logic changes.

PLL retained DFPS input is decoded with OF endian/address-cell contracts and
validated before its existing 32-bit mapping/free interface narrows it. Short,
high-address and crossing regions are rejected without mapping or releasing
untrusted physical memory. Allocation failure returns -ENOMEM. Counts above the
16-entry table are rejected before consumers can iterate out of bounds. Normal
RAM mapped with PAGE_KERNEL is copied with memcpy. Valid Kona mapping attributes
and existing reserved-memory release flow are preserved; high-address support is
not claimed. The actual source region, 0x9e300000 plus 1 MiB, remains accepted.

## Static, host and build evidence

The final pass emits 9,499 unique diagnostic records keyed by source path, line,
severity and text. These include compiler, sparse and kernel-doc findings and
are not 9,499 proven runtime bugs. Many are shared-header diagnostics, deliberate
initializers or lock-context patterns that require individual review. They are
not deleted or suppressed to obtain a passing whole-tree result.

Ten changed implementation objects have no diagnostics in the final log: FUSE
backing, BPF test_run, net datagram/skbuff, CNSS main/QMI, QDF defer, PLL utilities,
and rotator core/device. The neighbour source still has its separate context
warnings. Strict checkpatch has no errors/checks and retains the upstream QDF
abstraction's typedef style warning. Generic API heuristics that require newer
kernel versions were not blindly applied to 4.19.

Private regressions establish:

- Exact-source FUSE initializer: pinned baseline fails the 80-byte expectation;
  committed function passes, including opcode/count/node ID/output pointer and
  zero initialization. External inode access is mocked.
- MAC error formatting: baseline fails compile-time format checking; corrected
  result/error arguments print the expected values.
- Extracted QDF adapter: strict Clang plus ASan/UBSan checks dispatch, argument
  identity, independent instances, repeated scheduling, kill routing and missing
  callback handling. This is not a hardware tasklet lifecycle certificate.
- Exact PLL parser: 17 mocked cases cover valid Kona, one/two address cells,
  truncated/short/crossing regions, invalid counts, missing nodes/addresses and
  allocation/mapping failures. The baseline fails assertions; the final function
  matches the passing candidate modulo whitespace. Mocks verify call flow and
  arguments, not real MMU/PFN ownership or injected hardware failures.

The final normal Image passes with checkout Clang 21 at -j6. Configured modules
and all selected Kona DTBs/Alioth overlay pass; this configuration reports zero
loadable modules. The additional headers_check target **fails**: techpack traversal
exports internal audio headers instead of restricting itself to intended UAPI
paths. That exporter defect requires an ABI-aware follow-up. Do not silence
private driver declarations or simply flatten separate installs: the installer
can remove headers it thinks another invocation does not own. No headers or
consumer APIs were removed in this batch.

## Phone acceptance

The exact candidate boots temporarily with SELinux enforcing, stock graphics
libraries and mi_thermald running. No partition is flashed. Kernel and unchanged
rooted-ramdisk hashes are verified after repacking. Raw Image SHA-256:
`d1c139df705a248b5832bff9442f910169c8993419394a5e58e2dda3558800d1`.

- Both installed baseline and candidate pass 512 real LAN TCP echo rounds,
  verifying 16 MiB each way. wlan0 counters confirm the candidate uses Wi-Fi,
  not ADB reverse/USB forwarding. Synthetic data goes only to the local PC.
- Both pass FUSE statfs/fstatfs and a self-cleaning owned 16 KiB file integrity
  test on emulated storage. This does not prove the specific BPF-dispatched
  STATFS path is attached in the running mount; its size defect is host-proven.
- Both load/run an isolated socket-filter BPF program ten times with expected
  result/payload, then close its FD. No program is attached and no traffic sent.
  This does not certify BTF fentry attachment on this configuration.
- Candidate rendering passes six processes at physical 60 Hz and six at 120 Hz,
  three per ABI/mode. Each passes 62 native and six window checks in untrusted_app,
  including mappings, GLES/Vulkan submission/readback and presentation. Active
  mode is asserted before/after. This is functional coverage, not measured FPS,
  exhaustive game compatibility or a claim to resolve historical GPU faults.
- Read-only CPU/GPU sensors and cooling registration remain available. Thermal
  service stays running; representative GPU readings rise from about 33–34 C to
  40 C during tests. No limits/governors are changed and no trip is forced.
- No new BUG, WARNING, call trace, RCU stall, GPU/SMMU fault or CFI failure appears
  after the candidate test marker. Original refresh bounds and unset preferred
  mode are restored.

All eight commits are pushed on aosp-17 through a2be591af2b4. The phone is back
on its installed d2c680 kernel, enforcing and boot-complete, with the original
boot-partition SHA-256 unchanged. Retained pstore records normal-priority reboot
callbacks and perf teardown returning (about 5 ms), followed by restart. This is
one healthy restart, not proof of the intermittent shutdown cause.

Owned app/native probes, phone staging and Windows temporary image are removed;
the two-session local echo server finishes and exits. The original-kernel
shutdown observer and narrow SPU unmount live rule are rearmed only for the
current boot. No persistent autoload or permissive policy is installed. Windows
ADB server refresh recovers transport after boot without another phone reboot.

## Continuing work

Full strict compilation, header export and wider subsystem warnings remain open.
A private next-batch WALT format repair has source/host evidence but is not in
this published candidate. Prebuilt/device-tree audit is not substituted for the
unfinished kernel requirements. No claim that every possible kernel bug is fixed
follows from these scoped checks.

Raw commands, full logs, diagnostic inventories, fixtures and receipts remain in
`~/evo/.repo/kernel-full-audit-round2-20261026/`. No device identifiers, private
network addresses, raw logs, boot images or permanent diagnostic tests are
published with the kernel changes.

Historical test IDs retained; [kernel history mapping](kernel-history-map-20261026.json).
