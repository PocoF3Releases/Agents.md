# Intermittent shutdown stall — October 25, 2026

**Reported hang unresolved; verified SPU permission and perf deadlock repairs published.** The
maintainer reports frequent black-screen Power off stalls and rare Restart
stalls. Do not label this fixed from successful short-uptime tests.

## Retained evidence

The installed kernel matches the recorded SM8250 source and existing kernel
build output. It is 4.19.325-cip136-st20, user build, SELinux enforcing. A retained
previous-boot console shows init finishing userspace teardown in about 9.7 seconds
and entering the kernel restart syscall. CNSS and NPU reboot notifications appear,
then Wi-Fi/touch activity and init's emergency shutdown monitor continue for over
50 seconds. This establishes a kernel-stage stall in that particular restart;
it does not identify the last printed driver as the cause, or prove every
reported Power off stall has the same cause. No blocking-task stack was retained.

The same trace contains repeated init `unmount` denials for the SPU filesystem
label, followed by the unmount-timeout/kill-all fallback. Existing QVA policy
permits mounting/relabeling that label but omits unmount. The local common-tree
fix adds only `allow init vendor_spunvm_file:filesystem unmount;` in
`sepolicy/vendor/init.te`. The full `selinux_policy` target passed for
`lineage_alioth-cp2a-user`, including neverallow/context checks; generated vendor
CIL contains the mapped-init unmount rule. Published separately from recovery
patches as [975316a](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/975316a110b9edebee66816fec6a38048846ace7).
An enforcing A/B/A device probe used the actual init domain and a private mount
namespace: unmount returned EACCES before the exact live rule, succeeded with it,
and returned EACCES after rollback. The parent SPU mount remained unchanged.
A subsequent real restart with that one temporary rule unmounted SPU successfully.
The installed policy still predates the source fix; the live rule disappeared at
reboot. This repairs the proven permission gap, not the separate kernel stall.

## Controlled tests

All three tests reached a normal off/charging state, as confirmed by the
maintainer: connected idle shutdown; connected shutdown after launching the
installed game; and the usual Power off action with USB unplugged. The first
two used `svc power shutdown` (null reason); the third exercised the user's
normal action. Cold power-off cleared pstore on the third boot. These results
neither reproduce the stall nor prove a repair. USB enumeration in charging mode
alone is not evidence of failed shutdown.

## Temporary diagnostic state

A private external GPL diagnostic module was built against the exact installed
kernel configuration, symbol versions and compiler. It registers an early
reboot notifier and, only if the kernel remains running, prints the shutdown
task's stack after 10 seconds and twice more at 15-second intervals. It changes
no driver power-off logic and no thermal/security settings. No kernel image was
flashed. Loading an external module marks the kernel with the ordinary O taint;
that diagnostic context must be retained when interpreting future logs.

After temporary-image testing, the original installed kernel was restored and
its matching `shutdown_diag` observer was rearmed for this boot only. The exact
SPU live rule is also active for this boot; neither has persistent autoload.
`initcall_debug=N`, SELinux remains enforcing, and there is no autoload script or
persistent Magisk module. The staged file is `/data/local/tmp/shutdown_diag.ko`.
A reboot/power-off unloads it. Once the hang is captured or this investigation is
cancelled, unload the idle module and remove that owned file. Do not remove
unrelated root modules or change shutdown timeouts to hide a stalled callback.

If the black screen recurs, allow at least 45 seconds for stack capture, then
long-press Power to restart and retrieve pstore before another reboot overwrites
it. A future source fix requires a task/driver trace or another reproducible
causal test; it must preserve clean filesystem shutdown.

Private logs, diagnostic module and build receipts are under
`~/evo/.repo/shutdown-hang-20261025/`. No raw device identifiers or proprietary
logs are included here. The main failure remains open.

## Rootdir and policy audit

The built five-partition configuration passes host_init_verifier. All 29 common
rootdir service executables resolve in the product, including Android partition
symlink aliases. All eight rootdir shell scripts pass device shell syntax checks
and match installed hashes. Runtime AVCs include optional diagnostics/property
probes and diagnostic-harness entrypoint/fd failures; those are not grounds for
blanket permissions. No additional functional SELinux repair is established.

## Published perf repairs and acceptance

The healthy traced restart captured firmware, CNSS, NFC, NPU and ESOC notifiers,
followed by perf_reboot and the final observer. The failed historical trace has
no final marker or task stack, so its exact blocking callback remains unproved.

Source review found perf_event_exit_cpu_context calling hrtimer_cancel while
holding hrtimer_lock, also required by perf_mux_hrtimer_handler. perf_reboot
tears down remote online CPUs, making a running remote callback relevant. A
bounded device probe observed an entered callback and try_to_cancel returning
-1 while that lock was held; cancellation outside the lock completed. It did not
intentionally deadlock the phone. The first harness used an invalid IRQ-disabled
IPI context and generated a warning; the corrected harness starts the remote
timer before taking the lock and completed without that warning. Both probes
were unloaded and removed. Keep that harness warning distinct from production.

Published separately on the kernel aosp-17 branch:

- [Timer teardown](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d9a0bc96e102aab71f01e277d856f72a871ea966):
  gate timer rearming before cancelling outside the callback lock. Reset the
  gate in AP restart before deferred events are installed. Independent review
  caught and corrected the initially missing failed-CPU-down rollback case.
- [Resolved per-CPU pointer types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/4bd82288909db6b24fcc5e7a70ad1cd35427a3d0):
  derive generic fallback locals from raw_cpu_ptr, preserving ordinary-address
  typing after resolving the per-CPU pointer.
- [Perf ownership contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6d6310d6bc2f8a69724011e29d848c358bc32c0f):
  correct RCU/per-CPU declarations and protected accesses, missing hook
  prototypes, private linkage, poll/user-copy boundaries, conditional lock and
  output-handle ownership annotations, and stale kernel-doc descriptions.

All enabled kernel/events objects pass ARM64 W=1 and sparse without source
warnings/errors. No warning options were disabled. Separate pre-existing host
Genksyms grammar conflict notices remain outside this perf-source cleanup.
Strict patch checks have no errors/warnings; the per-CPU typeof expressions
produce five known unary-address-of spacing CHECK false positives. Source review
found no remaining blockers after the rollback correction. No config changes,
permanent diagnostics, test binaries or documentation were added to the kernel.

The final kernel Image built successfully. A temporary boot preserved the rooted
ramdisk byte-for-byte and kept SELinux enforcing. Baseline and candidate each
opened, multiplexed and read all 96 raw PMU events successfully. Sampling,
callchain/user-stack copying and fork/exit records passed with no malformed
records; the candidate repeated both checks after CPU7 offline/online recovery.
No new kernel warning appeared in that test interval. Forced CPU-down failure
was not injected; rollback coverage is source-reviewed, not runtime-certified.

The candidate's traced Restart completed all normal-priority callbacks, then
perf teardown in about 11 ms, followed by hardware restart. A separate candidate
Power off reached charging mode, confirmed by the maintainer. Charger startup
then overwrote the candidate Power off console; do not present the charger
console as its driver teardown trace. These are bounded regression checks, not
proof that the intermittent long-uptime report is fully resolved.

The installed boot partition SHA-256 is unchanged from its pre-test backup; the
phone returned to the original installed kernel, enforcing mode and
initcall_debug=N. Owned test-image staging and test executables were removed.
Only the original-kernel observer remains loaded, with its staged module owned
by root at mode 0600. A real recurrence still needs the retained stack/phase
capture; do not close this report from successful shutdowns alone.

## Upstream substitution audit

[Human-authored counterparts, tested replacement scope and remaining local
provenance](shutdown-upstream-review-20261025.md). The prepared replacement series
is local only; the published source and prior phone acceptance remain unchanged.
