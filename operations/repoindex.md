# Ready Android reference indexes

Use [references_code main](https://github.com/PocoF3Releases/references_code/tree/main)
for historical Android/Qualcomm reference searches. Both source trees, the tool and
ready index bundles are ordinary Git files. Do not rebuild or run a full verification
at chat startup. Start with the shipped wrapper, not an older `~/repoindex` copy.
This reference snapshot is separate from the active `~/evo` Android 17 build tree.

## Use the ready checkout

Resolve the checkout (normally `~/references_code`) and read its `AGENTS.md`.
If missing, clone it once; no submodule initialization, LFS or source scan is needed:

```bash
git clone --single-branch --branch main https://github.com/PocoF3Releases/references_code.git ~/references_code
cd ~/references_code
python3 scripts/refsearch.py status
python3 scripts/refsearch.py scopes
python3 scripts/refsearch.py files '*AudioFlinger*' --limit 20
python3 scripts/refsearch.py symbol BPSNode --scope camera --limit 10
python3 scripts/refsearch.py impl 'BPSNode::ExecuteProcessRequest' --scope camera --limit 5
python3 scripts/refsearch.py source LA.UM.8.12.r1-11900-sm8250.0/camx/src/hwl/bps/camxbpsnode.cpp --line 1351 --limit 20
python3 scripts/refsearch.py text AudioFlinger --scope frameworks --limit 20
```

File, symbol and implementation searches select **both** `android-t-qcom` and
`LA.UM.8.12.r1-11900-sm8250.0` by default. Add `--tree NAME` (repeatable) for one;
`--scope TOPIC` intersects the selection with a component. Output is JSON Lines
with source-qualified paths and a global default limit of 40. Narrow tree/scope
before increasing limits. First locate a file/symbol/body hit, then read a small indexed or live source
range; never load complete symbol inventories into the chat.

The committed bundles are `index/<tree>/manifest.json` plus compressed chunks.
First indexed use verifies/restores selected databases into ignored
`.cache/repoindex/<tree>/<hash>.db`; this is **restoration, not reindexing**, and
requires no network/model/source scan. Warm requests reuse those read-only caches,
including during a rebuild. Status shows `search_backend=trigram`, `cache_ready`,
saved counts and scan errors; a cold cache is normal, not a reason to rebuild.

Linux/WSL, Python 3.8+ and SQLite 3.34+ with FTS5/trigram support are required for
these accelerated bundles. Ripgrep supplies live text search. No Python packages,
embedding service or persistent daemon are needed. Related Python lookups may reuse
`workspace_index.query` in one process to amortize CLI startup.

## Pick the right evidence

| Need | Use |
| --- | --- |
| Filename/path fragment | `files QUERY --scope TOPIC --limit 20` |
| Exact C/C++ header type/macro/global name | `symbol NAME --tree NAME --limit 20` |
| Complete .cpp/.cc body text, method name or code fragment | `impl QUERY --scope TOPIC --limit 10` |
| Indexed body range after a hit (works without source folders) | `source PATH --line N --limit 20` |
| Live edits, regex, Java/Kotlin or other suffixes | `text QUERY --scope TOPIC` or scoped `rg` |
| Source details after a hit | Read only the relevant line range in that file |
| Shared Android 17 behavior/acceptance | Relevant workhub topic, active source and validation; historical reference is not device evidence |

Header declarations/includes are heuristic, not complete C++/Java symbol coverage.
File search uses literal case-insensitive substrings or case-sensitive globs;
live text is fixed-string unless `--regex` is supplied. Binary references remain
indexed by path; use appropriate ELF/string tools after locating a candidate.
Source/prebuilt contents are preserved, including one original generated header.

## Checked coverage and speed

**2026-10-25, host-tested/source-checked:** repoindex 1.4.0
([5fff5e6](https://github.com/johnmart19/repoindex/commit/5fff5e6867db265a8329db986a9a58338263939a)):

| Tree | All files | Full .cpp/.cc bodies | Header symbols |
| --- | ---: | ---: | ---: |
| `android-t-qcom` | 212,048 | 72,079 | 2,977,498 |
| `LA.UM.8.12.r1-11900-sm8250.0` | 44,561 | 2,490 | 225,021 |

Both have zero scan errors and complete implementation text, including all
function bodies; storage is not sampled or truncated. Every implementation's raw
and normalized-text SHA-256 passed, together with chunk/DB hashes, SQLite/FTS and
file/reference coverage. Non-implementation live checks compare path/size/mtime.
43 tool fixtures plus 6 workspace tests passed. Sampled warm body-query medians
were about 3–10 ms; results/ranges matched independent live-source checks. The
11-case filename/header/body benchmark passed its explicit 100 ms warm-median
budget. These are host measurements, not future guarantees.

`impl` is case-sensitive literal search, supports multiline fragments and returns
line/end-line/column with bounded excerpts (400 characters plus clipping markers).
Use `--context 1` only when useful; context is capped at 1600 characters per hit.
`source` reads indexed line ranges (up to 200 lines), including on a source-free
checkout. Original code is untouched; UTF-8 replacement/NUL and LF normalization
are recorded and raw hashes retained. This is full-text search, not compiler AST
or overload resolution. Cold restoration is larger now (about 15.5 seconds for the source-free
package check), but does not read or parse the source tree.
See [V-REF-INDEX](../state/validation.md#v-ref-index),
[implementation coverage/reproduction](https://github.com/PocoF3Releases/references_code/blob/main/docs/IMPLEMENTATIONS.md)
and [audit](https://github.com/PocoF3Releases/references_code/blob/main/docs/index-verification.json).
Do not benchmark again without a relevant change or an unresolved performance issue.

## Refresh only when needed

Saved status/audits do not prove future freshness. Verify a hit against live source.
After actual source changes, explicitly refresh only the changed tree:

```bash
python3 scripts/reindex.py --tree android-t-qcom
# Both only when both changed:
python3 scripts/reindex.py
# Explicit deep audit if warranted; never a startup prerequisite:
python3 tools/repoindex/repoindex.py workspace verify --live --hash-implementations
```

Normal index refreshes include complete .cpp/.cc text automatically. `workspace
implement` ingests implementation contents once into an unchanged older snapshot;
it reads those sources and must never be run just to start a chat.
`workspace optimize` adds newer acceleration to unchanged saved snapshots without
rescanning source; it does not refresh source changes. New bundles publish atomically
per tree, not as one cross-tree transaction. There is no incremental parser scan.
Preserve modified checkouts, source notices and unrelated edits. Follow the target's
maintenance guide for updates and cleanup, and never generate over curated `AGENTS.md`.

## Active build tree and historical indexes

The old `<root>/.repoindex.db` interface still applies to separate legacy/build-tree
indexes, not this ready multi-tree reference setup. Inspect the actual available
snapshot with `status --root ~/evo --json`; do not assume it was refreshed here.
Historical [V-INDEX](../state/validation.md#v-index): September 24 host tests of
repoindex 1.1.0 / c79c150 passed 20 recorded regressions. The September 30 read-only
metadata observation found a September 28 A17 scan: 1,756,352 files, 10,180,486
symbols, schema 2, known coverage, zero recorded errors, excluding `out` and VCS
metadata. It reported `live_tree_verified=false`; that update performed no new
scan or benchmark. These observations remain historical. Neither shipped references nor the new tool validate an A17
build/device, grant flashing/build scope, or synchronize account memory.

The canonical tool remains [johnmart19/repoindex](https://github.com/johnmart19/repoindex).
The reference checkout vendors the tested revision and should use that copy for
its bundles. Updating a standalone script is separate from updating a database.
