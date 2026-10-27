# Final production kernel — October 27, 2026

## Published and installed source

[Final kernel `e9b1eaf8af93`](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e9b1eaf8af938cf9a7413f17e6f61d94fc2ffbcf) on `aosp-17` is installed as main and verified after a normal Android reboot. The original ramdisk is preserved byte-for-byte; the full boot-partition hash matches the packaged image. SELinux is enforcing. This task changes kernel sources and this workhub; system-side sources and thermal protection are unchanged.

The audit covers the range after the [pre-cleanup baseline](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/36d8909a703d9575b221d89f4aff0a508b6a40b2): 611 original commits consolidated into 606, comprising 552 source-reviewed executable/build changes and 54 comment/documentation-only changes. Five follow-up pairs are folded into their features; final source-tree identity is preserved. Author identities/dates and unrelated messages are unchanged. One inaccurate legacy-hook adaptation description is corrected.

Of 54 human imports, 53 have pinned donor receipts: 19 exact stable patch IDs and 34 source-assessed adaptations, with donor author email/date preserved. The inherited WBT policy change lacks an independent donor receipt and makes no exact-upstream claim. Source review is not certification of every intermediate build or every supported board. [Historical-link mapping](kernel-history-map-20261027.json).

## Repairs retained

- Original-author [Tasks Trace holdout fix](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/36e0ed30ab96287cf8cb3e3ba461ab60d7d565a5) and [companion release fix](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1d8b5cbef7024724d96d8489c05862c60e18cf03), plus completed scheduler RCU reader/lifetime contracts. Extracted-source host ASan distinguishes the old overread/use-after-free paths from the fixes; finite phone stress is separate evidence.
- [SPS bitmap storage](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ea630164664cef56ad19feb86c177cb3d0952c6a) uses a real unsigned-long object for bitops. MMIO register-dump helpers retain MMIO types/accessors rather than blanket casts.
- [Wi-Fi statistics alignment](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/7ac719bf7e0162df2dded9875e7a5f274f18277a) preserves native pointer alignment and the previously accepted report capacity; host boundary testing covers 307,649 cases and a valid decoded event.
- SPCOM [allocation-failure cleanup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/58767c1087b7ba411f689796d8abace17cab3d30) and [short-header rejection](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/db6ec583a8b845e877948ec7f2cbe5a8c35a5bb7); bounded backlight reports and completed CH101 thread-failure cleanup. CH101 has no Alioth DT binding, so that unwind is host/source checked, not hardware-certified here.
- Redundant GFP conversion is removed while valid radix-tree RCU repairs remain. Approved hardware, audio, display and compression behavior is preserved. Valid documentation repairs remain; no further documentation-only cleanup was added to the release gate.

## Verification

**Build-tested:** complete production `Image`, W=1 and existing global `-Werror` via `CONFIG_CC_WERROR=y`, with **zero compiler diagnostics**. Config SHA-256 is `0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`. Image SHA-256 is `0743dab7fe834b07ab592e66eec38c7836614aed7121cafcda1c0cb4c0cc5f35`. Unneeded debug-info/V4L2/virtual-service diagnostics are off; KFENCE, CFI, security, crash logging and thermal limits are retained. No new warning suppressions were added; existing compiler capability probes became stricter.

**Device-tested, exact published head:** six video cases, 19 PCM cases, 21 crypto/library known-answer checks, four invalid notifier cases, nested Tasks Trace synchronization, eight finite exit-stress rounds/256 transient readers, 896 BPF checks, 128 fork/COW cycles, invalid media pointers, 64 pmsg writes and a generated 4 MiB storage comparison. All pass with no new critical splats. All private test modules/fixtures and the hash-verified GPU probe APK are removed.

Three ordinary-app GPU runs per ABI each pass 62 native and six window checks. Median 60-swap wall times: baseline/final 480.803/490.313 ms (32-bit), 482.664/481.862 ms (64-bit). These are presentation proxies, not FPS or broad game certification. Wi-Fi reconnects with IPv4 after toggling and after the normal main-kernel reboot; battery is present/healthy and audio/thermal services run.

## Static debt and limits

The exact-head unlimited sparse run uses synchronized per-target output to prevent parallel-log interleaving. It exits zero with **3,140 unique diagnostics, including 127 error-level reports**. All 127 error sites predate the cleanup baseline. This is not a clean sparse result: inherited SPS/Slimbus mixed RAM/MMIO contracts need origin-aware work, not casts.

The existing ARM64 CPU-feature variation still sets `TAINT_CPU_OUT_OF_SPEC` (value 4); feature-check behavior is unchanged from the baseline and the report was present in earlier boots. It is neither cleared nor suppressed. Further kernel-doc cleanup is outside the current release-critical goal. No global bug-free, full-ROM, all-device, deep-suspend or exhaustive concurrency certification is claimed. Broader UBSan-only boot experiments remain parked.
