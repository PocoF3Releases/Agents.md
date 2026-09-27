# Current state and topic directory

Updated **2026-09-27** from conversation evidence; no fresh device tests or head survey.

**Android 16:** Evolution X v11.11 was rebuilt and clean-installed by the maintainer, with Magisk installed. The maintainer confirmed audible AC-4 playback. September 27 release copy/banner is drafted; public release and ZIP identity remain unverified. See the [release ledger](memory/android16-android17-release-state.md) and [A16 acceptance](memory/validation.md#v-a16).

**Android 17:** September 23 / v12.2 remains its recorded published baseline. Prior acceptance retains its recorded scope; source checks alone do not prove installed behavior. Camera is finalized with accepted limitations and no planned work.

## Read one topic

| Task | Canonical record |
| --- | --- |
| Device trees, rootdir, kernel, NFC, ART/build flags, historical Turnip/UVC/input | [Platform](memory/kernel-frameworks.md) |
| Dolby, game/VoIP processing, AC-4, stock ABI | [Audio](memory/dolby-audio.md) |
| Camera delivery, accepted modes, rejected approaches | [Camera](memory/miuicamera.md) |
| XiaomiParts, thermal/touch, MiSound, translations | [Device UX](memory/xiaomiparts-device-ux.md) |
| New changelog, published features, Android 16 maintenance | [Release ledger](memory/android16-android17-release-state.md) |
| Banner, avatar, typography and visual checks | [Artwork](memory/release-assets.md) |
| A test result, acceptance limit or missing raw artifact | [Validation register](memory/validation.md) |
| Knowledge writes, Git conventions, model handoffs, repoindex | [Maintenance](memory/agent-memory-workflow.md) |

[Recorded source map](memory/repositories/TRACKED_HEADS.yaml) owns repository URLs, branches and observed heads. Resolve only the relevant live head before new code work. It is not a flashed manifest; its knowledge-repository entry is historical too.

Validation limits and unresolved historical findings live in the [register](memory/validation.md); consult the relevant entry, not the full archive.

Do not start work just because a record contains an old next step. For provenance not covered by a topic, use [the archive directory](archive/README.md), then retrieve only the required source record.
