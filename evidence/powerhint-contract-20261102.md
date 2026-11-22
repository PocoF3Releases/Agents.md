# Power-HAL provider checks — 2026-11-02

**Source/device checked; no production source or tuning change.** Follow-up to
the [kernel-to-consumer plan](kernel-contract-plan-20261102.md). Tests exercised
bounded normal framework requests rather than writing boost values directly.

## Selected consumer and installed identity

The common device tree packages `android.hardware.power-service.lineage-libperfmgr`
and `libperfmgr`. Installed and built artifacts match:

- Power HAL SHA-256:
  `27be206259c5872d706e4310a424b2b1f0d49c086da9f5a7800d843378fa3407`.
- libperfmgr SHA-256:
  `16096012451a404a2061a478ee9c31585da7a5a0d229f6859a6e46eb5192a65d`.
- Installed `powerhint.json` equals common source, SHA-256:
  `ac04e3ed6193dc332ca1d8c2923fc58bcae86837189ccb810247829736924903`.

The service/HintManager run normally in `hal_power_default`. All 29 configured
nodes were enumerated, including property nodes and the PM-QoS character device;
existence is not proof that every hint/action was exercised. ADPF is explicitly
unconfigured, so no session/headroom feature was enabled or claimed tested.
The running kernel is `4.19.325-Redline-1846f92-cip136`, enforcing, taint 0.

## Bounded request acceptance

A private client called IPowerManager, through the installed framework and HAL:

| Request | Observed kernel behavior | Release |
| --- | --- | --- |
| INTERACTION, 800 ms | CPU little/big/prime minima 1171200/1286400/1190400 kHz; CPU-to-LLCC and LLCC-to-DDR minima 9155/2597 | All sampled nodes returned to their exact baseline values |
| AUDIO_LAUNCH, 500 ms | CPU DMA latency aggregate became 97 microseconds | Returned to the baseline 2000000000 after expiry; explicit cancellation also issued |

CPU maximum frequencies and GPU maximum power-level controls were unchanged
by the interaction request. mi_thermald and the power service retained their
PIDs during that batch; no thermal or security setting was changed. The client
and staging were removed. No persistent profile/mode or unknown-duration boost
was requested.

The PM-QoS transport matters: this kernel parses a non-four-byte text write as
base 16, so the configured string `61` yields decimal 97. Readback used the
binary s32 API. Do not reinterpret that string as decimal 61 and alter it without
a demonstrated intent mismatch. With no active held request the aggregate
returns to the unconstrained kernel default, not an assumed decimal JSON value.

An initial 100-ms interaction sample saw baseline values because idle handling
can release a boost at that boundary. Sampling at 10 ms observed all expected
CPU/bus minima; the later snapshot verified release. This is a sampling issue,
not evidence of a dropped request. Native host-side dumpsys supplied service
statistics when the optional Java dump helper could not retrieve that service;
no policy grant was added to enable the helper.

## Boot-time power overrides

The common init script temporarily sets `sleep_disabled=1` during startup;
`init.qcom.post_boot.sh` restores `N`. Fresh readbacks confirm `N`, UFS clock
gating enabled, and C0/C1 usage counters increasing between two observations.
Foreground/global scheduler boosts are at runtime values rather than the boot
100 boost; top-app retains the configured 10. No missing low-power re-enable was
demonstrated. These checks do not measure suspend current or whole-device battery
life, and presence of an idle count does not certify every sleep state.

No source mismatch justified a patch in this pass. Not all modes, simultaneous
hint ownership, active workload behavior, thermal throttling, ADPF tuning or
hardware fast-charging adapters were tested. Keep the existing protection and
[charging limitations](charging-controls-20261102.md). No new production build
was needed for this read/request-only check; source heads and earlier build
acceptance remain separate in the [source map](../state/repositories.yaml).
The blocked touch task remains skipped.

Private receipts: `~/evo/.repo/powerhint-contract-20261102`.
