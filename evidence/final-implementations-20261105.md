# Final implementation history — November 5, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

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
| device/xiaomi/sm8250-common | 243 → 234 | [2838130a6fa0](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/2838130a6fa07154b16468ecc4bc06e7c77dd745) |
| vendor/xiaomi/sm8250-common | 28 → 26 | [7fab8d519fd6](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/7fab8d519fd62c244c54057c76a32380d5ef5398) |
| device/xiaomi/alioth | 7 → 5 | [694d770254f8](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/694d770254f8233d7c75752a228852dc702acfa9) |
| vendor/xiaomi/alioth | 5 → 3 | [ac728e26803b](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/ac728e26803b75edbaacd5fcf4f8e6922102ca7d) |
| device/xiaomi/camera | 15 → 11 | [065f4af3e771](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/065f4af3e7716981e6fc0bf5e13e73f7983cfba0) |
| vendor/xiaomi/camera | 7 → 6 | [61876c6e6953](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/61876c6e6953476e20bd8b6b27a07d9da9a7c4a3) |
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
