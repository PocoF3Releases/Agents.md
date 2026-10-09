# Current state

Evidence checkpoint: **2026-10-09** (source audit; runtime dates stay scoped). Task router, not a backlog.

- **Haptics:** stock-backed HAL/PCM with seven effects, three stock primitives and LOW_TICK fallback. Temporary tests are scoped; current installed identity unknown. No full RichTap/PWLE.
- **Recovery:** October 9 FBE/reboot fixes verified; shared recovery permissive. Fastbootd driver test pending. Published assets differ from HEAD.
- **Camera:** finalized; main 4K30/60 accepted, ultrawide 4K guarded. Ultrawide true 60fps is unproven.
- **Audio:** AC-4 stereo decode and audible playback confirmed on recorded A17/A16 builds; other routes retain their limits.
- **Sources:** track only repositories maintained by us. Upstream dependencies and retired forks are excluded from the source map; retain relevant integration facts in topic memory.
- **Releases:** Cumulative initial-release copy in [Releases](state/releases.md). A17 baseline: September 23. A16 later reported released; exact artifact/date unknown. Source completion is not a release delta.

| Task | Read |
| --- | --- |
| Project history / decisions | [Working memory](memory/project-history.md) |
| Custom recovery / PBRP | [Recovery development](memory/pbrp-recovery.md) |
| Vibrator | [Haptics](memory/haptics.md) |
| Dolby / AC-4 / audio | [Audio](memory/dolby-audio.md) |
| Camera | [Camera](memory/miuicamera.md) |
| Parts / touch / proximity | [Device UX](memory/xiaomiparts-device-ux.md) |
| Kernel / rootdir / A16 ports | [Platform](memory/kernel-frameworks.md) |
| GPU / games / frame generation | [Graphics](memory/gaming-graphics.md) |
| Changelog / builds | [Releases](state/releases.md) |
| First chat / install skill | [Onboarding](operations/first-chat.md) |
| Windows / WSL reinstall | [Recovery](operations/workstation-recovery.md) |
| Host / Android tools | [Tools](operations/host-tooling.md) |
| repoindex | [Indexing](operations/repoindex.md) |
| Exact source / test scope | [Sources](state/repositories.yaml) · [Validation](state/validation.md) |

Optional search: [INDEX.yaml](INDEX.yaml). Read [archive](archive/README.md) only for provenance.
