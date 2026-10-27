# RCU and documentation contracts — October 28, 2026

## Published source and main installation

[Final kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d63fdec72e32a820dde97eaac28ae7e9dc1234c6), `aosp-17`, is a normal fast-forward of the
[previous sparse follow-up](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4517f4c402cdeb1f234e23ee61a6646393def8a6). Nineteen feature-separated commits preserve
all prior implementations and upstream authorship. Only 29 kernel C/header
files changed; system-side sources, device trees, vendor files, production
configuration and thermal protection are unchanged. No new tests, logs or
Markdown were added to the kernel repository. Private regressions and backups
remain outside source history.

The exact final Image is installed as main and verified after normal Android
reboot: SELinux Enforcing, taint **0**, CPUs **0–7** online, no private modules
loaded and no CPU-feature variation report or new critical kernel splat.
The active slot's original ramdisk is byte-identical, the complete boot-image
hash matches its tested package, and the other slot's boot hash is unchanged.

## What changed

- **Generic/bit-locked lists:** use canonical typed RCU hlist views in seq_file;
  adapt Julian Anastasov's upstream bit-list typing repair, preserving the
  bit-lock predicate, checked first load, pointer masking and publication.
  All in-tree users of the renamed first-dereference helper were audited.
  The upstream continue iterator has no local consumer and was not added.
- **fsnotify:** retain the existing typed connector alias and hlist views through
  checked SRCU loads. Existing mark references and matching SRCU retirement
  remain. No raw-accessor replacement or generic-list layout change.
- **SELinux cache eviction:** read the writer-owned backward tail with
  list_last_entry under the existing cache spinlock, retaining an explicit
  lockdep assertion. Forward RCU traversal and deferred free remain unchanged.
- **QRTR/rmnet/NAT/TC:** snapshot QRTR slot identities through RCU and its final
  flow pointer under the existing mutex; correctly qualify and declare rmnet's
  exported callback and preserve its exact callable type; retain NAT array
  element and TC previous-link qualifiers. Comparisons and publication match
  the actual protected interfaces without inventing new locks.
- **LLC/socket initialization:** LLC's callback is immutable before its SAP is
  published and remains inside the pinned SAP lifetime; READ_ONCE describes
  that field correctly. Plain socket user-data/waitqueue fields are initialized
  before publication rather than being treated as concurrently replaced RCU
  pointers. Existing concurrent accessors elsewhere are retained.
- **XFRM:** adapt Sabrina Dubroca's current upstream per-netns socket repair.
  Request replies use the sending socket's real namespace-reference condition;
  asynchronous listeners/multicast keep their RCU/NULL checks. This avoids the
  older reverted approach that put request unicasts inside RCU. The source
  condition is inline because this older lockdep-disabled macro discards it;
  no unused local or suppression is needed. Afinfo identity uses the proper
  accessor under its existing writer lock.
- **TC protocol boundary:** carry `__be16` through private create/find/request/
  dump interfaces. The native-u32 tcm_info ABI contains priority in its high
  bits and the already network-order EtherType representation in its low bits.
  Two explicit representation bridges occur only at extraction/serialization;
  they preserve all bits, with no byte swap or blanket comparison cast. These
  are real UAPI boundaries, not an escape around RCU address-space checking.
- **Documentation:** correct 112 parameter/name/return descriptions across
  Binder, block, PM, CPUfreq and SELinux. Non-comment bytes are identical in
  all 13 documentation files. Existing parameter continuations were reviewed
  and retained; no marker deletion or parser filtering reduces the count.

These changes repair interface contracts; a sparse mismatch alone is not proof
of a reproducible runtime use-after-free. Source review checked publication,
reader protection, reference ownership and retirement rather than assuming
annotations alone prove lifetime safety.

Original human upstream sources: [bit-list typing](https://github.com/torvalds/linux/commit/1ac252ad036cdb18f5fb7f76bb6061adfed9cedf),
[XFRM namespace lifetime](https://github.com/torvalds/linux/commit/d87f8bc47fbf012a7f115e311d0603d97e47c34c).
Original authors, dates and existing upstream trailers are retained; adaptation
notes do not claim that upstream reviewers reviewed the different backport.
Independent source review found no material blocker in the accepted changes.

## Build, sparse and documentation evidence

Complete production Image with the checkout toolchain, **W=1** and existing
global **CONFIG_CC_WERROR=y** passes with **zero compiler diagnostics**.
Configuration SHA-256:
`0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`.
Image SHA-256:
`d08a24c8c5caad5b69c283a41ed3e5fdda631bf4ef42c7236e7a94e6a4cf8e5b`.
No configuration or compiler-warning policy changed; no defconfig regeneration
was needed. Existing CFI, SCS, KFENCE and thermal protections remain enabled.

The synchronized unlimited `C=2` comparison is **3,012 diagnostics / 38 errors →
2,989 diagnostics / 16 errors**. It removes **28 baseline rows**, including
**22 errors**, and newly exposes **five open lock-context warnings**. The net
reduction is 23 reports. No zero-additions or sparse-clean claim is made.
The [site ledger](kernel-rcu-contract-errors-20261028.json) links every resolved
baseline site, all remaining errors and the newly visible contexts.

All five contexts concern byte-identical files: three in fs/dcache.c, and two
in net/xfrm/xfrm_state.c/include/linux/rcupdate.h. Conditional inode-lock release
and conditional RCU acquisition/return complicate their checker contracts.
Whole-file Git blob equality is recorded, but is not exhaustive correctness
proof; these reports stay open rather than changing lock behavior to clear them.

The same **455-file** kernel-doc baseline changes **2,840 → 2,728 diagnostics**.
This is not all-tree documentation closure. Strict checkpatch has no source
errors; it still reports missing human Signed-off-by metadata on local changes,
coauthor/legacy spelling and style findings. No DCO certification was invented
and no checker flag hides those reports.

Host tests exercise the actual extracted TC helper/UAPI macros/packing expression
in **524,288** combinations covering all EtherTypes, priority boundaries and
little-/big-endian representation models. Every existing bit pattern and zero
wildcard is retained; 522,240 incorrect byte-swapping combinations are rejected.
This is a host model, not big-endian hardware acceptance. ASan/UBSan and strict
host compiler warnings pass. Private final-head negative cases still diagnose
untyped seq, fsnotify, rmnet and bit-list misuse; their raw diagnostics remain.

## Exact-image phone acceptance

With SELinux enforcing:

- **640** actual kernel list-iterator checks across 64 rounds, using local lists
  and the exported seq iterator; the private module unloads.
- **128** inotify create/delete events across 64 rounds.
- **192** XFRM requests across 16 disposable network namespaces: information,
  dumps, absent-object errors, private policy/SPI creation and read replies,
  followed by namespace teardown. No normal VPN/network state is changed.
- **48** TC add/replace/delete operations plus **16** dump round trips for IPv4,
  IPv6, ARP and all-protocol classifiers on a private namespace's loopback.
- Prior mincore, ptrace and address-only SMEM probes pass; no shared payload is
  dumped or modified. Recording/playback, video, BPF, fork/COW, media pointer,
  pmsg and owned-storage comparisons pass. Crypto/library, notifier and RCU
  regression modules pass and unload.
- Three ordinary-app GPU runs per ABI pass 62 native and six window checks per
  run, for 32 and 64 bits. This is finite rendering, not FPS/game certification.
- The TCP restricted-selection/reference test passes. Wi-Fi reconnects with
  IPv4 on temporary and persistent final boots. Normal battery health is Good;
  audio and thermal services run without a new critical splat.

The first normal-boot ADB wait timed out. Restarting the existing Windows ADB
server restored access; Android then passed all persistent-identity/hash/health
checks. No USB source change or permanent fix for intermittent host reconnects
is claimed. The GPU APK, owned fixtures/private modules and packaging staging
are removed; boot backups and host receipts remain. ADB-only app verification
remains disabled per the user's setting, with other verification settings intact.

## Remaining findings and limits

**16 sparse errors and 2,728 kernel-doc diagnostics remain**, plus the five
newly visible context warnings already included in the sparse total.

| Remaining error group | Sites | Unproved obligation |
| --- | --- | --- |
| Sighand/PID pointers | 4 | Complete field/producer/reader typing, including already-referenced users |
| Fasync | 2 | Public double-pointer API and many owner/close/teardown contracts |
| POSIX ACL | 2 | Inode fields, sentinel/CAS handoff and filesystem consumers together |
| Swap mapping | 1 | Published array plus ownership-proven direct-index helper callers |
| Generic RB trees | 4 | RCU/RTNL caller protection without weakening conditional checks |
| NF netlink | 1 | Whole socket publication/read/request/exit interface |
| Slimbus/Axon | 2 | Mixed RAM/MMIO and transport reference acquisition/lifetime |

A possible Axon zero-reference acquisition concern remains unproven; RCU delays
free but does not by itself authorize resurrecting a zero kref. External
serialization and active Alioth exposure have not been established. Compilation
of the optional microvisor backend is not proof that this phone binds it.
The previously identified optional Slimbus mapping/device-ownership limitations
also remain open. No speculative optional-backend rewrite was applied.

No broad fasync field migration, partial PID/ACL annotation, fabricated
protected-condition, unchecked RCU load or blanket cast was used to force
closure. No complete ROM/VTS, out-of-tree module source API, live swapoff/OOM,
exhaustive concurrency, modem endpoint teardown, headset or deep-suspend
certification is claimed. Raw device logs and test sources stay private under
`~/evo/.repo/kernel-sparse-final-20261028/`. Thermal protection remains enabled.

## Feature-separated history

| Change | Original author |
| --- | --- |
| [seq_file: Use typed RCU links in hlist iteration](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7520159fe818782ce0fea17af481071981d2d7d1) | johnmart19 |
| [rculist_bl: Preserve RCU types in bit-locked list accessors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/46ef3f4bffacfdb16419cab259d89f41ec62adb0) | Julian Anastasov |
| [fsnotify: Preserve connector and hlist SRCU types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7a139101a3fb39f187b442c391007c288fa80410) | johnmart19 |
| [selinux: Read cache tails under their writer locks](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3e9b3ee8ccee85a8c44ff262fc8eaee014b6ccdc) | johnmart19 |
| [qrtr: Snapshot radix slot identities through RCU](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7d49bae5cf6d95f1c95fc9483bde1359b7fc42dd) | johnmart19 |
| [net: rmnet: Put the RCU qualifier on the slow-start callback](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/000f8e58a8a5bfb451cd87cbefa099255e236508) | johnmart19 |
| [llc: Read the immutable receive callback from its pinned SAP](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9977b1024dfcf6ede0386970398464d10415a4c1) | johnmart19 |
| [netfilter: Preserve RCU element typing while registering NAT protocols](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b4b0e20ca9d219e517aef4dc126ac7c7078fef60) | johnmart19 |
| [net: sched: Preserve RCU chain link types under RTNL](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5f09f9cc99958d6617786c83ecd30a20c4723645) | johnmart19 |
| [net: Initialize unpublished socket fields with their actual types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d41a1f230895d3a69153004ec7c0e94ee78979a9) | johnmart19 |
| [xfrm: Read afinfo identity through the RCU accessor](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a37fc7e1a033d05a768dfdd0d405b7c63489ed0c) | johnmart19 |
| [xfrm: avoid RCU warnings around the per-netns netlink socket](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/76cd2431dfce7e0570764c296cc8e598dc4434ff) | Sabrina Dubroca |
| [binder: Match kernel-doc to current transaction and allocator contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e5f114e5cec0f72e9687071018017bf50b0ec8c2) | johnmart19 |
| [block: Describe delay, service and device-number helper parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3386c6adbc8b4ca49013e522910e74532e0b53a4) | johnmart19 |
| [PM: Document current domain, timer and wakeup callback parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/83aae92649d05b476092984e45b80a0c3a545fff) | johnmart19 |
| [cpufreq: Describe sysfs and policy helper parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/61c220505c2857dbfa13ebca8253f7dd3e7af584) | johnmart19 |
| [selinux: Document security-server state and output parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ebb912d81258e1e6729bbe04374dd1f7ddb2595f) | johnmart19 |
| [selinux: Match AVC kernel-doc to stateful permission interfaces](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ada6ab3ad69f65fd58e714e095f2bfa1e8c12799) | johnmart19 |
| [net: sched: Keep classifier protocol types through the UAPI boundary](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d63fdec72e32a820dde97eaac28ae7e9dc1234c6) | johnmart19 |
