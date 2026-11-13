# Kernel rebase and history review — November 12, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

`source-checked`, `host-tested`, `build-tested`, `device-tested` within the scopes below.
Published [aosp-17 2f2467b](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e91f4c2803c1a931f070d55c4c82148355662991), rebased over the current
[LineageOS Qualcomm SM8250 base](https://github.com/LineageOS/android_kernel_qcom_sm8250/commit/e3f6acd662618dabb3a7a953e48743019badc373)
with **46 new upstream commits**. System, device-tree, vendor and recovery sources were not modified.

## History and retained behavior

The [per-commit ledger](kernel-history-review-20261112.json) accounts for all **767** original fork commits:
723 fresh topic entries; 44 approved audio commits carried unchanged without a fresh audio-lane review.
Bulk vendor imports received provenance/wiring/selected-function checks; this does not mean every imported line or firmware table was audited.

- Omit the redundant CFI-enable and F2FS statistics commits because the new base already supplies their final behavior and upstream authorship.
- Consolidate the owned KGSL worker pair and RCU include-placement correction; finish owned WLAN startup-error, MHI text-bound and dual-KTZ self-test implementations in their existing feature commits.
- Replace the incorrect sysctl user-buffer annotations with the demonstrated kernel-buffer contract; preprocessed production behavior is unchanged.
- Replace two generated snapshots with one separate final all-device regeneration using `scripts/update_defconfig` and Android Clang `r563880c`.
- Retain the approved `lz4` zram default. Keep `NAME = "People's Front"`, README, DT sources and `include/uapi/` unchanged versus the original fork tip.

All 763 retained original entries preserve author name/email; folds join only owned same-author work.
Raw Codex trailers remain final with no trailing whitespace; GitHub API confirms Codex recognition for all 547 attributed commits. Owned `Fixes:` references were remapped to reachable current commits.
Original refs and a verified original-series Git bundle are retained privately before the lease-protected rewrite.

## Additional final implementations

**28 component-separated source corrections**, grouped by topic, are linked individually in the ledger:

| Area | Final behavior |
| --- | --- |
| Core/compression | Literal CMA names, safe LZO-RLE header capacity, exact root-device prefix, camera-pool constructor cleanup and live CPU-cooling backend selection. |
| Battery/LED | Managed Maxim/OneWire lifetime, real LED/parser errors, Dagu I/O/registration error reporting and integer representation of its existing NU2105 calibration factor. |
| GPU/display | Complete GPU-model publication, clone-cooling errors, FOD worker unwind, suspend command classification, failed DP bridge cleanup and core backlight-cooling withdrawal. |
| Input/camera | Drain FocalTech work before resources, single-owner Goodix input cleanup, peer-request guards, installed buffer-FD unwind in all matching copies and tablet private-helper closure. |
| USB/storage | Balanced supply references, managed HS-PHY allocation ownership, command-ring timeout ownership and completion of the incoming F2FS asynchronous cleanup backport. |
| NFC | Bound reset metadata reads by the actual received payload. |

The F2FS completion retains Zhiguo Niu's authorship and links its upstream origin.
The local corrections preserve existing interfaces. No warning suppression, hardware tuning, thermal bypass, production debugging, kernel test files or Markdown was added.

## Verification

| Evidence | Result and scope |
| --- | --- |
| Configs | All 12 regenerated after final source; deterministic output matches the checked generation. Resolved Alioth change versus the original is only `CMA_SYSFS=y`. Config SHA-256 `4334682f33f04d0e92ac647cdb15b3fd5d54532b94f2ed2292eeca812f9fe5f9`. |
| Kernel | Full Alioth `Image modules dtbs`, `W=1 KCFLAGS=-Werror`, Clang `r563880c`: pass. First complete compile and final integration pass both succeeded. Image SHA-256 `7b21263d5d515624e48182e3960cd6e87d8be9805bb8783e88e35b1f80a76745`. |
| Static | 137 display units: zero Sparse reports. 26 other affected units: zero errors, 116 warnings recorded. 493 wireless units: zero errors, 764 warnings. These are scoped checks, not a new whole-kernel backlog count or a complete line-mapped warning delta. |
| Variants | Compression-enabled F2FS object: strict compile, zero Sparse errors/one baseline declaration warning. CAS camera-FD object: strict/Sparse pass. Corrected Dagu charger plus tablet request/memory objects: strict/Sparse pass with zero reports. No complete Dagu/CAS kernel or hardware certification. |
| Host counterexamples | Extracted ownership/length/error models fail before and pass after the applicable fixes. They do not execute hardware, scheduler or every failure interleaving. Dagu arithmetic classifies all 65,536 codes: all 65,420 defined old results match; 116 old out-of-range casts remain explicitly outside the equivalence contract. ARM64 output needs no FP/NEON helpers. |
| Phone | Temporary boot of the exact Image with the phone's existing ramdisk; no partition write. `4.19.325-Redline-2f2467b-cip136`, Enforcing, taint 0; thermal service active, battery/charging healthy. 256 stable GPU-model reads, 82 real camera-preview frames, connected Wi-Fi/local-gateway ping, exact 4 MiB ADB/userdata round trip and sleep/resume pass. No kernel splat or fatal crash-buffer entry. Test files removed. |
| Repository | Reachable-object connectivity passes; source tree/payload and authorship receipts retained. Remote branch checked after exact-old-head `--force-with-lease`. |

Kernel-doc diagnostics and Bison grammar notices remain separate from compiler success; no documentation-only cleanup or suppression was introduced.
The early e2fsck linker-configuration warning is userspace output, not a kernel splat; system sources remain outside this task.

## Limits and next boundary

- The new audio-lane review, Airoha follow-up and thermal-clamp follow-up were parked after platform restrictions. Their new proposals were not integrated, retried, rephrased or handed to another reviewer. Preserve that boundary; old notes do not resume them.
- At this baseline, USBPD/PS5169 lifetime proposals were excluded as incomplete. The [separate validated follow-up](kernel-usb-lifetime-20261112.md) now fixes those findings; its Dagu hardware limits remain explicit.
- Bulk imports, inactive hardware, alternate camera modes, external USB/DP peripherals and adverse allocation/removal races retain their stated limits. Normal boot/preview does not certify every mode or every error path.
- The prior USB outage/mode experiment and GPU donor experiments remain paused. No new audio fault injection, radio call/SMS, storage wipe, permanent flash or long endurance qualification was performed.

The branch is prepared for an Alioth rebuild with the above validation. This record is not an all-bugs-resolved or all-board certification.
Private raw receipts live under `~/evo/.repo/kernel-final-review-20261112/`; they are not public downloadable artifacts.
