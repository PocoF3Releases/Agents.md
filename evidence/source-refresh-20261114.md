# Full source sync, November 14

**Source/Git/host checked; no Android rebuild or device acceptance.**

`repo sync -j50` completed successfully across 1,265 selected projects. Ten
upstream ROM/dependency checkouts changed; their current heads are below.
Our 50 maintained repositories / 105 public branches were read back before and
after sync. All 41 configured canonical routes already contained their latest
selected upstream commits, so no feature rebase or public source rewrite was
necessary. Historical branches and upstream authorship remain intact.

| Updated checkout | Current upstream commit |
| --- | --- |
| `device/lineage/sepolicy` | [475f0089602b](https://github.com/Evolution-X/device_evolution_sepolicy/commit/475f0089602be86de71f444bad76fdd9ed63c99b) |
| `evolution/OTA` | [a472081d1ac9](https://github.com/Evolution-X/OTA/commit/a472081d1ac9fe8dfffef863eeaa2518e3bb8829) |
| `evolution/manifest` | [adf002bcdf70](https://github.com/Evolution-X/manifest/commit/adf002bcdf70abd58ea74f3bb71ac37bc38b55dd) |
| `frameworks/native` | [4375f0eb6ad2](https://github.com/Evolution-X/frameworks_native/commit/4375f0eb6ad237f707374a1eb93996bdf24283a9) |
| `hardware/qcom-caf/sm8450-6.6/audio/pal` | [c6e543cdbfba](https://github.com/Evolution-X/vendor_qcom_opensource_arpal-lx/commit/c6e543cdbfba7f1d12080ea4b9b72b6574bcaba7) |
| `hardware/qcom-caf/sm8450-6.6/audio/primary-hal` | [d6b36b8ea7a6](https://github.com/Evolution-X/hardware_qcom_audio-ar/commit/d6b36b8ea7a64c5ded34681e8382dcf4325604a7) |
| `packages/apps/Evolver` | [7115f235ff0a](https://github.com/Evolution-X/packages_apps_Evolver/commit/7115f235ff0a0c8cf22e81e4f6a0f770a28603a9) |
| `packages/apps/Launcher3` | [bea0383b597c](https://github.com/LineageOS/android_packages_apps_Launcher3/commit/bea0383b597c00a67ead289ac664d46ca9657342) |
| `packages/apps/Settings` | [4abf57170eb8](https://github.com/Evolution-X/packages_apps_Settings/commit/4abf57170eb818ebdad0d5b0a77f22b8baec9bef) |
| `vendor/apn` | [2842825e44b5](https://github.com/LineageOS/android_vendor_apn/commit/2842825e44b5ad6e247467bd7a16c1d8bf80407f) |

The sync reset the three local recovery overlays to their public ROM bases.
Restored the exact saved overlay commits, retaining the existing four patch
files and their checksums. Independent temporary-index replay reproduces all
three live trees; preflight reports zero pending patches. The 44 maintained
build routes and published source ledger still match. The normal sync/patch
procedure remains in [the workflow](../operations/framework-manifest.md).

All 1,271 captured checkout identities were reconciled, including tool/docs
checkouts outside the project list. Existing staged/unstaged work, untracked
files and guidance were preserved. The local Repo tool customization is unchanged;
its self-update was skipped only for this command, without disabling verification.

Our published feature commit IDs and their validated Assisted-by trailers are
unchanged. The [attribution correction](attribution-variants-20261114.md) remains
separate from runtime evidence. No rebuild, installclean, flashing or phone test
was performed. New upstream source changes require the maintainer's next build;
older APK/kernel/device acceptance has not been transferred to the synced ROM.
