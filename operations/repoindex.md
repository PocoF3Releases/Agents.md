# Ready Android reference indexes

Use [references_code main](https://github.com/PocoF3Releases/references_code/tree/main)
for historical Android/Qualcomm searches. Read its short `AGENTS.md`, then only the
needed [search guide](https://github.com/PocoF3Releases/references_code/blob/main/docs/SEARCH.md).
The ready bundles select both trees by default. Do not rebuild, benchmark or run
a deep audit at chat startup. This snapshot is separate from active `~/evo`.

## Use the ready checkout

```bash
git clone --filter=blob:none --sparse --single-branch --branch main https://github.com/PocoF3Releases/references_code.git ~/references_code
cd ~/references_code
git sparse-checkout set tools/repoindex index docs evidence scripts
python3 tools/repoindex workspace status
python3 tools/repoindex workspace scopes
python3 tools/repoindex workspace files '*AudioFlinger*' --limit 10
python3 tools/repoindex workspace symbol BPSNode --scope camera --limit 5
python3 tools/repoindex workspace impl 'BPSNode::ExecuteProcessRequest' --scope camera --limit 5
python3 tools/repoindex workspace source LA.UM.8.12.r1-11900-sm8250.0/camx/src/hwl/bps/camxbpsnode.cpp --line 1351 --limit 20
```

Skip cloning when the checkout exists; preserve local modifications. Source trees,
tool and chunks are ordinary Git files: no submodules or LFS. The default recipe
is index-only: do not download source folders solely to query them. No pip install, virtual environment or setup script is required. Root configuration
is already tracked and included by cone-mode sparse checkout. First indexed use verifies/restores local SQLite caches
without parsing sources or calling a service. Warm queries reuse these caches.
A cold cache is normal. `status` shows saved provenance and cache readiness,
not a live freshness check.

The canonical v2 interface defaults to compact text: 20 global results, 400-character
excerpts and a 12,000-byte stdout budget. Narrow with `--tree NAME` (repeatable),
then either `--scope TOPIC` or `--path-prefix tree/component`. Use `--json` for
JSON Lines. Find a hit, then retrieve a small range; never load full inventories
or bodies into chat. Budget notices go to stderr. The compatibility
`scripts/refsearch.py` retains JSON and its old 40-result default; prefer the
canonical command for new usage. Compatibility scripts contain no search logic.

## Alioth reverse engineering

Follow the [source and binary correlation workflow](alioth-reverse-engineering.md)
for shipped prebuilts: locate historical contracts from binary names/logs/IDs,
then validate ABI, callers and hardware against current Alioth inputs. Empty
scoped queries do not prove a feature is absent.

## Choose a mode

| Need | Mode |
| --- | --- |
| Path substring or glob | `files QUERY` |
| Exact heuristic C/C++ header symbol | `symbol NAME` |
| Literal anywhere in full .cpp/.cc implementations | `impl QUERY` |
| Small indexed implementation range, even without live files | `source PATH --line N --limit 20` |
| Live changes, regex, Java/Kotlin or other languages | `text QUERY --scope TOPIC`, explicit `--regex`, or scoped `rg` |
| Current Android 17 behavior | Active source and relevant workhub acceptance |

Body search includes complete function bodies, comments and strings; it is not
compiler/overload analysis. Indexed UTF-8/NUL and newline normalization is disclosed
in the tool's [format reference](https://github.com/johnmart19/repoindex/blob/main/docs/FORMAT.md).
Live code remains untouched. Verify hits against live files when editing.

## Checked coverage and speed

**2026-10-25, host/source checked.** Both datasets remain unchanged through the
organization cleanup: 212,048 Android files / 72,079 complete implementations and
44,561 Qualcomm files / 2,490 implementations, with zero scan errors. Android's
restored database is 2,092,015,616 bytes; compression does not imply missing bodies.
The prior deep audit covered every implementation's raw/normalized hash, chunk/DB
hashes, SQLite/FTS and logical coverage. Other live files use metadata checks.

The standalone repoindex 2.1.1 suite passes 81 tests, including migrated consumer
contracts, bounded output and protected guide updates. The configured 11-case warm
benchmark passes its 100 ms median budget (observed about 2–13 ms). A source-free
package check verifies real bundle restoration, body queries and line retrieval.
These are host observations, not future speed/freshness or build/device guarantees.
See [V-REF-INDEX](../state/validation.md#v-ref-index), the consumer
[validation](https://github.com/PocoF3Releases/references_code/blob/main/docs/VALIDATION.md)
and its [evidence directory](https://github.com/PocoF3Releases/references_code/tree/main/evidence).
The reusable `python3 scripts/check_fresh_clone.py` passed 29 fresh GitHub
index-only acceptance checks with no site packages/pip or source checkout. It
restores and queries both indexes, guards the in-process probe against network,
subprocesses and ingestion, checks normal launchers and removes its temporary
clone. It requires only Git/Python/SQLite, about 401 MiB of network download and
3 GiB temporary disk; no source rebuild or runtime installation. Use it only for
explicit acceptance, never startup. `--report .cache/fresh-clone-report.json`
saves evidence. The 81 tool and 3 consumer-harness fixtures are separate explicit
`python3 scripts/check.py --tests`; only those build tiny synthetic indexes.
[Fresh-clone evidence](https://github.com/PocoF3Releases/references_code/blob/main/evidence/fresh-clone.json).
Exact current revisions belong in [repositories](../state/repositories.yaml).
The final review fixed empty API selections, EOF ranges, ignored maintenance
filters and failed-write/restore cleanup; ready data was not rebuilt.
An empty lookup is a reason to check spelling, case, scope and language coverage,
not to run ingestion. The consumer
[agent guide](https://github.com/PocoF3Releases/references_code/blob/main/AGENTS.md)
owns the short find → body hit → indexed range workflow. Its explicit
`python3 scripts/check.py` checks docs/config/chunk sizes without restoration or
source scans; `--tests` adds disposable tool fixtures. Neither is a startup step.

## Refresh only after relevant changes

Develop the canonical tool in independent `~/tools/repoindex`; the consumer keeps
a pinned complete copy, including `src/repoindex/`, and works without that checkout.
The package separates database/scanner/bundle/workspace services from CLI/reporting;
old file/import routes remain compatibility shims. Optional isolated installation
provides `repoindex` and `python -m repoindex`; default consumer commands above
still use its tested copy. See the canonical
[development map](https://github.com/johnmart19/repoindex/blob/main/docs/DEVELOPMENT.md).
The 2.1 installed-package check builds an sdist/wheel and tests every legacy
command plus console/module/API source-free queries offline.

Generic CLI, format, tests, guide generation and maintenance belong to
[johnmart19/repoindex](https://github.com/johnmart19/repoindex). Workspace roots,
scopes, benchmark cases and guide destination belong to consumer `repoindex.json`;
source provenance and actual measurements remain in the consumer. Use its vendored
tested tool rather than an unrelated older `~/repoindex` copy. Linux/WSL, Python
3.8+ and SQLite 3.34+ with FTS5/trigram are required; live text needs ripgrep.
No Python packages, models or persistent daemon are needed.

After source changes, explicitly run `python3 tools/repoindex workspace index
--tree NAME`; it includes full selected .cpp/.cc text. For unchanged older data,
`implement` explicitly adds bodies and `optimize` adds acceleration. Neither is a
startup step. Deep `verify --live --hash-implementations` is explicit and expensive.
Follow the consumer's
[maintenance guide](https://github.com/PocoF3Releases/references_code/blob/main/docs/MAINTENANCE.md).
Generated census belongs in marked `docs/INDEX_GUIDE.md`; preserve curated
`AGENTS.md`. `main` histories were consolidated with verified local recovery
bundles and exact expected-head leases; legacy reference branches are retained.

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
