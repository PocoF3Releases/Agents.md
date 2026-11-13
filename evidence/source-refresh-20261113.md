# Final maintained-source and recovery verification

**November 13, 2026 — source/Git/host checked.** No Android build, installclean,
flash or device test was performed. This supersedes older current-source summaries;
it does not overwrite their observed runtime versions, hashes or acceptance.

## Repository state

Live organization inventories cover 19 main and 30 recovery public repos, plus
the maintained GitLab camera source: **50 repos / 105 published heads**. Three
private signing/decompiled-camera repos were excluded. The maintained reference
tool is recorded separately in the source ledger.

All **41 selected EvoX/LineageOS/pinned-A17 routes** have zero missing upstream
commits. Standalone app/blob/docs/tools sources have no guessed upstream. Published
heads remain the repaired versions; no further feature rebase or fork push was
needed. Historical branches remain snapshots, not current intake targets.

| Selected source | Verified public commit |
| --- | --- |
| Framework base | [5dec056e50a8](https://github.com/PocoF3Releases/frameworks_base/commit/5dec056e50a89199c4320161f197e6a856607509) |
| Framework AV | [6f165815e06c](https://github.com/PocoF3Releases/frameworks_av/commit/6f165815e06ce56875cc41e22d499047db48f691) |
| Xiaomi hardware | [c40d1866051a](https://github.com/PocoF3Releases/hardware_xiaomi/commit/c40d1866051a6e23f9884cba036ed70f196e5296) |
| Common device / Parts | [b23466b7ef0f](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/b23466b7ef0ff905e474e2ea61daaf57b3cdd2d6) |
| Redline kernel | [b96d5fbe51a6](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b96d5fbe51a6d7ec74ecb500bd24437e3e12e131) |
| Native recovery | [e6fae205afde](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery/commit/e6fae205afde9cd02e14f81fdfd87f8b0c589d8f) |
| Recovery bundle | [c407ff85e340](https://github.com/PocoF3Releases-Recovery/local_manifests/commit/c407ff85e340e2d9c0b2765d76dd46a563261d80) |

The kernel base is exactly LineageOS/android_kernel_qcom_sm8250 `lineage-20`.
The [ledger](../state/repositories.yaml) owns all remaining current heads and
distinguishes public tips from local authored recovery overlays.

## Manifest and dependency update

Selected the exact [latest EvoX manifest](https://github.com/Evolution-X/manifest/commit/adf002bcdf70abd58ea74f3bb71ac37bc38b55dd).
Its cumulative change moves `external/zstd` from LineageOS to EvoX. The exact
[Ghosuto upstream change](https://github.com/Evolution-X/external_zstd/commit/72f8b7d8a2aa3c28a3b7484bd78926baf991a912)
adds one visibility entry for framework services, which already link `libzstd`.
Original authorship was retained; no custom production source was edited.

The resolved manifest verifies **44 selected maintained build routes**. The main
ROM interfaces publication is independently current while the enhanced recovery
build selects the recovery-owned interfaces fork. Existing source/tool edits and
guidance were preserved across **47 checkouts**. Repo-tool self-update remains a
separate local customization issue; [workflow and limits](../operations/framework-manifest.md#known-sync-maintenance).

## Recovery composition

The published runner/XML/series and patch bytes match the live installed bundle.
All four SHA-256 checks pass. Applying each stack in a temporary Git index on its
published base produces the exact live tree:

| Project | Mail patches | Result |
| --- | ---: | --- |
| frameworks/base | 1 | Exact overlay tree; zero pending |
| device/xiaomi/alioth | 1 | Exact overlay tree; zero pending |
| device/xiaomi/sm8250-common | 2 | Exact overlay tree; zero pending |

Follow the [single post-sync workflow](../operations/framework-manifest.md#recovery-overlay).
Do not publish these local overlay commits to normal ROM branches. Independent
review found no required issue in source coverage, preservation or replay receipts.
New image, decryption, USB/OTG, radio, headset and release acceptance remain
unestablished by this source-only milestone; use the dated validation owners.
