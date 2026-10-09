# October 9 recovery fix and acceptance

**Source/build/device/user evidence.** Temporary recovery boot, active slot B.
Original UI worked but Magisk and decryption failed; ADB shell returned ENOENT.
Android System mounted over /system hid ramdisk runtime; visible OS shell required
/system/bin/linker64, which was absent. Patch 0010 guards the SAR bind/unmount;
0011 blocks the non-SAR UI mount-point switch that bypassed the first guard.
0012 isolates bundled Magisk System mounts in a private updater child namespace.
Third-party Magisk ZIP unchanged; failed namespace setup aborts before updater.

After runtime protection, logs exposed metadata-key upgrade INVALID_ARGUMENT
(-38). Installed ROM reported Android 17 / 2026-10-01, while recovery Boot header
carried 17.0.0 / 2026-09. Matching header to verified October patch restored the
metadata-decrypted dm-backed Data mount. PIN entered only on device; user confirms
password decryption and bundled Magisk installation succeed. ADB then reads
`twrp.all.users.decrypted=true`; recovery shell/linker remain usable after Magisk.
Global SELinux Enforcing; shared recovery domain remains permissive.

User recovery build, ARM/ARM64 updater compilation, theme/policy/ramdisk integrity,
ZIP CRC and packaging passed. Source patch contract: recovery 0001–0012. Current
[source](../state/repositories.yaml) includes the final accepted handoff commit.
Existing recovery-core edits were preserved; only isolated patches exported.

Accepted candidate (Boot metadata 17.0.0 / 2026-10):

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| recovery_boot.img | 100417536 | `2da44881c418359a715b5f6563d0769947311f3feb4771d834e9583578807489` |
| recovery.zip | 70468800 | `f24afbee41f5663f2d3bf0924cc9c722487d1e98c476ce429c52acf4f13a9a61` |

Location: ~/pbrp-alioth/out/release-candidate. Temporary boot did not change slots
or flash recovery. Bundled Magisk installation was explicitly authorized and
user-confirmed; it modifies active Boot. No Data formatting. Standalone recovery
ZIP install and subsequent Android boot not retested. Published October 7 assets
were not replaced by these local candidates.

Never access ~/evo/out. ~/pbrp-alioth/out is allowed. No permissions/policy were
weakened for ADB logs; use only accessible sanitized diagnostics.

## Historical acceptance


**Recorded October 5/7 source/build/host/device/user evidence; no new runtime test.**
[Sources](../state/repositories.yaml), [release identities](../state/releases.md#pbrp-release), and
[recovery behavior](../memory/pbrp-recovery.md) separate current code from assets.
October 5 validated current-recovery installation, UI/touch/vibration, decryption
and USB. Earlier tests covered sideload, Magisk, Boot backup and 120 Hz selection;
not all operations were rerun against every final artifact.

October 7 source-owned handoff reports Format Data after FBE unmount/mapping
cleanup, shared-runtime sload_f2fs startup, and packaged temporary-boot password
decryption/touch/brightness/haptics with global Enforcing. Current infrastructure
domains enforce; shared recovery remains permissive. Patch replay, user policy
build, packaging, theme integrity and ZIP/image checks are recorded passes.

Unverified: live standalone ZIP/image-picker install, Data restore, other
credential types, physical Mi 11X/Redmi K40 acceptance and measured frame pacing.
Fastbootd flashing/postinstall not revalidated after enforcement changes.
External high-speed installer was reviewed only, not imported.
