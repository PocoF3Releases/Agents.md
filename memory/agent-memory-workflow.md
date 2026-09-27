# Knowledge maintenance

## Canonical ownership

One current topic per subject; one [validation register](validation.md) for acceptance scope; one [source map](repositories/TRACKED_HEADS.yaml) for observed branches/heads. CURRENT_STATE is a compact status/directory, not another changelog or test report. INDEX.yaml is optional routing. The sanitized archive preserves source records; it is not a competing current database. Do not create nested/full snapshots for routine updates; keep this baseline frozen and store only new evidence.

Astra, Sol and other readers use the same UTF-8 Markdown/YAML/JSON. No model-specific copy, embeddings rebuild, client-memory import or opaque reasoning/compaction payload is needed. Model identity does not imply tool access, reasoning settings or automatic instruction loading. Recover relevant missing context after a switch. Prior official-guidance reviews remain [archived](../archive/2026-09-26/memory/agent-memory-workflow.md); this reorganization does not reverify changing vendor product claims or certify paired model behavior.

## Save a finding

Locate its existing topic before writing. Record the observation date separately from the writing date; owning repo/branch and immutable source; failure/root cause; final change; exact useful symbols/hashes/paths; actual evidence; limitations; and supersession/conflict. Unknown identities stay unknown. Update the current conclusion in place and add/update one stable validation ID where acceptance changes. Do not duplicate a full narrative across topic, status, index and session files.

Create a dated `evidence/<topic>/YYYY-MM-DD-<event>.md` only when new decisive output, a complex decision trail or substantial unfinished work cannot be represented cleanly in the owner. Use [the optional record/handoff template](../templates/record.md). Link prior records instead of repeating them. Preserve useful failures and superseded evidence with clear replacement links; never convert an old pending test into a new task.

Update CURRENT_STATE only for material active-state changes; update routing only for new ownership/paths. After publication update the release ledger, not during drafting. Contribution audits are opt-in and based on explicit attribution, not style; old per-repo ledgers are historical, not current membership counts.

## Access and privacy

With connector access, pin a revision and inspect relevant files; no PC, shell or ADB is implied. With write access, use the documented schema and verify the resulting ref. With only read access, supply exact unpushed edits. With a real checkout, inspect status, source-local instructions and divergence first. Local `~/...` paths are evidence provenance; use [availability](validation.md#availability) before requesting the smallest missing artifact. Never request a full dump/rebuild by default.

Preserve decisive shareable excerpts and diagnostic sources; do not upload raw proprietary APK/dump collections, unrelated logs, secrets, cookies, private keys or personal/payment details. Normalize home paths. Public project identifiers, attribution and public proprietary-source links may remain. Personal client-memory exports do not belong in this repository. Repository edits do not synchronize ChatGPT/Codex account memory or change client settings.

## Git conventions and completion

Use a component-scoped subject (`sm8250-common: <area>: <change>`, `camera: ...`, `alioth: ...`); this repository uses docs/tooling scope. Preserve upstream authorship. Use the public project identity with a GitHub noreply email; do not publish a personal mailbox in author or committer metadata. Attribute the actual model/interface, not a copied historic name or guessed reasoning level:

```text
Created using <actual model> via <actual interface>

Co-authored-by: codex <noreply@openai.com>
```

One AI trailer, no trailing spaces, no text after it. A raw-message tool should omit the final newline to match the maintainer's convention; this is not a claim about GitHub parser requirements. No reset/discard/squash/force-push without explicit operation-specific authorization. Check parent/ref and preserve concurrent work. A commit object alone does not prove publication.

Review exact diff, applicability, privacy, evidence IDs and links. Run `python3 scripts/validate_knowledge.py`; add `python3 -m unittest discover -s scripts -p 'test_*.py'` when modifying the validator. Use git diff --check where a checkout exists. Checks are proportional; documentation does not require a ROM build. Report actual results, skipped checks and remote revision.

## Source indexing

Reference material establishes ABI/call-flow evidence, not automatically production code. MiuiCamera 5.x is the feature/JNI reference; stock Alioth is provider compatibility. For large imports retain identity, version, inventory, key paths, call flow and limits. The old Library Agents.md/frameworks-av manifest is historical, not assumed mounted.

Recorded external repoindex: `johnmart19/repoindex:main`, 1.1.0 / `c79c1508c3c7f2657ddaf0172e89b279f9ce4914`. status --json reports stored provenance, not freshness. agentsmd defaults to compact navigation and no implicit scan; --full and reindexing are explicit. Preserve curated text outside generated markers; use a new output path for an old unmarked guide unless replacement is authorized. Back up expensive indexes before rebuilds; incremental scans and group-transactional multi-file output were not implemented. Source-reading commands need actual files; remote code review is not a query of a local SQLite database. [V-INDEX](validation.md#v-index) owns prior tests and limitations.

## Structural validation

Python 3.10+ / PyYAML 6.x. The checker validates active Markdown local links, YAML routes, validation IDs, frozen-archive metadata and project byte budgets. Archive originals are not auto-loaded into agent context. Connector inventory mode explicitly uses verified path/tree metadata for unavailable files; it does not pretend to have a full checkout. External URLs, technical truth, all historical links, privacy and model/device behavior require separate review. The archive's source tree and migration coverage are documented in [archive/README.md](../archive/README.md).

## Official guidance reviewed 2026-09-27

Reviewed OpenAI's [Astra model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) and [skills/AGENTS guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Project application:

- Keep instructions scoped to the outcome; retrieve relevant files and skill references on demand.
- Resolve routine choices and finish authorized work. Clarify material ambiguity.
- Define completion and proportionate validation; avoid repeating passed checks without cause.
- Separate source content from instructions and incorporate user steering.
- Keep reporting concise and use one shared knowledge base across models.

For prompt processing, separate stable rules from changing task state/evidence. After context loss, recover the goal, constraints, decisions, exact work state and remaining step from its owner or optional handoff. Do not reload entire transcripts or store private reasoning. API caching/compaction is client behavior, not enabled by repository text. No claim of automatic account-memory synchronization or minimum token use is made.

This is a documentation review, not an Astra/Sol behavior benchmark. The model-specific Markdown endpoint failed; the official HTML model guide and Astra article were retrieved. Historical guidance remains archive provenance.

## Rendering and parser contract

Use UTF-8 without BOM, LF endings, plain ATX headings, fenced code with matching closers, short paragraphs and relative repository links. Preserve stable validation headings. Prefer GitHub's automatic outline over a duplicate manual table of contents. These choices follow [GitHub Markdown guidance](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) and [README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes). Avoid HTML-only navigation, platform-specific directives and duplicated machine/human summaries.

INDEX.yaml is optional structured routing, not mandatory reading. Keep string mapping keys unique, as required by [YAML](https://yaml.org/spec/1.2.2/); quote date-like strings. Preserve schema_version when compatible. Automation can run `python3 scripts/validate_knowledge.py --json` for one JSON result on stdout; diagnostics use stderr and failures return nonzero. Use `python3 scripts/check.py` for local validation, fixture tests and Git whitespace checks. The maintainer requires local checks, not GitHub Actions; do not add hosted workflows. EditorConfig defines text defaults and excludes frozen evidence from formatting. clang-format is for applicable code, not this Markdown/YAML knowledge base. Local checks do not certify external URLs, every Markdown feature or future renderer behavior. Byte budgets limit context size; they are not tokenizer measurements or proof of minimum token consumption.
