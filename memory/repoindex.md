# repoindex recovery and usage

Canonical repository: [johnmart19/repoindex](https://github.com/johnmart19/repoindex), branch `main`. Inspected local revision: `c79c1508c3c7f2657ddaf0172e89b279f9ce4914`, version 1.1.0. It is a Python source/file/symbol indexer, **not** Repo (Android multi-repository manager) or repopick (Gerrit helper).

## Restore the canonical copy

```bash
git clone https://github.com/johnmart19/repoindex.git ~/repoindex
python3 ~/repoindex/repoindex.py --version
python3 ~/repoindex/repoindex.py --help
```

If the directory already exists, inspect status, remote and divergence before updating. The tool requires Python 3.8+ and standard library only; PyYAML is a dependency of this knowledge repository's validator, not of repoindex. Use the remote's current documentation if its CLI changes.

## Recover existing indexes

Default database: `<indexed-root>/.repoindex.db`; `--db` can select another location. Preserve databases and any SQLite sidecars consistently with no writer running. Back up the whole directory or use SQLite backup rather than copying a live database piecemeal. Dumps and source files must also exist: an index is not their backup.

```bash
python3 ~/repoindex/repoindex.py status --root ~/evo17 --json
python3 ~/repoindex/repoindex.py status --root ~/references_code --json
```

`status` reports stored root, scan/provenance and coverage, not present freshness. After moving a root, verify stored paths and source identity; rebuild deliberately if mismatched. Do not claim the old September 9 snapshot describes today's checkout. [V-INDEX](validation.md#v-index) records historical checks and limitations.

## Scan and generate only when needed

```bash
python3 ~/repoindex/repoindex.py index ~/evo17 --ignore out
python3 ~/repoindex/repoindex.py agentsmd ~/evo17 --out ~/evo17/INDEX_GUIDE.md
# Full inventories belong outside automatically loaded agent instructions:
python3 ~/repoindex/repoindex.py agentsmd ~/evo17 --full --out ~/evo17/STRUCTURE.md
```

A scan can be large; choose the intended root and exclusions first. `--no-ignore` includes VCS metadata and is rarely appropriate. `--no-symbols` produces a file-only index. Use `lookup`, `search`, `headers` and their `--help` for narrow retrieval; declarations are heuristically extracted, not compiler-certified ABI. `agentsmd` defaults to compact output and does not scan unless `--reindex` is supplied. Preserve curated instructions: use a new output filename for an unmarked guide instead of `--replace`.

## Other copies

Search only expected workspaces and reference roots for `repoindex.py`; compare versions, SHA-256 and local diffs with `~/repoindex/repoindex.py`. Do not overwrite a modified copy. Prefer calling the canonical script by its full path. Where a standalone copy is required, update it only after review and verify its hash, then refresh that tree's database explicitly. Database updates and script updates are separate operations. Do not scan every dump on agent startup.

The current tool does not implement incremental indexing or an atomic transaction across every generated output. A successful script copy is not evidence that indexes were refreshed. Keep exact command, source revision, root/exclusions and completion result with any new scan record; do not publish private path inventories.
