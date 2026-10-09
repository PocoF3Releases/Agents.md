# Cold-start retrieval checks

Local routing/content checks, not live Astra/Sol evaluations or paid API calls.

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

`test_context.py` covers discovery, topic/source scoping, retained intro/nested
sections, byte-limit rejection without truncation, unknown topics and containment.
Validator fixtures cover malformed links/YAML/heads, archive integrity and sensitive
patterns. Technical truth still requires source/evidence review.

## Size contract

`INDEX.yaml` budgets startup/root/topic bytes; `scripts/validate_knowledge.py --json`
reports startup usage. Context JSON reports UTF-8 content bytes, excluding wrappers
and tool schemas; these are not exact model tokens.

Read more when needed to retain evidence/uncertainty and finish authorized work.
Measure model tokens/cost/quality with matched tasks in the actual client; fixture
results imply no performance percentage.
