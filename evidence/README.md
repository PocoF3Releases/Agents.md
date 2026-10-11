# Portable evidence

Load only the record needed for the task. These files preserve shareable
observations without requiring the original workstation or a raw log archive.

| Record | Scope |
| --- | --- |
| [Haptics, 2026-10-04](haptics/2026-10-04.md) | Temporary final candidate, stock composition, PCM/AAC scope and restoration |
| [Haptics, 2026-09-30](haptics/2026-09-30.md) | Installed baseline, corrected candidate, stock gains and user acceptance |
| [AC-4 diagnostic](ac4/README.md) | Reusable decoder test and recorded PCM result |
| [Parts and Dolby UI](device-20261010.md) | Final sizing, icons, phone checks and production history cleanup |
| [MiSound worker and recovery](legacy-hardware-research-20261011.json) | Final source, APK identity, saved settings, tiles and audioserver recovery |
| [VINTF compatibility](vintf-compatibility-20261011.json) | Selected metadata and generated kernel configuration; no full ROM certification |
| [Translations](production-final-translations-20261011.json) | Historical resource audit, placeholders and canonical names |
| [Compatible Gerrit changes](lineage-gerrit-applied-20261011.json) | IWLAN, fingerprint and flashlight component checks |
| [Kernel WBT removal](wbt-removal-20261011.json) | Authorship-preserving import and separate defconfig regeneration |
| [Workhub review](workhub-review-20261011.md) | Standards/spec corrections, official guidance and network limits |
| [Post-sync sources](post-sync-source-audit-20261011.json) | Maintained fork head verification |
| [Archive skeleton](../archive/README.md) | Empty reserved structure; no hidden evidence files |

The [validation register](../state/validation.md) owns acceptance status. A copied
record is not a test performed in the reader's new session. Raw dumps, private
logs and original media are not bundled; request only a necessary missing artifact.

Historical identifiers and private diagnostic filenames are provenance, not bundled downloads. The archive is an empty skeleton; current records are linked above. [Framework override](../operations/framework-manifest.md) is available for future checkouts.
