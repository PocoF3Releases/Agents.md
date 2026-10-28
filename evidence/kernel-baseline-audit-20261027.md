# CPU feature and baseline sparse audit — October 27, 2026

Historical acceptance. The [October 28 follow-up](kernel-sparse-followup-20261028.md)
now owns the current kernel and diagnostic counts; this record preserves the
original CPU investigation and test scope.

## Published source and installed kernel

[Current kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/68fe321774661c4150b80edd93f7ddc75f32ac06) on `aosp-17` is a fast-forward of the
[prior acceptance](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e9b1eaf8af938cf9a7413f17e6f61d94fc2ffbcf). Twenty feature-separated commits preserve
original upstream authorship and dates. Only kernel sources and this workhub
changed in this task; production configuration, system-side sources, thermal
protection, CFI, SCS and KFENCE are retained. No new suppressions or blanket
address-space casts were added.

The exact Image is installed as main in the active slot and verified after a
normal Android reboot. Its full boot-image hash matches the package. The
active slot's existing ramdisk is preserved byte-for-byte, and the other slot's
hash is unchanged. An old slot-A installation record failed the guard before
writing; the actual slot B was backed up, its different ramdisk preserved, and
all phone gates repeated on that package before installation.

## CPU variation: cause and repair

**Source-checked and device-tested:** read-only register probes captured 30
feature registers across all eight cores. A55 raw CTR was `0x84448004`; A77 was
`0x9444c004`. All cores had CLIDR `0xc3000123`: LoC=3, LoUIS=0, LoUU=0, so the
architectural effective IDC value is 1 on both clusters. The old code compared
raw CTR rather than the effective cache-maintenance requirement. The
Suzuki K Poulose upstream repair also preserves the required user CTR trap/
emulation behavior; neither the warning nor taint is cleared artificially.

The remaining differences concerned privileged AArch32 ISAR4/PFR1 fields when
the sanitized system cannot run AArch32 EL1, plus the CSV2 field omitted from
the old PFR0 table. Will Deacon's field/capability/check series and Anshuman
Khandual's PFR0 definitions address those precise architectural cases.
AArch32 EL0 guards, KVM gating, unknown-field strictness and existing capability
numbers are retained; the new internal capability uses a previously reserved
slot without renumbering `NCAPS`. KVM-enabled variants are compile-tested;
production KVM is disabled and has no live acceptance here.

The captured-register model changes 16 strict mismatches to zero. Host tests
cover 2,135 CTR/cache/UCT cases and 1,864 field-boundary cases, including negative
strictness checks. On the final phone boot, all eight CPUs are online, the
variation report is absent and kernel taint is **0**. A per-core self-modifying
code/cache probe passes **1,024** cases. EL0 CTR exposes IDC=1 on both clusters;
the allowed non-strict L1IP difference remains. This is not a claim that the
physical cores have identical features or that every supported board is tested.

## Verified fixes

- **Virtual-service access:** replace bitwise masking of a boolean with logical
  tests, restoring read/write open-mode rejection while preserving the LSM
  decision. Extracted actual-code tests change 14 failing combinations to zero
  across 32 cases.
- **Block errors:** convert six negative errno assignments through the real
  `errno_to_blk_status` API instead of truncating them into `blk_status_t`.
  The seven-status regression changes five failures to zero.
- **Poll callbacks:** UIO, nanosic, DVB, QBT and USB GSI return error event masks
  rather than negative errno/negative event constants. Callback and local mask
  types match `__poll_t`; normal readiness bits are unchanged. The full sparse
  rerun caught incomplete types, which were fixed within their original feature
  commits. UIO's four extracted ready/quiet/error cases now pass.
- **Kernel-buffer contracts:** writeback/IPv6 sysctl signatures and keyring read
  callbacks match their actual kernel-buffer callers. The final copy-to-user
  boundaries remain. Audit annotates its actual RCU-published global pointer;
  this removes six error reports without changing its layout or locking.
- **CFI:** allocation failure safely publishes NULL and uses the existing checked
  address lookup instead of dereferencing NULL or retaining a stale shadow.
  Helper parameters accept already-dereferenced protected snapshots; the global
  publication remains RCU-typed. Shadow retirement uses the grace period matching
  explicit scheduler-RCU readers. The partly backported RCU flavor unification
  is insufficient reason to assume all special-unlock paths are equivalent.
  Eight extracted allocation/update scenarios pass ASan/UBSan; the old path
  fails on NULL. Live OOM and exhaustive RCU race reproduction were not attempted.
- **TCP:** reject forbidden namespace defaults before acquiring module/BPF-owner
  references. An extracted 10,000-denial test changes 10,000 leaked references
  to zero. The phone passes 32 denied selections plus an allowed positive control
  in a private namespace; module refcount stays zero and the module unloads.
- **Wi-Fi:** replace an unaligned eight-byte native-word IPv6 header read with
  an exact four-byte copy and endian conversion. All 20,000 classification cases
  preserve their result; the boundary guard fails before and passes after.
  This does not claim complete truncated-packet or SNAP-path validation.

The CFI allocation repair is adapted from Sami Tolvanen's upstream work; TCP
uses Zhiling Zou's public fix and Eric Dumazet's permission-first ordering
recommendation. Adaptations are identified in their commit bodies rather than
claimed as exact donor patches. Independent source review found no material
blocker in the final core, CPU, WLAN or poll changes.

## Sparse accounting and unchanged findings

The immutable baseline has **3,140 unique diagnostic rows**, including **127
errors**. Every row has a private source/owner/classification entry. Error sites
are published in the [127-site ledger](kernel-baseline-sparse-errors-20261027.json).
The final synchronized-per-target `C=2` run uses sparse's unlimited warning
setting and reports **3,098 diagnostics / 119 errors**, with **42 baseline rows
removed and no new rows** after source-line mapping. Exit zero does not mean
that sparse is clean.

Eight error reports are resolved: six audit pointer-contract reports and two
sysctl signature mismatches. Of the remaining 119 errors, **115 remain
unresolved** (111 core/net and four mixed-origin driver reports); four more are
known type-contract reports. The [23-group source review](kernel-baseline-sparse-unchanged-20261027.md)
records actual reader/update/free edges, exact IDs and unproved caller obligations.
No unchanged error is dismissed merely because it predates this work.

Remaining baseline classifications are 1,926 unresolved, 598 type-contract,
550 type-only and 24 source-supported checker/encoding limitations. These
categories are triage, not certification of runtime safety. The generated
configuration string exceeds sparse's parser string limit; extraction from
the built Image preserves the complete original configuration. Conditional lock
returns, intended integer extraction/serialization and dead narrow cmpxchg arms
have separate source explanations. Reports stay visible; no source casts or
warning filters hide them.

Mixed RAM/MMIO Slimbus/SPS/SMEM origins still need producer/consumer-aware work.
A conditional Slimbus context-bank allocation/free-device mismatch is recorded,
but no active Kona context-bank route or target corruption is established;
no speculative optional-backend refactor was applied. Generic RCU callback and
list annotations also retain incomplete caller/teardown proof.

## Build and device verification

**Build-tested:** complete production Image with `W=1` and existing global
`CONFIG_CC_WERROR=y`: **zero compiler diagnostics**. Config SHA-256:
`0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`.
Image SHA-256: `b76912c8afc53b628a809bfa987416300a69423719761849b0b40cd7be8bc859`.
Targeted object/sparse replays, negative annotation probes and the complete
unlimited sparse comparison are retained privately. Configuration was not
changed, so no defconfig regeneration was needed.

**Kernel-doc limit:** the full rebuild still emits **2,993 inherited kernel-doc
diagnostic lines**, plus parser notices. These are separate from compiler and
sparse counts. Reported contexts in task-modified files are unchanged from the
baseline. This pass prioritizes verified correctness defects; it does not claim
kernel-doc closure. Strict checkpatch has no errors; the old checker still flags
the required coauthor trailer, legacy scheduler-RCU spelling, and minor
alignment/message-format findings. None is hidden by a source suppression.

**Device-tested, exact final head, enforcing:** six video cases, 19 PCM cases,
21 crypto/library known answers, four invalid notifier cases, nested Tasks Trace
synchronization, eight exit-stress rounds/256 transient readers, 896 BPF checks,
128 fork/COW cycles, invalid media pointers, 64 pmsg writes and an owned 4 MiB
storage comparison pass. Three ordinary-app GPU runs per ABI each pass 62 native
and six window checks; these are finite rendering checks, not FPS/game
certification. CPU/cache and TCP checks above pass. Wi-Fi reconnects with IPv4
after toggling and after normal main-kernel boot. Battery health is Good;
audio and thermal services run with no new critical splat.

All private modules, probe executables, fixture files, the hash-verified GPU APK
and packaging staging are removed. Boot backups and host receipts are retained.
Per the user's separate request, ADB-install app verification is disabled on the
test phone; other installation verification settings are unchanged. This is not
a production source or security-policy change.

No complete ROM/VTS, other-device, headset, deep-suspend, live OOM or exhaustive
concurrency certification is claimed. Virtual-service, nanosic, DVB and optional
backend availability is not inferred from successful compilation. Private
receipts are under `~/evo/.repo/kernel-baseline-audit-20261027/`; public evidence
contains no raw device logs, identifiers or proprietary dumps.

## Feature-separated commits

| Change | Original author |
| --- | --- |
| [vservices: Enforce read and write modes before device I/O](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/81d28fb6041b4131d15a5ac6d40e33ff979fa69a) | johnmart19 |
| [block: vservices: Convert errno values to block status](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/41b38abeb411d098469411791e7928fe378505ac) | johnmart19 |
| [uio: Return an error event when polling an unavailable device](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/aa4fa3117fb5274deeba74591032bdb9205a0007) | johnmart19 |
| [input: nanosic: Return a valid poll error mask](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2e85b2e98ce422f11e33cb92d30e2cc69c220568) | johnmart19 |
| [media: dvb: Return valid poll masks on invalid or removed devices](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/fc872f2c3cf530f64cd37ee1272e005d8fb729ea) | johnmart19 |
| [soc: qcom: qbt: Return error events from invalid poll requests](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/31a79ae9260b9f1cccaed74a7859734f6dd1a468) | johnmart19 |
| [usb: gadget: gsi: Return error events for unavailable control ports](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7e6efe62b8eafa0a42474b7230e08ec8de8d78c9) | johnmart19 |
| [sysctl: Match writeback and IPv6 kernel-buffer handlers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/83829610449f132bd9b6be0df8f20d6129cca7e0) | johnmart19 |
| [audit: Annotate the published audit daemon connection pointer](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c3abc609dfd9eaddd3158661901f5b78cbc3216b) | johnmart19 |
| [keys: Match keyring reads to the kernel-buffer callback ABI](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7afa42cb144f2f1e07b1eb74119a944363de673c) | johnmart19 |
| [cfi: Fall back to checked lookups when shadow allocation fails](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5879e54f793f336dbb027977b5684a133ccccd39) | Sami Tolvanen |
| [cfi: Pass dereferenced shadow snapshots to lookup helpers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/85c19294df92cd487b0141eaa72e8c8987295326) | johnmart19 |
| [tcp: Reject restricted defaults before acquiring congestion references](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e4d4ea54120c7bd3321bbb2cb03c1c317452dd9a) | Zhiling Zou |
| [wlan: Read only the IPv6 word needed for transmit priority](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9fb98e031c308b019f76e30d125d2e0c73e55077) | johnmart19 |
| [cfi: Match shadow retirement to scheduler-RCU readers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/65b360fbc2589446a23810f8ffdfaf64a9c79164) | johnmart19 |
| [arm64: cpufeature: Fix handling of CTR_EL0.IDC field](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e53de41ab8c91e19444099fcf33b12410ddf3039) | Suzuki K Poulose |
| [arm64: cpufeature: Spell out register fields for ID_ISAR4 and ID_PFR1](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/12b38807f8924b14c670e45af7b8a49a9885dc01) | Will Deacon |
| [arm64: cpufeature: Add CPU capability for AArch32 EL1 support](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/01f9639339230eabed332426408654b92cfc9e48) | Will Deacon |
| [arm64: cpufeature: Relax AArch32 system checks if EL1 is 64-bit only](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3c0e40c4b15fde970756ac7f95480001e0fff3fb) | Will Deacon |
| [arm64/cpufeature: Add remaining feature bits in ID_PFR0 register](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/68fe321774661c4150b80edd93f7ddc75f32ac06) | Anshuman Khandual |
