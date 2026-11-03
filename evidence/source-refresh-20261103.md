# ROM and maintained-fork refresh — 2026-11-03

`source-checked`, `host-tested`, `build-tested` (component scope).

## Source integration

Completed network sync with `repo sync -n --current-branch --no-tags -j50`,
then local checkout with `repo sync -l -d -j50`, across 1,265 projects.
Retained the Android 17 user product and existing build output.
ROM updates include Settings, Evolver, framework/native, Lineage device-settings
resources and other manifest-selected applications.

Fetched all 43 maintained build forks and their 40 selected upstream mappings.
Rebased three published branches while retaining imported authorship:

- [frameworks/base](https://github.com/PocoF3Releases/frameworks_base/commit/91855f5c732fbf5318df9c778e696b2a2289e2fc):
  replayed nine unique feature patches on the current Evolution X base. Dropped
  the now-upstream ColorOS callback import; retained recording/blur controls,
  thermal listener registration, NFC shell dispatch, vendor camera opt-in,
  torch recovery and USB gadget lifecycle handling. Removed the unreferenced
  root-level saved mail patch in a separate cleanup commit.
- [hardware/xiaomi](https://github.com/PocoF3Releases/hardware_xiaomi/commit/fff3348c2d9837ad278e8e701b638022f35a6028):
  imported the upstream eSIM translation update; all 85 existing patches remain
  patch-equivalent, including Dolby, DSPVolume, fingerprint, sensors and haptics.
- [NXP NFC](https://github.com/PocoF3Releases/android_hardware_nxp_nfc/commit/2ef0542a86ac3b12c13b8281e3b01816202a15a4):
  integrated upstream unsupported-firmware feature handling and preserved the
  client-queue teardown correction without overlapping behavior changes.

No speculative feature deletion or warning suppression was added.

## Recovery and local work

All four authored recovery mail patches reapply to the selected ROM branches;
postflight reports zero pending patches. The canonical manifest/runner/series
and patch bytes remain unchanged. No recovery-only patch was pushed into a
ROM-only branch, and no dependency override was dropped merely for a small delta.

Private root-level agent guidance is locally excluded from Git status, not
removed or shipped as product source. The unmodified preflight passes and still
rejects an unrelated untracked source file. Existing unrelated Workhub edits
were preserved outside this isolated publication worktree.

An unfinished WLAN candidate was preserved byte-for-byte in a separate local
worktree before sync. It is excluded from the active build tree and publication.

## Kernel intake held

The kernel remains at the previously published
[Redline head](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/d5936f1e0ba3a1fbb2cc22ab3540cfb56788d38c).
A separate upstream intake candidate and script-generated config changes are
unpublished: required regression work was platform-blocked. The dependent
kernel build was stopped; it is not a passing build or verified new release.
Do not retry the restricted operation through another route. No kernel ABI,
thermal policy or compression default change was shipped by this refresh.

## Verification and limits

The user-product component build passed (exit 0):

```sh
. build/envsetup.sh
lunch lineage_alioth-cp2a-user
m -j2 nothing SystemUIGoogle XiaomiParts XiaomiDolby android.hardware.nfc-service.nxp
```

SystemUI, Parts and Dolby Kotlin/Java, NFC native compilation, packaging and
dexpreopt completed. Build time was 33m50s; Ninja reports 1,436 executed steps.
Existing toolchain/deprecation warnings remain; this is not a warning-free build.
Built APK/NFC artifact hashes are retained in the private refresh receipt.
All 75 Workhub checks pass; they validate documentation structure and local
fixtures, not hardware behavior.

Range comparison preserves every retained feature patch. Recovery replay,
clean source state, raw Codex trailers and source/remote identities were checked.
No full ROM build, installclean, image installation or device test was performed.
Prior phone evidence remains attached to its original artifacts; neither this
refresh nor component compilation establishes a newly flashed release.
