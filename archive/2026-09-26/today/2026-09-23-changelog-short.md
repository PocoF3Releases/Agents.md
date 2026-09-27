# POCO F3 — Evolution X | Android 17 / v12.2

> Superseded for generation by [the latest packet](2026-09-24-changelog-preparation.md). Keep this file as historical evidence; camera, AC-4 and libmeminfo status below may be stale.
Draft summary of 23.09.2026 work; final package inclusion pending.

- System: extensive startup/service cleanup, device defaults, network-selection configuration and SQLite defaults.
- Audio/charging: corrected boot routes, removed obsolete mixer controls, restored two-input policy and preserved health-service ownership.
- Kernel/display: disabled unused WiGig, guarded panel calibration, added NNAPI boost-group support and reduced routine diagnostics.
- USB/NFC/core: configfs/controller-readiness handling, NFC shell/API correction and property policy, absent-kernel-node handling.
- Camera source work: guarded SAT buffer correction and VideoSAT extraction/EIS patches; ultrawide 4K remains unresolved and final artifact inclusion must be verified.
- Optional libmeminfo fix committed; missing DMA-BUF warnings still occur on the installed device.

Verified: WiGig, invalid audio-route and LHBM boot errors are gone on the new kernel. Remaining: ultrasound, Cirrus PDN and DMA-BUF errors.

Project work: repository/Agents.md cleanup completed. Existing framework features rebased today are not counted as new features.
