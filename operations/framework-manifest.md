# Keep maintained framework forks selected

The active checkout has .repo/local_manifests/poco-frameworks.xml, using
[the maintained override](manifests/poco-frameworks.xml). It extends the existing
framework projects to PocoF3Releases and explicitly selects refs/heads/cnb.

For a new checkout, copy this XML into .repo/local_manifests/ before syncing.
Do not edit repo's generated manifest or the upstream Evolution X manifest.
Verify with repo manifest, then run repo sync -j2 frameworks/base frameworks/av.

October 11 verification: effective project entries select the PocoF3Releases
remote and cnb. Targeted sync succeeded; base remains [d88e1ba6da08](https://github.com/PocoF3Releases-Recovery/frameworks_base/commit/d88e1ba6da08dcd11127560a7eae81c5537ce0b5)
and av remains [81b959f7c519](https://github.com/PocoF3Releases/frameworks_av/commit/81b959f7c5197a52e5f3588e8c94f230fb9848a4), with clean trees.

Correction to the earlier audit: Evolution X's remote already specifies cnb.
The inherited lineage-24.0 default was incorrectly treated as the effective
framework revision. The override makes fork ownership explicit and keeps our
patches in future syncs. Upstream changes still require review and integration
into the maintained forks; selecting a fork does not automatically import them.

## Recovery overlay

For enhanced native recovery, also use [the dedicated recovery manifest](https://github.com/PocoF3Releases-Recovery/local_manifests/tree/cnb). It overrides frameworks/base and both Xiaomi device trees with recovery-enabled variants; frameworks/av remains in PocoF3Releases. Without this overlay the ROM forks intentionally omit recovery-specific changes. Repo sync retains the selected organization branches.

## Maintained repository ownership

Keep Evolution-X and LineageOS fork relationships. Required recovery dependencies
from other mirror owners are standalone repositories at the same URLs and branches;
their Git refs and authorship are preserved. Each maintained override contains
custom changes used by the build; do not remove it merely because the delta is small.

Use `android_bootable_recovery` for native ROM recovery. The unused `bootable_recovery`
duplicate was consolidated; its history remains on
[the legacy branch](https://github.com/PocoF3Releases-Recovery/android_bootable_recovery/tree/legacy-native-recovery).
Public development tags were removed at the maintainer's request; branch heads
were retained. Signing and camera-development repositories are excluded.
