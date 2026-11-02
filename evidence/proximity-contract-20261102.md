# Proximity compatibility — 2026-11-02

## Published lifetime fix

[14af593](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/14af5935f0fbc9a1e8e3a61a5c034cf032d00bbf)
protects the ultrasound IIO device used by APR proximity callbacks. The previous
code published its global pointer before setup completed and kept it after
removal freed the object. Failed setup also retained stale driver data and leaked
the allocation. An asynchronous callback could access an incomplete/freed device.

The small source change publishes only after successful setup, serializes callback
use and unpublication, clears the pointer before teardown, and releases failed
setup allocations. The configured IIO FIFO push does not sleep; the IRQ-safe lock
covers that push and is released before device teardown. No ABI, event values,
calibration, HAL selection, configuration, thermal or security policy changed.
No matching published upstream replacement was found in the bounded search.

## Checks and phone acceptance

- **Host:** extracted callback/probe/remove functions fail five ownership
  assertions before the fix. The corrected fixture passes setup failure,
  pre-publication callbacks, 100 normal 0/5 mappings and 50 callback/removal
  interleavings under ASan/UBSan. This models IIO operations; it is not a
  device allocator-failure or hot-unbind test.
- **Static/build:** affected W=1/Werror, unlimited Sparse and strict checkpatch
  pass. Full incremental Image/modules/DTBs build passes with no compiler
  diagnostics; 12 unchanged trace kernel-doc warnings remain. Production config
  SHA-256 remains `6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48`.
- **Device:** the exact kernel boots and is persistently installed as
  `4.19.325-Redline-14af593-cip136`, Enforcing, taint 0. Installed boot image
  SHA-256 is `3688fec013bc92d43fbde59f74aef79676f1dfc35338744e80c1c83d89c02aca`.
  Original Magisk ramdisk and AVB packaging are preserved.
- **Ordinary-app regression:** all 48 playback/recording cases pass. Motion,
  light, timestamps and 20 rapid sensor lifecycle cases pass. APR proximity events
  are observed. Audio, sensor and thermal service PIDs remain unchanged within
  the temporary-boot test window; no new critical kernel message matches it.
  Both test apps and remote staging were removed, and the sleeping display restored.

## Separate vendor flush delay remains

The actual stack is Sensors HIDL 1.0 plus Xiaomi multihal, with stock MIUS/SSC/touch
sub-HALs. The ordinary-app sensor matrix passes 45/46 checks before and after the
kernel fix: proximity flush misses the fixture's two-second deadline. An isolated
proximity-only test confirms six accepted requests eventually complete in
6.76–8.01 seconds. Two seconds is the test's deadline, not a quoted Android SLA.

Disassembly shows MIUS sets pending flags without waking its blocked poll; the
poll waits up to eight seconds before checking them. This is independent of the
kernel lifetime defect. No guessed timeout, periodic wakeup, fabricated completion
or replacement calibration was shipped. A correct fix must preserve pending-event
ordering and every accepted flush request; see the
[Android sensor contract](https://source.android.com/docs/core/interaction/sensors/batching).

Private source/artifact identities and results:
`~/evo/.repo/sensor-contract-20261102`. Broader compatibility remains incomplete;
external audio routes and the paused touch boundary are not certified by this check.
