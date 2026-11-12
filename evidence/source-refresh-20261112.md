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

[Published framework head](https://github.com/PocoF3Releases/frameworks_base/commit/2cb26cda17a41c8ad03aa9f1f14b40351268a1a6)
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

The [consolidated recording-blur implementation](https://github.com/PocoF3Releases/frameworks_base/commit/a3c7448a71a3ef716388adbb36f4cadaeabe0f89)
adds process-local suppression to the existing hidden cross-window helper and
connects it to the common recording state. Live/late dialog, toast and transition
consumers receive the effective state. User settings and the current underlying
WindowManager state are preserved for restoration; other processes are unchanged.
Animation/shade cleanup writes zero for owned blur and balances early wakeups,
including a cancelled prepare with no applied radius. Keep blur effects,
device opt-in and failed-recording recovery remain independent of maximum FPS.

## Verification and limits

- Actual Java listener/Kotlin recording-state host harness: **10/10 pass**,
  compared with six relevant before-code failures.
- Actual shared-animation Kotlin helper plus extracted legacy cleanup predicate:
  **10/10 pass**, compared with six relevant before-code failures. Cases cover
  backend/settings changes, suppression/restoration, queued/direct listeners,
  re-entry, new surfaces, invalid targets, opacity and early-wakeup balance.
- Source copies/hashes match the final folded implementation; independent
  correctness/architecture review found no blockers. Diff/author/trailer and
  source-selection checks pass. The existing checkout-built `aidl_hash_tool`
  accepts the current frozen DuckRKP AIDL API/hash.

Android/SystemUI integration compilation, actual rendering and recording
performance remain for the maintainer's rebuild/device check. Existing in-window
`RenderEffect` source blur is unchanged; poll-only vendor consumers observe the
policy on their next apply. This is not a blanket disable of every app/content
blur. No new setting, global blur override, vendor fork or hidden root dependency
was added. Parked investigations remain parked. Raw host fixtures, source/ref
receipts and logs remain private; this record is the portable summary.
