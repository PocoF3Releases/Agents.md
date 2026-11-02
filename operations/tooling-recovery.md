# Recover from tooling failures

Use this when host tools, transport or approval failures interrupt development.
First recover the current user goal and owner through the supported chat tools
and [continuity protocol](continuity.md). Preserve running operations, dirty
work and original source/artifact/test identities. A saved next step may lag
newer receipts: verify completion before rebuilding, packaging or publishing.

## Bound diagnosis and retries

- Record the exact operation, error and outcome: denied, pending, failed or
  uncertain. A timeout/disconnection does not prove the operation never ran;
  check its actual result before retrying. Checkpoint these states privately.
- Inspect only relevant bounded diagnostics. A program name, feature metadata
  or nearby warning does not establish a kernel defect or a rejection cause.
  Keep host/harness failures separate from source/build/device failures.
- Stop identical retries without materially new relevant evidence. After a
  denial, check trusted user history; retry the denied operation only once per
  new relevant evidence and only when known not to have executed. Preserve the
  exact block when handing off. Do not vary executors, wrappers, credentials or
  payloads to evade the restriction, disable protections or patch installed tools.
- Use a supported alternative only when it respects the same access boundary.
  Do not restart the host/chat, kill builds or create competing owners merely
  because a status request is pending. Steer an active owner at a safe boundary.
- Park optional blocked diagnostics and continue independent authorized fixes.
  If required acceptance is blocked, report that limit; never call it passed,
  suppress checks or publish an unverified fix as verified.

## Alioth boundary

The [recorded Daybreak notice](../evidence/kernel-contract-plan-20261102.md#paused-task-and-tooling-limitation)
had no exact reason code or rejected-operation identity. Feature metadata and
separate stream-disconnection warnings did not establish causality. Preserve the
paused touch-ioctl reproduction; workflow recovery does not reopen it. Do not
reproduce restricted probes merely to diagnose the tooling notice. Continue the
current authorized kernel/HAL/device goal with its existing security and device
boundaries. Keep private chat/logs out of public Git.
