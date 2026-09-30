# Cold-start retrieval checks

These are local routing/content checks, not live GPT-6 Astra, GPT-6.1 Sol or
GPT-5.6 Sol evaluations. No model API calls or paid hosted workflows run.

## Representative tasks

| Fresh-chat request | Primary owner | Essential boundary |
| --- | --- | --- |
| Weak gesture vibration | Haptics | Final stock effects, 48/80/128; no synthetic primitives; candidate deployment distinct from next ROM |
| AC-4 or VNDK helper failure | Audio | 21-entry private OMX ABI and opted-in helper path; no blanket VNDK links |
| Camera 0.6x / 4K | Camera | Finalized, 4K ultrawide guarded; true ultrawide 60fps unproven |
| Windows reinstall / restore tools | Recovery → tools | Knowledge is portable; private dumps/keys/local edits need backup |
| Android 16 changelog | Releases | Later release reported, exact artifact unknown; do not reuse A17 tests or old links |
| Vulkan / Myron frame generation | Graphics | Experiments parked; hardware backend not a device-tree toggle |
| Proximity / touch / translations | Device UX | Actual supported controls and test scope, no general all-device claim |
| Upstream ownership / branch status | Source map | Observed refs and local divergence, not flashed inclusion |

`test_context.py` checks discovery, bounded topic bundles, scoped source retrieval,
unknown-topic rejection and path containment. Validator fixtures check malformed
links/YAML/source heads, archive integrity and sensitive-data patterns. Human
review reconciles technical statements with source and saved observations.

## Size contract

`INDEX.yaml` sets byte budgets for the two startup files, root rules and each
active topic. `scripts/validate_knowledge.py --json` reports actual startup bytes.
The helper's JSON reports selected content bytes; wrappers and tool schemas are
additional context. Byte counts are reproducible but are not exact model tokens.

A complete task must retain necessary evidence even when a longer read is needed.
The target is less unnecessary retrieval, not an artificial cap that discards
uncertainty or stops authorized work. Measure actual model tokens/cost/quality only
with matched tasks and the available client; no performance percentage is inferred
from these fixture tests.
