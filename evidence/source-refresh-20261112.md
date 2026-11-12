# ROM refresh and recording blur — November 12, 2026

**Source/host checked; no Android build, installclean, flash or phone test.**

## Source refresh

`repo sync -n --current-branch --no-tags -j50` and
`repo sync -l -d -j50` completed for 1,265 projects. Twelve project HEADs changed; all tracked
trees are clean and the original untracked files remain. All pre-sync HEADs are
protected privately. One upstream PAL repository-name/object-store migration
needed a targeted force-sync after a verified bundle and metadata backup; its
original source and backup ref were retained.

Forty-four maintained ROM/native-recovery forks were checked: forty selected
upstreams are contained, and four standalone device/vendor sources have no
external replay base. Only frameworks/base needed upstream integration. The
separate main-organization hardware/interfaces branch is also current. No
empty rewrites were made to already-current repositories; private signing and
camera-development repositories were excluded.

[Published framework head](https://github.com/PocoF3Releases/frameworks_base/commit/53e0061d824e3c6c571aebe95fb7bfa83258b3e6)
contains the latest selected
[EvoX base](https://github.com/Evolution-X/frameworks_base/commit/c51e18250230cba3de5708e8034ae3d3c92e26f4)
and eleven retained feature commits. Range-diff/patch IDs preserve ten unchanged
patches; only recording blur was adapted. All eleven author identities/dates
and existing trailers remain; translations and maximum-FPS recording stay
separate. GitHub recognizes Codex on the ten attributed commits. Publication
used an exact expected-head force-with-lease and its remote result was verified.

The [canonical recovery integration](https://github.com/PocoF3Releases-Recovery/local_manifests/tree/cnb)
is unchanged and matches the deployed runner/XML/mail-patch hashes. All four
patches preflighted, applied and passed the idempotent post-check: one framework
Keystore2 build overlay, one Alioth overlay and two common init/policy overlays.
They remain local, outside ROM-only public branches. Device-tree overlay trees
match their pre-sync source exactly. The kernel source did not change; earlier
kernel build/device results keep their original source identities.

## Recording blur

The new [EvoX dialog/toast blur](https://github.com/Evolution-X/frameworks_base/commit/e7e2a67a773cd030e439a4c243ff56fdf204358a)
uses cross-window listeners. The old recording flag did not notify those
consumers; the shared animation helper could retain its radius/early wakeup,
and legacy shade cleanup was gated on unrelated feature flags.

The [consolidated recording-blur implementation](https://github.com/PocoF3Releases/frameworks_base/commit/c26c5983f985010b9a6dc9fd7979da4fe7ee33ad)
adds process-local suppression to the existing hidden cross-window helper and
connects it to the common recording state. Live/late dialog, toast and transition
consumers receive the effective state. User settings and the current underlying
WindowManager state are preserved for restoration; other processes are unchanged.
Animation/shade cleanup writes zero for owned blur and balances early wakeups,
including a cancelled prepare with no applied radius. Keep blur effects,
device opt-in and failed-recording recovery remain independent of maximum FPS.

### Final restoration recheck

Two further defects were reproduced against the earlier implementation. Service
disconnection skipped the stopped-controller update when its Binder was null;
transport exceptions could also terminate the lifecycle observer. Dream/transition
callers that kept requesting nonzero blur could leave a previous radius applied.

The final implementation dispatches stopped state independently of a live Binder,
uses the existing `safeBinderCall` for start/update/stop, and drops only failed
connections. Successful stops retain their binding until asynchronous saving
finishes. The shade helper caches effective support and normalizes forbidden
nonzero requests to zero, including early-wakeup cleanup. Normal rendering,
opacity/scale, persistent wakeup ownership and saved preferences are preserved.

## Verification and limits

- Actual Java listener/Kotlin recording-state host harness: **10/10 pass**,
  compared with six relevant before-code failures.
- Actual shared-animation Kotlin helper plus extracted legacy cleanup predicate:
  **10/10 pass**, compared with six relevant before-code failures. Cases cover
  backend/settings changes, suppression/restoration, queued/direct listeners,
  re-entry, new surfaces, invalid targets, opacity and early-wakeup balance.
- Final actual repository/controller/state/core lifecycle harness: **20/20 pass**
  with real coroutines on Unconfined and Default dispatchers. Covers disconnect,
  start/update/stop transport failures, the next recording, retained save binding,
  Keep blur, device opt-out, the latest preference and countdown cancellation.
  The frozen old repository failed eight of twelve targeted cases.
- Full actual shade helper: **10/10 pass**, compared with six old-code failures;
  covers nonzero requests during suppression, backend changes and wakeup ownership.
- Actual dialog/toast controller: **6/6 pass** for existing/late-created windows,
  copied renderers, latest settings/radius/backend state and detach cleanup.
- All **56 focused host cases** pass. Android transport/view/surface plumbing is
  stubbed; this is not device rendering acceptance. Source copies/hashes match
  the final folded implementation; independent correctness/architecture review
  found no blockers. Diff/author/trailer and
  source-selection checks pass. The existing checkout-built `aidl_hash_tool`
  accepts the current frozen DuckRKP AIDL API/hash.

Android/SystemUI integration compilation, actual rendering and recording
performance remain for the maintainer's rebuild/device check. Existing in-window
`RenderEffect` source blur is unchanged; poll-only vendor consumers observe the
policy on their next apply. This is not a blanket disable of every app/content
blur. No new setting, global blur override, vendor fork or hidden root dependency
was added. Parked investigations remain parked. Raw host fixtures, source/ref
receipts and logs remain private; this record is the portable summary.
