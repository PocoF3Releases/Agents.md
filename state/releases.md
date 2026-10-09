# Release ledger and changelog workflow

## Authority

Android 17 historical published baseline: **23.09.2026 / Evolution X v12.2**,
from maintainer-supplied September 22/23 notes. Exact ZIP hashes/included-commit
manifest unknown. October 9 local vendor source declares 12.3, which does not
establish a published build. [V-RELEASE](validation.md#v-release).

Maintainer subsequently removed previous posts and requested cumulative initial-
release notes. This changes public presentation, not historical implementation or
acceptance. No new ROM publication identity has been established.

## Android 16 release preparation

Historical September 14 v11.11 notes and September 27 draft are preserved in the
[consolidated project history](releases.md).
Maintainer later reported A16 released and clean-install AC-4 playback with
Magisk; exact newer date/artifact/links remain unknown. Saved A16 refs were
unchanged October 9, with no A16 checkout identified. Do not reuse September 14
links or A17 runtime results. Maintainer's A17→A16 instruction was clean install.
[V-A16](validation.md#v-a16).

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
rebased equivalents. For an initial post, summarize cumulative supported features;
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
[PBRP 4.0 release](https://github.com/PocoF3Releases/device_xiaomi_alioth-pbrp/releases/tag/pbrp-4.0-20261005)
for alioth/aliothin. Tag `pbrp-4.0-20261005`, release target and branch `pbrp-a17`
were verified at `c8a628c80f34105e2c165b28fbf5284cf3a2e05e` after the requested
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
[PBRP release](https://github.com/PocoF3Releases/device_xiaomi_alioth-pbrp/releases/tag/pbrp-4.0-20261007).
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
