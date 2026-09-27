# September 24 delta after the published September 23 release

Authority: the maintainer supplied both published changelogs in conversation. September 23 is the latest shipped semantic baseline; September 22 remains an older cumulative baseline. No final ZIP manifest was supplied.

| Work | Classification | Evidence / handling |
| --- | --- | --- |
| Dolby AC-4 initialization and helper lookup | New functional release candidate | frameworks/av `801d9c6ecd`, `6c0db963ed`, `ae242b56da`; common `428db4a`, `e019493`. Stereo 48 kHz sample reached EOS and audible playback was user-confirmed. Absent from both published changelogs. |
| Thermal Profiles title/footer clipping and spacing | New functional release candidate | Common `3c30e7d` is the final implementation, superseding `db27251`; maintainer approved the screenshot/result. Absent from both published changelogs. |
| libmeminfo optional DMA-BUF iterator log suppression | Validation/commit preparation today; optional unannounced maintenance note | `09538b6` is the current revision; maintainer confirmed no more log spam. The solution existed before today's commit-message preparation. Do not claim newly implemented today, and do not infer prior artifact absence merely because published notes omit it. Keep out of the strict today-only feature draft unless the maintainer chooses to announce it. |
| HBM/Camera2/framework compatibility opt-in guards | Portability/refactoring, not a new Alioth feature | Alioth `1a6be06`; framework guards retain existing Alioth behavior. Already announced underlying functionality must not be counted again. |
| Camera video, startup, audio routes, charging, kernel, USB/NFC and vendor cleanup | Already announced September 23 | Exclude entirely from new-feature bullets, even if rebased, validated again or assigned new hashes. |
| Dolby UI/game-audio, XiaomiParts overhaul, NFC teardown and older framework/media work | Already announced September 22 | Exclude equivalent rebases and history rewrites. AC-4 playback and the later dialog regression fix remain distinct. |
| Profile/README/Agents.md updates, repository alignment and history cleanup | Project maintenance | Exclude from ROM changelog. |
| Marble/VNDK/64-bit-only investigation | Audit, not additional implementation | Only the implemented OMX helper path is included under AC-4. No donor codec migration, extra foundation/xlog symlink or 64-bit-only conversion was shipped. |

This index groups semantic results, not every intermediate commit. The source-head snapshot locates candidate code but does not prove a final artifact includes it. No new upstream ROM delta has been established by this packet.
