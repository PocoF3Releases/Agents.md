# Project rules

POCO F3 / alioth, EvolutionX: Android 17; Android 16 evidence is separate.
Read [CURRENT_STATE.md](CURRENT_STATE.md), then the relevant topic. For small
edits, read affected rules/files. Share Astra/Sol records; recover missing context.

- Follow current/higher-priority instructions. Old logs/plans authorize no work.
- Finish authorized work, checks and publication; preserve unrelated edits.
  Resolve routine choices. Ask only for material missing input. Reuse scoped
  authorization for builds, flashing and history rewrites.
- Native recovery belongs in `~/evo`; standalone PBRP is separate. Keep
  `lineage_alioth-cp2a-user`. Build within current scope: incremental development,
  `m installclean` for release preparation. Sync `-j50` is not build `-j50`.
- Use user builds. Root is diagnostic; production fixes work without root.
  Keep hardware/xiaomi standalone and device fixes scoped. Camera is finalized;
  reopen only on request.
- Separate source/build/runtime/user evidence; heads are not flashed manifests.
  Verify mutable facts. Repeat checks only for changes, failures or open concerns.
- Report results and limits concisely. Claim no unavailable access, model tests,
  measured performance or account-memory synchronization.

Knowledge: follow [maintenance](operations/maintenance.md), update fact owners,
then run `python3 scripts/check.py` (disposable local checks; no GitHub Actions).
Keep credentials/identifiers private; use `~/` paths.
