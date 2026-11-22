# Clean checkout and source rebase, November 20

Restored 44 maintained source paths and verified 41 canonical bases against
Evolution X, LineageOS and the selected Android 17 tags. Published eight updated
branches after replaying 1,160 commits and confirming that upstream already
contains two fixes. Retained author metadata and verified 724 Assisted-by
trailers across the replay. Current commits are in the [source ledger](../state/repositories.yaml).

The LineageOS qcom/sm8250 kernel rebase produces the same complete source tree.
All 12 outputs from `scripts/update_defconfig` match the tracked defconfigs.

The recovery rebase combines upstream damage tracking with the existing DRM
canvas and preserves menu bounds on viewport changes. Its F2FS wipe actions
and its Magisk/APatch installer actions use distinct IDs. Fourteen minui tests
and two menu checks passed with ASan/UBSan. The four published overlay patches
apply byte for byte to the selected ROM sources and reproduce the three local
recovery trees. The patch runner reports zero pending patches.

## November 21 GitHub updates

All 46 selected branches were checked against the current fork refs. The 41
canonical routes had zero commits behind. Refreshed the committer dates of 1,312
project commits on 44 branches and verified all remote tips after leased pushes.
Per-commit trees, messages, original author records and upstream commit IDs were
preserved. All four recovery patches reproduce the exact earlier trees on the
updated tips. The local checkout now uses those tips and the published overlays.

## Initial Alioth user OTA

Started with an empty output directory and ran `m installclean` and `m evolution`
for `lineage_alioth-cp2a-user`. The build continued across two unexpected host
restarts with the same 1,267-project source manifest and regenerated affected
outputs. The build used the pinned pre-refresh commits. Their source trees match
the refreshed histories.

| Artifact | Verified value |
| --- | --- |
| Superseded OTA | `EvolutionX-17.0-20261120-alioth-12.4-Unofficial.zip` |
| Bytes | 3158628684 |
| SHA-256 | `db7db195d7a3835be5aeebcd7d38a4b87ccaaf016d2edf033164093fe06d202b` |
| Pinned source manifest SHA-256 | `3f9e9d4cb801b3e9cf0c8f5817fde4d7a31482f94c59ea0580552f6904ff7b03` |
| Build | Android 17, SDK 37, `user`, `test-keys` |
| Kernel build | `#1 SMP PREEMPT Sat Nov 21 01:33:36 UTC 2026` |

Verified the ZIP checksum against the generated checksum file and checked the A/B
payload and metadata hashes. Checked boot, vendor boot and DTBO images and
confirmed the recovery and recovery-storage executables in the vendor ramdisk.
Device acceptance is pending.

## Release signing correction, November 21

The clean sync omitted the private signing checkout. EvoX's optional include
then selected the AOSP test certificate for the initial package. Restored the
maintainer's private signing checkout and verified the selected certificate and
`release-keys` tag before rebuilding. The signed run reused completed compilation
and used the current post-refresh ROM and recovery source refs.

| Artifact | Verified value |
| --- | --- |
| OTA | `~/evo/out/target/product/alioth/EvolutionX-17.0-20261121-alioth-12.4-Unofficial.zip` |
| Bytes | 3158589592 |
| SHA-256 | `fc16561ba2fbb4d9e60a789603aab758def7ff0bb63b1c06875310d71482a1ac` |
| Pinned source manifest SHA-256 | `ab53317a20a5a06a0b0f46c926a1cc6696f77ae32b55f77931f262958bc2e6eb` |
| Build | Android 17, SDK 37, `user`, `release-keys` |
| Kernel | `4.19.325-Redline-264bc8e-cip136`, `#2 SMP PREEMPT Sat Nov 21 02:30:08 UTC 2026` |

Verified the whole OTA and A/B payload signatures against the expected release
certificate, the same certificate in native recovery's trust store and the
platform signature on `framework-res.apk`. The earlier test-key package is
preserved separately for build evidence. Device acceptance is pending.
