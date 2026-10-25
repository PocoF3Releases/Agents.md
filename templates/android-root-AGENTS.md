# Alioth Android source workspace

Use the project workhub for shared instructions and current state:
`~/project-knowledge/AGENTS.md`, then `~/project-knowledge/CURRENT_STATE.md`
and only the topic relevant to the request. If unavailable, retrieve those files
from https://github.com/PocoF3Releases/Agents.md; do not assume old chat context.

Preserve unrelated edits. Use user builds; full ROM builds/flashing/history rewrites
require applicable authorization. Root is for research; final fixes are source-based.
Keep hardware/xiaomi standalone. Camera is finalized unless explicitly reopened.

For historical Android/Qualcomm reference searches, use the ready bundles in
`~/references_code` and its `scripts/refsearch.py`: both trees by default, or
`--tree`/`--scope` with bounded output. Restore the cache automatically; do not
reindex at chat startup. See the workhub's `operations/repoindex.md`.
`impl` searches stored .cpp/.cc bodies; `source` reads bounded indexed ranges.
Use rg for live edits, regex or other languages. The full generated census is optional reference,
not startup instructions; regenerate to INDEX_GUIDE.md or STRUCTURE.md, never over
curated AGENTS.md. Follow target-repository instructions when editing its files.
