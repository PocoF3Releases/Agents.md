# repoindex 1.1.0 upgrade

## Canonical source

[Repository](https://github.com/johnmart19/repoindex), branch `main`, commit [c79c1508c3c7f2657ddaf0172e89b279f9ce4914](https://github.com/johnmart19/repoindex/commit/c79c1508c3c7f2657ddaf0172e89b279f9ce4914). This is external development tooling, not a PocoF3Releases ROM dependency or release feature.

The local checkout was `~/repoindex`. Its original master commit matched remote main; origin/main was configured without rewriting history. Identical original script copies at `~/evo17/repoindex.py` and `~/references_code/repoindex.py` were synchronized after verifying their old SHA256. Existing indexes and AGENTS.md guides were not regenerated or changed.

## Problems addressed

- Read-only queries previously opened a schema-writing connection, potentially modifying an invalid database. They now use SQLite read-only mode and validate schema/completed-scan metadata.
- `agentsmd` previously started indexing automatically when the index was missing. Scanning now requires an explicit `index` or `agentsmd --reindex` request.
- Compact generation previously loaded all file paths before discarding the full report. It now uses aggregate queries and returns before full inventory materialization.
- Full guides overwhelmed agent context. Compact navigation is now the default; detailed inventory requires `--full`.
- Regeneration overwrote curated instructions. Outputs now use `<!-- repoindex:begin -->` and `<!-- repoindex:end -->`; only that block is regenerated. Unmarked files are refused unless explicitly replaced. Aliases are preflighted before writes, with atomic replacement of each individual output.
- File symlinks and special headers are not parsed, avoiding external target reads and FIFO blocking in the scanner. Direct duplicate hashing skips nonregular entries. Database exclusion now matches only the exact database and SQLite journal filenames, preserving similarly named source files.
- Scan errors, exclusions and symbol mode are stored. `status --json` exposes these without a tree scan; older schema-2 coverage fields are unknown rather than assumed complete. Writer errors are no longer swallowed as worker failures.
- Guide dates identify the stored scan date, not report-generation time. `--version` identifies copies; the nonfunctional `gitignore` filename was corrected to `.gitignore`.

## Safe usage and migration

```sh
python3 repoindex.py --version
python3 repoindex.py status --root /path/to/tree --json
python3 repoindex.py agentsmd /path/to/tree --out /path/to/tree/INDEX_GUIDE.md
# Detailed inventory only when needed:
python3 repoindex.py agentsmd /path/to/tree --full --out /path/to/tree/STRUCTURE.md
# Explicit scan only when authorized/needed:
python3 repoindex.py index /path/to/tree --ignore out
```

For old unmarked AGENTS.md files, prefer a new output path. Preserve curated instructions before choosing `--replace`. Put durable instructions outside generated markers; TODO text inside the block is regenerated. `--also` requires `--out`; `--key-files` requires `--full`.

A copied compatible SQLite snapshot supports indexed queries using `--db` without the original source tree. Source-reading commands such as `headers`, duplicate hashing and reindexing need actual files. Root-bound guide generation rejects a mismatched root. A GitHub-only reader can inspect source, tests and documentation but cannot query a local-only database; request a targeted export if necessary.

## Validation

20 fixture-based unittest regressions passed, covering read-only access, missing/invalid indexes, protected curated text and symlinks, aliases, compact/full modes, root mismatch, recorded errors, old metadata compatibility, dates and serial/parallel results. Python compilation and `git diff --check` passed.

A read-only `status --json` check against the existing Android index reported 1,751,834 files and 10,137,789 extracted symbols, snapshot date 2026-09-09, schema 2, coverage unknown. This was not a new full scan, performance benchmark or verification of current tree freshness. No ROM build ran.

## Limits

Header parsing is heuristic, not compiler-complete. Incremental indexing is not implemented. An interrupted rebuild is not guaranteed to preserve the preceding database; back up expensive indexes before rebuilding. Multi-file output is not transactional as a group even though individual writes are atomic. File statistics reflect the recorded scan, not present runtime/device state.

Tests and implementation are available remotely in the canonical repository; local access is not necessary to review this upgrade. It does not change the Android release baseline or the finalized camera decision.
