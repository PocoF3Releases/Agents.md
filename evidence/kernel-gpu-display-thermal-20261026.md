# GPU, display and thermal warning audit — October 26, 2026

Continues the [configured audit](kernel-subsystem-audit-20261026.md) from
kernel baseline 6ab769d4a561. Final source eb8826a50995 is kernel-only: no
system sources, configurations, panel timings, thermal limits, governors,
firmware or proprietary drivers changed. Diagnostic artifacts remain private.

## Separate source changes

- [thermal: cpu_cooling: Remove unused cur_freq variable](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/32254851b50b8001c264faa2ef6ce3287ccd172f).
- [thermal: qcom: Correct TSENS symbol visibility](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/15f7d9ed7244709bd988ecc5aa58b6199bb224af).
- [gpu: msm: Preserve fault and allocation flag types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5356f6871a07d568206fcbd066cd724ee7507f27).
- [drm: msm: sde: Correct CRTC helper input contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/eb8826a50995e8ada3c2ac42ae9c9ae1e60f0d6c).

The CPU-cooling import is Shaokun Zhang's exact upstream
[e0fda7377d30](https://github.com/torvalds/linux/commit/e0fda7377d30685feaef4d93d9fdfde91c5d7d9a),
with original authorship/date/trailers and matching stable patch ID. It removes
an unused frequency query, not a cooling decision. TSENS changes retain exported
MTC reset access, make driver-only functions private and remove an unused
critical-threshold address calculation. Interrupt/register operations remain.

KGSL callbacks now use vm_fault_t and allocation-mask construction uses gfp_t.
The caller already returns vm_fault_t; all mask consumers use allocator flags.
The GFP function body is identical apart from its local type. GMU context state
is private. Both snapshot flags are bool, so logical conjunction retains the
existing diagnostic panic condition. No hardware panic was injected. Stale
kernel-doc signatures are corrected rather than suppressing their diagnostics.
A proposed large fault-offset repair was rejected: this allocation path rejects
sizes above UINT_MAX, so the hypothesized supported >4-GiB case was invalid.

CRTC scaler pointers and the plane iterator are initialized inside their owning
helpers instead of passing uninitialized caller values that are overwritten.
The copied fence FD is a kernel scalar, not a user-address-space object. FPS
formats now match their 64-bit values. Dead local projections and stale parameter
descriptions are removed. Validation, fence operations and dimming remain.
An independent source review found no actionable regression; that is not runtime
proof for alternate devices/configurations.

## Build and warning scope

Ten selected objects have no source diagnostics in the final W=1/C=2 output:
KGSL sharedmem, pool, reclaim, GMU, snapshot; CPU cooling, msm-tsens, tsens2xxx,
tsens-mtc; SDE CRTC. The real display parent Kbuild target is required to load
Kona's display configuration. A direct nested directory target that did no work
was rejected as evidence. The broader parent audit still returns failure from
other files; no whole-tree or whole-display clean claim is made. No warning flags
were relaxed. Strict checkpatch has zero errors/checks and one warning on the
existing BUG_ON policy; replacing that policy merely to silence it was rejected.

The normal final Image build passes with the checkout's Clang 21 at -j6. No
installclean/full ROM build or defconfig regeneration is needed for these edits.
Raw Image SHA-256:
`00eeaebd147f94aad3d46b6589d1dc723d655b2bac211a01577c72a55c6a6fb2`.
The matching private shutdown observer builds; its inherited sparse annotation
warnings are separate from the production ten-object result.

## Phone checks

A temporary fastboot boot runs the exact final revision with SELinux enforcing,
stock V502 userspace and mi_thermald active. Repack round-trip verifies the exact
kernel and unchanged installed rooted ramdisk. No partition is flashed.

The installed-kernel baseline passes six GPU audit processes. The candidate
passes six processes at verified physical 60 Hz and six at 120 Hz, three per ABI
per mode. Each process passes 62 native and six window checks, covering KGSL
context/memory/map lifecycles, GLES/Vulkan submissions and pixel/buffer readback,
AHardwareBuffer/EGL import, fences and window presentation in untrusted_app.
These are bounded functional checks, not measured FPS, exhaustive races, games,
protected-content certification or a repair for historical game page faults.

The initial settings-only attempt stayed physically at 120 Hz; its mislabeled
60-Hz result was discarded. Android's nonpersistent preferred-mode control plus
compatible bounds selected the actual modes, asserted before and after each run.
Original 120/120 bounds and the unset preferred mode are restored. No new GPU
fault, WARNING, BUG, call trace or RCU stall appears after the runtime marker.

A second temporary boot completes read-only thermal telemetry after a quoting
error invalidated the first per-zone collection. Real TSENS CPU/GPU values are
read before/after bounded load, cooling devices retain registered maximum/current
states, mi_thermald remains running and battery health stays Good. CPU cooling
states are nonzero where reported; no trip was forced and no protection bypass
was applied. Representative GPU readings remain about 37–39 C. A shell-domain
KGSL lifecycle probe passes 32 process teardowns (16 normal, 16 SIGKILL); this is
separate from app-domain rendering coverage. No new fault/warning/stall appears.

All four commits are pushed on aosp-17 through eb8826a50995. The phone returns
to its installed d2c680 kernel, enforcing and boot-complete, with unchanged boot
partition SHA-256, original refresh bounds and no preferred-mode override.
Retained pstore records this candidate returning from normal-priority reboot
callbacks and perf teardown (about 6 ms), followed by restart. This successful
restart does not establish the historical intermittent shutdown cause.

Owned test app, phone staging/probe and Windows temporary image are removed.
The original-kernel shutdown observer and narrow SPU unmount live rule are
rearmed only for the current boot; initcall_debug=N, no persistent autoload or
global permissive policy is installed. Windows ADB server refresh recovers the
post-boot transport without another phone reboot.

Raw builds, device logs and test receipts remain under
`~/evo/.repo/kernel-gpu-display-thermal-20261026/`; no raw logs or binaries are
published. Wider warnings and intermittent shutdown causality remain open.
