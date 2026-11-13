# Co-author and source-integrity recheck — 2026-10-31

`source-checked`, `metadata-verified`, `GitHub-API-verified`. No source-code,
translation, defconfig, build or device changes in this recheck.

## Findings and correction

The earlier normalization changed four Codex-attributed commits that were
already shared with EvolutionX: three AC-4 table commits in frameworks/av and
one HBM opt-in commit in frameworks/base. Source content was unchanged, but
rewriting their IDs broke exact upstream ancestry and made GitHub show these
forks as behind. Restored the exact upstream commits and replayed only fork-local
metadata changes. Valid upstream trailers retain their original formatting.

| Fork | Final public tip | GitHub comparison to EvolutionX cnb |
| --- | --- | --- |
| `frameworks/av` | `0c471ea794d999884744c0843c73a70320ed44d1` | 4 ahead, 0 behind |
| `frameworks/base` | `f154e5aa0c5001385be9bf37e28246bac697a0ac` | 8 ahead, 0 behind |

Freshly fetched the selected upstream branches for all 40 non-standalone
maintained build forks. These two were the only ancestry mismatches; both are
fixed and pushed with exact expected-head leases. The other three build forks
are standalone. The main-ROM hardware/interfaces fork remains distinct from
the recovery-selected fork.

## Attribution and preservation

- Refetched and checked all 56 recorded repository/branch tips, including
  the workhub and GitLab camera.
- GitHub GraphQL `Commit.authors` recognizes user `codex` with
  `noreply@openai.com` on all 1,126 existing matching commits in the checked
  branches, including the four restored upstream commits. No failures.
  This checks GitHub’s attribution data directly, rather than inferring it
  from message formatting. The new workhub evidence commit is checked separately
  after publication.
- Rechecked all 1,580 mapped original commits: tree and original author/committer
  fields/dates match; non-Codex message text is preserved; parent counts match.
  Every mapped commit remains reachable on the final branch. No feature commits
  were dropped or combined.
- All 55 non-workhub branch-tip trees and commit counts match the saved originals.
  The workhub contains the explicit documentation/ledger updates only.
- All 1,265 source-project worktrees are clean. Local framework/device recovery
  overlays remain separate from ROM public branches.

## Manifests and future replay

The seven deployed recovery XML/runner/series/patch files match the current
canonical local-manifests checkout byte-for-byte, with matching patch SHA-256s.
All 43 maintained effective manifest entries select the expected repository and
branch; all six build/make linkfiles and the envsetup link remain correct.

Applied the four recovery patches to the freshly fetched public tips using
temporary private Git indexes. Each resulting tree exactly equals its actual
local framework/device checkout. The normal runner also reports zero pending
patches on all three paths. Thus a sync followed by the documented patch runner
reproduces the current recovery integration without pushing overlays to ROM refs.

The previous `lineage_alioth-cp2a-user` build-graph check and minui regression
remain applicable to identical source trees. A full ROM compile, packaging and
device verification are still pending the user’s rebuild. Generated SCM/version
identifiers naturally use the new commit IDs. No installclean or new build ran.

Private diagnostic maps/results are under
`~/evo/.repo/coauthor-recheck-20261031/`. The maintained repository ledger records
the repaired public tips and current local recovery-overlay HEADs.
