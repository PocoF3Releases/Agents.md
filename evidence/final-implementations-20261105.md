# Final implementation history — November 5, 2026

Continued the maintainer-requested review beyond the original Dolby range. Seven
maintained device/vendor/control repositories were reviewed. Their selected
fork histories shrink from **390 to 364 commits**, dropping 26 superseded steps.
Every final public and active-overlay source tree remains exactly unchanged.
This pass introduces no runtime code, firmware or tuning change.

## Consolidation decisions

- Alioth: omit canceled CLICK/LOW_TICK trial imports and their removals. Preserve
  DOUBLE_CLICK, settled RAM samples, the later RAM 1 THUD update and active
  FCSAM32/tuning. Keep the real FCSAM64 removal: that copy came from upstream,
  so dropping its removal would resurrect an unused library.
- Common integration: eliminate exact tinyxml/Bluetooth/QCC add/remove pairs.
  Put the settled thermal-service package exclusion at its original fork change,
  retaining mi_thermald and all thermal protection. Fold guarded Wi-Fi country
  fallback into its own origin; keep independent audio/density fixes intact.
- Parts: fold resume-once, HBM rollback, refresh-write retry and rejected custom
  EQ rollback into their corresponding feature introductions. Keep namespace,
  native ownership and other independent MiSound stages separate.
- Dolby: keep settled process bootstrap, endpoint documentation and equalizer
  failure handling with their features. Consolidate the supported DAP controls
  and omit the temporary unused documentation artwork. All non-Dolby hardware
  snapshots, including the existing haptics implementation, remain unchanged.
- Camera: use the final settled permission/policy configuration at its first
  introduction and omit unused ARM32 OpenCL/f2player inputs from their original
  imports. Camera patches, approved modes, JNI and APK payloads are unchanged.

Upstream base commits are untouched. All 364 retained raw author headers and
original attribution/sign-off trailers are preserved. Fourteen translation
commits retain their original authors/messages and exact resource-only deltas;
they were not absorbed into runtime commits.

Three canceled fork-local imported workarounds disappear with their undo steps:
dkpost3's Bluetooth workaround and Michael Bestas's source tinyxml/vendor QCC
copies. Their original identities/authors remain in the provenance map. No
remaining contribution is reassigned to another author.

## Current canonical sources

| Repository path | Commits before → after | Current public source |
| --- | --- | --- |
| device/xiaomi/sm8250-common | 243 → 234 | [6fed13f4da77](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/6fed13f4da772d3f38253e8a33fd63cf255d8125) |
| vendor/xiaomi/sm8250-common | 28 → 26 | [a9a3cc77e033](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/a9a3cc77e0334842d1ffdbbc7771e4751e105144) |
| device/xiaomi/alioth | 7 → 5 | [f7a82eadfef6](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/f7a82eadfef6e78566ac550a167a26d11a4f1ff6) |
| vendor/xiaomi/alioth | 5 → 3 | [431c6019fe1f](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/431c6019fe1f9c5c9a8741cd980462b2da1f8576) |
| device/xiaomi/camera | 15 → 11 | [ac369e25f015](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/ac369e25f0159c3fcc65110dfb64bb680e05a837) |
| vendor/xiaomi/camera | 7 → 6 | [01543bb0d5b0](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/01543bb0d5b0e693022128ea5905ffb661e83fde) |
| hardware/xiaomi | 85 → 79 | [6762a5238e69](https://github.com/PocoF3Releases/hardware_xiaomi/commit/6762a5238e69c7b4b96f5c68f4b4b1ee9ff5e336) |

[Old-to-new provenance](implementation-history-map-20261105.csv) distinguishes
replayed, edited and dropped rows. Dropped rows resolve to the preceding retained
state. This does not relabel historical build/device results as new tests.
Private backup refs retain the original histories. Publication uses exact-head
force-with-lease, and all public refs are verified afterward.

## Correctness and preservation checks

Independent reviewers recomputed complete historical path/mode/blob maps and
checked author/message/trailer preservation. All seven final trees match their
pre-cleanup trees: 2,702 entries, including 1,301 proprietary entries and 777
ELF/APK/JAR-named payload entries. Explicit SHA-256 checks cover retained haptics,
FCSAM/tuning and all APKs. Hydrated MiuiCamera/ExtraPhoto payload hashes match
their preserved LFS pointer identities; unchanged pointers are not mistaken for
full APK hash verification.

The current Parts/Dolby review found no demonstrated additional runtime defect;
it checked DSP serialization/control recovery, enabled-state persistence, retry
and failure handling. Resource XML well-formedness passes for 663 files. This is
not complete Android resource linking or proof of every hardware endpoint.

All three extractors regenerate identical vendor output. The four authored
recovery patches reapply and postflight reports zero pending; active trees match
exactly. Mini GMS, prior prebuilt/Codec2 cleanup, kernel and paused investigations
remain unchanged. Previously recorded graph checks apply through exact source
identity; no new ROM build or device test was performed for this history-only
pass. Earlier reduced-image rebuild/runtime acceptance remains pending.

Private helpers, independent reviews, backup/source identities and publication
receipts are in `~/evo/.repo/implementation-cleanup-20261105/`.
