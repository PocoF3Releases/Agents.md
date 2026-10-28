# Android 17 source refresh — October 24, 2026

This records source preparation, not a new ROM release or device acceptance.

- Fetched the selected Evolution X manifest and all ROM projects with repo -j50,
  then completed the checkout sync. No tracked local edits blocked the update.
- Checked 43 maintained build repositories against their selected Evolution X,
  LineageOS or manifest-pinned AOSP upstreams. Already-current repositories were
  retained without artificial update commits.
- Rebased the recovery libselinux Rust-binding addition on the new upstream
  public-policy type-transition fix. Range-diff confirms the recovery patch's
  payload and original authorship are preserved.
  [Published SELinux integration](https://github.com/PocoF3Releases-Recovery/android_external_selinux/commit/1bf27a46b9da80724eb23eeb213b3b6b02002c57).
- Reapplied the four authored recovery patches: one framework patch, one Alioth
  patch and two common-device patches. Their shared ROM forks remain free of the
  recovery-only additions; the authored series lives in the
  [recovery integration repository](https://github.com/PocoF3Releases-Recovery/local_manifests/tree/cnb).
- Installed the complete post-sync patch runner and series beside the existing
  local ROM overrides. Idempotent preflight reports zero pending patches.
- Kept the latest published kernel hardening and regeneration policy. No kernel
  upstream movement required another defconfig change.
- Removed obsolete platform guidance, source-map branches, routing references and
  the retired profile catalogue. Current development instructions target Android 17.
- Kept the output directory without manual cleanup and preserved unrelated local workhub edits. Private keys
  and decompiled development repositories were not modified.

## Verification

Source sync, patch preflight and range-diff passed. The production target `lineage_alioth-cp2a-user` and `m -j4 nothing`
build-graph check passed. The focused `version_policy`, `libselinux` and
`sepolicy.recovery` build passed. A public-policy fixture containing ordinary
and named type transitions, typechange and typemember fails with the saved prior
tool and passes with the rebuilt tool, preserving the expected versioned types.
All 43 selected published fork heads were checked against the final checkouts;
the three shared ROM checkouts include the explicitly recorded local overlay.

[Current maintained source identities](../state/repositories.yaml) distinguish
published fork heads from locally applied recovery patches. Previous phone tests
retain their original revision/build scope; no flash, wipe, installclean or full
ROM build was performed for this source refresh.
