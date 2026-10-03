# Current state

Evidence checkpoint: **2026-09-30**. Choose a task below; this is not a backlog.

- **Haptics:** stock-backed AIDL HAL finalized and pushed. Rebuilt baseline and corrected candidate passed device checks; user accepted stronger feedback. The accepted candidate was a temporary mount: the next build must include it. No primitives/PWLE advertised.
- **Camera:** finalized; main 4K30/60 accepted, ultrawide 4K guarded. Ultrawide true 60fps is unproven.
- **Audio:** AC-4 stereo decode and audible playback confirmed on recorded A17/A16 builds; other routes retain their limits.
- **Sources:** upstream now owns local `system/core` and `libmeminfo`. Optional font branch diverges from its remote; preserve it. Branches/heads live only in the source map.
- **Releases:** A17 published baseline is September 23; A16 was later reported released, exact newer artifact/date unknown. Source completion alone is not a release delta.

| Task | Read |
| --- | --- |
| Vibrator | [Haptics](memory/haptics.md) |
| Dolby / AC-4 / audio | [Audio](memory/dolby-audio.md) |
| Camera | [Camera](memory/miuicamera.md) |
| Parts / touch / proximity | [Device UX](memory/xiaomiparts-device-ux.md) |
| Kernel / rootdir / A16 ports | [Platform](memory/kernel-frameworks.md) |
| GPU / games / frame generation | [Graphics](memory/gaming-graphics.md) |
| Changelog / builds | [Releases](state/releases.md) |
| First chat / install skill | [Onboarding](operations/first-chat.md) |
| Windows / WSL reinstall | [Recovery](operations/workstation-recovery.md) |
| LLVM / Ghidra / ADB | [Tools](operations/android-tooling.md) |
| repoindex | [Indexing](operations/repoindex.md) |
| Exact source / test scope | [Sources](state/repositories.yaml) · [Validation](state/validation.md) |

Optional search/router: [INDEX.yaml](INDEX.yaml). [Historical evidence](archive/README.md) loads only for a specific provenance question.
