# Kernel diagnostic readiness — October 27, 2026

## Source and production acceptance

The published [kernel head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/62b69d00cb35709bcd3caff5c929175eeb8dc17e) on `aosp-17` includes the sparse/kernel-doc follow-up, debug-configuration build fixes and upstream scheduler prerequisites. The [Tasks Trace backend](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5d8e1320085e01551622703d158f205689ab8779) supplies the missing reader-grace-period worker, hooks and exported synchronization APIs. Classic Tasks RCU behavior is retained. Exact scheduler imports preserve original authorship; the adapted backend documents its upstream basis.

**Build-tested/device-tested:** production-config full `Image` at `5d8e1320085e01551622703d158f205689ab8779` passes W=1 without compiler diagnostics. Production config SHA-256 is `6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`. It is installed as main and survived an additional reboot, reconfirmed in Android on October 27. SELinux is enforcing and thermal protection remains active.

Phone acceptance includes six video cases, 19 PCM cases, 21 crypto/library cases, four expected-invalid notifier cases, nested sleeping Tasks Trace readers and callback/synchronization/barrier completion. Fork/COW, unattached BPF, CVP/Synx invalid-pointer handling, generated-storage roundtrip, Wi-Fi, USB and battery checks passed in the recorded scope. Fresh critical-log matching found no splats in those runs. Private test modules/staging were removed after the production checks.

The two subsequent Tasks Trace/tracing documentation commits pass scoped `scripts/kernel-doc -none`; content outside block comments is byte-identical. The running kernel remains the tested code revision above, not a binary rebuilt for comment changes.

## Diagnostic boundary

**Build-tested, not runtime accepted:** the all-at-once debug profile exceeds the observed boot/expanded-memory budgets and was never booted. Split profiles retain production functional/security/thermal features. The lock/memory profile uses targeted UBSAN; the second uses whole-kernel UBSAN with the standard size-optimization choice. Their W=1 builds pass without compiler diagnostics. Gzip payloads roundtrip to their exact raw Images. Actual encoded boot-package size and expanded kernel memory must be checked separately; compression cannot cure an excessive expanded image.

The lock/memory diagnostic image did not reach an accepted Android session in either gzip or smaller raw temporary packaging. It returned to production Recovery. Its actual failure is unresolved. Recovery shell access is unprivileged and cannot read retained pstore logs. Retrieved recovery history did not provide the diagnostic crash trace. An F2FS recorded-version string mentions the diagnostic kernel, but that alone neither establishes a successful Android boot nor identifies the fault. Private root-debug ramdisk work is diagnostic only and is not a production source change.

No new runtime UBSAN finding has been captured or claimed fixed. Whole-tree sparse/kernel-doc findings remain; this record does not claim the kernel globally warning-free or certify a full ROM release. Android system-side sources and production configuration remain unchanged. Raw logs, firmware and diagnostic artifacts stay private under `~/.repo` in the checkout.
