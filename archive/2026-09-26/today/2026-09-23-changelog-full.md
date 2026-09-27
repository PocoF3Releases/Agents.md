# POCO F3 (alioth) — Evolution X

> Superseded for generation by [the latest packet](2026-09-24-changelog-preparation.md). Keep this file as historical evidence; camera, AC-4 and libmeminfo status below may be stale.
Android 17 | Evolution X v12.2

Draft covering completed work on 23.09.2026. Release date and final artifact inclusion still require confirmation. Already-shipped rebases and project maintenance are listed separately from new release changes.

## System / startup
- Removed obsolete non-Kona initialization and post-boot branches, unused services and missing helper invocations.
- Cleaned up old Wi-Fi migration/factory hooks, radio fallbacks, diagnostic logging hooks, legacy memory setup and duplicate camera scheduling writes.
- Removed unsupported MIGT/node permissions and aligned startup ownership with Android 17 init.
- Removed the unused device init import, obsolete charger system mount and forced ADB activation in charger mode.
- Removed inapplicable RMNET module hooks and the orphaned QCC HAL implementation.
- Dropped the unused experimental thermal observer and obsolete kernel GCC build flag.
- Restored framework SQLite durability defaults.
- Updated automatic network-selection UI and scan timeout configuration.
- Aligned camera and dialer defaults with selected product packages.

## Audio / charging
- Fixed invalid ASoC routing controls and unused Alioth speaker links; the previous route errors are absent from the latest boot.
- Removed stale headphone compander controls while retaining the codec's supported controls.
- Restored two-input recording limits in audio policy; simultaneous capture still requires a functional check.
- Preserved health-service ownership of the fast-charge preference and removed the conflicting vendor-init operation.

## Kernel / display
- Disabled unused WiGig drivers; repeated PCIe enumeration failures are absent from the latest boot.
- Guarded white local-HBM calibration by panel capability; unsupported reads are absent from the latest boot.
- Enabled the Android NNAPI scheduler boost group.
- Reduced routine battery/thermal telemetry, touch tracing, continuous CVP firmware logging and forced Cirrus amplifier debug logging.

## USB / NFC / core utilities
- Updated Qualcomm USB initialization to use platform configfs ownership and gate unsupported GSI NCM creation.
- Added a bounded wait for USB controller readiness.
- Added the device policy label for the NXP NFC debug-mask property.
- Replaced the incompatible NFC API call in `svc` with NFC service shell commands.
- Preserved the missing-file error for absent kernel attributes instead of attempting to create unsupported nodes.
- Added quiet handling of an absent optional DMA-BUF BPF iterator in the libmeminfo fork. Installed inclusion is not confirmed; the latest device still logs missing DMA-BUF backends. This is not advertised as a resolved runtime issue.

## Camera compatibility work completed in source
- Added a hash-guarded, repeatable CHI SAT buffer-dimension correction and updated the vendor buffer-allocation candidate.
- Preserved the high-quality VideoSAT extraction patch, including quality gates and rear 4K EIS handling.
- Recorded decompiled-camera buffer correction and rear 4K EIS changes.

These camera entries describe completed source/patch work, not confirmation that all recording modes work. Ultrawide 4K remains unresolved. Verify the final APK/blob inclusion before using these as shipped-feature bullets; no new camera tests were performed during the boot audit.

## ROM resync / already-shipped features
- Today's recorded upstream framework updates include coalesced package-change broadcasts and the framework side of a clipboard-overlay toggle. Complete ROM-side history and the toggle's companion UI are not established by this packet.
- HBM timing, high-refresh recording/blur and Camera2 reprocessing changes were rebased during resync. They remain part of the 22.09 semantic baseline and are not new features.

## Completed validation and project maintenance
- Verified the newly installed kernel is 10f8a106de65, with user build, enforcing SELinux and Magisk root.
- Captured boot and later service logs; no new fatal crash or ANR signature was found. USB, NFC and audio initialized.
- Refreshed all 22 repository records; removed six dropped-repository ledgers and 20 non-ancestor commit records.
- Updated Agents.md ownership/routing and prepared full/short changelog drafts, evidence and banner copy.

Maintenance/validation entries are part of today's work record, not ROM feature announcements.

## Remaining / excluded
Ultrasound polling errors, Cirrus PDN timeouts and missing DMA-BUF accounting backends remain. The reverted DMA-BUF kernel option is excluded. No FPS, battery-life, audio-quality or complete VideoSAT success claim is made. No new Dolby/XiaomiParts overhaul is listed because those features were already shipped.
