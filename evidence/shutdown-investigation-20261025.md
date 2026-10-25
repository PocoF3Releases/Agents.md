# Intermittent shutdown stall — October 25, 2026

**Unresolved kernel hang; independently corrected source policy denial.** The
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

The latest diagnostic restart unloaded `shutdown_diag`; it is not currently loaded.
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

## Perf timer investigation — candidate only

A healthy restart captured firmware, CNSS, NFC, NPU and ESOC notifiers, followed
by perf_reboot and the final observer. All returned before device_shutdown.
The failed historical trace has no final marker or task stack, so its precise
blocking callback remains unproved.

Source review found perf_event_exit_cpu_context calling hrtimer_cancel while
holding hrtimer_lock, also required by perf_mux_hrtimer_handler. perf_reboot
tears down remote online CPUs, making a running remote callback relevant. A
bounded device probe observed an entered callback and try_to_cancel returning
-1 while that lock was held; cancellation outside the lock completed. It did not
intentionally deadlock the phone. The first probe used an invalid IRQ-disabled
IPI context and generated a warning; the corrected probe starts the remote timer
before taking the lock and completed without that warning. Both were unloaded
and removed. Keep this harness warning distinct from a production failure.

A local candidate gates timer restart during teardown, cancels outside the lock,
and clears the gate when the CPU returns online. Normal ARM64 object compilation
and strict checkpatch pass. W=1 finds three missing-prototype errors also present
on the unchanged baseline. Sparse reports existing address-space/context issues;
exit zero is not a clean sparse result. Full image/device acceptance and causal
attribution to the intermittent shutdown hang remain pending. No kernel fix is
published or claimed installed.
