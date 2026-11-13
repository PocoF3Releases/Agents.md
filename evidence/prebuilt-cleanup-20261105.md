# Prebuilt closure and ABI cleanup — November 5, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

Scope: Alioth's installed proprietary payload and three matching Xiaomi
extraction/vendor pairs. Inventory covered 1,321 Xiaomi source blobs, 3,122
installed ELFs and 467 APKs. A missing direct reference was only a candidate,
not sufficient deletion evidence.

## Final source changes

Removed 20 files, totaling **4,257,888 bytes (4.06 MiB) before OTA compression**:

- Alioth: unused ARM64 FCSAM copy. The running stock audio service is ARM32 and
  still loads the retained ARM32 FCSAM, Dolby and MiSound libraries.
- Common: 15 unregistered legacy OMX audio wrappers and their private DSD helper.
  The fixed Qualcomm registry exposes video components only. Codec2 uses separate
  factories; AC-4 and other working software codecs remain.
- Common: unused ARM32 GPU counter helper; the installed producer and retained
  helper are ARM64. Both Vulkan profiling-layer ABIs remain.
- Camera: unused ARM32 private OpenCL bridge and standalone f2player offline
  replay tool. Retained OpenCL clients are ARM64. Camera APKs, modes, sensor
  schemas, supplier firmware, tuning and calibration are unchanged.

Generated vendor declarations were regenerated from extraction lists. Baseline
regeneration reproduced all three repositories without changes before pruning.
Signed APKs were not repacked. ARM32 audio, graphics and IMS dependencies remain;
Hexagon DSP binaries are not ARM32 pruning candidates.

| Component | Current public commit |
| --- | --- |
| device/xiaomi/alioth | `7141e43eb9bf6364282474f4ee45344863cd2ea7` |
| device/xiaomi/camera | [065f4af3e771](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/065f4af3e7716981e6fc0bf5e13e73f7983cfba0) |
| device/xiaomi/sm8250-common | [2838130a6fa0](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/2838130a6fa07154b16468ecc4bc06e7c77dd745) |
| vendor/xiaomi/alioth | [ac728e26803b](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/ac728e26803b75edbaacd5fcf4f8e6922102ca7d) |
| vendor/xiaomi/camera | [61876c6e6953](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/61876c6e6953476e20bd8b6b27a07d9da9a7c4a3) |
| vendor/xiaomi/sm8250-common | [7fab8d519fd6](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/7fab8d519fd62c244c54057c76a32380d5ef5398) |

The two device checkouts retain their unchanged authored recovery overlays.
Recovery patches and manifests require no content changes; new active identities
are recorded in the source ledger. Public ROM branches exclude recovery patches.

## Missing-library investigation

All 26,216 DT_NEEDED edges from 3,102 retained installed ELFs were checked for
lost providers, matching ELF class and machine: zero provider regressions.
Baseline flat-map gaps resolve through installed APEX providers, except remote
Hexagon DSP libc/libgcc contracts. Those are not missing ARM bionic libraries;
remote DSP runtime coverage is not established by this audit.

The platform review also resolved 118 init service paths and found interface
libraries for 77 HIDL package/version declarations. Presence alone does not
prove registration, namespace visibility or complete symbol compatibility.

No required stock import was demonstrated. Optional audio HAL plugin names are
also absent from the stock dump. VPP's software-decoder branch selects from the
same fixed registry; no current row requests the stock software wrapper. It does
not retry software loading when hardware loading fails.

Two debug-level private Google app-loader failures were observed. Turbo embeds
ordinary TFLite JNI and catches unavailable backend loads; packaged Velvet embeds
ordinary Geller JNI. The updated Google app's fallback was not inspected. Copying
private app JNI libraries into vendor would not establish classloader visibility
or compatibility. No associated crash or failed feature was established.

## Verification boundaries

- Three independent preservation/dependency reviews: no required findings.
  Retained proprietary blobs and all 14 vendor APKs are unchanged.
- Extractor regeneration, declared proprietary source existence and six Git
  whitespace checks pass. The complete Soong/Make graph passes
  `. build/envsetup.sh && lunch lineage_alioth-cp2a-user && m -j8 nothing`.
- On the connected Android 17/API 37 rooted phone, private ARM32 and ARM64 OMX
  probes each enumerate 16 video components and finish successfully. Installed
  core hashes match the host copies. No removed candidate was mapped during the
  sampled process scan. This is a snapshot, not proof of every optional path.
- Seven retained library hashes match the phone, including both primary HALs,
  both OMX cores, FCSAM32, GPU helper64 and OpenCL bridge64. Temporary diagnostic
  executables were removed; no system library, device setting or partition was
  changed.
- The phone still runs the pre-cleanup build. No full ROM rebuild, pruned-image
  flash, camera/audio functional matrix or new OTA size measurement was performed.
  The raw-byte saving is not the final ZIP saving. Rebuild and runtime acceptance
  remain necessary before release.

Private inventories, source hashes, dynamic-loader analysis, build receipts and
probe sources/results remain in `~/evo/.repo/prebuilt-prune-20261105/`.
Kernel work and all previously paused investigations remain untouched.
