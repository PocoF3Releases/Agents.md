# Native recovery and full ROM verification — 2026-10-14

**Source/build/host/device-tested, scoped.** Product `lineage_alioth-cp2a-user`,
Android 17 / SDK 37, active checkout `~/evo`. Raw logs and screenshots remain
private; this record contains the decisive sanitized results.

## Source and manifest identity

Full sync resolved 1,265 projects, with 15 upstream advances. All 30 maintained
native-recovery integration heads were retained, clean and matched GitHub in the
completed baseline audit. [Exact linked heads](../state/repositories.yaml).

[Manifest repair](https://github.com/PocoF3Releases/local_manifests/commit/50ef2cbe4ca339d8591d3c00adfeb7a72e87f373)
preserves upstream project groups and build/make linkfiles. Eight clean standalone
checkouts were preserved privately before Repo recreated managed checkouts; their
approved heads were retained. Frameworks/base and frameworks/av remain on the
explicit maintained `cnb` overrides.

## Built and installed artifact

Full production build passed. Generated file:
`EvolutionX-17.0-20261013-alioth-12.3-Unofficial.zip` (filename uses build date).
SHA256: `a98d708fb8dc060457035a3596c46e493734c310e58ded87baae406752a47e52`.
Secure vendor_boot SHA256:
`194ce299e4c7e55a77078cf6aa5cd933ea6b0ee31a09460aeae44d497b4a8b82`.

Secure recovery full-ROM sideload completed with exit 0. Android subsequently
reported incremental `1791926851`, SDK 37, boot complete, slot A and SELinux
Enforcing. This confirms installation rather than merely transfer completion.
No wipe/format was performed. Secure ADB remained enabled and debuggable was 0.

## Bounded runtime acceptance

- No-credential decryption, read-only `/data`, matching plaintext fixture hash,
  crypto-service shutdown and vendor dependency unmounts passed before and after OTA.
- Signed harmless ZIP installation from decrypted storage verified its whole-file
  signature and returned recovery install status 0 after the updated ROM.
- Diagnostic init/adbd were permissive; recovery/crypto domains were enforced.
  Secure production recovery was restored on active slot A after testing.
- MiSound and Dolby opened; saved MiSound switches matched pre-update state.
  Thermal controls opened and camera activity launched. Captures retained approved UI.
- Final crash buffer was empty; the plaintext fixture hash was unchanged.
  Owned phone fixtures and temporary transfer copies were removed.
- Recovery root: 142 ELF files, zero unresolved dynamic-library dependencies.

## USB and remaining limits

An unauthorized recovery shell does not establish failed decryption. Windows ADB
server reconnect was tried; diagnostic recovery provided logs. A large fastboot
transfer lost USB before a write was reported. A hash-verified local Windows copy
with `fastboot -S 32M` restored secure recovery successfully. These are observed
host procedures, not a universal USB/kernel fix. Enter actual bootloader mode
from working Android; check product/slot/download capability before flashing.

## Final PIN and rendering update

Final incremental production build passed without installclean:
`EvolutionX-17.0-20261014-alioth-12.3-Unofficial.zip`.
SHA256: `7f36958c4f7d77a41fa2f704e27c34349ea3ed06cb49e343cf9d6eb27429d55c`.
Secure vendor_boot SHA256:
`c1c5869eb22a1fc090b46ef70d6cf7994158ff87ddef933cf403922882accc58`.
Corrected secure recovery restored to slot A; secure properties and absence of
diagnostic init/ADB permissiveness were checked in its packaged ramdisk. The
upstream permissive `su` declaration is unchanged and is not an authenticated
production recovery shell.

Initial PIN checks enforced recovery/crypto domains with diagnostic init/adbd. Wrong PIN
was rejected; correct PIN restored the original plaintext hash with read-only
data. RAM credentials were removed and services stopped. The final UI reports
“Internal storage unlocked.” without logging normal credential entry as a process
error. A trusted no-op ZIP installed from unlocked storage with status 0.

Physical vblank changed from 60 Hz to 120 Hz after the preferred/requested KMS
handoff. Device-local scroll gestures measured approximately 55–60 FPS software
rendering; the user confirmed it looked much better. Offline bounds, layout and
presentation-failure checks passed. No experimental kernel tuning remains.

The initial secure check exposed missing ramdisk service transitions, manifest
directory reads and vendor crypto linker access. The corrected path passed with
init, recovery and crypto domains enforcing; only diagnostic ADB/su access was
permissive. Service cleanup and vendor dependency unmounts passed. The user
confirmed PIN unlock and normal folders in the final secure image. ASCII password layout is
checked offline; type-4 password, Weaver, pattern, Unicode and multiple-user
runtime acceptance are not claimed. This update does not certify exhaustive
camera modes, Android Auto projection, CTS/VTS or every recovery feature.

### Final source heads

- [bootable/recovery](https://github.com/PocoF3Releases/android_bootable_recovery/commit/6eddf2d113ca1902c508860e8aa167da39cecf08)
- [system/vold](https://github.com/PocoF3Releases/android_system_vold/commit/51ede7310adb133c13025533c1f20cff56cb3bcc)
- [system/sepolicy](https://github.com/PocoF3Releases/android_system_sepolicy/commit/054bec92b1d8ea9ea176220109926b1138421b64)
- [device/xiaomi/sm8250-common](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/7b3d66b9a426e35c4a1d039ba84f64d245c6e895)
