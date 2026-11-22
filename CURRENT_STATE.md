# Current state

Source checkpoint **2026-11-21**. Published 44 branches with refreshed committer dates.
All 41 canonical routes are current and the four recovery patches reproduce the local trees.
Release-signed Alioth user build **Evolution X 12.4** packaged as `EvolutionX-17.0-20261121-alioth-12.4-Unofficial.zip`.
[Source, OTA and recovery evidence](evidence/source-refresh-20261120.md).

- **Recovery:** native ROM recovery in `~/evo`; use the [sync/patch workflow](operations/framework-manifest.md).
  PIN/local ZIP acceptance is dated; password/Weaver remain unverified.
- **Parts/audio:** [November 12 checks](state/validation.md#v-parts) retain their dated artifact scope.
- **Other limits:** haptics scale-zero/physical calibration and the manual display
  color mismatch remain in their topic owners.
- **Release status:** [November 4 published baseline](state/releases.md).

| Task | Read |
| --- | --- |
| Exact current heads / acceptance | [Source ledger](state/repositories.yaml) · [Validation](state/validation.md) |
| Sync / native recovery | [Workflow](operations/framework-manifest.md) · [Recovery](memory/evox-recovery.md) |
| Parts / touch / thermal / sensors | [Device UX](memory/xiaomiparts-device-ux.md) |
| Dolby / MiSound / codecs | [Audio](memory/dolby-audio.md) |
| Haptics | [Vibrator](memory/haptics.md) |
| Camera | [Finalized camera](memory/miuicamera.md) |
| Kernel / rootdir | [Platform](memory/kernel-frameworks.md) |
| GPU / display / games | [Graphics](memory/gaming-graphics.md) |
| Changelog / artwork | [Releases](state/releases.md) · [Artwork](operations/release-artwork.md) |
| Source search / reverse engineering | [Ready indexes](operations/repoindex.md) · [Binary correlation](operations/alioth-reverse-engineering.md) |
| Host recovery / tools | [Restore](operations/workstation-recovery.md) · [Tools](operations/android-tooling.md) |
| Resume / editing knowledge | [Continuity](operations/continuity.md) · [Maintenance](operations/maintenance.md) |

Use [INDEX.yaml](INDEX.yaml) for more topics. History stays on demand.
