# Whole-kernel warning audit — October 26, 2026

**Source/build/host/device checked; full strict gate remains failing.**
Published 24 separate feature commits on `aosp-17`, from
[the prior RNG fix](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/52f64ac609e05245596f878aebafb0e02d7cf9bd)
to [the tested head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/39b0f55bca781248e58aa15d4234bc6a7a2c1003).
All previous crypto/library changes remain ancestors. No system-side sources,
configuration, thermal limits, compiler flags or warning suppressions changed.
Tests and raw receipts remain private; no test code or Markdown entered the kernel.

## Coverage and remaining gate

The initial configured `W=1 C=2 CHECK='sparse --arch=arm64' -k Image` pass
made 3,881 source checks and emitted 1,351 compiler diagnostics in 410 files.
These are diagnostic counts, not distinct runtime defects or physical driver probes.
Actual phone bindings were used to prioritize FastRPC, SPS, IPA, RPMh, clocks,
charging and fingerprint code over unrelated enabled device variants.

The final whole-tree repeat exits **2**, with **3881 source checks
(3880 unique paths), 1218 compiler diagnostics in
368 files**. The most frequent remaining compiler categories
are 408 -Wmissing-prototypes, 380 -Wunused-but-set-variable, 221 -Wformat, 98 -Winitializer-overrides, 38 -Wunused-const-variable, 21 -Wvoid-pointer-to-enum-cast.
The whole kernel is **not W=1/sparse clean**. Many enabled paths remain for
further review; successful normal compilation does not close those reports.

The affected 44-object command, including core/fair/topology, stop_machine,
wireless utility and NCM consumers, exits **0**, with 46 source checks and
no compiler errors or sparse parser/type errors. It retains **269 sparse and
kernel-doc warning entries** across direct and included files. No analysis
output was hidden. Existing conditional lock/API debt remains visible.

An additional SPS review separates 77 documentation warnings from four
address-space diagnostics. Its FIFO buffer API carries both coherent RAM
and ioremapped SRAM; blanket `__iomem` annotations or casts would be wrong.
No runtime FIFO repair is claimed. UAC1 getter reports likewise need an
instance/lifetime audit rather than invented default values. Inactive keyboard,
LED, external-modem and USB-retimer paths were not changed merely because
shared configuration compiles them.

## Repairs and preserved behavior

- FastRPC: define compat success results; snapshot VMA addresses while mmap
  locking protects the VMA; preserve compat ABI and correct diagnostic types.
- SPS: unwind only successfully acquired IRQ/wakeup/local-BAM resources on
  setup failure; preserve remote hardware ownership and normal success order.
- IPA: reject invalid action/channel/probe/endpoint inputs before indexing;
  retain supported UL/DL operations and use the actual RMNET start result.
- RCG clocks: propagate configuration-read failures, retain no-op behavior,
  mux/divider precedence and all clock/voltage policy.
- QC3/BQ: use the actual thermal property result, define voltage-reset
  success/timeout, propagate ADC write failures and report registration errors.
  Thresholds, delays, retry count and thermal protection are unchanged.
- FPC: retained no-op vendor attribute returns count, without retired MIUI hooks.
- RPMh: remove unread latency inputs and bookkeeping without changing votes,
  source-ID debug logging or commit ordering.
- Scheduler: correct format, kernel sysctl buffer, private linkage and RCU
  contracts; readers/writers were audited before annotations. Existing
  `task_current()` handles membership checks. No scheduling/thermal tuning.
- ARM64/init: shared declarations match global/assembly definitions and guards;
  preserve entry linkage and initial task values. Cache policy strings remain
  identical at all four indices. Legacy initrd I/O uses kernel file APIs with
  explicit offsets while retaining prompts, multi-disk reset and close handling.
- NCM: restore the `status = 0` hunk omitted from an existing upstream backport,
  preserving registration errors and successful subsequent binds.

## Upstream provenance

Original author names/dates and supplied human trailers are preserved.
Arnd Bergmann's TRAMP fix and Nathan Chancellor's cfg80211 fix have exact
stable patch-ID matches to the fetched original upstream patches:
`6601f56eeb1e07d32a42c633d570087f5e49e57a` and
`658aecda3da1837dd1312e044f325bf17e808847`, respectively.
The latter clarifies the always-returning WARN branch; it is compiler
compatibility, not a claimed runtime bitrate defect.

The init prototype subset and initrd file-I/O adaptation document their
4.19-specific scope; they are not represented as verbatim full cherry-picks.
The NCM completion preserves Hardik Gajjar's authorship and identifies the
missing hunk in the earlier local backport. No new human DCO was invented.
Independent agent source reviews found no introduced blocker. Checkpatch
still reports missing human DCO on assistant changes, its old unsupported
co-author trailer warning and style/documentation observations; it is not
claimed globally clean. The optional SPDX checker lacked its host `ply`
dependency; the new header's SPDX identifier was source-reviewed.

## Build and host checks

- Normal ARM64 Image and matching private test modules pass with checkout
  Clang `clang-r563880c`; configuration SHA-256 remains
  `6c0f80e241ca3c136b29a8594a70060c63e028c89617b4617e1603ebf5807ff7`.
- Image SHA-256: `3177ac264bf260bca198d201487d2190fbd295c9a59dcc9ed66552e931353586`.
- ASan/UBSan fixtures reproduce old FastRPC result/VMA-lifetime, SPS unwind,
  clock-read, thermal-result and ignored ADC-error defects, then pass fixes.
  The VMA and NCM bind tests are explicitly fragments, not whole-driver models.
- Exact-function IPA validation, QC3.5 retry boundaries, BQ registration roles
  and FPC count cases pass; no physical charger fault injection is claimed.
- Exact cfg80211 HE calculation: **20,173 cases**, matching baseline/fixed
  outputs and warning counts; fixed version passes strict host compilation.
- The first restarted audit encountered empty generated offsets after WSL
  restarted. Only verified empty generated artifacts in the audit output were
  regenerated; no source workaround was added. New header dependency mistakes
  were corrected before final packaging, not published as add/revert commits.

## Phone acceptance and restoration

The tested kernel identity contains `39b0f55bca78`. Temporary fastboot boot
preserved the installed ramdisk, SELinux **Enforcing**, active `mi_thermald`
and audio services. No partition flash, data wipe or credential operation.

- 6 hardware video encode/decode and 19 PCM recording/playback cases pass.
- 21 crypto/library cases; 256 unaligned/exact-length hardware RNG requests;
  33 lock-contract cases and 512 once-only attempts with one winner pass.
- A generated 4 MiB storage round-trip passes; fixture removed.
- **816 graphics checks** pass: 32/64-bit app domains, three runs each at
  60/120 Hz. Display preferences restored and private app removed. The first
  harness checked mode before waking the screen; only that setup was corrected
  and rerun, without a kernel change or latency/performance claim.
- Wi-Fi association and four gateway pings pass; USB ADB remains usable.
  The actual FPC no-op vendor write succeeds. Battery health reports Good.
- Fresh marked logs contain no matched BUG/WARNING/panic/RCU stall/CFI or
  GPU/SMMU fault signatures. All private test modules were unloaded.
- Original installed kernel restored; slot and boot-partition hash unchanged;
  exact task staging removed. Temporary module taint ends with restoration.

These bounded regressions do not certify every camera mode, external headset,
charger adapter, NCM host/multi-instance setup, hardware failure unwind, legacy
block/floppy initrd, scheduler race or full kernel warning set. Prior
[crypto/library and conditional-lock limits](kernel-crypto-lib-recheck-20261026.md)
and GPU/display/shutdown limits remain open.

## Published commits

| Feature commit |
| --- |
| [init: consolidate prototypes in linux/init.h](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0fbfac51f1882ac44cec4b9658b67b656202b7e8) |
| [arm64: fix clang warning about TRAMP_VALIAS](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/c87e6cc092ee8e578648be95cda815f9a45fe95a) |
| [initrd: switch initrd loading to struct file based APIs](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cb5c4bc3207178fedf4863deaa4441125e2175cc) |
| [arm64: describe cache policy table without overlapping initializers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f7a1e0501ebc23b0a158e1926e9bb91f090475a9) |
| [arm64: share architecture hook and assembly entry declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e5172a8cdc93020cb44891f26971c29de4457249) |
| [initrd: share the correct initial environment declaration](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5a3a2fa048c62b4042d96c58f216d145a745d76f) |
| [init: declare architecture delay calibration hooks](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6b8cbfb4c1a9e8f7fa75552d6cc93e36dde97028) |
| [init: initialize task RCU pointers through their typed interface](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/3061532667e43107aada278bd69d4547a41a7127) |
| [misc: fastrpc: fix compat results and diagnostic lifetime contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6ed7786b49ec52fcd125190f3972697fca274979) |
| [clk: qcom: propagate RCG configuration read failures](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cc11fdce3fc272c4647e7db0f5c131f14aa6db1e) |
| [input: fpc: return the accepted vendor write length](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d4e59814ef9aaed6f9740bd8db517e999cee4ca3) |
| [platform: msm: sps: unwind failed BAM interrupt setup](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/571a6e6a09094a0593bebe8854470088103638c8) |
| [platform: msm: ipa: validate MPM channel actions and results](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bf7c3d4cc7129e42833d640050208c8348f57e95) |
| [power: supply: bq2597x: preserve registration and ADC errors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/908e4c10d3af58c6243c6f1531ec84c99485632d) |
| [power: supply: qc3: return actual thermal and voltage reset results](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6095583140d774c32b15b617060fb3f46313d5d5) |
| [soc: qcom: msm_bus: drop unused RPMh vote inputs](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9b5e87e9db66ae6485127ce31c0b3964cae88712) |
| [sched: walt: match diagnostic formats to task accounting types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/f9e5cbe21a8dfd2710a9152c292148e2928dce07) |
| [sched: walt: use kernel buffer contracts in sysctl handlers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2f16670012ef1a4017ceb43557293cc5ff40d04d) |
| [sched: keep private WALT and schedtune helpers local](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5642ad0148060b194670c99ea6158303cda77e28) |
| [sched: declare utilization callbacks as RCU pointers](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6d8f0ff8c3debcb8c17761cd844b0c3a7bbbb3b0) |
| [sched: preserve RCU contracts for task groups and performance domains](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/6c222358e9b830b121f32fc36b0874e446028c8d) |
| [sched: complete shared consumer and current-task contracts](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/80da942d0b071b23d0c1f3f7e05b964bd75a441d) |
| [usb: gadget: ncm: complete bind status initialization](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/bc227b18fbdd77486ae7109aff3b68580068862d) |
| [cfg80211: Change an 'else if' into an 'else' in cfg80211_calculate_bitrate_he](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/39b0f55bca781248e58aa15d4234bc6a7a2c1003) |
