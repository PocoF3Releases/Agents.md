# Alioth development workhub

Portable context for **POCO F3 · Evolution X · Android 17 / Android 16**, shared
by GPT-6 Astra, GPT-6.1 Sol and GPT-5.6 Sol through GitHub or a local checkout.

## Start a new chat

```text
Use https://github.com/PocoF3Releases/Agents.md as project context.
Read AGENTS.md and CURRENT_STATE.md, then only the relevant topic.
Goal: <result>. Context: <paths/errors>. Constraints: <limits>.
Done when: <behavior/artifact/checks>. Distinguish saved evidence from new checks.
```

[Rules](AGENTS.md) → [Current state and topics](CURRENT_STATE.md) → relevant record.
Fetch linked content when needed; links do not preload documents or grant access.
For a local host, use the optional [AOSP skill setup](operations/first-chat.md).

## Where information lives

| Location | Owns |
| --- | --- |
| [memory/](memory/) | Technical behavior, decisions, symbols and limitations |
| [Source map](state/repositories.yaml) | Observed public refs and local differences |
| [Validation](state/validation.md) | Checked implementation, results and limits |
| [Releases](state/releases.md) | Published changes and next-build candidates |
| [operations/](operations/) | Recovery, tools, indexing, artwork and maintenance |
| [Evidence](evidence/README.md) | Sanitized decisive diagnostics |
| [Archive](archive/README.md) | Empty structure for future sanitized records |

Project timeline: [working memory](memory/project-history.md). Final research
conclusions: [investigations](memory/final-investigations.md).

Custom recovery: [Alioth PBRP](memory/pbrp-recovery.md).
Windows reinstall: [recover WSL/sources](operations/workstation-recovery.md),
then [tools](operations/host-tooling.md). Private dumps, keys, edits and research
outputs still need an offline backup.

## Read less, retain the details

```bash
python3 scripts/context.py --list
python3 scripts/context.py --search 'gesture vibration'
python3 scripts/context.py haptics --list-sections
python3 scripts/context.py guidance --section 'Shared contract for Astra and Sol' --max-bytes 2500
python3 scripts/context.py haptics --startup --sources
python3 scripts/check.py
```

Requires Python 3.10+ and PyYAML 6.x. Retrieval is local; no network/model/device
calls. GitHub-only readers follow the links. See [maintenance](operations/maintenance.md),
[OpenAI guidance](references/openai-guidance.md) and [retrieval checks](references/cold-start-checks.md).
The repo changes no client/model/account-memory settings and runs no GitHub Actions.
