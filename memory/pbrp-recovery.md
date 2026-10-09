# Alioth PitchBlack recovery

Checkpoint: **2026-10-09** (source review; runtime evidence October 7). Separate PBRP Android 14 userspace checkout at
`~/pbrp-alioth`; ROM checkout is `~/evo`. Android 17 compatibility does not mean
recovery userspace was rebased to Android 17. Read this topic only for recovery.
Public source/ref identities belong in [Sources](../state/repositories.yaml),
artifacts in [Releases](../state/releases.md), acceptance in
[V-PBRP](../state/validation.md#v-pbrp).

## Implemented scope

- PBRP 4.0 for `alioth` (POCO F3 / Redmi K40) and `aliothin` (Mi 11X).
  Board assertions and installer accept both; physical acceptance was on Alioth.
  About avoids the duplicated POCO brand. Keep ROM regional variant detection
  separate from recovery branding; never replace Alioth identifiers with Peridot.
- Recovery-as-Boot, header v3. Boot is 201326592 bytes; vendor_boot is
  100663296 bytes. Distribute Boot only; never flash the generated placeholder
  vendor_boot. Main Android 17 kernel/DTB/DTBO remain separately maintained.
- Working UI/touch, manual brightness, RTC correction, timed AW8697 vibrations,
  MTP/ADB, DRM 120 Hz selection and 120 FPS GUI configuration. No auto-brightness;
  configured refresh/frame rate is not proof of measured smooth animation.
- FBE metadata/password decryption with Keymaster/keystore2 and matching ROM
  boot OS/security patch metadata. Never solicit credentials in chat.
- Virtual A/B product inheritance/properties for ROM sideload. Preserve the
  existing update_engine path and snapshot lifecycle.
- Bundled unmodified Magisk v31.0, installed only by explicit action. Provenance
  and SHA256: device tree `recovery/root/twres/tools/MAGISK_SOURCE.md`.
  KernelSU proposal was cancelled; no KSU integration or installer is shipped.

## Safe partition and GUI exposure

Mount offers Android filesystems, Data and connected USB-OTG. Protected
Persist/EFS/Firmware/Metadata service partitions are hidden. Backup/restore
exposes Boot, Vendor Boot, DTBO and Data, defaulting to Boot only; stale backup
selections cannot re-expose protected entries. Install opens `/data/media/0`.
Unsupported SD repartition, manual snapshot/unmap, filesystem repair/resize/
conversion, legacy fixes, kernel replacement and unfinished OTA settings are
hidden or guarded. PBRP Special has Tools, Customizations, Settings and About.

Advanced keeps **Install Current Recovery** above **Install Recovery from
Image**. Current opens swipe confirmation and uses upstream
`Flash_Current_Twrp`; image opens a picker. Both replace only the active Boot
ramdisk while retaining the current kernel. The image path follows its optional
backup checkbox. Keep subtitles short, provide English resource keys, and check
for missing-string warnings and stale packaged themes.

The standalone `recovery.zip` stages original Boot in `/tmp`, verifies inputs,
repackages its ramdisk, checks kernel/header/partition size and readback bytes.
It needs neither decrypted storage nor mandatory persistent backup/OTG/cache,
and does not automatically reboot or change slots. Ramdisk replacement removes
an existing Magisk patch; reinstall Magisk afterward. An installer ZIP writes
Boot; only `fastboot boot recovery_boot.img` is a temporary RAM launch.

## Recovery policy boundary

Current source permits only the shared `recovery` domain. Infrastructure
`init`, `logd`, `adbd`, `fastbootd`, `postinstall` and `ueventd` enforce.
Recovery-only permissions cover measured hardware/rootfs/keyring/scheduling
operations and exact USB mode labels; logd uses an init-owned control socket.
Neverallow and Android policy checks remain intact. Global Enforcing does not
make the shared UI/decryption domain fully enforcing. October 5's seven-domain
policy is historical; do not restore its allowlist for a current build.

## Reproduce and update

The device tree [README](https://github.com/PocoF3Releases/device_xiaomi_alioth-pbrp/blob/pbrp-a17/README.md),
[handoff](https://github.com/PocoF3Releases/device_xiaomi_alioth-pbrp/blob/pbrp-a17/Agents.md)
and [patch manifest](https://github.com/PocoF3Releases/device_xiaomi_alioth-pbrp/blob/pbrp-a17/patches/README.md)
are the source-owned build contract. Patch baselines:

| Sibling repository | Clean base | Application order |
| --- | --- | --- |
| `bootable/recovery` | `4ea56986534da92b29c73ea1907e10e3c0d5ef50` | recovery 0001–0005 TeamWin imports, then 0006–0009 Alioth/FBE/haptics/logd changes |
| `vendor/pb` | `2124e85c72c4d4ff9ef18a7303950d0480257e34` | vendor-pb 0001 adbd context, 0002 infrastructure enforcement |
| `external/f2fs-tools` | `a7424d458d4b924be8205986c7b7829c934127d8` | 0001 shared C++ runtime for sload_f2fs |
| `system/sepolicy` | `dd91f58a018a43d70c40abb86dddb85368015b96` | system-sepolicy 0001 historical allowlist, 0002 restrict to recovery |

1. Verify clean status, relevant remotes and patch bases. Apply each series once
   with `git am` in filename order to clean bases, never the patched development
   checkout. Preserve upstream authorship. Original final recovery replay matched
   the built Git tree; repeat that comparison when replacing patches.
2. Use the tracked Android 17 kernel artifacts in `prebuilt/`: `Image`,
   `dtbs/alioth.dtb`, `dtbo.img`, with provenance/SHA256SUMS. Recorded tested kernel: `ac2a025a05e6f6d9cf12b020c739019fafb33987`,
   Linux 4.19.325-cip136-st20. Recheck kernel compatibility when updating it.
3. Build only when requested, using user target and checkout tools:

```sh
cd ~/pbrp-alioth
device/xiaomi/alioth/tools/build-recovery.sh
python3 device/xiaomi/alioth/tools/package-recovery.py --rom /path/to/matching-ROM.zip
python3 device/xiaomi/alioth/tools/package-installer.py
```

The wrapper lunches `pb_alioth-user` and builds `bootimage` with `JOBS` default 8.
Packaging derives OS/security patch metadata from the matching ROM ZIP, checks
source/staged theme equality, validates the recovery-only permissive policy, and regenerates
ramdisk-file integrity hashes. Direct Ninja can leave stale theme resources;
refresh/rebuild the theme rather than bypassing the packaging mismatch check.
Never disable `Flash_Current_Twrp` integrity checking. Final check covered 3500
files. Packaging tools do not flash.

Deliver `out/release-candidate/recovery_boot.img`, `recovery.zip`, `SHA256SUMS`.
Installer signing uses existing signapk/public AOSP test keys, not private keys.
Check ZIP CRC/payload hashes, Boot size/header and exact shipped policy before
publication. Commit source with required co-author trailer; update patch series
and source-owned docs together. Verify remote branch/tag/release target and
GitHub asset digests. The initial history squash was explicitly authorized;
future updates do not inherit blanket force-push authorization.

## Bounded device acceptance

Use Windows platform-tools for USB, WSL Ubuntu 26.04 for sources/builds. Resolve
actual paths first. Fastboot UNC transfers timed out; a Windows-local image copy
and reconnect worked. Temporary boot does not authorize partition flashing.
User-build recovery ADB is unprivileged; do not relax SELinux or file permissions
to read root-only logs/ORS. Prefer UI/MTP. `/tmp` pushes can fail at fchown;
Windows binary stdin was truncated. For necessary transfers use ASCII base64
and verify the remote hash. Do not use `adb wait-for-device` to wait for recovery
state; inspect `adb devices` with bounded waits.

After relevant changes: temporary boot, UI/touch/brightness/haptics/time, USB,
password decryption, supported menus, current/image ramdisk paths and explicit
sideload/Magisk tests as authorized. Preserve userdata; no format/Data restore
just to validate UI. Compare Boot kernel/header before and after repack, verify
written bytes and active slot, then verify Android boot. Record exact tested
artifact and distinguish tests carried over from earlier candidates.

## High-speed flashing research — not imported

External OrangeFox `17` at
[c447ba31612d01e3b305788d700cf5c493bba256](https://github.com/khargosxh18/android_bootable_recovery_fox/commit/c447ba31612d01e3b305788d700cf5c493bba256)
was source-reviewed only. It replaces payload installation with liblp/custom
Go logic, can discard source-slot groups and directly modifies metadata/slots.
Its recovery_a/b assumptions do not fit Alioth Boot-ramdisk installation.
No port or measured 40–60 second result exists. Keep update_engine; any requested
port needs snapshot/slot safety, verification and ramdisk preservation. The
reviewed launcher did not pass --no-verify despite older documentation wording.

## Latest FBE and startup behavior

Source adds FBE unmount-before-format handling, sload_f2fs C++ linkage,
recovery hardware labels/haptic write corrections and secure Qualcomm library
lookup. Current policy removes six infrastructure permissive declarations;
global Enforcing still leaves the shared recovery domain permissive. Commit
messages report packaged temporary-boot password decryption, touch, brightness
and haptics acceptance; not fresh tests in this audit. Fastbootd flashing,
postinstall and standalone ZIP installation were not revalidated. October 7
published assets predate latest source; see [release ledger](../state/releases.md).

## October 9 live diagnosis

[System-overlay evidence](../evidence/recovery-system-overlay-20261009.md):
UI works; command execution fails with the mounted System hiding recovery runtime.
Slot identity and complete decryption/Magisk causes remain unconfirmed.
