# OpenAI guidance applied to this workhub

Online model/prompt guidance reviewed **2026-10-06**. Project guidance; no client changes or measured model savings.

## Shared contract for Astra and Sol

Use one knowledge record and a task with **goal, context, constraints, done when**.
[Codex best practices](https://learn.chatgpt.com/guides/best-practices) recommends
this structure. Retain source identities, evidence scope and missing facts; no per-model memory copy.

| Reader | Application |
| --- | --- |
| GPT-6.1 Sol | Complex coding/professional work; compare with Astra on matched tasks. Retain selected model/effort. |
| GPT-6 Astra | Define completion/scope; avoid blanket rereads, extra approvals and repeated passed checks. |
| GPT-5.6 Sol | Share records with explicit evidence and remaining scope. |

The [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model)
covers both requested models. Its API settings are not Codex client defaults:
Sol's documented API default is medium; both models reject none/minimal effort.
Use the client's configured default unless the task/user warrants a change.

## Retrieve only missing context

OpenAI's [Astra skills and prompts review](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends task-specific document access, narrow skill triggers and small routers.
Keep rules once in AGENTS, current state in its owner and details behind links.
No blanket delegation or model-specific workflow copies.
Preserve authorization for builds, flashing and publication; routine in-scope
work should continue without repeated approval. Tests should address the change;
repeat/broaden them only after a relevant change, failure or unresolved concern.

Use the local context helper to discover a topic and select an exact heading:

```bash
python3 scripts/context.py --search 'Astra prompt tokens'
python3 scripts/context.py guidance --list-sections
python3 scripts/context.py guidance --section 'Shared contract for Astra and Sol' --max-bytes 2500
```

A selected section retains the document intro and nested headings. Startup rules
are included only with --startup and remain complete. --sources stays scoped to
the topic. A byte limit rejects an oversized bundle before output; it never
silently truncates evidence. Follow links when the excerpt lacks needed facts.
For size/measurement limits see [retrieval checks](cold-start-checks.md).

Fetch remote links explicitly. Use readable records, not encoded/safetensors
archives. For optional [AOSP skill](../skills/aosp-wsl/SKILL.md) installation see
[first-chat setup](../operations/first-chat.md).

## Resume and evaluate

Recover goal/scope, source revision, decisive results, local/published state and
remaining work after compaction. Use the [handoff template](../templates/record.md)
when needed; omit private reasoning/unrelated logs. Client memory, caching and
compaction remain harness-managed.

Compare matched tasks before/after one prompt change, retaining required facts.
[Cold-start checks](cold-start-checks.md) establish retrieval behavior only; actual
model/client evaluations are required for token/cost/quality claims.
