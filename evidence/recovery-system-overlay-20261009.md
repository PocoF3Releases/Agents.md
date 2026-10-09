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

Initial accepted candidate (superseded below; Boot metadata 17.0.0 / 2026-10):

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| recovery_boot.img | 100417536 | `2da44881c418359a715b5f6563d0769947311f3feb4771d834e9583578807489` |
| recovery.zip | 70468800 | `f24afbee41f5663f2d3bf0924cc9c722487d1e98c476ce429c52acf4f13a9a61` |

Location: ~/pbrp-alioth/out/release-candidate. Temporary boot did not change slots
or flash recovery. Bundled Magisk installation was explicitly authorized and
user-confirmed; it modifies active Boot. No Data formatting. Standalone recovery
ZIP install and subsequent Android boot were pending in that initial cycle. Published October 7 assets
were not replaced by these local candidates.

Never access ~/evo/out. ~/pbrp-alioth/out is allowed. No permissions/policy were
weakened for ADB logs; use only accessible sanitized diagnostics.

## Follow-up: installer signing, real reboot and fastbootd

The initial accepted recovery was followed by Android boot on slot B with
Magisk 31.0 and October patch verified over ADB. Removed package-installer.py
references to ROM output signing tools; JDK 17, SignApk/JNI and public test keys
now come only from the recovery checkout. Recovery-local `m -j4 signapk` and
optimized-Python packaging passed explicit CRC, image and payload hash checks.
Corrected outdated policy descriptions in the installer and patch guide.

Standalone ZIP `10e9903810feef40e045fbfa94e4693d706c9b42adbc139bab7d48fa869b3736`
was sideloaded on slot B. User confirmed written-image verification and Magisk
installation. Android boot then completed but su was absent; installer completion
alone did not prove Android root. User manually reinstalled Magisk; subsequent
ADB verified Magisk 31.0. The resulting working Boot was privately backed up and
hash-verified before further changes. No root regression cause was established.

Reboot Recovery/fastboot initially restarted the recovery process without
rebooting. Init AVCs showed enforcing write denial on misc `/dev/block/sda11`,
which had generic block_device context. The device-only recovery file_contexts
now labels this verified node misc_block_device, using the existing platform
init permission. No broad block-device allow or permissive change was added.

User recovery build and packaging passed. A policy-only Boot deployment
preserved kernel/header and Magisk contents; only file_contexts.bin,
vendor_file_contexts and ramdisk checksum list changed. Temporary Android boot
completed with Magisk 31.0. Flashed only active boot_b. Recovery showed the correct
misc context, Enforcing and decrypted=true. `adb reboot recovery` performed a real
kernel reboot: uptime reset from 34.40 to 22.93 seconds; recovery returned on slot
B without the prior init denial. The GUI uses the same init power-control path;
a separate physical GUI-button test was not performed.

Fastbootd then enumerated as 18d1:d00d, but Windows reported missing driver Code
28. Existing signed Google driver supports 18d1:4ee0, so source USB config now
uses that standard generic fastboot identity. Its final device compatibility
validation remains pending. No fastbootd partition flash was attempted. A stale
Windows ADB server after temporary Boot re-enumeration was resolved by restarting
that server; this was not a recovery policy failure.

Final published recovery source: `77fb84dc755f13f1b8208371bb40812e65f986db`.
Final follow-up user build and packaging checks passed. Candidate hashes (new
fastboot USB ID not yet device-tested):

- recovery_boot.img: `c3a28f66381226995a98bdd2186479750f62f8922e869a604753ad117b64a8fd`
- recovery.zip: `eef82bb2c0b8fec2107875f11e81bbe2197d456494bdc4783296ca8a1ae7a1a2`

The deployed policy-only Boot is distinct from these distributable candidates.
The phone remains in fastbootd with no host driver; Reboot System on-device
returns Android. No final fastbootd flashing or postinstall test is claimed.

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
