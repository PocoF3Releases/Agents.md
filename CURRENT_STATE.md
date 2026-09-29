# Current state and topic directory

Updated **2026-09-30**: public refs and tools inspected; device results retain their recorded scope.

**Android 17:** camera is finalized. Latest Alioth haptics source is pushed and compile/host-tested, but physical validation awaits the maintainer's rebuild/reconnection. Do not request the device again until available or claim PWLE/FOAM support. September 23 / v12.2 is the recorded published baseline, not the installed identity of later development builds.

**Android 16:** rebuilt and clean-installed; audible AC-4 confirmed. Exact ZIP identity/publication of later drafts remains unverified. See the release ledger before writing changelogs.

## Read one topic

| Task | Record |
| --- | --- |
| Windows/WSL backup and recovery | [Recovery](memory/workstation-recovery.md) |
| Ghidra, LLVM, JADX, ADB and build helpers | [Tools](memory/android-tooling.md) |
| repoindex restore, copies and databases | [Indexing](memory/repoindex.md) |
| AW8697 implementation and pending tests | [Haptics](memory/haptics.md) |
| Rootdir, kernel, NFC, build compatibility | [Platform](memory/kernel-frameworks.md) |
| Dolby, AC-4, stock audio ABI | [Audio](memory/dolby-audio.md) |
| Camera delivery and accepted limitations | [Camera](memory/miuicamera.md) |
| Parts, touch, proximity and translations | [Device UX](memory/xiaomiparts-device-ux.md) |
| Changelog baseline and A16/A17 releases | [Release ledger](memory/android16-android17-release-state.md) |
| Banner and visual checks | [Artwork](memory/release-assets.md) |
| Acceptance and missing evidence | [Validation](memory/validation.md) |
| Knowledge edits and model handoff | [Maintenance](memory/agent-memory-workflow.md) |

[Source map](memory/repositories/TRACKED_HEADS.yaml) owns observed URLs/branches/heads. It is not a flashed manifest. Recheck relevant refs before code work; local font divergence and upstream libmeminfo ownership are recorded there.

Old next steps are not new authorization. Use [archive routing](archive/README.md) only for provenance missing from the current topic.
