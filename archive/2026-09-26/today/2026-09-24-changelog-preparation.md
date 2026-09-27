# Latest changelog preparation

The maintainer supplied the published September 22 and September 23 changelogs. **September 23 is the latest shipped semantic baseline**, superseding the earlier September 22 cutoff in this preparation packet. Generate only the September 24 delta; do not recycle already-announced camera/startup/audio/kernel fixes.

## Authoritative generation inputs

- [Published semantic baseline](../memory/android16-android17-release-state.md)
- [Today-only classification index](2026-09-24-changelog-delta-index.md)
- [Full draft](2026-09-24-changelog-full.md)
- [Short draft](2026-09-24-changelog-short.md)
- [Source candidates](2026-09-24-changelog-sources.json), not a shipped artifact manifest
- [AC-4 and Parts validation](2026-09-24-ac4-validation-and-thermal-dialog.md)

## Current selection

Include **AC-4 playback correction** and **Thermal Profiles dialog correction**. Both have user-confirmed runtime results; preserve the sample/dialog scope described in the evidence.

Track libmeminfo separately as an older implementation with today's validation/commit preparation, not new code written today. Its omission from the supplied published notes does not establish when it entered a ZIP. Keep it out of the strict today-only draft unless explicitly selected as an unannounced maintenance note.

Framework opt-in guards preserve existing behavior and belong in maintainer integration notes. Camera, startup, audio routing, charging, kernel, USB/NFC and cleanup were already announced on September 23. Earlier Dolby/game-audio/XiaomiParts overhauls were announced on September 22. Documentation, profile updates and history cleanup are excluded.

## Before publication

Confirm final package inclusion, build date/version, ZIP/hash and download links. Do not infer exact shipped SHAs from publication prose or add unverified upstream changes. Do not change the September 23 cutoff until the next release is published or explicitly approved as a baseline.

Suggested highlights: **AC-4 Playback Fixed | Thermal Profiles Dialog Fixed**.
