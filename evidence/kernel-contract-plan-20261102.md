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

Still unverified: exact runtime ALSA mixer enumeration (tinymix unavailable),
physical headset/USB/Bluetooth routes, acoustic quality, encrypted thermal-map
semantics, and exhaustive downstream success/error paths. Root-run PCM tests
establish transport behavior, not ordinary application permission coverage.
The paused boundary test remains untouched.
