# Keep maintained framework forks selected

The active checkout has .repo/local_manifests/poco-frameworks.xml, using
[the maintained override](manifests/poco-frameworks.xml). It extends the existing
framework projects to PocoF3Releases and explicitly selects refs/heads/cnb.

For a new checkout, copy this XML into .repo/local_manifests/ before syncing.
Do not edit repo's generated manifest or the upstream Evolution X manifest.
Verify with repo manifest, then run repo sync -j2 frameworks/base frameworks/av.

October 11 verification: effective project entries select the PocoF3Releases
remote and cnb. Targeted sync succeeded; base remains [d88e1ba6da08](https://github.com/PocoF3Releases/frameworks_base/commit/d88e1ba6da08dcd11127560a7eae81c5537ce0b5)
and av remains [81b959f7c519](https://github.com/PocoF3Releases/frameworks_av/commit/81b959f7c5197a52e5f3588e8c94f230fb9848a4), with clean trees.

Correction to the earlier audit: Evolution X's remote already specifies cnb.
The inherited lineage-24.0 default was incorrectly treated as the effective
framework revision. The override makes fork ownership explicit and keeps our
patches in future syncs. Upstream changes still require review and integration
into the maintained forks; selecting a fork does not automatically import them.
