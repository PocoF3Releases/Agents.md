# Alioth development workhub

Portable project memory for **POCO F3 · Evolution X · Android 17 / Android 16**.
Designed for a new chat with no previous context, including GPT-6 Astra,
GPT-6.1 Sol and GPT-5.6 Sol. The same records work through GitHub alone or a local checkout.

## Start a new chat

Paste this with the task:

```text
Use https://github.com/PocoF3Releases/Agents.md as project context.
Read AGENTS.md and CURRENT_STATE.md, then only the topic needed for this task.
Goal: <concrete result>. Done when: <required behavior or artifact>.
Use available access; distinguish recorded evidence from checks you run now.
```

[Rules](AGENTS.md) → [Current state and topics](CURRENT_STATE.md) → one relevant record.
A linked document is retrieved when needed; GitHub links do not preload its contents.

Install the optional [AOSP skill and first-chat setup](operations/first-chat.md) when
preparing a local Codex host; normal chats need not reread the setup guide.

## Where information lives

| Location | Owns |
| --- | --- |
| `memory/` | Current subsystem behavior, decisions, symbols and limitations |
| [Source map](state/repositories.yaml) | Observed public refs and local checkout differences |
| [Validation](state/validation.md) | What was checked, on which implementation, and what remains unknown |
| [Releases](state/releases.md) | Announced changes versus candidates for the next build |
| `operations/` | Recovery, analysis tools, indexing, artwork and maintenance |
| [Evidence](evidence/README.md) | Small portable diagnostics and decisive sanitized results |
| [Archive](archive/README.md) | Historical technical evidence; excluded from normal startup |

Need to reinstall Windows? [Recover WSL and sources](operations/workstation-recovery.md),
then [restore tools](operations/android-tooling.md). Private dumps, keys, local edits
and research outputs still require an offline backup.

## Read less, retain the details

```bash
python3 scripts/context.py --list
python3 scripts/context.py --search 'gesture vibration'
python3 scripts/context.py haptics --startup --sources
python3 scripts/check.py
```

Python 3.10+ and PyYAML 6.x. The context helper reads selected local records only;
it makes no network, model or device calls. GitHub-only readers can follow the
same links manually. [Formatting and update contract](operations/maintenance.md).

[OpenAI guidance](references/openai-guidance.md) explains the shared prompt design.
[Cold-start checks](references/cold-start-checks.md) describe the measured retrieval
coverage and its limits. No model settings or account memory are changed by this repo.
Local checks enforce links, routing, source records, privacy patterns and size limits;
there are no GitHub Actions workflows.
