# Full W=1 kernel Image completion — October 27, 2026

**Source/build/host/device checked.** The earlier [1,138-diagnostic failure](kernel-main-install-20261027.md) is superseded by a successful full Image W=1 target at [40c7e956508d](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/40c7e956508d329580f457740b4ef5bd5efc7fac). [Focused changes](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/compare/a028da5feaa05034c7cf8d3956cf36c94f25a961...40c7e956508d329580f457740b4ef5bd5efc7fac) retain approved implementations and original human authorship. Android system-side sources, production config, Werror, toolchain and thermal policy are unchanged. No warning-suppression flags/attributes, production test fixtures or feature disabling were added.

## Source and review

Core fixes supply owning declarations, retain weak/exported/compiler entry points, restrict genuinely private helpers and remove unread bookkeeping while preserving calls and locking effects. ARM64 syscall, PMU and exception tables avoid overlapping defaults without changing their values. Rmap callbacks receive typed synchronous flags. PCM snapshots and trace calls share their existing CONFIG_SND_DEBUG consumer; no empty trace consumers remain.

Driver fixes include failed GENI DMA submission cleanup, the minidump count decrement, PS5169 register/error handling, bounded input parsing and real Wi-Fi buffer/status/output contracts. Separate cleanup topics preserve firmware, hardware values and live interfaces. Final review restored LLCC missing-match rejection before a typed dereference and retained the RCU license position. All 376 final source hashes match the reviewed snapshot. Configured-driver compilation does not imply external-device execution.

Adapted human backports retain author/date/trailers and describe legacy deltas:

- [Kees Cook: BPF code-address immediates](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6a5bbef9749e7be94ef3d0bd3635fd12f006e8d9).
- [He Ying: SMP panic-stop declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c69d60c5ceeb3ccbe113581eed1bd50481f90fae).
- [Arnd Bergmann: remaining task-cache declaration](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ca2aaf9f2398fdf435c530671cfe2f4eb061b173).
- [Andy Shevchenko: hrtimer clock switch](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/65b86cd87403201fe19b159c186823f4d8557090).

## Build and host regressions

The full configured Image target passes with checkout clang-r563880c, W=1 and unchanged CONFIG_CC_WERROR. The clean committed source stayed unchanged throughout the final build; parsed compiler diagnostics are zero. Incremental object reuse follows the earlier full object build. Matching private test modules also pass W=1.

Configuration SHA-256: `6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`.

Tested Image SHA-256: `40dee5ae5dc7468af73ec29f1c41a0781054295c7efcc25591667ae7d6a28914`.

Host checks compare all 884 native/compat syscall slots, 262 PMU cells, 64 exception classes and hrtimer mappings/fallbacks. Sanitizer fixtures cover 1,000,001 LED timing inputs, 511 minidump patterns, 8,741 PS5169 cases, LLCC missing/zero/supported match data, Wi-Fi MAC bounds/status/input cases and NAPI/FILS equivalence. GENI cleanup uses exact fragments in a modeled transfer, not hardware termination timing proof. PCM W=1 passes in production and an isolated SND_DEBUG-enabled config.

Cumulative checkpatch has zero errors, nine warnings and 236 checks, including legacy compatibility/style and declaration-placement notices; it is not globally clean. Kernel-doc, host parser and pre-existing sparse findings remain distinct from the cleared compiler blockers. Scoped sparse checks do not establish a globally clean result: CVP, RCU/address-space and SPS mixed-memory limits remain open.

## Phone acceptance and main installation

The exact final Image is repacked with the existing Magisk ramdisk; unpacked hashes verify both kernel identity and unchanged ramdisk. Temporary boot acceptance passes six hardware video cases, 19 PCM cases, 21 crypto/library cases, four invalid notifier-handle checks and a generated 4 MiB storage round-trip. Unattached BPF map/helper programs pass 128 cycles / 896 checks on both baseline and candidate; programs/maps are ephemeral.

Wi-Fi gateway ping receives four of four packets, USB ADB works, GPI binding is observed, battery health is Good, SELinux remains Enforcing and mi_thermald/audio services run. Fresh logs contain no matched kernel splat/panic/stall/CFI/GPU/SMMU fault signatures. Ordinary userspace notices are retained separately, not hidden or claimed fixed.

After acceptance, the tested package is flashed to the active boot slot. Its boot-image prefix hash matches. An additional Android reboot confirms the installed image/source identity, Wi-Fi, battery, enforcement and thermal service. Task-owned device staging is removed. The latest verified kernel remains installed as main; the original backup stays private for emergency recovery only.

Physical external peripherals, rare teardown races and the intermittent shutdown investigation are not globally certified. This task built and installed a kernel, not a new full ROM ZIP, and does not claim exhaustive production-release sign-off.
