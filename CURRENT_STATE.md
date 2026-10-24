# Current state

Checkpoint: **2026-10-23**. [Android 17 status](state/android17-status.md).

- **Haptics:** stock-backed HAL/PCM with seven effects, three stock primitives and LOW_TICK fallback. Temporary tests are scoped; current installed identity unknown. No full RichTap/PWLE.
- **Native recovery:** A17 no-wipe OTA, PIN unlock and signed storage ZIP checks passed. Secure recovery restored; scrolling improved. Password/Weaver remain unverified. [Scope](memory/evox-recovery.md).
- **Camera:** finalized; main 4K30/60 accepted, ultrawide 4K guarded. Ultrawide true 60fps is unproven.
- **Audio:** AC-4 stereo decode and audible playback confirmed on recorded A17 builds; other routes retain their limits.
- **Sources:** 44 sources checked; framework updated and recovery patches reapplied. User lunch passes; no new runtime acceptance. [Tools](operations/android-tooling.md).
- **Releases:** October 20 update drafts use the confirmed October 14 build as baseline; see [Releases](state/releases.md). Drafts do not establish publication.

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
| GPU / games / frame generation | [Graphics](memory/gaming-graphics.md) |
| Changelog / builds | [Releases](state/releases.md) |
| First chat / install skill | [Onboarding](operations/first-chat.md) |
| Windows / WSL reinstall | [Recovery](operations/workstation-recovery.md) |
| Host / Android tools | [Tools](operations/host-tooling.md) |
| repoindex | [Indexing](operations/repoindex.md) |
| Exact source / test scope | [Sources](state/repositories.yaml) · [Validation](state/validation.md) |

Optional search: [INDEX.yaml](INDEX.yaml). Read [archive](archive/README.md) only for provenance.
