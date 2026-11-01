# Review of Claude’s latest changes — 2026-11-01

`source-checked`, `host-tested`, `module-build-tested`.

## Scope and retained behavior

Reviewed the source changes recorded after the previous SystemUI build fix:
Parts resume refresh, DSPVolumeSynchronizer/camera/QTI allowlists, Alioth
waveform extraction and packaging, and the AW8697 palette, composition strength
and synthesized envelope primitives. Kept Claude’s original commits/authorship
and approved tuning; added one independent correctness fix.

- Parts: LifecycleRegistry replays ON_RESUME when an observer is added to an
  already resumed owner. Removing the second explicit refresh is correct;
  rememberUpdatedState and observer disposal are retained.
- DSPVolumeSynchronizer requests only normal permissions. The removed cross-user
  entry is not privileged in this framework, so its privapp allowlist was inert.
- Camera: the actual packaged APK does not request WRITE_MEDIA_STORAGE. It does
  request the Mediatek APU name, but that permission is undefined here and its
  allowlist entry has no grant effect. Unshipped Mimoji/Scanner blocks stay removed.
- QTI: scanned 196 built app/priv-app APKs. The only surviving targets of the
  removed system allowlist are WfdService, qcrilmsgtunnel and ims, all on
  system_ext. Their requested privileged framework permissions from the old list
  are covered by the system_ext allowlists (0/1/3 applicable entries).
- Haptic assets: three extracted RAM slices match their packaged bytes; extraction,
  idempotency and rejected tampered-bank checks pass (seven checks). DOUBLE_CLICK
  matches the stock HyperOS payload exactly. No whole proprietary dump was copied.
- Preserved the CLICK/THUD selections, unchanged stock primitive slices, LOW_TICK
  fallback, composition gain, effect strengths, stream ownership/lifetimes and
  callback/cancellation implementation. No new control or unsupported HAL API.

MiSound’s latest entry records tests and a coexistence decision; no new MiSound
source diff appeared in this interval. This review does not replace Claude’s
recorded device checks with new runtime acceptance.

## Corrected finding

[Full-cycle envelope settling](https://github.com/PocoF3Releases/hardware_xiaomi/commit/e08273f42a55ac1af328f09b7a9dcfd33f6e080b)
changes only `vibrator/aw8697/PrimitiveSynth.cpp`. The old stop condition checked
instantaneous model velocity after one cycle. It could stop near a zero-crossing
while the next free oscillation still exceeded the stated 5% peak threshold.

Now check the maximum modeled velocity over a complete rounded-up period before
stopping. The 40 ms damping-tail deadline stays unchanged. Waveforms loaded from
stock files and the approved amplitude mappings are untouched.

The regression uses the production synth and resonator: four envelope shapes
at 401 f0 values from 100 through 300 Hz (0.5 Hz steps), then simulates two free
cycles. Before: 150/1,604 cases exceeded 5%, worst 6.927%. After: zero failures,
worst 0.205%. Empty/oversized output is rejected by the fixture, and 24 invalid-f0
fallback cases match 170 Hz. Clang -Wall/-Wextra/-Werror plus ASan/UBSan passed.
These are model results, not measured phone acceleration or new feel acceptance.

## Build and publication

`lineage_alioth-cp2a-user`,
`m -j4 android.hardware.vibrator-service.xiaomi_aw8697` passed with the module’s
existing -Wall/-Wextra/-Werror flags. Artifact SHA-256:
`1e4fc25a2fd8d552c6491e19d76484426bfb88083156e512e2870bf88a0939a0`.

The independent fix is published on hardware_xiaomi `cnb`; all earlier Claude
commits remain ancestors. No translation changes, kernel changes, warning
suppressions, full ROM build, installclean, flash, mount or phone operation.
No production test/temporary files were added. Private regression fixtures/logs
remain under `~/evo/.repo/claude-review-20261101/`. A pre-existing untracked
Alioth `__pycache__/` was left untouched.
