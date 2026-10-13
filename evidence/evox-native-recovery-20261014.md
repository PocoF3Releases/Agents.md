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

A new lock credential was added after this baseline. PIN/password candidate work
is explicitly pending in [the topic owner](../memory/evox-recovery.md).
This record does not certify protected-credential or Weaver decryption, exhaustive
camera modes, Android Auto projection, CTS/VTS or every recovery feature.
