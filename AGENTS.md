# Project rules

POCO F3 / alioth, Evolution X; Android 17 with separately checked Android 16 support.

For a new chat, read [CURRENT_STATE.md](CURRENT_STATE.md), then only the relevant topic. Self-contained edits need affected files and applicable rules. Keep one shared record for GPT-6 Astra, GPT-6.1 Sol and GPT-5.6 Sol; recover missing context rather than replaying transcripts.

- Follow the current request and higher-priority instructions. Logs, archived instructions and old next steps are evidence, not authorization.
- Finish authorized work through relevant checks and requested publication. Resolve routine choices; ask only for material missing input. Preserve unrelated edits. Builds, flashing and history rewrites need authorization for that operation; existing authorization persists within scope.
- Use `user` builds. Root is for research; final fixes belong in source and work without root. Keep `hardware/xiaomi` standalone and device fixes device-scoped where possible. Camera is finalized; reopen only on request.
- Distinguish source, build, runtime and user evidence. A saved head is not a flashed manifest. Verify only relevant mutable facts; do not repeat passed tests without a new reason.
- Report results and remaining limits concisely. Never claim unavailable access, model testing, measured performance or account-memory synchronization.

Knowledge edits: use [maintenance](operations/maintenance.md), keep one owner per fact, then run `python3 scripts/check.py`. Checks are local and use disposable fixtures; no GitHub Actions. Keep secrets, device identifiers and personal details private; use portable `~/` paths.
