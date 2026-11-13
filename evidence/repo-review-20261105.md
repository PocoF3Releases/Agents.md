# Maintained implementation review — November 5, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

This is scoped source/build/host/device evidence, not a whole-ROM certification.
The [coverage table](repo-review-coverage-20261105.csv) pins 43 local build paths;
the ROM-only interfaces variant, GitLab camera delivery and deployed manifests
were checked separately. The current kernel was preserved; the previously held
candidate and paused hardware investigations remain excluded.

## Corrected implementations

- [Qualcomm media range feature](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media/commit/6773462f3e744462299c6ad9d72564fcceb56a0c):
  encoder surface comparison now receives the same effective full-range flag as
  surface creation. Equal-size limited-to-full setup could miss reconfiguration;
  stable full-range setup could request unnecessary recreation. This branch is
  pre-stream/reconfiguration-only, not every steady-state frame. The correction
  is folded into the existing range/PI feature; the lifetime feature and original
  author are preserved. Strict extracted-source regression: old code fails two
  cases, correction passes five plus ten adversarial cases. No ABI, format,
  layout or codec-capability changes.
- [Thermal listener feature](https://github.com/PocoF3Releases/frameworks_base/commit/5c19617108cb079b4038b3c7c6c1fc21740bceeb):
  the existing no-HAL test now expects successful listener registration/removal,
  retaining zero callbacks and NaN headroom. The production implementation and
  thermal protection are unchanged.
- [Service fixture compatibility](https://github.com/PocoF3Releases/frameworks_base/commit/419f23067ab17cf1afa598546e4fcf6af8da4157):
  four inherited fixtures use current API signatures: display-touch capability
  stays false, and both pattern decoding and credential creation use the existing
  default 3x3 size. No test cases or assertions were removed, no skipped tests or
  warning suppressions were added. Separate topic from the thermal feature.

**Build-tested:** the user product's `libOmxVenc`, `libc2dcolorconvert`,
`libaudioclient`, `libaudioflinger` and `cameraserver` targets pass, including the
selected 32/64-bit variants. The full `FrameworksServicesTests` APK target passes.
Its first build exposed four stale API calls; after correcting the decoder,
three outer factory calls also required the grid argument. Both failed-build
receipts were retained; the same full target was rebuilt without narrowing it.
Existing deprecation/missing annotation-enum warnings remain unsuppressed.

**Device-tested:** only `ThermalManagerServiceTest#testNoHal` was executed from
that APK: one test passed on Android 17, SELinux Enforcing. APK SHA-256:
`7f904ac6180dd431e0367a55e09c97116bac4eeb4bebd4a3178cc79f3ab476a5`.
The package was absent before installation and uninstalled afterward; Android
remained booted and enforcing. This does not execute every service test or test
the physical thermal HAL. The corrected media encoder was not deployed to the
phone in this pass.

## Retained features and checks

- Framework AV: all four local features/21 changed files and complete DAP
  ownership/lifecycle paths reviewed; retain camera identity and reply validation.
  Approved inherited AC-4/codec support remains intact.
- Framework UI/services: recording FPS limits, independent blur controls, vendor
  reprocess metadata, torch retry, USB proxy recovery and signed task observation
  retain their contracts. A proposed torch race was rejected: real mode/strength
  writes share a serial background executor. Ninety-three locale files have the
  same string keys; 98 reviewed XML files parse. The inherited torch-test
  constructor mismatch is an uncorrected SystemUI test coverage limitation.
- Audio interfaces: ROM/recovery variants have identical stream guards. All 36
  host ABI cases and six protected-slot controls pass. Recovery adds eight
  availability declarations only; no unsupported stock callback slot is read.
- Tinycompress: 14 existing host cases pass, including partial/error reads,
  stop/pause handling and blocking/nonblocking tail behavior. NFC matches the
  selected upstream. Other QCOM audio/display/USB feature contracts are retained.
- Recovery: 25 infrastructure repositories plus all 13 core commits/38 changed
  files reviewed. Dependencies have consumers, including NTFS's actual module
  alias. Shell syntax, VINTF XML, bundled APK checksum/ZIP contents pass. Seven
  deployed recovery manifest/patch files match their published source; two extra
  local ROM override XMLs have separate ownership. All four canonical patches
  replay backward successfully in private candidate indexes. Active-tree
  postflight is a publication gate. No recovery image was installed or runtime
  decryption/MTP claim added.
- Device/vendor/Parts/Dolby payloads retain the
  [completed implementation identity review](final-implementations-20261105.md).
  The [haptics correction and installed HAL checks](haptics/2026-11-05.md) remain.
  Fork-added file checks found no temporary tests, saved patches or debug files
  in the resolved review ranges. Required notices/developer tooling are retained.

The framework anchor was corrected using the newer AIDL-repair receipt, not a
stale refresh-plan object. A separately fetched newer EvoX tip changes 58 files
with no overlap in these custom features; it was not imported as an unrelated
full-ROM resync during this cleanup.

## Remaining limits

The [haptic scale-zero minimum](haptics/2026-11-02.md#demonstrated-remaining-scale-zero-defect)
needs measured calibration/human acceptance; no Pixel gain was guessed. The
56 KB AAC library remains available for the approved optional renderer, not a
claim of production RichTap support. Rebuilt MINI/pruned-image acceptance,
complete physical endpoint coverage and the paused investigations are not closed
by source review. This broader goal remains active; no bug-free release claim.
