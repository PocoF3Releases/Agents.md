# Dolby rapid VoIP re-entry — 2026-11-12

**Status:** source-checked, host-tested, build-tested and temporarily device-tested. Original artifacts/preferences and temporary test state are restored; both implementation fixes are published with a freshly verified remote tip. This follows the [earlier audio audit](alioth-audio-features-20261112.md), which recorded two enable-confirmation rejections without aligned native traces.

## Reproduced cause

The frozen earlier XiaomiDolby APK, SHA-256 `151d0964f54c81fb229a4b2017edc555dd35e37e9a77ca75f0a54d1108cc5a4d`, reproduced fourteen processing-confirmation errors with the original saved workload: first GEQ band −42 and nineteen zeros, Bass On, Virtual Bass Off, dialogue enabled and amount 4. Its normal-UID fixture completed 28 VoIP duplex cycles, four microphone cycles and media playback. Fixture completion did not mean error-free Dolby recovery. The first baseline saved only the preset; its zero-error result did not cover this five-key workload.

DMS accepts SET by posting asynchronous handler work; GET reads native state directly without a queue barrier. Continuous logs and 1,619 complete native probe records mapped all fourteen rejections to enable still queued behind profile/reset/override work. Enqueue-entry to native On-entry measured 39.791–55.192 ms, beyond the old immediate/5/15/35-ms read schedule. Framework enable was true while native GET correctly returned false; compensating Off began before queued On applied.

Recorded fixture mode was normal at enqueue, rejection and native application. No false GET followed native On before later explicit Off. This establishes a queue-completion mismatch in the reproduction. Maximum single-handler occupancy was 25.013 ms; lock, scheduling, I/O and DSP time were not isolated. The original two historical warnings lack equivalent aligned captures: this proves the reachable defect and matching signature, rather than direct identity with those events.

## Independent quiet-window guard

A callback during profile restoration or enable could renew the existing 500-ms media quiet window while mode remained normal. Mode-only checks could enable before that renewed deadline; two old-source host counterexamples reproduce the gap.

The guard rechecks communication state and quiet eligibility after profile restoration and enable. It applies during media resume, retaining existing ongoing-media behavior and the 500-ms window. The quiet-only APK built in 300.42 seconds and completed the phone matrix, but still logged fourteen confirmation rejections. It fixes this independent eligibility race without resolving queue latency.

## Enable acknowledgement correction

The combined correction sends native On and framework On once, then polls read-only at 10-ms intervals within a finite 200-ms enable-confirmation budget on the serialized controller I/O worker. This is application policy informed by measured latency, not a vendor completion guarantee.

Every attempt checks fresh communication state and the resume quiet deadline; successful readback gets a final policy check. A new call or renewed quiet window closes both gates and preserves the recovery phase. Phase/cache cleanup survives shutdown failure; uncertain bypass is reasserted before another mode/quiet query. Predicate errors propagate without generating restore events or renewing the controller's bounded retry budget.

Transport, malformed-read, dead-effect, control-loss, timeout and cleanup errors remain visible. Enable SET is never replayed for acknowledgement. Off confirmation keeps its 35-ms policy. Saved requests, profiles, Bass/Virtual Bass, dialogue range, GEQ wire values, translations and native prebuilts retain their existing contracts.

## Host and build verification

The final source passed 229 host groups: 29 extracted production Engine, twenty whole production effect, eight whole-controller groups using real coroutines, and 172 retained settings-method regressions. Scripted Android/native/clock boundaries cover delayed/absent ACK, concurrent Off, renewed quiet, calls and error cleanup. Two old actual-effect counterexamples reject 55/150-ms ACKs; the correction confirms them. These checks do not execute proprietary processing.

`XiaomiDolby`, `lineage_alioth-cp2a-user`, built successfully in 361.9 seconds with both source hashes unchanged.

| Item | Identity |
| --- | --- |
| Hardware base | [cb7ab6c](https://github.com/PocoF3Releases/hardware_xiaomi/commit/cb7ab6c33b4bf96fbc0493602d08ac9e102ca621) |
| Final Engine SHA-256 | `8de8bdce7ea4871213e506394342ca04aa61fc4ca2fbfb2a7a27f62833b20006` |
| Final effect SHA-256 | `f554c1d229ba8370e79320c3ce4904ba93f62131e68cdba04579082959f57ed0` |
| Tested XiaomiDolby APK SHA-256 | `87b3f17063260709195adb20ab3b760279a1edae8fbac6aeac08fac7181027da` |
| Published quiet-guard commit | [9002673](https://github.com/PocoF3Releases/hardware_xiaomi/commit/90026732dfb14fa64ac1d4595d1df4456e612e9d) |
| Published enable-ACK commit | [fd1e7be](https://github.com/PocoF3Releases/hardware_xiaomi/commit/fd1e7be434943c1e13ba24578e6913e4c990c286) |
| Freshly verified remote tip | [`cnb` → fd1e7be](https://github.com/PocoF3Releases/hardware_xiaomi/commit/fd1e7be434943c1e13ba24578e6913e4c990c286) |

## Phone acceptance and remaining limits

The original five-key workload and all sixteen supported saved profile settings each passed 28 VoIP cycles with 700-ms active intervals and gaps 0/100/450/500/550/650/1,000 ms, four microphone cycles and six-second media playback. Both full continuous captures had zero processing-confirmation errors and zero owner warning/error/fatal records. All fixture cleanup completed; playback had zero underruns.

In the matched final native trace, twelve enable requests exceeded 35 ms, maximum 59.265 ms, and recovered through readback; two further attempts correctly aborted for communication policy. The sixteen-control trace also retained ten accepted enables beyond 35 ms, maximum 61.888 ms, without errors. One call began after ACK had finished and reached Off enqueue about 203 ms after the fixture observed communication mode. The 10-ms poll is not a hardware or real-time bypass guarantee.

Five controls passed: sixteen-value native snapshot, explicit UI Off, On preserving values, app-owner restart and audioserver restart with saved settings retained. Intentional audioserver termination produced visible −7 effect errors before recovery; the zero-error claim applies to the re-entry matrices.

The three original Dolby APK/OAT artifacts and two preference files were restored byte-for-byte. Original audioserver/Parts identities, SELinux Enforcing and stay-awake 0 were verified; fixture, owned scratch, probes and active test bindings are absent and tracing is Off. Temporary deployment is not installed-release acceptance. No full-ROM/kernel build, flash, headset, acoustic or new DSP-execution claim follows. Raw proprietary code, probe locations, logs and identifiers remain private.
