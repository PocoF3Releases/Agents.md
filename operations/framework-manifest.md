# Sync maintained sources and native recovery

Current heads are recorded once in the [source ledger](../state/repositories.yaml).
The [November 14 verification](../evidence/source-refresh-20261114.md) checks
upstream ancestry, effective routes and exact recovery-tree replay; older runtime
acceptance stays in the [validation register](../state/validation.md).

## Framework selection

Install the maintained [poco-frameworks.xml](manifests/poco-frameworks.xml) in
`.repo/local_manifests/`. It explicitly selects PocoF3Releases `cnb` for both
framework repositories. Preserve the device/kernel overrides and inspect the
resolved `repo manifest`; inherited defaults alone do not establish the route.
Do not hand-edit generated manifests or an upstream manifest to retain our forks.

## Recovery overlay

Use [PocoF3Releases-Recovery/local_manifests](https://github.com/PocoF3Releases-Recovery/local_manifests/tree/cnb).
Keep its XML, `apply-recovery-patches.py`, `patches/series.json` and patch files
together. Recovery-only dependencies are forked there; shared frameworks/base
and both Xiaomi device trees remain on the normal ROM repositories.

After preserving existing edits and syncing the selected sources:

```bash
repo sync -j50
python3 .repo/local_manifests/apply-recovery-patches.py --check
python3 .repo/local_manifests/apply-recovery-patches.py
python3 .repo/local_manifests/apply-recovery-patches.py --check
```

The runner preflights all projects, verifies patch hashes, rejects incompatible
or dirty tracked trees and skips an already-applied stack. The final check must
report zero pending patches for **frameworks/base (1), device/xiaomi/alioth (1),
and device/xiaomi/sm8250-common (2)**. These local commits are not public ROM tips;
do not push them into the normal framework/device branches. On a conflict,
preserve the tree and inspect the exact base/patch before adapting anything.

`-j50` applies to Repo sync, not Soong. Build only when authorized using
`lineage_alioth-cp2a-user`; use incremental builds for development and reserve
`m installclean` for release preparation. Native recovery is built with the ROM;
standalone PBRP is separate. Preserve build/make's upstream linkfiles and groups.

## Known sync maintenance

The November 13 EvoX manifest moved `external/zstd` to its EvoX fork, adding the
framework-services `libzstd` visibility rule. That exact upstream change is in
the checkout. A project-identity transition can require scoped `--force-sync`;
back up its refs/metadata and confirm a clean tree before allowing replacement.

On this host, a pre-existing `git_config.py` edit blocks Repo's self-update.
Preserve it. The supported per-command `REPO_SKIP_SELF_UPDATE=1 repo sync ...`
was used for the scoped dependency sync; it neither disables source verification
nor reconciles the local tool patch. Do not set it globally or use
`--no-repo-verify` to resolve that maintenance conflict.

## Maintained repository ownership

Preserve Evolution-X/LineageOS fork relationships and imported authorship.
Recovery dependencies from other mirror owners are standalone at their maintained
URLs. Keep the explicit qcom/sm8250 kernel base from the source ledger; do not
substitute a differently named Xiaomi kernel repository.

Native recovery uses `android_bootable_recovery`. Public tags were removed by the
maintainer; historical branches are retained snapshots, not automatically updated
build inputs. Private signing and camera-development repositories are excluded.
