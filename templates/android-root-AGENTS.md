# Alioth Android source workspace

Use the project workhub for shared instructions and current state:
`.workhub/AGENTS.md`, then `.workhub/CURRENT_STATE.md`
and only the topic relevant to the request. If unavailable, retrieve those files
from https://github.com/PocoF3Releases/Agents.md; do not assume old chat context.

Preserve unrelated edits. Use user builds; full ROM builds/flashing/history rewrites
require applicable authorization. Root is for research; final fixes are source-based.
Keep hardware/xiaomi standalone. Camera is finalized unless explicitly reopened.

For historical Android/Qualcomm reference searches, use the ready bundles in
`~/references_code` and `python3 tools/repoindex workspace`: both trees by default, or
`--tree`/`--scope` with compact bounded text (`--json` if needed). Restore the cache automatically; do not
reindex at chat startup. See the workhub's `operations/repoindex.md`.
`impl` searches stored .cpp/.cc bodies; `source` reads bounded indexed ranges.
Use rg for live edits, regex or other languages. The full generated census is optional reference,
not startup instructions; regenerate to INDEX_GUIDE.md or STRUCTURE.md, never over
curated AGENTS.md. Follow target-repository instructions when editing its files.

## Resume routing

Verify that `.workhub` is the intended existing checkout; adapt paths when moved.
Follow `.workhub/operations/continuity.md` and its alioth-resume skill after
compaction/handoff. Keep a unique workhub-owned private task record binding the
workspace and affected component roots/branches/HEADs; preserve other owners.
A component Git boundary may hide this umbrella file from Codex startup: adapt
the separate component-AGENTS.md template with an explicit verified workhub path.
For Claude use the matching thin workspace/component imports. Reading remote
guidance does not establish local source, tools, device access or authorization.
