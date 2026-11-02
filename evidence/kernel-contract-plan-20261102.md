# Kernel and userspace compatibility plan

Updated: 2026-11-02. Status: incomplete; no blanket production-compatibility claim.

## Scope and evidence

Audit the entire maintained kernel series against device trees, hardware/xiaomi,
HALs and packaged consumers. The current [kernel head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/1cfe734008290c228abf15a8f8ae67a03d52fc1e)
contains 759 downstream commits: 158 foundation commits and 601 later changes.
The earlier [integration check](kernel-correctness-followup-20261102.md) covers
repository/recovery alignment and the last five fixes, not all downstream behavior.

Source reviews covered public ABI, audio, touch, thermal and power-control
contracts. These reviews found no demonstrated new audio ABI mismatch; they do
not establish every proprietary path or runtime combination. Private inventory
and review artifacts are in `~/evo/.repo/kernel-contract-audit-20261102`.
The captured running configuration matches the reviewed production configuration;
that does not prove all consumers behave correctly.

## Paused task and tooling limitation

Two Codex feedback submissions were accepted for the repeated Daybreak notice.
The screenshot supplies no exact reason code or rejected-operation identity.
A bounded local log inspection found Daybreak feature metadata and separate
stream-disconnection warnings, but no causal rejection record. Do not label the
cause confirmed or attempt to bypass the restriction.

Pause the touch-ioctl boundary reproduction as a precaution. Static review found
a mismatch between ordinary HAL request-buffer size and the kernel copy size.
A private host model reproduces failures; the native phone probe was never run
because staging failed. No source fix, device verification or publication is
claimed. The paused task is not proven to have caused the restriction.

## Remaining work, in order

1. Complete the commit-to-consumer inventory, including configuration gates,
   native/compat ABI, sysfs values, init ownership and access labels. Mark opaque
   proprietary behavior and unchanged baseline findings explicitly.
2. Continue ordinary read-only checks: actual haptic nodes, display controls,
   thermal protection, charging controls, power-hint paths and packaged services.
   Compare providers with callers; do not infer a missing feature from a guessed
   path or grant permissions without a demonstrated caller requirement.
3. Finish audio mixer/control inventory and normal playback/recording checks.
   Preserve Dolby, MiSound, saved settings and thermal/security behavior. Keep
   unavailable headset and proprietary calibration cases as limitations.
4. For any independently demonstrated, unrestricted mismatch, find the matching
   upstream/vendor fix first. Preserve authorship and apply the smallest
   feature-separated correction with an old/new regression where appropriate.
5. Run affected static checks and strict W=1/Werror builds, then relevant phone
   checks. Record source, host, build and device evidence separately. Publish
   only verified fixes; do not imply all 759 commits passed from sampled tests.
6. Update this plan with resolved findings, unchanged baselines and remaining
   limitations. Keep translation changes separate and recovery patch alignment
   intact. No unrelated sync, history rewrite, flashing or cleanup is implied.

No kernel, HAL or device-tree source was changed by this planning update.

## Continuation acceptance — 2026-11-02

**Device-tested:** the installed kernel reports
`4.19.325-Redline-3d374cb-dirty-cip136`, Enforcing, taint 0. This is the
previously verified precommit artifact, not proof of a freshly flashed HEAD.

- Audio HAL/effects 6.0 and health/vibrator services are registered. The reviewed
  PCM fixture passed all 19 cases: four capture sources at 16/48 kHz, two cycles
  each, plus three generated-playback cycles. Capture data was discarded in
  memory. Audioserver and mi_thermald PIDs remained unchanged; taint stayed zero.
- All sysfs paths selected from the 29-node power-hint configuration exist.
  Existence is not proof of every write or performance outcome.
- The actual AW8697 node advertises custom-wave ABI 2, ID 193, period 512,
  maximum 8192 and RAM gain ABI 1, matching the configured consumer. Custom-wave
  and charging-speed DAC/labels match their configured ownership.
- mi_thermald is running, its map-ready property is 1, and its board temperature
  estimate is readable. Android Thermal HAL readiness remains false, matching
  the deliberate [thermal HAL decision](thermal-hal-decision-20261031.md).
  Preserve that decision; no invented thresholds or thermal-engine activation.

No new actionable defect was demonstrated in this continuation, so no kernel,
HAL or device-tree patch was manufactured. No flash, policy relaxation or
persistent setting change was needed; the temporary PCM fixture was removed.
Private receipts: `~/evo/.repo/kernel-contract-audit-20261102/final-runtime`.

Remaining at that checkpoint: exact runtime ALSA mixer enumeration, external
audio routes, acoustic quality, encrypted thermal-map semantics and exhaustive
downstream paths. The mixer inventory is closed by the later check below. Root-run PCM tests
establish transport behavior, not ordinary application permission coverage.
The paused boundary test remains untouched.

## Repository pairing and mixer inventory — 2026-11-02

**Source-checked:** current maintained remote heads match local kernel,
hardware/xiaomi, hardware/interfaces, Qualcomm audio/display and both Xiaomi
vendor trees. Local Alioth/common device trees and frameworks/base differ by
published recovery overlays: applying the four manifest-listed patches to the
current public bases reproduces all three local Git trees exactly. The normal
patch runner reports zero pending patches. This proves source composition;
it does not certify all kernel downstream behavior or current upstream freshness.

**Consumer-checked:** common BoardConfig selects `kernel/xiaomi/sm8250`, the
Alioth defconfig and Clang r563880c. Fstab F2FS/inline-encryption requirements
match the mounted userdata filesystem. ZRAM exposes LZ4 and Zstd and actively
uses the configured LZ4 compressor; page-cluster is 0. The installed primary
audio HAL hash matches the reviewed blob. A literal-path scan found no missing
Alioth/Parts-specific sysfs consumer path. Generic init/other-device references
still need capability-aware classification; presence alone proves no write.

**Build/device-tested:** the standard `tinymix` target built with the selected
user product, at `-j4`, retaining its Werror checks. Read-only enumeration found
5,426 controls on `kona-mtp-snd-card`. All four installed mixer XML files equal
current Alioth sources. The static overlay's 120 unique controls, dynamic
overlay's four and sound-trigger XML's 67 all exist; their enum selections match
live provider metadata. The temporary utility was removed after listing.

The generic base XML contains 82 absent control names and four unavailable enum
selections; after overlay replacement, 30 generic paths retain absent direct
controls. These include other amplifier hardware and optional routes. For
example, the low-latency-resume QOS control exists only in the unrelated
SDM660 machine driver, including at the foundation revision. Do not describe
these as newly introduced kernel regressions or silently discard routes without
proving activation. Reads of some DSP-backed values failed; successful metadata
enumeration does not establish DSP-state or acoustic acceptance.

No source edit is required merely to accompany internal kernel correctness
fixes when the consumed ABI remains compatible. No new source correction was
proven by this pairing check; production worktrees remain clean. Full-series
compatibility is still incomplete, including optional generic-route reachability,
external endpoints and opaque thermal behavior. Device `checkvintf` is not
installed, so no new device VINTF pass is claimed. The paused test stays paused.
Private receipts: `~/evo/.repo/kernel-contract-audit-20261102/repo-alignment`.

## Generic-route and declared-interface closure — 2026-11-02

**Source/binary checked:** all 30 effective paths with absent direct controls
were classified. Dependencies expand this to 34 paths. The complete 769-path
post-overlay graph has no cycles or missing nested references; maximum depth is
four. The checked speaker, handset, protected-speaker, media and built-in capture
paths contain no missing provider controls.

| Generic path group | Count | Activation / remaining limit |
| --- | ---: | --- |
| Different amplifier/channel topology | 13 | Other speaker-bank controls; Alioth binds two CS35L41 devices, at I2C 1-0040/1-0041, with its own overlay. |
| VBAT | 6 | Feature availability does not enable the paths: `persist.vendor.audio.vbat.enabled` is unset. |
| MMAP capture | 2 | Product `aaudio.mmap_policy=1` means NEVER in the framework API. |
| Dynamic QoS resume | 1 | Explicit opt-in is unset; the absent control belongs to SDM660, not Kona. |
| FM capture | 1 | Kernel RADIO_IRIS is disabled; no FM endpoint exercised. |
| Qualcomm protected second speaker | 1 | Separate `persist.vendor.audio.speaker.prot.enable` opt-in is unset. Preserve Cirrus processing. |
| DisplayPort voice routes | 4 | External endpoint not exercised. |
| GSM / handset sidetone | 2 | Cellular-call behavior unverified; no calls placed. |

Exact binary references confirm the VBAT property at primary HAL
`audio_extn_can_use_vbat` VA 0x84e74 and the Qualcomm protection property at
`libspkrprot.so` Thumb VA 0x603a. Its initialization clears the enable flag and
requires explicit `true`; the feature flag alone is insufficient. Do not enable
these optional paths to satisfy unused XML. Sidetone's direct caller/fallback
was inspected, but PCM VoIP acceptance does not establish cellular sidetone.
The six external/cellular paths retain runtime limitations rather than a
claim that their configuration is proven correct.

**Device-tested:** a bounded, silent, 48-kHz duplex fixture completed three
speaker/earpiece pairs (six switches), maintaining capture after each change.
Mixer snapshots confirm the actual product overlay: receiver-only versus dual
DSP routing, S24_LE / 96-kHz backend, receiver gain and ultrasound selection.
Normal mode was restored, audioserver/mi_thermald PIDs stayed unchanged, SELinux
remained Enforcing and taint stayed 0. Samples were discarded; staged DEX and
mixer utility were removed. These checks do not measure acoustic quality.

**Build-tested:** `m -j4 check-vintf-all` passed, reporting COMPATIBLE. The check
used kernel version/config and all mapped system/vendor/odm/product/system_ext
and APEX declarations, with first API level 30. Generated kernel metadata is
`4.19.325-Redline-1cfe734-cip136`; its configuration SHA-256 equals the captured
running configuration (6a3c2dff85db6e80d35aed7efa82c9b5950687f975c975d5fcee6b49a8a39c48).
The phone still runs the earlier precommit artifact described above. This is
build-tree VINTF acceptance, not a new device checkvintf invocation or every HAL
behavioral test. The target rebuilt its kernel prerequisite without source edits.

No new actionable source mismatch was established. Kernel, device-tree and HAL
worktrees remain clean; there is no new implementation patch in this closure.
Public ABI, controls, audio, power/thermal and recovery-composition reviews retain
their earlier limits; exhaustive internal behavior is not certified. The blocked
boundary task remains skipped. Private receipts are under
`~/evo/.repo/kernel-contract-audit-20261102/generic-route-audit`.
