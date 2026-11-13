# USBPD and PS5169 lifetime fixes — November 12, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

`source-checked`, `host-tested`, `build-tested`; USBPD also `device-tested`
within the explicit scope below. Two independent kernel-only follow-ups to
[the rebase checkpoint](kernel-final-review-20261112.md):

- [PS5169 bfc6165](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/2b2c6498c4a09480b73677b8c000e8ccf0f6f081): initialize work/hardware before publication; match callbacks to the live published supply under one mutex; withdraw access before draining work. Return the real pinctrl error and remove an unowned GPIO free.
- [USBPD cd1f8df](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/e49a4518e6d191246e09ee043742f748823b0bd8): stop every enqueue/rearm producer, wait admitted callers, drain system work/timer/private queue, then close PHY callbacks and release messages, Type-C objects and supply references.

Published on `PocoF3Releases/kernel_xiaomi_sm8250:aosp-17`. The previous human
commits and authorship are unchanged; these are ordinary fast-forward follow-ups.
Only `drivers/usb/pd/policy_engine.c`, `ps5169.c` and `ps5169.h` differ from
that checkpoint. No config, DT, UAPI, system, recovery, firmware, register tuning,
security policy, thermal bypass or warning-suppression change.

## Correctness and behavior

Cancellation alone is insufficient: system work or a live PHY/exported producer
could requeue after cancellation and retain freed policy-engine state. The new
stopping state is serialized with every queue/timer arm. Existing device references
pin exported consumers; admitted calls finish before resources are released, while
late resource-using calls reject with `-ESHUTDOWN`. Selector work stays on the
system queue because it waits for the private ordered state-machine queue.
Normal PDO/PPS, roles, SVID/VDM and alternate-mode request logic is preserved.
The PPS monitor now returns its per-poll charge-pump reference.

PS5169 previously published state before work/hardware initialization and retained
a global pointer across failed probes/removal. Independent review found a further
case: a consumer can retain a power-supply handle before registration subsequently
fails. Reading that handle's `drv_data` could still reach freed I2C state. Final
callbacks instead match the currently published controller **and supply identity**
under the teardown mutex. Registration-time, failed and stale-reprobe handles are
rejected; the supply descriptor is static. USB/DP, orientation, gain and EQ
programming are unchanged. Cancellation occurs outside the callback mutex.

PS5169 is bound by **Dagu**, not Alioth. Its fix does not improve Alioth's physical
USB path. Alioth exercises the Qualcomm policy engine; Dagu redriver hardware
operation remains unverified.

## Verification

| Check | Verified result / limit |
| --- | --- |
| Counterexamples | Baseline extracted USBPD teardown/source-check bodies reproduce ASAN use-after-free, including requeue after naive cancellation. PS5169 old probe/publication/remove assertions fail. Both the baseline and first candidate reproduce the retained-registration-handle ASAN UAF; the final implementation rejects it. |
| PS5169 host | 12/12 extracted callback/lifecycle cases pass ASAN+UBSAN and TSAN: initialization, failed/deferred probes, registration-time rejection, normal controls, cfg/remove concurrency, retained failed-registration and stale-reprobe handles. Actual pinctrl helper deferral fails before/passes after. Hardware operations and queue cancellation primitives are modeled. |
| USBPD host | Actual gate/admission/kick/destroy bodies pass 200 concurrent teardown cycles with two million late producer-loop rounds under ASAN+UBSAN and TSAN. All raw queue/timer arms are gated. Resource/IRQ/workqueue transport is modeled; this is not exhaustive policy-state or hardware coverage. |
| Review | Independent source/framework/caller review found the retained-registration defect; it was fixed and retested. Final reviewed file hashes match published source; no remaining required scoped finding. Nine existing request bodies match baseline after the queue-gate substitution. |
| Alioth build | `Image modules dtbs`, Clang `r563880c`, `W=1 KCFLAGS=-Werror`, `-j8`: pass. Resolved config unchanged: SHA-256 `4334682f33f04d0e92ac647cdb15b3fd5d54532b94f2ed2292eeca812f9fe5f9`. Image SHA-256 `c87951ce316a54b01259511854d59b1246ddfc55908bd1a9efd75d2383312544`. |
| Static / Dagu | Final policy-engine, PS5169 and QPNP PHY object checks: W=1/Werror and Sparse pass with zero reports under Alioth and separately resolved Dagu configs. No full Dagu kernel/hardware certification. Both patches pass strict checkpatch. Existing unrelated kernel-doc/Bison diagnostics remain separate from compiler success. |
| Phone normal USB | Exact candidate temporarily booted with original ramdisk/header, Enforcing and taint 0. MTP/ADB functions applied and both configfs interfaces present; device/sink roles and charging retained. Exact 4 MiB **ADB** round trip passes. This does not claim a Windows MTP file-transfer test. Original function selection restored. |
| Phone real teardown | Private one-shot module pins a real consumer reference, calls actual `usbpd_destroy`, then verifies 6,000 late API checks: all pass. Secure wireless ADB stays usable. This does not stress every PPS/extended-message interleaving or remove the parent PHY/other consumers. Diagnostic out-of-tree taint is recorded separately. |
| Restoration | Reboot and temporary boot of the same candidate restore a fresh policy engine, wired ADB, device/sink roles and charging. Kernel `4.19.325-Redline-cd1f8df-cip136`, Enforcing, taint 0, thermal service active, no kernel splat. Test module absent and only owned test files removed. No partition write. |

## Remaining boundaries

Physical PS5169/DP peripherals, actual OTG accessories, high-voltage PPS chargers,
all USB function combinations and long endurance are not certified by these checks.
No feature was disabled to obtain the result. Temporary boot acceptance is not a
claim that an OTA or persistent boot partition contains this kernel.

Audio, Airoha GPS and thermal-clamp restricted tasks stay parked. The older USB
outage and GPU donor experiments also remain paused; this bounded lifetime check
did not induce a PC outage or resume those experiments.

Raw fixtures, sanitizer/build/device receipts and original artifacts remain private
under `~/evo/.repo/kernel-usb-lifetime-20261112/`. Test code is not shipped in the
kernel repository. Historical Sparse backlogs retain their earlier scope.
