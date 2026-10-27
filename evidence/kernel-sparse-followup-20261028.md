# Sparse and kernel-doc follow-up — October 28, 2026

## Source and installed kernel

[Final kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4517f4c402cdeb1f234e23ee61a6646393def8a6), branch `aosp-17`, is a fast-forward of the
[October 27 baseline](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/68fe321774661c4150b80edd93f7ddc75f32ac06). The 24 feature-separated commits preserve
upstream authorship, dates and existing certification trailers; adaptations
are identified in their messages. System sources, device trees, vendor files,
production configuration, thermal protection, CFI, SCS and KFENCE are unchanged.
No warning filters, `__force` escapes, weakened flags or private test fixtures
were added to the kernel repository.

The exact Image is installed as main and verified after a normal Android reboot:
Enforcing, taint 0, eight CPUs online, no CPU-feature variation warning or new
critical splat. The active slot's original ramdisk is preserved byte-for-byte;
its full boot-image hash matches the package and the other slot's boot hash is
unchanged. Backups and private receipts remain. This is kernel acceptance, not
complete ROM release certification.

## Verified repairs

- **Netfilter callbacks:** annotate actual RCU-published NAT helper, H323, PPTP
  and conntrack-attach slots and match dereferenced local snapshot types.
  Older `typeof(hook)` declarations otherwise inherit the slot's address space.
  Non-NULL publication is ordered; existing NULL teardown and grace periods
  remain. Reader/writer/retirement review, affected translation-unit sparse and
  negative raw-read probes pass. Optional SNMP was compiled privately, not enabled.
- **UDP/module symbols:** preserve the UDP offload snapshot's RCU type; initialize
  kallsyms before publication and use its protected snapshot under the existing
  module lock. UNFORMED visibility and matching scheduler-RCU retirement remain.
  These adapt Eric Dumazet, Madhuparna Bhowmik and Sebastian Andrzej Siewior's
  upstream work, with no new locking scheme.
- **Process identity and mm owner:** equality-only RCU accessors in ptrace,
  credentials, keyrings and conntrack do not escape into unprotected dereferences.
  Parent traversal uses the already-held tasklist lock; mm-owner publication is
  ordered. Existing task references, task locking, mm rechecks and unlock/put
  paths remain intact.
- **mincore lifetime:** a normal RCU read section spans tmpfs swap-entry lookup
  through swap-cache page pinning. A single NULL-checked swap-space snapshot
  avoids use after concurrent clear/free. The existing swapoff clear, grace
  period and free sequence provides the matching lifetime; page-state checks
  and puts remain outside the read section. This is a local 4.19 adaptation of
  Huang Ying's newer device-reference repair, whose API is absent here. Donor
  review tags are not represented as review of this different implementation.
- **SMEM bounds:** retain typed RAM/MMIO inputs and use integer addresses only
  for bounded interval/physical-offset calculations. Reject NULL and out-of-range
  values before subtraction, avoid end-address overflow and preserve `size_t`
  width. No MMIO dereference, allocation or physical-base change is introduced.
- **BPF line information:** use byte-address arithmetic for JIT offsets rather
  than arithmetic on a function pointer; preserve metadata and function values.
- **Timer-of:** import Daniel Lezcano's removal of an unused broken per-CPU IRQ
  interface. Every in-tree consumer was checked for zero initialization and no
  use of that API. This supersedes an unpublished mixed-pointer attempt.
- **Kernel-doc:** repair 151 actual parameter/return contracts across BPF, PM QoS,
  IPC logging, keys, networking and WLAN. Paired token and outside-comment byte
  comparisons confirm no executable changes in these documentation commits.
  Randy Dunlap's parser repair is a one-line Perl adaptation: two false
  `__always_unused` reports disappear while genuine missing parameters still
  report. Broader unnecessary parser edits were omitted.

## Static and host verification

Complete production Image, checkout toolchain, `W=1` and existing global
`CONFIG_CC_WERROR=y`: **zero compiler diagnostics**. Config SHA-256:
`0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`.
Image SHA-256:
`2a26ec5146f2ba2ca7326ff8d93875f43498df6f774fbcbec822d9f2eca51ab8`.
No configuration change required defconfig regeneration.

The synchronized unlimited `C=2` comparison changes **3,098 diagnostics / 119
errors to 3,012 diagnostics / 38 errors**: **86 removed, including 81 errors,
zero added** after source-line mapping. The [follow-up error ledger](kernel-sparse-followup-errors-20261028.json)
links all resolved baseline and current error sites. The [original inventory](kernel-baseline-sparse-errors-20261027.json)
and [grouped review](kernel-baseline-sparse-unchanged-20261027.md) remain historical.
Sparse exit zero is not a clean-analysis claim.

The same 455 baseline kernel-doc files report **2,993 → 2,840 diagnostics**:
151 real contract repairs and two parser false positives removed. This is a
baseline-file comparison, not an all-tree documentation-clean claim. Strict
checkpatch reports no errors; coauthor metadata, legacy spelling and style
findings remain visible, including inherited `strlcpy` context. No suppression
hides these findings.

Private host regressions cover 10,000 extracted BPF mappings plus NULL handling,
parser positive/negative fixtures, and 140,000 SMEM interval cases per 32/64-bit
address width. The source-extracted mincore model exercises four controlled
retirement schedules: two old lifetime violations become zero. This is an
ownership model, not reproduction of a live swapoff UAF; ASan/UBSan compilation
alone does not prove a live race. Independent review found no material blocker
in the final lifetime, RCU, SMEM or timer changes.

## Phone verification

On the exact final image, enforcing:

- All eight cores pass 128 self-modifying-code/cache cases each: **1,024** total.
  EL0 CTR exposes effective IDC=1; allowed A55/A77 L1IP variation remains. Later
  redundant runs sometimes receive EINVAL for temporarily unavailable affinity
  targets. The accepted receipt contains a complete all-eight-core run on this
  same image; partial repeats are not treated as full coverage. No thermal,
  CPU-isolation or global cpuset policy was changed to force the test.
- Tmpfs/memfd mincore: 64 rounds, 32 pages, **4,128** residency checks and invalid
  argument checks. Ptrace: **64** owned child peek/continue/exit cycles.
- SMEM: four address-only translations on an existing item, without dumping,
  modifying or allocating a shared payload.
- Recording/playback, six video cases, 19 PCM cases, 896 BPF checks, 128 fork/COW
  cycles, invalid media pointers, 64 pmsg writes and an owned 4 MiB storage
  comparison pass. Crypto/library, notifier, Tasks Trace and exit-stress modules
  pass and unload.
- Ordinary app-domain GPU: three runs per ABI, each with 62 native and six window
  checks, for 32 and 64 bits. This is finite rendering, not game/FPS certification.
- Private TCP namespace: 32 restricted selections fail, allowed Reno succeeds,
  module references remain zero and the module unloads.
- Wi-Fi reconnects with IPv4 after toggling on temporary and persistent final
  boots. Normal boot battery health is Good; audio and thermal services run.
  Final normal boot has taint 0 and no loaded private test modules.

Owned fixtures, hash-verified GPU APK and packaging staging were removed; backups
and host receipts remain. The user's ADB-only app-verification setting remains
disabled on the test phone, with other verifier settings and production sources
unchanged by that preference.

## Open findings and limits

**38 sparse errors and 2,840 kernel-doc diagnostics remain.** Paths below count
report sites, not proven runtime bugs. RCU public-pointer/list interfaces still
need complete caller/publication/free proof. An XFRM donor was rejected because
upstream reverted it; PID/fasync interfaces were not partly annotated without
caller audits. Mixed-origin Slimbus and Axon contracts remain unresolved. No
unchanged report is certified safe merely because it predates this batch.

SMEM's pre-existing resource-size versus 4 KiB mapping assumption and 32-bit
physical-base limits remain separate from the numeric-boundary repair. Active
Kona corruption was not established for those concerns. No exhaustive live
swapoff, OOM, concurrency, H323/PPTP endpoint, other-board, headset, deep-suspend
or full VTS certification is claimed. Thermal protection remains enabled.
Private receipts live under `~/evo/.repo/kernel-sparse-followup-20261027/`;
raw device logs, identifiers and proprietary dumps are not published.

| Remaining source path | Errors |
| --- | --- |
| [drivers/net/ethernet/qualcomm/rmnet/rmnet_handlers.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/drivers/net/ethernet/qualcomm/rmnet/rmnet_handlers.c) | 1 |
| [drivers/net/tun.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/drivers/net/tun.c) | 1 |
| [drivers/slimbus/slim-msm.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/drivers/slimbus/slim-msm.c) | 1 |
| [drivers/vservices/transport/axon.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/drivers/vservices/transport/axon.c) | 1 |
| [fs/fcntl.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/fs/fcntl.c) | 2 |
| [fs/notify/fsnotify.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/fs/notify/fsnotify.c) | 3 |
| [fs/posix_acl.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/fs/posix_acl.c) | 2 |
| [fs/seq_file.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/fs/seq_file.c) | 2 |
| [include/linux/rculist_bl.h](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/include/linux/rculist_bl.h) | 1 |
| [include/net/xfrm.h](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/include/net/xfrm.h) | 2 |
| [kernel/exit.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/kernel/exit.c) | 1 |
| [kernel/pid.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/kernel/pid.c) | 2 |
| [kernel/signal.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/kernel/signal.c) | 1 |
| [mm/swap_state.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/mm/swap_state.c) | 1 |
| [net/core/sock.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/core/sock.c) | 1 |
| [net/ipv4/nexthop.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/ipv4/nexthop.c) | 1 |
| [net/llc/llc_input.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/llc/llc_input.c) | 1 |
| [net/netfilter/nf_conncount.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/netfilter/nf_conncount.c) | 3 |
| [net/netfilter/nf_nat_core.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/netfilter/nf_nat_core.c) | 1 |
| [net/netfilter/nfnetlink.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/netfilter/nfnetlink.c) | 1 |
| [net/qrtr/qrtr.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/qrtr/qrtr.c) | 2 |
| [net/sched/cls_api.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/sched/cls_api.c) | 2 |
| [net/xfrm/xfrm_input.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/xfrm/xfrm_input.c) | 1 |
| [net/xfrm/xfrm_user.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/net/xfrm/xfrm_user.c) | 2 |
| [security/selinux/netnode.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/security/selinux/netnode.c) | 1 |
| [security/selinux/netport.c](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/blob/4517f4c402cdeb1f234e23ee61a6646393def8a6/security/selinux/netport.c) | 1 |

## Feature-separated commits

| Change | Original author |
| --- | --- |
| [netfilter: annotate NAT helper hook pointers with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6a4ea2f441a0838a1773f87984701a8c7b9c1f32) | Sun Jian |
| [netfilter: h323: Match RCU callback publication and snapshot types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5829b287adf5c61c3d939740bd8b92af6e8bce5f) | johnmart19 |
| [netfilter: pptp: Match RCU callback publication and snapshot types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2d092c99ad6a229ccabd9b9ac1256bd2911e81a9) | johnmart19 |
| [udp: Preserve RCU typing in tunnel offload snapshots](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/57cdc002f3ccb92b23dc147b90368154cbbf2e31) | Eric Dumazet |
| [module.h: Annotate mod_kallsyms with __rcu](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/863843f72a3d7b461a01a01b833daa5468eabdea) | Madhuparna Bhowmik |
| [module: Use proper RCU assignment in add_kallsyms().](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c0168c6a18bcc1f889d09a2235f1bd88065459af) | Sebastian Andrzej Siewior |
| [bpf: Correct cgroup link kernel-doc parameters](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b3ed285acceab3928fbfebb6d1f329eb598440dc) | johnmart19 |
| [PM / QoS: Describe device requests and per-CPU update results](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/80ea0e3be91b166605cf645e5972e4fc14b43928) | johnmart19 |
| [trace: ipc_logging: Correct read and return documentation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d91479b9d1c412cd2a81878a4ceb9a27f334ad48) | johnmart19 |
| [keys: Match restriction documentation to current interfaces](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/04c4ee2f5a55fd76668d35c1b229abb0346250e2) | johnmart19 |
| [net: Correct ICMP offset and delayed ACK timer documentation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a6078471894e5efa4e6c8498dd3712d19d610f9a) | johnmart19 |
| [wlan: wma: Match data callback documentation to current contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0bb1b0f72def3da2c4c70d1d17b849cf0cf1b30b) | johnmart19 |
| [wlan: hdd: Match cfg80211 documentation to current contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f5a16442654da8802e1957ecc1538c57af2df3df) | johnmart19 |
| [wlan: csr: Correct roam configuration documentation](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f4f7be4b95db2cbd0e1e2dc6557df5dea2cdd6d6) | johnmart19 |
| [sched: Match task identity and mm-owner RCU contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0fc9e049d1089dfa05a53a8e1f3117821f74dcf4) | johnmart19 |
| [cred: Snapshot published credentials for identity assertions](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/991689a1e9fc65168f3bd5ebd305d277edb00030) | johnmart19 |
| [keys: Snapshot session keyring identities through RCU](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/aa5f7f25b3ca6f7108c4617fde37ab12fbf8b8a7) | johnmart19 |
| [netfilter: Read conntrack helper identity through RCU](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/28e02ca714897a1fd84c6d358e480ea056d1514b) | johnmart19 |
| [netfilter: Match conntrack attach callback RCU publication](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f23f48505de90c92651948e9b0f0aa187084b535) | johnmart19 |
| [bpf: Express JIT line offsets as byte-address arithmetic](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6a7e4ebdf0cbff8942984fa57c130dcb824ebf8f) | johnmart19 |
| [soc: qcom: smem: Bound virtual-address translation offsets](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bfab667d4b37c9580dc2bac398758a3b5b2f36d3) | johnmart19 |
| [mm: Keep mincore swap-cache mappings alive through page lookup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a00cef2703e2fd315cf0f40aead6254008aa2b32) | johnmart19 |
| [scripts: kernel-doc: Handle __always_unused parameter attributes](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/705708d28df6b8969b074bcf27e191ab92ad469b) | Randy Dunlap |
| [clocksource/drivers/timer-of: Remove percpu irq related code](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4517f4c402cdeb1f234e23ee61a6646393def8a6) | Daniel Lezcano |
