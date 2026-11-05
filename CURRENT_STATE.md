# Current state

Checkpoint: **2026-11-05**. [Android 17 status](state/android17-status.md).

- **Haptics:** seven effects/eight primitives tested temporarily; older ROM restored. Scale-zero gap remains. [Scope](memory/haptics.md).
- **Recovery:** no-wipe OTA, PIN/local ZIP checks passed; secure image restored. Scrolling improved; password/Weaver unverified. [Scope](memory/evox-recovery.md).
- **Camera:** finalized; main 4K30/60 accepted, ultrawide 4K guarded. Ultrawide true 60fps is unproven.
- **GPU/display:** [Scope](memory/gaming-graphics.md): anti-flicker RRO active; manual mismatch remains.
- **Audio:** AC-4 stereo decode and audible playback confirmed on recorded A17 builds; other routes retain their limits.
- **Sources:** [Refresh](evidence/source-refresh-20261105.md); [kernel checks](evidence/kernel-audio-boundaries-20261102.md).
- **Releases:** October 28 published; November 4 build completion reported. [Releases](state/releases.md).

| Task | Read |
| --- | --- |
| Project history / decisions | [Working memory](memory/project-history.md) |
| Native ROM recovery | [EvoX recovery](memory/evox-recovery.md) |
| Custom recovery / PBRP | [Recovery development](memory/pbrp-recovery.md) |
| Vibrator | [Haptics](memory/haptics.md) |
| Dolby / AC-4 / audio | [Audio](memory/dolby-audio.md) |
| Camera | [Camera](memory/miuicamera.md) |
| Parts / touch / proximity | [Device UX](memory/xiaomiparts-device-ux.md) |
| Kernel / rootdir | [Platform](memory/kernel-frameworks.md) |
| Hardware inventory | [Subsystem map](memory/alioth-subsystems.md) |
| GPU / games / frame generation | [Graphics](memory/gaming-graphics.md) |
| Changelog / builds | [Releases](state/releases.md) |
| First chat / install skill | [Onboarding](operations/first-chat.md) |
| Windows / WSL reinstall | [Recovery](operations/workstation-recovery.md) |
| Host / Android tools | [Tools](operations/host-tooling.md) |
| Source search | [Ready indexes](operations/repoindex.md) |
| Exact source / test scope | [Sources](state/repositories.yaml) · [Validation](state/validation.md) |

Optional search: [INDEX.yaml](INDEX.yaml). Read [archive](archive/README.md) only for provenance.
