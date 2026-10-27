# Kernel release acceptance — October 27, 2026

## Published release source

The [current kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/48b6b395671aa63a715e48a466e7c9e8c6d39b0f) on `aosp-17` contains 37 feature-separated follow-ups to the previously published base. The maintainer requested release-active fixes rather than further diagnostic-only work. Eighteen unpublished diagnostic-only commits were excluded from this push and retained in a local recovery ref. Imported author identities were preserved. No tests, Markdown files, warning suppressions or production-config changes were added to the kernel series. System-side sources are unchanged.

Retained fixes address BPF/map and host-buffer alignment, packed MHI accesses, RCU/memcg contracts, slab-node accounting, CPUidle RCU ownership, DCI state, WLAN packet reads and MMIO types, CNSS IRQ state, and real initialization/error handling. The [WLAN startup fix](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/415119f6ca6eb1a4390ca2ebd39ddb17f425c9e3) preserves failure propagation and removes a self-reference wait; a worker relocation used only for diagnostic initialization was removed. No thermal-limit or performance-tuning changes were made.

The final batch initializes the [KGSL per-process mutex](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3f38e33c1d7a8ae6c3149946b4b546a63581724e), forms [CVP user-field addresses](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/99b624377f7fd6d48930610f8235e840646e65f3) through byte offsets before fault-safe access, and traverses [Tasks RCU holdouts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/48b6b395671aa63a715e48a466e7c9e8c6d39b0f) without fabricated terminal tasks. These affect release-active paths even though diagnostic instrumentation exposed them. Source review found no missing dependency after excluding the diagnostic commits.

## Build and phone acceptance

**Build-tested:** full production `Image` with W=1 passes with zero compiler diagnostics. Existing kernel-doc reports are separate and remain. Production config SHA-256 is `6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`, unchanged. UBSAN, lockdep, function tracing, DMA-debug and kmemleak are disabled; existing security, KFENCE and thermal settings remain.

**Device-tested:** the exact current release head booted Android with SELinux enforcing. Six video cases, 19 PCM cases, 21 crypto/library cases, four invalid notifier cases, three Tasks Trace rounds with nested readers/callbacks/synchronization/barriers, 896 BPF checks, 128 fork/COW cycles, invalid CVP/Synx pointers, 64 pmsg writes and a generated 4 MiB storage roundtrip passed. Wi-Fi off/on reconnected and IP connectivity passed after network configuration completed. Battery was present/Good; audioserver and the thermal daemon were running. Fresh critical-log matching found no new splats. Private test modules and functional-test fixtures were removed.

The latest release kernel is installed as main, not just temporarily booted. The original ramdisk was restored, the complete boot-partition hash verified, and a normal reboot reconfirmed the current kernel, enforcing state and healthy services. The temporary Recovery log-access ramdisk is no longer installed.

## Limits and parked diagnostics

A separate lock/targeted-UBSAN diagnostic profile reached Android and exposed the final fixes. The broader whole-kernel UBSAN profile still black-screened; its measured expanded image fits the observed carveout, so size alone is not a proven cause. No retained panic established its cause. That private diagnostic investigation is parked per the maintainer's release focus; it is not evidence of a failure in the accepted normal configuration.

No global warning-free/bug-free claim, deep-suspend certification, acoustic certification or full-ROM release sign-off is implied. Existing whole-tree sparse/kernel-doc findings and untested external hardware remain outside this targeted acceptance. Raw logs, firmware and private diagnostic artifacts are not published.
