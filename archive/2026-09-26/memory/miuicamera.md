# MiuiCamera — finalized

The maintainer accepted the current implementation as the final camera solution. **No future camera changes, optimization experiments or test campaigns are planned.** This is a completed component, not paused work. Only a new explicit user request can reopen it.

## Canonical delivery

- [Device integration](https://github.com/PocoF3Releases/device_xiaomi_camera), branch `aosp-17`, recorded head `1335f9ada0a7b9450f3f10658154300fc795c64c` (documentation after implementation `6c25fe9babca33dfc37813be7a92f5bbbe4d6319`).
- [Vendor APK and prebuilts](https://gitlab.com/johnmart19/vendor_xiaomi_camera), branch `aosp-17`, recorded head `f13797ef3d93508756e06a4a185c9208dbc3ee88`.
- Final APK: 223517496 bytes; SHA256 `29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`.
- Both trees are mandatory device dependencies. Use the ready-to-use vendor APK; maintained [patch documentation](https://github.com/PocoF3Releases/device_xiaomi_camera/tree/aosp-17/patches) explains implementation and provenance.

These are recorded accepted identities, not a claim of a fresh remote/device check. Decompiled experiments and old Stage-1 rollback SHAs are not delivery authority.

## Accepted behavior and limits

- Main-camera 4K30 and 4K60 recordings passed decoding and visual checks; corrupted 4K60 output was corrected by preserving the non-EIS session mode.
- Ultrawide 1080p recording works. The 1080p60 UI selection measured about 30 fps in testing; do not advertise verified ultrawide 60fps.
- Ultrawide 4K is intentionally guarded. Switching to 4K safely restores 1x. Do not propose enabling unsupported 0.6x 4K as unfinished work.
- Logical VideoSAT uses role 60 / camera 4. Do not invent missing role 62 or confuse vendor ArcSoft IDs with Android camera IDs.
- Existing runtime/JNI/capability-cache and compatibility work remains part of the shipped integration. MiuiCamera 5.x is the feature/ABI reference; stock Alioth is a compatibility reference, not a planned replacement.

The maintainer accepts these limits. Finalization does not claim every camera feature, long recording, lens transition or frame rate was exhaustively tested.

## Evidence and release status

[Final recording checkpoint](../today/2026-09-23-camera-video-validation.md) contains the mode matrix, measured clip rates, failure signatures and final artifact details. Those tests used a temporary Magisk installation. User-supplied published September 23 release notes already include these camera fixes; do not announce them again as new work.

[Closure record](../today/2026-09-24-camera-finalized.md) records the maintainer's decision. [Historical investigation archive](miuicamera-history.md) preserves prior ABI findings and experiments, but its pending tasks and alternatives are not a backlog. Read it only for a specific provenance question or an explicitly reopened issue.
