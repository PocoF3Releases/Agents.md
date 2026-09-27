# PocoF3Releases knowledge base

Technical continuity for POCO F3 / alioth on Android 17 Evolution X, usable through repository access alone by maintainers, GPT-6 Astra, GPT-5.6 Sol and other assistants.

**Begin with [agent rules](AGENTS.md), [task routing](START_HERE.md) and [current state](CURRENT_STATE.md).** Read only the selected route afterward; [INDEX.yaml](INDEX.yaml) is an alternative machine-readable router, not an archive-loading instruction.

| Need | Canonical record |
| --- | --- |
| Current results, accepted limitations, release cutoff | [Current state](CURRENT_STATE.md) |
| Source ownership and recorded branch observations | [Repository map](memory/repositories/README.md) |
| Remote-only work and unavailable artifacts | [Workflow](REMOTE_WORKFLOW.md), [evidence index](EVIDENCE_INDEX.md) |
| Next ROM changelog | [Preparation](today/2026-09-24-changelog-preparation.md) |
| Memory storage, retrieval and Astra-Sol compatibility | [Shared workflow and official sources](memory/agent-memory-workflow.md) |
| Transfer a task or evaluate model compatibility | [Handoff template](templates/cross-model-handoff.md), [optional replay checks](templates/model-compatibility-checks.md) |
| Save a session's useful findings | [Offload protocol](OFFLOAD_PROTOCOL.md), [template](templates/chat-offload-template.md) |

`memory/` contains durable conclusions; `today/` contains dated evidence. Dates record observations, not daily-refresh guarantees. Old snapshots and contribution ledgers remain historical. A repository update does not synchronize ChatGPT memory or generated Codex memory, nor grant access to the maintainer's machine.

## Validate knowledge edits

With Python 3.10+ and PyYAML 6.x available:

```sh
python3 scripts/validate_knowledge.py
# Run when changing the validator:
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Install PyYAML in your chosen environment if needed: `python3 -m pip install 'PyYAML>=6,<7'`. The validator checks governance links, index paths/shape and the root instruction budget without network access. It does not certify technical claims, external URLs or device behavior. See [coverage and limitations](memory/agent-memory-workflow.md#validation).

The [initial guidance review](today/2026-09-26-agent-memory-guidance-review.md) and [Astra-Sol compatibility review](today/2026-09-26-astra-sol-compatibility.md) record documentation maintenance, not ROM releases. Both models read one shared knowledge base; no model-specific database or API service is required.
