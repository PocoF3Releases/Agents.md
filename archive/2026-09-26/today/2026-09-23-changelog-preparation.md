# Changelog preparation — next release after 22.09.2026

> Superseded for generation by [the latest packet](2026-09-24-changelog-preparation.md). Keep this file as historical evidence; camera, AC-4 and libmeminfo status below may be stale.

## Status

Prepared, not published. The user requested preparation covering all work completed today. Do not advance the shipped cutoff until publication or explicit baseline approval. The user's completed rebuild is runtime evidence, not a publication event.

Baseline: Android 17 / Evolution X v12.2 shipped 22.09.2026, as recorded in [release-state memory](../memory/android16-android17-release-state.md). Compare semantic features, not commit timestamps. The recorded 22.09 branch heads were treated as included at the time; no exact old artifact manifest was supplied for this preparation.

Deliverables:
- [Full draft](2026-09-23-changelog-full.md)
- [Short mirror/Telegram draft](2026-09-23-changelog-short.md)
- [Latest boot validation](2026-09-23-latest-kernel-boot-verification.md)
- [Pinned source candidates](2026-09-23-changelog-sources.json)

## Source reconciliation

Queried all 17 current code/integration repository default heads used for preparation; they match the refreshed organization index. Dropped repositories are excluded. Unchanged repositories do not generate new release bullets.

The latest boot verifies kernel 10f8a106de65. Installed vendor init.qcom.rc/init.target.rc matched current source in the earlier capture. There is no final ZIP hash or exact installed build manifest in this packet; source inclusion is not universally inferred from pushed HEADs. Local frameworks/av and libmeminfo differed from remote in the resync snapshot.

## Evidence and wording

| Group | Candidate source | Evidence / permitted claim |
|---|---|---|
| Startup cleanup | sm8250-common 6e964d1..cbd5d41 | Device init file hashes matched source; current boot completes. Describe cleanup, not measured speed/battery gains. |
| Audio routes | kernel 16cb6b09c791 | Four old route failures absent on installed kernel. Fixed boot-time invalid routes, not all audio issues. |
| WiGig | kernel 580f12a214a8 | Live WIL6210 disabled; 53 prior probe errors became zero. |
| LHBM | kernel 10f8a106de65 | Both prior read errors absent. No brightness-quality or FOD feature claim. |
| Logging | kernel e091c8586481, 940f43f82166, 2f88a912e3ef, bbf646c1f9e9 | Source changes included in running kernel ancestry; no measured FPS/battery claim. |
| Mixer cleanup | alioth c6c2e98 | Controls checked against device inventory and XML checked; accessory playback not exercised. |
| Concurrent inputs | sm8250-common cbd5d41 | Configuration restored to two inputs; simultaneous capture not exercised. |
| Charging ownership | alioth 8c74dd9; vendor alioth 3e16bfe | Ownership integration present in source; no new fast-charging throughput claim. |
| Network/app defaults | sm8250-common 83e62c6, 5624f9c; alioth 10662c7 | Configuration changes; no radio throughput claim. |
| SQLite | sm8250-common 6eb67a3 | Framework durability defaults restored; no performance claim. |
| Vendor cleanup | vendor common c6c92b9, ff4a56a | Removed unused module hooks/QCC implementation; no ZIP-size reduction measured. |

## Inclusion and release exclusions

- Camera buffer/VideoSAT candidates (alioth 2d181c8, vendor alioth a397258, camera d7356c2, decompiled camera changes): include as completed source work with explicit artifact/runtime limits; do not call it a fully working shipped feature. Camera remains parked; preparation does not resume testing.
- Existing XiaomiParts overhaul, Dolby UI/game-audio work, NFC teardown, Camera2 compatibility, HBM timing and high-refresh recording features are already in the semantic 22.09 baseline. Rebasing them is not a new feature.
- No new Dolby section: hardware_xiaomi is unchanged and standalone.
- NFC svc shell dispatch is a maintenance candidate, not a new NFC teardown feature; include only if the release scope warrants it.
- USB/system_core/libmeminfo forks have no exact 22.09 shipped cutoff in the ledger. Do not infer novelty or installed inclusion from their creation dates. DMA-BUF warnings still reproduce on the device.
- Reverted DMA-BUF kernel option, dropped repository patches, documentation and history cleanup are excluded.
- Full Evolution X upstream ROM changelog is outside this device-side packet. No version bump or upstream release content was inferred.

## Banner copy ready for later generation

Highlights: Startup Cleanup | Audio Routing | Cleaner Kernel Boot

Compact sections:
- System: legacy startup cleanup; updated device defaults.
- Audio: corrected boot routes; mixer configuration cleanup.
- Kernel / Display: unused WiGig disabled; panel calibration guard; quieter routine diagnostics.

Follow memory/release-assets.md for the established 16:9 black/crimson design and previous-banner continuity. No image was generated because release metadata is not final.

## Inputs needed at publication

- Final build date/version and ZIP filename/hash.
- Artifact manifest or confirmed included source revisions, especially remote/local mismatches and optional camera candidates.
- Download/mirror and image links.
- Confirmed installation guidance; do not invent a clean-flash requirement.
- Final selection of held items based on evidence.

After publication, update the semantic release cutoff and included heads in memory/android16-android17-release-state.md. Until then the cutoff remains 22.09.2026.

## Expanded daily coverage

The [completed-today source index](2026-09-23-changelog-completed-today.md) lists the recorded changes individually. Full and short drafts now include USB, NFC/core utility fixes, libmeminfo, NNAPI boost-group support and camera source candidates as well as startup/audio/kernel work. Separate maintenance and resync sections prevent these from being mistaken for new shipped functionality. The 22.09 release cutoff is unchanged.
