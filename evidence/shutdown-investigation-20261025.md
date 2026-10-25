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
CIL contains the mapped-init unmount rule. The change is committed locally,
not deployed or published. It repairs the proven permission gap, not the
separately observed kernel stall. Keep its eventual publication separate from
local recovery patches in the common checkout.

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

At this checkpoint `shutdown_diag` is loaded for the current boot only.
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
