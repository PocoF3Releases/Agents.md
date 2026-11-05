# Original Dolby integration cleanup — November 5, 2026

The maintainer requested review of the original 23-commit Dolby integration,
not another late removal commit. The range mixed hardware video OMX, Dolby
software audio, effects, policy changes and unrelated display/thermal work.

## Final history

The device replay contains 158 commits instead of 165; the matching vendor replay
contains 28 instead of 29. Eight redundant commits are gone. Unrelated changes
retain their contents and original authors. All retained raw author headers were
checked; unchanged commit messages remain byte-identical.

- Restore hardware video OMX/VPP/DSMode without importing the 15 unregistered
  audio wrappers or their private DSD helper. The encoder follow-up becomes empty.
- Keep Dolby DAP/game/VQE, DMS, software AC-4/DDP, the 32-bit plugin and the v33
  foundation compatibility contract. Trim three never-owned 64-bit codec/plugin
  extraction fixups; retain the real 64-bit DMS library fixup.
- Remove transient media XML creation/deletion and device-local Dolby SELinux
  churn. Shared hardware/xiaomi policy ownership is established at integration.
- Keep the original two-input recording limits; remove the mistaken deletion and
  later restoration. Fold valid USB masks into the retained legacy USB change.
- Combine the Qualcomm effect configuration with its three matching libraries.
  ANUSH remains the primary author, with John credited for packaging. Original
  Woomymy/Flicker coauthor attribution and other human authors remain preserved.
- Keep XiaomiDolby and DSPVolumeSynchronizer: the shipped primary HAL implements
  the helper's volume_change protocol. Unrelated display/thermal commits remain.

The final vendor payload, generated declarations and file modes are identical.
The device's only new source delta is five removed lines: three unused fixup
entries and two unnecessary explicit Codec2 package roots. No mixer, route,
effect UUID, active HAL, thermal, security or kernel behavior was retuned.

## Current sources

- [device/xiaomi/sm8250-common — 6fed13f4da77](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/6fed13f4da772d3f38253e8a33fd63cf255d8125).
- [vendor/xiaomi/sm8250-common — a9a3cc77e033](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/a9a3cc77e0334842d1ffdbbc7771e4751e105144).

The [old-to-new map](dolby-history-map-20261105.csv) records provenance, not new
test identities. Dropped rows map to the preceding retained state. Private
backup refs preserve the original histories; published updates use exact-head
force-with-lease. The original published/tested IDs remain historical evidence.

## Verification

- Independently recomputed all 194 transformed snapshots and checked complete
  path/mode/blob trees. Eight dropped commits are empty after normalization.
  Separate helper checks cover media, service ownership and policy transformations.
- Extractor regeneration succeeds with no vendor diff; the complete
  lineage_alioth-cp2a-user Soong/Make graph passes (m -j8 nothing). The reworded
  final candidate has the same tested source tree; native recovery reapply and
  postflight pass with zero pending patches.
- Actual partition install targets lose 15 unreferenced vendor Codec2 support
  paths, add none, and retain the required 32-bit QTI Codec2 service/HIDL library.
  All 38 existing media.swcodec APEX paths remain. Inspection of 4,015 remaining
  runtime ELFs finds no lost compatible DT_NEEDED provider or parse error.
  Dynamic stores load named codec factories and libc2plugin_store; these are
  distinct from the retired vendor software-common roots.
- Fresh rooted-phone maps show the retained DAP/game DAP/VQE/MiSound stack, the
  vendor 32-bit Codec2 HIDL library and APEX software-common libraries. The OMX
  service maps AC-4/DDP and its Dolby plugin; no relevant linker failures were
  observed in the sampled logs. Both private ARM32/ARM64 OMX registry probes
  enumerate 16 video components and pass; their temporary files were removed.

No new current playback defect was demonstrated. This is integration/history and
packaging cleanup, not a claim of a new acoustic fix. The phone still runs the
previous installed build. No ROM rebuild, candidate flash or new audible/VoIP/
recording matrix was performed. Rebuild and validate the reduced image before
release; do not infer exact OTA savings from removed package roots.

Mini GMS, the withdrawn LZ4 snapshot feature, all 20 prior prebuilt removals,
recovery overlays and paused investigations remain preserved. Private receipts,
original patches and probe results are in `~/evo/.repo/dolby-history-audit-20261105/`.

The [later final-implementation pass](final-implementations-20261105.md) preserves
this final source content while consolidating other histories. The provenance
map resolves to those current canonical commits; original test IDs stay historical.
