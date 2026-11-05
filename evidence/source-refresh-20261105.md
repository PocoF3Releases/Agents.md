# ROM and maintained-fork refresh — 2026-11-05

`source-checked`; documentation host checks are scoped below. No Android rebuild
or new device acceptance was performed.

## Updated branches

Full network sync and local checkout both passed for all 1,265 selected projects
using Repo `-j50`. The current manifest moved 12 paths from AOSP to LineageOS;
all 12 complete Git bundles were verified before a targeted metadata force-sync.
An interrupted first attempt left empty manifest objects and default.xml; the
originals were preserved, recovered from an independent upstream clone, and
Git connectivity/XML checks passed. Existing ROM output was preserved.

Fetched 43 maintained build forks plus the separate main-ROM interfaces fork.
The current selected manifest supplied upstream URLs and branches; no stale
merge-base was used to replay rewritten Evolution X history. Thirty-nine unique
allowed upstream heads were checked again immediately before publication.

| Repository | Branch | Published source |
| --- | --- | --- |
| [PocoF3Releases-Recovery/android_hardware_interfaces](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/7f3788f397c18d7fd36b797112fc531b5229066e) | `cnb` | `7f3788f397c1` |
| [PocoF3Releases/android_hardware_nxp_nfc](https://github.com/PocoF3Releases/android_hardware_nxp_nfc/commit/0b8bf91ca3a41a207ccb7429a553dac771433ca2) | `lineage-24.0` | `0b8bf91ca3a4` |
| [PocoF3Releases/frameworks_av](https://github.com/PocoF3Releases/frameworks_av/commit/406810da81b7a68d1f21e197d166dae67e6f0e69) | `cnb` | `406810da81b7` |
| [PocoF3Releases/frameworks_base](https://github.com/PocoF3Releases/frameworks_base/commit/ef5eed4877fbab5038ca77291c5b917bc8112ce9) | `cnb` | `ef5eed4877fb` |
| [PocoF3Releases/hardware_xiaomi](https://github.com/PocoF3Releases/hardware_xiaomi/commit/2ce7b4064a5aa5f42e43a5303fe3279c4adc30d9) | `cnb` | `2ce7b4064a5a` |
| [PocoF3Releases/android_hardware_interfaces](https://github.com/PocoF3Releases/android_hardware_interfaces/commit/580860c5653153f13511b8ed46b7db9a02ca5490) | `cnb` | `580860c56531` |

Five stacks retain all 101 feature commits with equivalent stable patch IDs and
unchanged author names, emails, dates and full messages. Main and recovery
interfaces variants retain their distinct content. No approved camera, DAP,
recording, Xiaomi device controls, thermal-listener or USB lifecycle change was
lost. The upstream ATMS task-options permission check is independent of the
retained signed PixelSystemService listener permission helper.

Two obsolete local commits are omitted:

- Root `1.patch` cleanup: upstream already removed the saved patch file.
- NFC saved-client-ID workaround: the human-authored upstream teardown fix now
  invalidates the live handle, terminates failed receives and releases the saved
  queue correctly. Keeping a cached receive handle would bypass that invalidation.
  Upstream's separate TML read-abort correction is retained unchanged. No new
  adaptation or fabricated author credit was added.

These are source-level review conclusions, not new runtime tests of NFC teardown.
The latest upstream multimedia/interface changes remain upstream commits with
original authorship; they were not rewritten as local features.

## Recovery integration and preservation

The canonical branch-tracking manifest, runner, series and all four authored
mail patches are unchanged. Their SHA-256 values match the series; apply and
postflight both pass, with zero pending patches in all three projects. Recovery
changes are local overlays and were not pushed to ROM-only framework/device refs.

Current framework source plus recovery overlay: `7740198bc2ca02abac684c5980ffe9b85c95ec38`.
The two unchanged device overlays were restored to their previous exact commit
identities after tree-equality proof. Local agent guidance and six pre-existing
Workhub edits remain unchanged. The parked WLAN candidate remains excluded from
the active source tree; no paused charging/touch investigation was reopened.

## Build-failure follow-up

The reported frozen Duck RKP AIDL integrity failure was reproduced with the
existing host tool (exit 1). The checked upstream snapshot carried a mismatched
hash; both AOSP hash generators agreed on the canonical value for the unchanged
API. No API or hash validation was modified locally.

Five newer Evolution X framework commits, ending at
[08e948ba4216](https://github.com/Evolution-X/frameworks_base/commit/08e948ba4216de96137c267ed86d070aa197de4b),
remove the native interface and its module upstream. Replayed all nine custom
patches unchanged onto that head; raw author/message bytes and stable patch IDs
match. No references to the removed native interface remain. Both remaining
frozen framework API hashes pass the actual host integrity verifier (exit 0).
Recovery application and postflight pass unchanged. All 1,265 checkout heads
match the expected source set and have no tracked edits. Rechecked all 39 allowed
upstream mappings with annotated tags peeled; only frameworks/base had advanced.
This is source/host verification; the failed Android build has not been rerun.

## Kernel boundary

The kernel remains at the previously published
[Redline head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d5936f1e0ba3a1fbb2cc22ab3540cfb56788d38c).
The prior upstream intake is still held because required regression work was
platform-restricted. It was not retried, rebased, built or published in this pass.
Do not describe the kernel as updated to the latest upstream or infer new kernel,
configuration, thermal or security acceptance from the ROM source refresh.

## Verification and limits

- All selected source checkouts are clean apart from preserved private guidance.
- Each updated public branch contains its checked upstream. Retained patches,
  author/message bytes, raw Codex trailers and whitespace checks pass.
- Independent read-only reviews found no Required/Critical replay defect and
  supported replacing the local NFC workaround with unchanged upstream fixes.
- The Workhub's 75 local checks pass; these validate documentation/fixtures,
  not Android compilation or hardware behavior.
- No build, installclean, flashing, phone operation, or new functional test was
  performed. The previous November 4 build report predates this source set.
  The maintainer must rebuild separately to obtain updated artifacts.

Private snapshots, backup refs, migration bundles, range comparisons and sync/
publication receipts remain under `~/evo/.repo/source-refresh-20261105/`.
