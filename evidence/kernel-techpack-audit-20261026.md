# Full configured-techpack recheck and scoped driver repairs

Date: 2026-10-26. Base: `90971a36383ff107cff55c7b37001eb6283d036b`.
Source-checked, host-tested and build-tested. No system-side sources, defconfigs,
warning flags, firmware, thermal limits or panel timings changed. Existing upstream
commits/authorship are preserved; these new scoped changes have their own feature
commits. No phone flashing/runtime acceptance occurred in this batch.

## Scope and full-pass result

`make -k -j4 W=1 C=2 techpack/` traversed the configured audio, data, display,
video, stub and selected camera-xiaomi trees with checkout Clang 21. Alioth selects
CONFIG_TECHPACK_CAMERA_XIAOMI; camera, camera-bengal, camera-xiaomi-cas and
camera-xiaomi-tablet are not its active camera backend. These other source trees
were not relabeled as tested or imported into Alioth's build. Compiled supplier
branches and DisplayPort code do not establish physical hardware use.

Both full diagnostic passes **fail**. The baseline parser records 2,062 unique
techpack path/line/severity/message records, including 585 errors. The completed
final pass records 1959 records, including 542 errors. These are diagnostics,
not proven runtime bugs or a precise fix counter: line movement, compilation
progress, cached objects and parallel output affect the inventory. Remaining
parsed records by selected area:

| Area | Records |
| --- | ---: |
| audio | 697 |
| camera-xiaomi | 394 |
| data | 260 |
| display | 336 |
| video | 272 |

The final command additionally checks the RMNET hook producers under drivers/net.
Other SHS hook annotations and unused descriptor fields there remain unresolved.
The full techpack result must not be presented as a whole-tree warning-clean or
release-wide functional certificate.

## Separate repairs

- [ASoC: cs35l41: Preserve DSP raw register endian types](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/cace5faa4a777aeb61cf6607b89c735000b4e7a4).
- [ASoC: cs35l41: Bound calibration control buffers and errors](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/af86ab9f96535ef86776dcb29b3af7a40aeea31c).
- [media: camera: Correct CDM helper ownership](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/9ca8795803a720f098a41f75454ee96ed009c87e).
- [media: camera: Keep RAM and MMIO copy addresses distinct](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e609be40bfa354a2e13ec5600ff31ea58cf5ba84).
- [media: vidc: Keep V4L2 callbacks private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e8d7f14e6104c183628f6cde960d28e2248ce303).
- [media: vidc: Return native poll masks through the stack](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e59c9e97e6f0b95b43e15e3d4c4ac7408fdb5367).
- [drm: dsi: Keep panel command builders private](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/5b63c6196adee14a28b0a2981c8bbad8a2743e6e).
- [drm: sde: Correct command encoder helper ownership](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/0add194f924417363213166fcc36a350da80cfb0).
- [net: rmnet: Share RCU-aware performance hook declarations](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a7a655ccadb22fe516b7f0c84063b8f93a29ee95).

CS35L41 is an observed bound amplifier on this phone. Raw DSP scratch/ack words
retain big-endian types without changing encoded values. Scalar control buffers
are initialized and bounded to the ALSA byte buffer; failed reads/writes propagate
rather than reporting success or decoding uninitialized output. Failed cached
reads no longer copy stale data into the caller's buffer. This does not establish
physical speaker calibration or every firmware control width.

CDM includes its existing shared declarations and keeps table-only builders
private. The copy helper now distinguishes a const RAM command buffer from its
MMIO destination, retaining ordered word writes and existing barriers. Its loop
counter uses an unsigned kernel type instead of mixing signed and unsigned bounds.
No command layout or camera mode was changed.

VIDC keeps active V4L2 callbacks private and removes only an unreferenced empty
encoder table: both sessions still register the populated table. Poll types now
carry native masks end-to-end, and a missing instance returns EPOLLERR rather than
negative errno bits. Valid readiness bits and all three wait queues remain.

DSI/SDE helper visibility and dead locals are corrected without changing DSC,
ROI payloads, backlight decisions, IRQ/fence/wait policy or refresh timings. The
scheduler-status MMIO callback is still invoked even though its return is unused.

RMNET performance hooks have one declaration owner in the existing handler
header. __rcu applies to the pointed-to function type, as required by this tree's
RCU sparse check; producers and techpack consumers agree. Presence-only checks use
rcu_access_pointer. Exported names, callbacks and publication/removal sequence
remain; this batch does not claim a concurrency/lifetime proof for all RMNET paths.

## Validation

The final full-pass log has no diagnostics in the changed cam_cdm_soc,
cam_cdm_util, cam_io_util, msm_v4l2_vidc, dsi_panel or sde_encoder_phys_cmd units.
Their original prototype/unused-local/address-space failures are removed. The
selected Cirrus endian and RMNET performance-hook errors are gone; other
pre-existing diagnostics in those files/subtrees remain in the private inventory.

Private exact-function fixtures use strict Clang with Wall/Wextra/Werror and
ASan/UBSan:

- Cirrus: baseline fails error propagation and oversized-buffer assertions/sanitizers; final passes these plus 24 valid width/value/volatile combinations, deterministic zero tails and missing-control behavior.
- Camera register copies: final passes 132 length/barrier combinations and null-input cases, verifying word values/order, unchanged trailing sentinels and existing barrier counts. Baseline also exposes the signed-comparison compile diagnostic under these host flags; no test flag was removed.
- VIDC: all 32 valid queue/event readiness combinations retain the expected masks and three wait registrations. Baseline fails missing-instance EPOLLERR; final passes it. Queue and hardware boundaries are mocked.

Strict checkpatch reports zero errors/warnings and 21 style checks, largely the
existing camera uint32_t/CamelCase conventions plus blank-line checks exposed by
touched signatures. No checker options were used to suppress them. Git whitespace
checks pass. Temporary regression fixtures remain outside production sources.

The normal configured kernel Image passes under its original fatal-warning policy
with no compiler warning/error diagnostics. Raw Image SHA-256:
`40e6db0d03cbc15072e25f370d2ceac513c1964885d8cf550caef344193ff0c5`.

Raw full logs, exact commands, inventories and fixtures remain private under
`~/evo/.repo/kernel-techpack-audit-20261026/`. The source map records the published
head separately from historical phone acceptance; this Image was not installed.
