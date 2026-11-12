# Release ledger and changelog workflow

## Authority

Published baseline: **04.11.2026**, explicitly confirmed by the maintainer November 12. Exclude its features and all earlier announced equivalents from the next update.

Android 17 historical published baseline: **23.09.2026 / Evolution X v12.2**,
from maintainer-supplied September 22/23 notes. Exact ZIP hashes/included-commit
manifest unknown. October 9 local vendor source declares 12.3, which does not
establish a published build. [V-RELEASE](validation.md#v-release).

Removed posts led to cumulative initial-release copy. Later publication
confirmations supersede that presentation, without changing implementation
or acceptance history.

## October 14 installed update and drafts

Android17 `lineage_alioth-cp2a-user` installclean/kernel#1 completed. Secure
sideload and data wipe, final localized sound heading, Settings and Wi-Fi passed.
The maintainer later identified October14 as the previous build.
[Artifact/source evidence](../evidence/evox-native-recovery-20261014.md#resynced-installclean-release-build).

[Full](telegram-20261014-full.md), [short](telegram-20261014-short.md) and
[banner](assets/evolutionx-alioth-20261014-banner.png) cover native recovery/PIN/
installers, Parts/Dolby refinements and Wi-Fi startup repair. Older camera, AC-4,
haptics and WireGuard announcements are excluded. At drafting time the initial
post remained the latest confirmed publication; no Telegram message was sent.

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

[Audit](changelog-audit.md):19 organization repositories/16 custom ROM inputs,
including GitLab camera and tinycompress. Initial copy includes recording,
media/display and capture-read changes once; source completion is not rebuilt-ROM
acceptance. The October11 [standalone recovery source](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp)
had no published assets; retained older hashes identify historical releases.

## Next-update history preparation

[Workflow](../operations/changelog-history.md): immutable checkpoints and
patch-equivalence filtering. A source checkpoint is not an artifact manifest.

## October 25 published update

The maintainer confirmed publication on October 28. The saved
[full](telegram-20261025-full.md) and [short](telegram-20261025-short.md) Telegram
copy cover the rebuilt October 25 v12.3 release relative to October 20.

[Banner](assets/evolutionx-alioth-20261025-banner-v2.png) ·
[exact imagegen prompt](assets/evolutionx-alioth-20261025-banner-v2-prompt.txt).
Approved phone geometry and six-card layout checked; refresh highlights excluded.

[Eligibility](../evidence/changelog-20261025.md) excludes earlier announcements,
rebased equivalents and unused components.
[Installed-build smoke checks](../evidence/release-smoke-20261025.md) retain their
short-test scope; release copy does not certify all endpoints.

## October 28 published update

Confirmed by the maintainer November 4; saved [long](telegram-20261028-full.md),
[short](telegram-20261028-short.md), [review](../evidence/changelog-20261028.md)
and [banner](assets/evolutionx-alioth-20261028-banner-v1.png). October 25 cutoff:
Redline, kernel repairs and SPU unmount permission. No exact final artifact
manifest was captured. Refresh highlights remain excluded; shutdown hangs no
longer occur per the maintainer.

## November 4 published update

Maintainer reports `EvolutionX-17.0-20261104-alioth-12.3-Unofficial.zip` built
successfully (42,815 steps; 01:22:03). Publication was explicitly confirmed on
November 12. The exact published source manifest remains unavailable; this
confirmation does not add historical phone acceptance.

## November 12 installed release candidate

v12.4 / Android17 / SDK37: [artifact identity and phone scope](../evidence/release-smoke-20261112.md)
pass. New changes since November4: [long](telegram-20261112-full.md),
[short](telegram-20261112-short.md), [banner](assets/evolutionx-alioth-20261112-banner.png)
and [built-in imagegen prompt](assets/evolutionx-alioth-20261112-banner-prompt.txt).
Drafts only; no download URL or publication. November4 remains the baseline.
