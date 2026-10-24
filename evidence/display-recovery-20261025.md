# Alioth refresh-switch recovery — October 25, 2026

**Source/build/host/device tested.** The maintainer reported that fresh-boot
60 Hz felt normal, while returning from 120 Hz became severely delayed.
Continuous scrolling across mode changes reproduced a persistent queued-buffer
case that earlier tests with process restarts or settling pauses had missed.

## Failure and implementation

The original framework reproduced about **82 ms** intended-vsync-to-associated-
presentation latency after a 120→60 Hz switch, versus normal **32.33 ms** at
60 Hz. Frames could remain classified as Buffer Stuffing while being presented
on time. This metric is **not physical touch-to-photon latency**.

Android's existing single-step Choreographer recovery delays only the first
blocked frame within an animation. The inspected runtime compiled both
`bufferStuffingMultiRecovery()` and `bufferStuffingRecoveryThreshold()` as false.
The [Alioth fix](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/22436519a2ed598ffb7ce519ab72b4726e560c8f)
enables those existing paths together through a product-scoped release value set.
The upstream cumulative-delay threshold is 100 ms; its check can permit one
additional frame interval before further recovery delays stop.

The explicit Alioth map lives under `configs/release`, outside global map
auto-discovery, and adds its value set to cp2a. Normal aliases and descendants
of cp2a inherit it; independent releases and other products are unaffected.
The [published 120 Hz profile](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/c54c45f196ffa37f26a26273a674ed61499fd768)
and stock panel timing remain unchanged. No shared framework or kernel source
change, diagnostic APK, test fixture or temporary module is in the device commit.
A second-model source review found no blocking configuration or scoping issue.

## Build and runtime identity

`lineage_alioth-cp2a-user`, `m -j6 framework-minus-apex` passed. A host harness
extracting the checkout's actual recovery state machine passed 33 checks:
repeated blocking, 120/60 Hz intervals, half-frame signalling, cumulative-delay
bounds and idle reset. These are state-machine checks, not an Android runtime.
Generated view flags differed from the installed framework in exactly the two
intended values; the other 40 matched.

The temporary enforcing deployment used the built framework and its 17 changed
boot ART/OAT/VDEX files. All ten other system boot-classpath JARs matched the phone.
Only `classes5.dex` differed inside the framework JAR; its other entries matched.
Runtime readback confirmed both flags true, and Perfetto recorded the multi-step
recovery path executing in Settings. Installed kernel remained
[the recorded baseline](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/b8fc2fc50a5cca0e3fa9bfb9381c2f2efd2bf2da)
(build 2); no kernel, DTBO or ROM partition was flashed for this framework test.

| Artifact | SHA-256 |
| --- | --- |
| Original framework | `41bda894ea8c5940ae87b7ee6b8ebb3d06a5f515675fce0a8cc19a133bcc1525` |
| Tested framework | `bcbecf59681332f174c80c79277c65ed164bdbbbd691f223111c93edd1c95a7c` |

## Device results

- Eighteen continuous return-to-60 transitions completed across six traces,
  including six returns with the exact published seven-property timing profile.
  The sustained 82 ms plateau did not recur. Settled 60 Hz returned to about
  32.33 ms; the published 120 Hz profile retained about 20 ms. Occasional
  transition misses remain; this is not a zero-jank claim.
- A separate controlled missed-frame pair requested a 50 ms compositor pause.
  Recorded pause spans were 71.52 ms original and 69.56 ms candidate. In the
  0.1–3 s window after resumption, presentation-latency p95 was **48.85 ms original
  versus 32.47 ms candidate** (173/157 samples). Medians were both about 32.33 ms.
  This is one fault-injection pair, separate from normal transition acceptance.
- GLES completed at both rates with no GL error and correct readback. App frame
  cadence remained within the prior accepted observations: 718/1378 frames in
  the 60/120 Hz runs; 120 Hz p95 12.27 ms versus prior 12.67 ms. These app callback
  measurements do not certify every game's performance.
- Vulkan FIFO acquisition/submission/presentation and teardown passed on both
  app ABIs at both rates, with zero reported presentation errors. The clear-only
  queue-idle fixture is a functional API check, not a game benchmark.
- Deterministic 1080p AVC 24/30/60 fps and HEVC 60 fps clips at both display rates
  used Qualcomm OMX decoders: **2,088/2,088 frames rendered**, EOS reached and
  timestamp ordering checks passed.
- Ten additional mode selections and two sleep/wake cycles matched the requested
  configurations without a compositor restart. SELinux remained enforcing.

## Rejected experiments and restoration

A temporary 60 Hz MDP transfer-budget change from 14,000 to 7,000 µs doubled
requested MDP clock without reducing measured UI latency; the original DTBO was
restored and verified by full readback hash. Guarded auto-latch, idle-timer removal,
framebuffer-count reduction and a longer HAL FPS deferral also failed to justify
production changes. Their original values were restored. The earlier
[panel/scheduling findings and playback limits](display-timing-20261024.md) still apply.

After acceptance, the original framework hash and both false flag values were
verified restored. The disabled diagnostic module, both test APKs, temporary
helper/archive, instrumentation forwards and 42 copied traces were removed.
All temporary properties/preferences were restored; the original 60 Hz preference
was retained. No active probe or diagnostic overlay remains. The source fix is
for the next ROM build; no full ROM rebuild or release installation is claimed.

Raw traces, test fixtures and reports remain private under
`~/evo/.repo/display-latency-20261024`. Earlier diagnostics incorrectly searched
only slice names: single-step recovery uses the **Buffer stuffing recovery track**
with thread/offset slice names. Inspect track names before concluding recovery is
absent. Shipped flag classes are relocated under
`com.android.internal.hidden_from_bootclasspath.android.view.flags`.
