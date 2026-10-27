# Kernel cleanup checkpoint — October 27, 2026

## Scope and current source

The full W=1 cleanup and fidelity audit is **in progress**, not signed off as complete. The [published, installed kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ec72c290a76b0edb5d52dae5ac6b60dbfc6c622f) on `aosp-17` includes a verified batch of 21 feature-separated commits after the prior release-config checkpoint. System-side sources, production configuration, security policies and thermal limits are unchanged by this batch.

The history audit uses the conservative [pre-cleanup baseline](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/36d8909a703d9575b221d89f4aff0a508b6a40b2). Scoped core, GPU/display and USB/MMC/UFS reviews identified real fixes and recorded unproven coverage; they do not establish that every introduced change is reviewed. Approved historical features are preserved rather than removed merely because a static review cannot exercise hardware.

## Verified repairs

- Original-author [Tasks Trace holdout lifetime fix](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/63cb67bb90e8af097813a5f5d6f85c2ad5650b83) and [companion cleanup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/dff9a1d99493bf354d6dc74b67e609253bebb273): defer holdout release to the scanner. The restored backend contained a known upstream task use-after-free. The first backport documents comment-context adaptation; the companion is unchanged upstream content.
- [SPS bitmap storage](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e08be55a7d5f1cbcc3ea6b72ab2637f856573adb): supply a full unsigned-long object to bitops instead of reading eight bytes from a four-byte mask. Host sanitizers reproduce the old overread; fixed exact-helper tests cover 100,000 masks plus zero.
- [Backlight input boundary](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e282f44cb3fa72285d35ac7a1f657391b241b494) and [bounded reports](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e183f09527b90191c1242785afe19a1e0bcae15a): preserve ordinary newline-terminated selectors and prevent maximum-width timing text from overrunning the result buffer. These are host-tested parser/type boundaries; physical dual-chip hardware is not certified by Alioth testing.
- [SPS register access](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/ec72c290a76b0edb5d52dae5ac6b60dbfc6c622f): use MMIO types/accessors for two register-dump helpers, resolving six address-space reports. The separate mixed RAM/SRAM FIFO contract is not relabeled or cast away.
- Original-author kernel-doc attribute/enum parser fixes plus comment-only keyring, core, SPS, IPA, WMI, SPCOM and bus repairs. Positive and negative parser regressions prove genuinely missing enum/member descriptions still warn. Comment-only patches retain executable tokens and firmware layouts. Tests and evidence remain outside kernel Git.

## Build and phone acceptance

**Build-tested:** full production `Image` passes W=1 with zero compiler diagnostics. `CONFIG_CC_WERROR=y` and the existing global `-Werror` policy are active. Config SHA-256 remains `0ebdfbb3e5ac0c9bf63e7d4bb061f087873a63547e10056c8b8fb86dde66bb05`. Optional compiler/V4L2/virtual-service diagnostics remain disabled; KFENCE, security, crash logging and thermal protection remain enabled as previously selected.

**Device-tested:** the exact published head boots Android with SELinux enforcing. Six video, 19 PCM, 21 crypto/library and four invalid notifier cases pass, along with nested Tasks Trace reader/callback/synchronization checks, eight finite exit-stress rounds with 256 transient readers, BPF/fork-COW, invalid media pointers, pmsg and generated storage tests. Exit stress is not a deterministic reproduction of the holdout-UAF race; the extracted-source host ASan old-fails/fixed-passes fixture provides separate ownership evidence with mocked scheduler/refcount primitives.

Ordinary-app 32/64-bit GPU tests pass three runs per ABI, each with 62 native and six window checks. Baseline/candidate median 60-swap wall times were 480.803/482.545 ms for 32-bit and 482.664/476.166 ms for 64-bit. These are presentation proxies, not display FPS or game certification. Wi-Fi reconnect/IP connectivity, battery reporting, audio service and thermal daemon checks pass. Fresh critical-log matching finds no new splats. Test modules are unloaded.

The tested kernel is installed as main with the original ramdisk. Full boot-partition hash verification and a normal reboot confirm persistence. No diagnostic Recovery ramdisk remains installed.

## Remaining gates and limitations

The untruncated configured Image sparse run makes 3,880 source checks and reports **3,273 unique diagnostics, including 145 error-level entries**. Make exits zero but that does not constitute a clean sparse gate. The earlier default limit of 100 warnings truncated some files; the new inventory uses the documented unlimited setting without suppressing diagnostics. The remaining four SPS RAM/SRAM FIFO reports require genuine producer/consumer contracts, not blanket pointer casts.

Direct kernel-doc checking of all 539 previously reported files retains **4097 diagnostic entries**. Full history review, remaining sysctl/scheduler contracts, documentation cleanup and final consolidated-history acceptance remain open. Pending private proposals are not published or device-tested changes. No global bug-free, warning-free, full-ROM or deep-suspend certification is claimed. A broader whole-kernel UBSan diagnostic boot failure remains parked outside this release-focused effort.
