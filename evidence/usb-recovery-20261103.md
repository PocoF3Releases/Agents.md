# USB recovery — 2026-11-03

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

`source-checked`, `host-tested`, `build-tested`, `device-tested` within this scope.

## Published fixes

- [Reconnect after gadget reset](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/0f54e1bd62865d427f7d80b3d87230096f1540aa): restore the selected controller after unbinding, serialize against function changes and report failures. Accept a verified same-controller FunctionFS rebind.
- [Initialize queried functions](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/c16fd5cafb0e86917b3c0f15668ba2c88e2e6e8d): initialize the bitmap to NONE before a query can read it.
- [Recover the framework proxy](https://github.com/PocoF3Releases/frameworks_base/commit/3e77a60e56eb1cc8bc0f7ac71dd6df4d11dd54ce): register Binder death handling, ignore obsolete death notifications and reacquire a missing proxy before requests.

The original HAL reported reset success but left MIDI-only USB unbound across
40 samples. ADB-only reset masked the defect through FunctionFS recovery.
The framework's existing service-death method had no Binder registration.
Function selection, descriptors, authorization and security policy are unchanged.

## Acceptance

Host source-extracted regressions: reset 109 cases, initialization 16 and proxy
lifecycle 37 pass. Original sources fail 108, 12 and 36 respectively. Reset
fixtures use ASan/UBSan and compiler Werror; they do not emulate kernel configfs.
The normal user-product gadget module and services targets both build successfully.

Temporary phone tests retained Enforcing SELinux and the normal HAL domain.
Three HAL restarts produced changed PIDs, Binder death notifications and successful
MIDI+ADB callbacks. The actual candidate executable then passed three MIDI-only
resets, all 36 configured-state samples, plus ADB-only and MTP+ADB reset callbacks
and configured-state checks. Original functions and ADB enablement were restored.
The original framework/HAL hashes and running executable were verified afterward;
staging, logger and temporary mounts were removed. No flash or wipe occurred.

Test lesson: a bind-path hash alone was insufficient across mount namespaces;
early attempts still executed the original HAL. Verify `/proc/<pid>/exe`, bind
before restart, and wait for a replacement PID. A waiting Binder client can
automatically restart a stopped service. Earlier staging attempts are excluded
from candidate acceptance. Windows ADB also needed a server restart to reconnect.

All four authored recovery patches reverse/replay to exact expected trees using
isolated indexes, including the new ROM framework base. The stock preflight
rejects existing untracked AGENTS.md/CLAUDE.md routers; those were preserved.
No patch runner or cleanliness requirement was weakened.

These fixes need a ROM rebuild for permanent installation. No full ROM/recovery
rebuild, exhaustive USB-host certification, physical cable matrix or proof that
every historical USB outage has the same cause is claimed. The wider compatibility
audit and paused boundary-task exclusion remain in force.
