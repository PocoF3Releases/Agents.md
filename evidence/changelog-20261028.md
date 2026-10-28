# October 28 next-build release-copy review

## Baseline and inclusion

The maintainer confirmed on **October 28** that the **October 25 build was
published**. New [long](../state/telegram-20261028-full.md) and
[short](../state/telegram-20261028-short.md) drafts use October 25 as their cutoff.
They are copy for the next rebuild containing current sources: no new build
date, artifact identity, release version, download URL or publication is invented.
No Telegram message was sent and no new artwork was requested/generated.

The saved October 25 source checkpoint and prior published-copy topics were
compared with 44 maintained checkout paths. Seven have net tree changes.
The checkpoint was collected during that build, not extracted from its artifact;
late audio additions already covered by the October 25 post are excluded
conservatively. Tree/semantic comparison is used rather than commit dates/counts.

The old kernel source object was rewritten, but its saved tree
`a0b1c1a4d16c276ea8c9ec987d59ed6b3218aa85` exactly equals the retained
[baseline equivalent](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/97dc957c03c4cdec55d2045381b6d80dadc8c7d9).
That commit is an ancestor of the [current source](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1e45b8cc1cbb9229a464395b5a8e12d8b4bc349c).
Rewritten IDs and documentation-only commits are not new user features.

## Eligible new behavior

| Copy group | Source and scoped acceptance |
| --- | --- |
| Redline identity, short source ID and trailing CIP revision | [Identity and regeneration](kernel-redline-20261028.md); host-checked, not yet built into an installed branded Image |
| CPU feature/cache detection and low-memory CFI handling | [CPU and baseline audit](kernel-baseline-audit-20261027.md) |
| GPU import/accounting, startup cleanup and display fence/power failure cleanup | [GPU audit](kernel-gpu-audit-20261026.md), [techpack acceptance](kernel-techpack-completion-20261026.md) |
| Audio DSP reply bounds, cleanup and voice/echo sample widths | [Techpack](kernel-techpack-completion-20261026.md), [DSP status follow-up](kernel-techpack-eos-gem-20261026.md) |
| Camera firmware/IRQ cleanup and hardware video EOS/STOP failure ownership | [Camera paths](kernel-techpack-completion-20261026.md), [EOS ownership](kernel-techpack-eos-gem-20261026.md) |
| MTP length/compat handling, WLAN IPv6 reads and rejected-TCP-change resource leaks | [USB](kernel-mtp-dwc3-contracts-20261026.md), [CPU/network audit](kernel-baseline-audit-20261027.md) |
| Swap-cache lifetime, partial hardware RNG reads and crypto-engine cleanup | [Swap lifetime](kernel-sparse-errors-20261028.md), [RNG tests](kernel-crypto-lib-recheck-20261026.md), [crypto audit](kernel-crypto-lib-audit-20261026.md) |
| SPU unmount permission and perf timer cancellation lock cycle | [Common policy](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/f59ca6bca5f838cb0030cd5a4dd96d7ee1625083), [timer/provenance tests](shutdown-upstream-review-20261025.md) |

On October 28 the maintainer confirmed that intermittent shutdown hangs are no
longer occurring. Both drafts omit a shutdown known-issue warning. Historical
traces retain their original dates, source identities and causal limits; this
confirmation does not relabel their evidence as a new instrumented test.

## Exclusions and validation boundary

The non-kernel net deltas mostly finish already-announced Qualcomm Dolby game
processing, MiSound recovery/EQ, recording recovery and audio-zoom packaging.
They are not repeated. The AudioFlinger dump boolean is diagnostic-only.
The SPU policy is the distinct newly eligible common-tree change.

Earlier recovery/PIN/installers, camera modes/JPEG fixes, Zstd/zRAM, Bluetooth,
Parts/Dolby UI redesigns, thermal controls, NFC/font/media and October 25 ROM UI
features are not re-announced. Refresh-rate tuning remains excluded at the
maintainer request. Build-tool, test, static-analysis and documentation work is
not marketed as a feature. No general FPS, battery-life, audio-quality,
security-patch-month, Wallet or bug-free claim is made.

The [accepted functional kernel](kernel-sparse-errors-20261028.md) passed full
strict W=1/Werror and finite enforcing phone regressions. Branding is the later
identity-only source change. No complete new ROM build, flash or universal
USB/headset/camera/VTS acceptance was performed for this copy. Host fault models
are not physical fault injection. The final artifact must include these sources
before publishing these posts as its changelog.

Both posts fit Telegram's UTF-16 limits: fewer than 4,096 units for the long
message and 1,024 for the short caption. Explicit Markdown hard breaks preserve
Unicode bullet layout in rendered copy. Private comparison, prior-post hashes
and plain-text copies are under `~/evo/.repo/changelog-20261028/`.
