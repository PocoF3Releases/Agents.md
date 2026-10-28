# Release ledger and changelog workflow

## Authority

Current published baseline: **25.10.2026**, confirmed by the maintainer on October 28. Exclude its features and all earlier announced equivalents from the next update.

Android 17 historical published baseline: **23.09.2026 / Evolution X v12.2**,
from maintainer-supplied September 22/23 notes. Exact ZIP hashes/included-commit
manifest unknown. October 9 local vendor source declares 12.3, which does not
establish a published build. [V-RELEASE](validation.md#v-release).

Removed posts led to cumulative initial-release copy. Later publication
confirmations supersede that presentation, without changing implementation
or acceptance history.

## October 14 local release candidate

Resynced Android 17 `lineage_alioth-cp2a-user` installclean build passed with
kernel build #1 and verified OTA archive metadata/integrity. Wi-Fi labels and
Settings were checked after secure sideload and a completed data wipe. The
final localized sound-category ZIP is installed and boots with kernel #1;
Settings, category navigation and validated Wi-Fi pass.
The maintainer later confirmed October 14 as the previous build. [Artifact hashes and source heads](../evidence/evox-native-recovery-20261014.md#resynced-installclean-release-build).

## October 14 update drafts

The maintainer confirmed the initial post is still the latest published Telegram
baseline. These [full](telegram-20261014-full.md) and
[short](telegram-20261014-short.md) drafts cover the verified October 14 v12.3
artifact: native recovery/storage/PIN/installers, specific Parts/Dolby UI
refinements and Wi-Fi startup repair. They exclude previously announced camera,
AC-4, haptics, WireGuard and other equivalent feature families. No Telegram
message has been sent and this draft does not advance the published baseline.
[Generated update banner](assets/evolutionx-alioth-20261014-banner.png).

## October 20 published update

[Full post](telegram-20261020-full.md) and [caption post](telegram-20261020-short.md) compare current sources with the October 14 release manifest. The October 20 ZIP identifies Android 17 / SDK 37, v12.3, Alioth and the October 1 security patch. The copy focuses on upstream Settings/Evolver/SystemUI changes, flashlight behavior, pattern input, thumbnails and translations. Kernel content and recovery features are not re-announced. On October 25 the maintainer confirmed publication of the October 20 build; that confirmation adds no new runtime acceptance.

[Generated update banner](assets/evolutionx-alioth-20261020-banner.png).

## Android 17 post-September 23 delta

Historical accepted additions: AC-4 stereo playback and Thermal Profiles dialog
correction. Later candidate behavior and exact scope live in the owning memory
and validation records, not commit timestamps. Use the cumulative Telegram notes for the requested initial-release presentation.

## Already announced — cumulative ledger

| Historical cutoff | Feature families |
| --- | --- |
| September 16 | Display/recording pacing, kernel/dimming, power/init, Dolby routing/VQE, mixer cleanup. |
| September 22 | MIUI Camera integration/native 48MP/macro/front video; XiaomiParts/thermal/touch/MiSound; Dolby controls; audio battery listener; display/media compatibility; battery/charging/kernel safeguards; NFC and app-compilation defaults. |
| September 23 | Main 4K30/60 fixes, ultrawide guards, startup/audio/charging cleanup, USB/NFC/platform modernization. |

Initial-release notes may describe those cumulative families once. Incremental
future notes must exclude announced equivalents. Ultrawide true 60fps, full
RichTap, generic FPS/battery-life gains and complete endpoint certification are
not established. Historical VDS presence is not proof it survives current resync.
Exact chronology and old heads remain in the original ledger linked above.

## Produce and publish notes

Use [current sources](repositories.yaml) and [scoped validation](validation.md).
Group user-visible behavior; omit reverted experiments, docs/build tooling and
rebased equivalents.
Use bold Telegram headings and explicit Markdown hard breaks for Unicode bullet
lines and blank spacing, so rendered GitHub copy does not collapse paragraphs.
Copy rendered text into Telegram; raw Markdown contains formatting escapes. For an initial post, summarize cumulative supported features;
for an update, compare with its actual published semantic baseline.

[Full Telegram post](telegram-initial-full.md) and
[short Telegram post](telegram-initial-short.md) are the October 9 initial-release
copy. They follow grouped emoji headings; the short copy keeps only highlights.
No message was sent. Confirm matching artifact inclusion before publication.
Do not invent a build date, version, download link or install requirement.
Banner highlights must come from the same features; see
[artwork](../operations/release-artwork.md).
After actual publication or explicit baseline declaration, record artifact identity
and update current state. A draft never advances the release baseline by itself.

## Later source-completed candidates

Stock-backed AW8697 and LOW_TICK fallback, proximity correction, firmware touch
controls, Parts lifecycle/refresh fixes, modem initialization/cache permissions,
atomic thermal maps, sensor/fingerprint and battery/touch safeguards are included
as applicable in the current initial draft. Their temporary/host/target evidence
is not acceptance of a complete rebuilt ROM. See the owning topics and
[V-SOURCE-20261009](validation.md#v-source-20261009).

## PBRP release

**2026-10-05 — published recovery, separate from ROM release baselines.**
Historical PBRP 4.0 release (former repository deleted; original download link unavailable)
for alioth/aliothin. Tag `pbrp-4.0-20261005`, release target and branch `pbrp-a17`
were verified at [c8a628c80f34](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp/commit/c8a628c80f34105e2c165b28fbf5284cf3a2e05e) after the requested
initial-history squash. Asset identities rechecked using GitHub API:

| Asset | Bytes | SHA256 |
| --- | --- | --- |
| recovery_boot.img | 100495360 | `096f1b99e017dd75a235ef81d766db4486b29ed8fc0f55092222b1d927800896` |
| recovery.zip | 70551257 | `c8b96b947e3907a7184d00e684d009386c382883f65558de2bb8e15e97b1178a` |
| SHA256SUMS | 163 | `61010be84dc30068e512d97de9b982f4a6f9579417eb679aef64c671f0c05fd3` |

Matching ROM used for packaging and installation validation:
`EvolutionX-17.0-20261004-alioth-12.2-Unofficial.zip`. This reference does not
establish its public publication date or certify all ROM components. Recovery
installation modes, policy boundary and validation limits live in
[Recovery](../memory/pbrp-recovery.md) and [V-PBRP](validation.md#v-pbrp).

## October 9 source audit and latest draft

Current presentation uses the cumulative initial-release posts above. The
October 9 audit does not establish a new ROM publication.

**2026-10-07 — newer published PBRP release, rechecked October 9.**
Historical PBRP release (former repository deleted; original download link unavailable).
GitHub API reports these publisher asset digests (not a new download/hash test):

| Asset | Bytes | SHA256 |
| --- | --- | --- |
| recovery_boot.img | 100417536 | `eaec69e04b3b27ee2373426384d32c62ea5280cc006904a691df35a27d988379` |
| recovery.zip | 70466929 | `237eaf34aa05bbbbf3adcfa5ebbae971ff9c3957c8446b6c97f93b9541eb4b0c` |
| SHA256SUMS | 163 | `302b39491656fc32b7cb700899cd4d0e4adbc1bd02762760f584be118a610d9a` |

Current recovery source is newer than this release; do not equate branch HEAD
with the October 7 artifacts. October 5 asset identities remain historical.

## Final initial-build source review

The [implementation audit](changelog-audit.md) covers all 19 organization repositories and 16 current custom ROM
source inputs, including required GitLab camera and newly tracked tinycompress.
The full/short Telegram posts now include recording controls, final media/display
compatibility and capture-read safeguards, grouping duplicate changes once.
No new ROM publication or universal runtime acceptance is implied.

The October 11 standalone [recovery source](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp) has no published release assets. Historical asset hashes above are retained as records, not current download links.

## Next-update history preparation

[Workflow](../operations/changelog-history.md): immutable checkpoints and
patch-equivalence filtering. A source checkpoint is not an artifact manifest.

## October 25 published update

The maintainer confirmed publication on October 28. The saved
[full](telegram-20261025-full.md) and [short](telegram-20261025-short.md) Telegram
copy cover the rebuilt October 25 v12.3 release relative to October 20.
The assistant sent no Telegram message; publication was confirmed by the maintainer.

[Banner](assets/evolutionx-alioth-20261025-banner-v2.png) ·
[exact imagegen prompt](assets/evolutionx-alioth-20261025-banner-v2-prompt.txt).
The approved phone geometry and six-card layout were visually checked.
Refresh-rate highlights remain excluded per the maintainer.

The [eligibility review](../evidence/changelog-20261025.md) separates actual new
behavior from earlier announcements, rebased equivalents and unused components.
[Installed-build smoke checks](../evidence/release-smoke-20261025.md) retain their
short-test scope; release copy does not certify all endpoints.

## October 28 next-build drafts

[Long](telegram-20261028-full.md) · [short](telegram-20261028-short.md) ·
[eligibility/limits](../evidence/changelog-20261028.md).
October 25 cutoff; Redline, distinct kernel fixes and SPU shutdown permission.
The maintainer confirms shutdown hangs no longer occur. Prior announcements,
refresh-rate tuning and repicks are excluded. New artifact/date unspecified:
these drafts require latest-source inclusion, advance no publication baseline
and send no message. No new artwork was requested.
