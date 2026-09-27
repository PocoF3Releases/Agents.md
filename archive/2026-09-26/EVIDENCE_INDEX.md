# Evidence available without WSL

All relative links below are checked-in files. Local paths in dated records are collection provenance only. Do not assume raw artifacts are remotely available.

| Area | Self-contained evidence | Scope / raw-artifact availability |
| --- | --- | --- |
| AC-4 | [Root cause, ABI, fixes and output](today/2026-09-24-ac4-validation-and-thermal-dialog.md); [diagnostic source/result](evidence/ac4/README.md) | Explicit OMX decode reached EOS; user heard sound. Official sample URL is in the record. Full original logcat/disassembly stays local and is not required to understand the fix. |
| Thermal Profiles | [Implementation and user approval](today/2026-09-24-ac4-validation-and-thermal-dialog.md) | User-confirmed System Profile result. Original screenshot is not uploaded; no separate per-app test claimed. Source is in common-tree `parts/src/org/lineageos/settings/thermal/ThermalSettingsFragment.java`. |
| Camera | [Patch identities, APK hash, clip metrics and limits](today/2026-09-23-camera-video-validation.md) | Main 4K30/60 and ultrawide 1080p tested. Original clips/logs stay local; canonical APK on GitLab, patch rationale on GitHub. Ultrawide 4K is guarded and ultrawide 60fps unproven. |
| Kernel / boot | [Capture conclusions](today/2026-09-23-latest-kernel-boot-verification.md) | Historical installed-kernel test, not a current connection check. Request a fresh narrow log only for a new regression. |
| Published baseline | [Release ledger](memory/android16-android17-release-state.md) | Maintainer-supplied September 22/23 published changelogs; exact ZIP manifest/hash absent. |
| Current release delta | [Classification](today/2026-09-24-changelog-delta-index.md) | Separates new fixes from already-announced, validation-only and maintenance work. |
| Stock / Marble / VNDK audits | [Recorded conclusions](today/2026-09-24-ac4-validation-and-thermal-dialog.md) | Stock `~/miui/out`, `~/munch/out` and generated audit folders are not hosted here. No additional symlink or donor-codec migration was justified. |

For new binary questions, the [references repository](https://github.com/PocoF3Releases/references_code) may supply code context, but is not automatically equivalent to the exact tested stock binary. If an original ELF is essential, request that file and its identity; do not silently substitute another OEM/version.

## Additional rework lessons

[Dolby lifecycle, property ownership, per-app touch and MiSound reconciliation](today/2026-09-24-rework-memory-reconciliation.md) preserves historical technical findings without requiring local memory access. It distinguishes prior control acknowledgments from acoustic proof and excludes superseded continuation instructions.
