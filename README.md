# PocoF3Releases knowledge base

Use [AGENTS.md](AGENTS.md) for rules and [CURRENT_STATE.md](CURRENT_STATE.md) to route unfamiliar work to a relevant topic. The same plain-text records serve Astra, Sol and human readers.

Current conclusions live in `memory/`; [validation](memory/validation.md) records what was actually checked; [the sanitized archive](archive/README.md) retains shareable Android evidence. Do not load the archive at startup.

For edits, see [maintenance](memory/agent-memory-workflow.md). Run `python3 scripts/check.py` with Python 3.10+ and PyYAML 6.x. No client memory, model selection or device access is changed by reading this repository.

Checks run locally; no GitHub Actions workflow is used. EditorConfig supplies text-format defaults without reformatting the sanitized archive.

Public preparation removes personal memory exports and uses noreply Git attribution. See the [privacy boundary](archive/PRIVACY.md); public proprietary-source references are retained.

Moving to a new PC? Start with [WSL recovery](memory/workstation-recovery.md), then [Android and analysis tools](memory/android-tooling.md). The public records preserve project knowledge; private dumps, signing keys and uncommitted work require a separate offline backup. Latest haptics handoff: [implementation and validation limits](memory/haptics.md).

September 30 documentation validation: 39 local tests passed; 155 local references and archive integrity checked. Default startup is 4719 bytes. Recovery commands were syntax-reviewed, not executed as an installation.
