# OpenAI guidance applied to this workhub

Official documentation reviewed **2026-09-30**. These are project design choices,
not model certification, API configuration or claims of measured model savings.

## Shared contract for Astra and Sol

All three requested models use one record format and one task prompt:
**goal, relevant context, constraints, done when**. Keep stable rules in AGENTS,
changing facts in state, domain details in one topic and output evidence behind
links. Load the task's missing facts; do not mandate a repository tour for a
small edit. Give exact symbols/paths and accepted limitations so no prior chat,
private transcript or PC is needed to understand a recorded conclusion.

| Reader | Application |
| --- | --- |
| GPT-6 Astra | Clear completion criteria and scoped authorization support follow-through; remove repeated rules, unnecessary questions and repeated passed checks. |
| GPT-6.1 Sol | Use the same explicit task and evidence contract; retrieve the relevant source/evidence instead of a separate model-specific memory copy. |
| GPT-5.6 Sol | Preserve concrete identifiers, test scope and the next authorized step so a resumed task does not depend on implicit conversation history. |

OpenAI's [GPT-6 guidance](https://developers.openai.com/api/docs/guides/latest-model)
covers Astra and 6.1 Sol and recommends evaluating prompts on the chosen workload.
The [GPT-5.6 Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
establishes that model's identity; it does not prescribe a different project-memory schema.
Do not infer model availability, client effort levels or tool access from these files.
Keep the user's selected model/effort; no automatic switches or maximum-effort mandate.

## Reduce unnecessary context

OpenAI's [Astra skills and prompts review](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends narrow triggers, minimal routers and task-relevant retrieval. This hub
therefore has no blanket skill/delegation policy, full-tree census at startup,
mandatory transcript replay or duplicate per-model instructions. Tool responses
should expose relevant fields/snippets instead of whole search payloads.

Use independent read batches where useful; keep dependent edits, publication and
verification sequential. Delegate only when current policy permits it and a
separable task warrants the extra context/coordination. A documentation refresh
does not justify device testing or a ROM rebuild.

[AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
loads directory-scoped instructions with a combined default 32 KiB limit. A huge
inventory can crowd out useful rules. The optional Android-root template points
to this hub; full inventories remain separate. GitHub browsing requires fetching
linked content explicitly; local auto-discovery does not apply to a remote link.

[Skills guidance](https://learn.chatgpt.com/docs/build-skills) loads metadata first,
then a selected SKILL.md and references as needed. The task router follows that
principle. The optional [AOSP skill](../skills/aosp-wsl/SKILL.md) can be installed
using [first-chat setup](../operations/first-chat.md); cloning the workhub alone
does not install it, change client settings or load every referenced file.

## Resume and evaluate

After a new chat or compaction recover: goal/scope, relevant current topic,
source identities, actual results, uncommitted/pushed state and the remaining
step. Use [the handoff template](../templates/record.md) when this is not already
clear. Do not serialize private reasoning or promise account-memory synchronization.

[Cold-start checks](cold-start-checks.md) exercise routing and retrieval without
model calls. Byte/word counts are deterministic context-size measures, not exact
model token counts. Lower mandatory context should reduce avoidable input, but
real token/cost/quality differences require matched tasks on the actual models.
