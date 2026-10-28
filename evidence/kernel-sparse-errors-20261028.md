# Sparse error and lock-context closure — October 28, 2026

## Scope and final source

[Final kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1efb0bf8d7a52abc450285c470bb34c28ad57dfd),
`aosp-17`, is a fast-forward of the [prior acceptance](kernel-rcu-contracts-20261028.md).
Fourteen feature-separated commits change kernel C/header files only. System
sources, device trees, vendor files, production configuration and thermal
protection are unchanged. No tests, logs or Markdown enter kernel history.
Original upstream ancestry/authorship is retained. These new adaptations are
locally authored; research proposals are not represented as accepted upstream
fixes, and no human DCO/review certification is invented.

## Corrections

- **Signals/PIDs:** retain the ordinary owner interfaces while expressing
  concurrent snapshots, actual RCU/tasklist requirements and release publication.
  Sighand's slab-reuse identity recheck and signal lock remain. PID references
  are acquired inside RCU; the retiring reference survives its grace period.
- **Swap/memcg:** pin transient swap mappings through page-reference acquisition,
  handle a retired NULL mapping, and begin shmem RCU before sampling exceptional
  entries. Mutation owners retain their existing page/entry lifetime contract.
- **Fasync/ACL:** carry queue/cache-slot RCU types through all in-tree interfaces.
  Preserve signal/file locking, deferred retirement, ACL sentinel/CAS decisions
  and reference transfers. Public compiled layouts and user ABI do not change.
- **Networking:** retain checked conncount RCU tree traversal through typed link
  views; use the real nexthop writer lock and namespace-owned netlink snapshots.
  XFRM afinfo acquisition/release is explicit in all thirteen callers, including
  failures, callbacks, module pins and lazy-load retries outside RCU.
- **VFS:** acquiring callers release inode locks. Parent move-lock branches are
  explicit; the shared payload actually acquires both child locks, returns them
  held, and releases parents before children in the original order.
- **Vendor backends:** Axon takes only a live nonzero reference before leaving
  RCU. Slimbus/SPS preserves RAM/MMIO provenance, including internal pool
  allocation, full-extent validation and CPU-alias/physical-range agreement.
  TX uses controller-owned RAM staging before MMIO publication; ordinary DMA,
  ring bounds, barriers and supported modes remain.

No warning flags, diagnostic filters, unchecked RCU escape, fabricated lock
operation or generic force cast is introduced to clear reports. The checked
VFS acquisition annotations describe real unconditional operations.

## Build and checker evidence

Complete production Image: **W=1**, existing **CONFIG_CC_WERROR=y**, zero compiler
diagnostics. Configuration SHA-256:
`0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`.
Image SHA-256: `673a38bc2e311601b18079acfce77a647105ad8e9abfc90e6ffe7d1604ca3e2f`.
CFI, SCS, KFENCE, SELinux and thermal policy are retained; no configuration
change or defconfig regeneration was needed.

Synchronized unlimited **C=2**: **2,989 reports / 16 errors → 2,954 reports /
zero errors**. All five requested lock-context warnings are resolved, together
with related caller/MMIO reports: **35 rows removed, zero added** after line
mapping. The [resolved-site ledger](kernel-sparse-errors-20261028.json) retains
the exact baseline sites. The other **2,954 baseline warnings remain**; this is
not an all-warning-clean claim. Kernel-doc cleanup was deliberately outside
this update and was not rerun as a separate documentation audit.

Strict checkpatch retains legacy coauthor/DCO metadata findings, nine moved
NULL-comparison style suggestions and three pre-existing VFS BUG checks.
Their original behavior is preserved; no checkpatch options hide them. Duplicate
coauthor trailers and newly introduced formatting defects were corrected.

Private negative sparse fixtures still reject untyped fasync, ACL and RB-tree
uses and a deliberately missing VFS child-lock acquisition. Sanitized positive
host regressions cover **102,592** source-extracted VFS states/event orders,
**80 ACL scenarios plus four CAS assertions**, **74 XFRM scope scenarios** and
**87,336 SPS assertions** with ASan/UBSan. Controlled swap models demonstrate
the old retirement/UAF counterexample and the new RCU-to-page-ref handoff.
Host RCU/MMIO stubs are finite models, not real hardware/concurrency proof.

## Exact-image phone checks

All run with SELinux **Enforcing**, production configuration and thermal
protection intact:

- Each ABI, **arm64 and arm**: 64 fasync enable/disable cycles; 128 ACL xattr
  round trips and 129 child permission checks; 256 rename/exchange/move checks.
- Each ABI: **64 non-leader thread execs**, **1,024 PID-owner updates**, **1,024
  signal probes** and **1,024 proc-status reads**, with owned children reaped.
- **16** disposable network namespaces: **16 ESP state initializations** and
  **256 XFRM requests**; **48 TC mutations**, **16 protocol dump round trips**;
  **128 inotify events** and **640 actual kernel list checks**.
- Mincore, ptrace and address-only SMEM probes; **19 PCM cases**, **six video
  cases**, BPF, fork/COW, media-uaccess, pmsg and owned-storage comparisons.
- Crypto/library, notifier and both RCU regression modules pass and unload.
  Three ordinary-app GPU runs per ABI each pass **62 native + six window
  checks**. TCP restricted-selection references balance; Wi-Fi reconnects with
  IPv4. No new critical kernel splat is observed.

The exact final Image is installed **as main** and verified after a normal
Android reboot: SELinux Enforcing, taint **0**, CPUs **0–7** online, matching
production config, no CPU-feature variation report and no new critical splat.
The original ramdisk is byte-identical, the whole boot hash matches the tested
package, and the other slot is unchanged. Wi-Fi reconnects with IPv4 after this
persistent boot too. Audio/thermal services run and battery health is Good.

Restarting the existing Windows ADB server restored access after reboot; no
permanent USB-source fix is claimed. Private modules, the hash-matched GPU APK
and owned fixtures/packaging staging are removed. Boot backups remain.

## Limits

The optional Axon and legacy LPASS/SPS paths have source, compiler/sparse and
finite host coverage; this phone is not proof that every optional backend binds
or every other board works. Off-configuration fasync/JFFS2/NFS consumers were
source-reviewed, not all built. No exhaustive concurrency, live swapoff/OOM,
headset/VoIP endpoint, complete ROM/VTS, game/FPS or other-device certification
is claimed. Raw logs, fixtures, build commands and backups remain private under
`~/evo/.repo/kernel-sparse-errors-20261028/`.

## Feature-separated commits

| Change | Author |
| --- | --- |
| [signal: Use owned sighand snapshots at the slab-reuse boundary](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c935130894de716dd2480d2924830159b7b5968f) | johnmart19 |
| [memcg: Pin shmem swap mappings until the cache page is referenced](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ac639b531c60545bd859c4454bdcf3bfccd97bac) | johnmart19 |
| [pid: Match concurrent snapshots to the owned PID slot interface](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d89cf23160bb8f2f9ed897d3417c65c07aad1be0) | johnmart19 |
| [mm: Separate swap mapping ownership from transient RCU lookup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6a94d820864d442abe8eed73bd772715ece6e7fb) | johnmart19 |
| [fs: carry fasync RCU types through queue slots and helpers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/55e032059ee0ccfa266e0f896fefdf0284723c11) | johnmart19 |
| [posix_acl: preserve RCU cache-slot types across atomic updates](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c6d59cf9f7008aeba6aaa6c7357b0e965af92f45) | johnmart19 |
| [nexthop: Traverse the insertion tree under its writer lock](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/558346a28f79afc308a834311980d69d45f550ba) | johnmart19 |
| [rbtree: Preserve checked RCU views of generic tree links](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/20ac3b3b364554154ed0cfd6ed9f2c68aa351ff3) | johnmart19 |
| [vservices: axon: Pin service state only while its reference is live](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/daa47360d66be6094e440fa1d9ec17e421c78a0e) | johnmart19 |
| [netfilter: Match netlink socket snapshots to namespace ownership](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/200136951f1dcb9bb04fb9ffc59672247eee6895) | johnmart19 |
| [dcache: Keep inode lock release in the acquiring callers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4b870804c81048cdc0c93325fc9d1d7a29a791a6) | johnmart19 |
| [dcache: Keep move parent lock scopes explicit](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e0fde1097a4a4bef1fa375ea7033d3729c24a14e) | johnmart19 |
| [xfrm: Make state afinfo read-side ownership explicit in callers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/38e10031823c27bc602f7409aad30685ae5505ab) | johnmart19 |
| [slimbus: Preserve RAM and MMIO buffer provenance through SPS](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1efb0bf8d7a52abc450285c470bb34c28ad57dfd) | johnmart19 |
