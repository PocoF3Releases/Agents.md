# Current project state

Recorded checkpoint: September 24, 2026. This is repository-backed knowledge, not a live connection to the maintainer's machine. Read [remote workflow](REMOTE_WORKFLOW.md) for access limits and [evidence index](EVIDENCE_INDEX.md) for self-contained results.

## Release baseline and next draft

The maintainer supplied published September 22 and September 23 notes. **23.09.2026 / Android 17 / Evolution X v12.2 is the shipped semantic cutoff.** The [next changelog packet](today/2026-09-24-changelog-preparation.md) contains only new AC-4 playback and Thermal Profiles dialog fixes. Camera/startup/audio/charging/kernel/USB cleanup is already announced. libmeminfo is tracked separately as earlier implementation with later validation/preparation. Final release metadata and exact ZIP inclusion remain unspecified.

## Camera workstream closed

The maintainer accepted the [final camera implementation](memory/miuicamera.md) and known limitations. No future changes or test campaigns are planned. Old paused/continuation instructions are historical; reopen only on a new explicit request.

## Accepted results

| Area | Recorded outcome | Detail |
| --- | --- | --- |
| AC-4 | Official 32-second stereo/48 kHz sample reached EOS with 6,144,000 PCM bytes; maintainer confirmed audible playback on rebuilt non-rooted user installation. | [ABI, commits, output and limits](today/2026-09-24-ac4-validation-and-thermal-dialog.md) |
| Thermal Profiles | Maintainer approved final common-tree `3c30e7d` clipping/spacing fix and supplied a System Profile screenshot. No separate per-app test is claimed. | [Parts record](memory/xiaomiparts-device-ux.md) |
| Camera | Main 4K30/60 and ultrawide 1080p clips passed. Ultrawide 4K selection is blocked; ultrawide UI 60fps measured about 30fps. Test APK used a temporary Magisk mount. | [Final recording evidence and APK identity](today/2026-09-23-camera-video-validation.md) |
| libmeminfo | Maintainer reported absent optional DMA-BUF iterator log spam resolved. This does not add a missing kernel backend. | [Delta classification](today/2026-09-24-changelog-delta-index.md) |

These are recorded tests/confirmations, not new tests run by a remote reader. Current root/connection/installed state is unknown until supplied again.

## Source authority

Use [repository map](memory/repositories/README.md), [remote heads](memory/repositories/TRACKED_HEADS.yaml) and [JSON](memory/repositories/LATEST_COMMITS.json). The source snapshot includes GitHub plus required GitLab camera delivery; it is not an artifact manifest. Kernel uses `aosp-17`; frameworks and libmeminfo use their actual `cnb` defaults. The earlier baseline-alignment record and contribution ledgers are historical.

Both camera trees are mandatory delivery dependencies. `hardware/xiaomi` remains standalone. Preserve device-specific opt-ins; do not enable legacy Dolby/Camera2/HBM behavior globally merely because Alioth needs it.

## Older boot findings

The [September 23 kernel capture](today/2026-09-23-latest-kernel-boot-verification.md) verified kernel `10f8a106de65` with user build, enforcing SELinux and Magisk. Earlier WiGig, invalid ASoC route and unsupported LHBM read errors were absent. Cirrus PDN/ultrasound issues remained in that capture; do not infer their present status from later AC-4 tests. The old DMA-BUF log observation is superseded by the maintainer's later libmeminfo confirmation within its stated scope.

## Continuation

No code work or test is automatically started by reading this repository. Follow the user's task and [START_HERE.md](START_HERE.md). No ROM rebuild without an explicit request; `user` variant only. No daily rescan or entire-history import is needed for ordinary work.

## Source-index tooling

[repoindex 1.1.0](today/2026-09-24-repoindex-upgrade.md) is pushed to external `johnmart19/repoindex:main`; the two known WSL copies were synchronized. Compact guides, explicit scans and preservation of curated instructions are the new defaults. Existing Android indexes/guides remain unchanged. This is tooling maintenance, excluded from the ROM changelog.
