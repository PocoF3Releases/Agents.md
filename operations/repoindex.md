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

The dated [V-REF-INDEX](../state/validation.md#v-ref-index) and consumer
[validation](https://github.com/PocoF3Releases/references_code/blob/main/docs/VALIDATION.md)
own measured coverage, tests and speed. They establish neither current live-tree
freshness nor a new Android build/device pass. Do not repeat audits or benchmarks
at startup; an empty lookup first calls for spelling, scope and language checks.

## Refresh only after relevant changes

Generic CLI/database/bundle development belongs to
[johnmart19/repoindex](https://github.com/johnmart19/repoindex); the reference
consumer vendors its tested copy. Use that copy with its bundles, not an unrelated
older installation. Consumer `repoindex.json` owns roots/scopes and query defaults.

For an explicitly requested data refresh, follow the consumer's
[maintenance guide](https://github.com/PocoF3Releases/references_code/blob/main/docs/MAINTENANCE.md).
`workspace index --tree NAME`, `implement`, `optimize` and deep live/hash verification
change or rescan data and are not startup commands. Keep generated census in its
marked guide; preserve curated AGENTS.md and source provenance. Source-free and
fixture checks are explicit acceptance, not a reason to rebuild the real indexes.

## Active build tree and historical indexes

The ready historical references are separate from `~/evo`. For active source edits,
use bounded scoped `rg`/`git grep` and verify the actual owning source. A build-tree
index requires its own freshness check; the old [V-INDEX](../state/validation.md#v-index)
is historical and does not establish current coverage.

Use [repositories](../state/repositories.yaml) for maintained tool/reference heads.
Updating a tool, its vendored consumer and a data snapshot are distinct operations.
No index result grants build, flashing or publication scope.
