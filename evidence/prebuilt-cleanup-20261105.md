# Prebuilt closure and ABI cleanup — November 5, 2026

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
| device/xiaomi/alioth | [7141e43eb9bf](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/7141e43eb9bf6364282474f4ee45344863cd2ea7) |
| device/xiaomi/camera | [ac369e25f015](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/ac369e25f0159c3fcc65110dfb64bb680e05a837) |
| device/xiaomi/sm8250-common | [6fed13f4da77](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/6fed13f4da772d3f38253e8a33fd63cf255d8125) |
| vendor/xiaomi/alioth | [431c6019fe1f](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/431c6019fe1f9c5c9a8741cd980462b2da1f8576) |
| vendor/xiaomi/camera | [01543bb0d5b0](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/01543bb0d5b0e693022128ea5905ffb661e83fde) |
| vendor/xiaomi/sm8250-common | [a9a3cc77e033](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/a9a3cc77e0334842d1ffdbbc7771e4751e105144) |

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
