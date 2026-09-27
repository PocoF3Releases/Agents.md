# Repository baseline and documentation refresh — 2026-09-24

## Verified source state

All 17 local build/profile checkouts mapped to the public PocoF3Releases repositories now use their GitHub default branch and exact fetched head. The reference-only repository was inventoried remotely, not checked out or modified. The public organization inventory contains 18 repositories; Agents.md remains accessible as a separate maintenance repository despite not appearing in that public listing. Current branches and full SHAs are in `memory/repositories/LATEST_COMMITS.json` and `TRACKED_HEADS.yaml`.

- Kernel `kernel/xiaomi/sm8250` now uses `aosp-17`, tracking `origin/aosp-17`, at `10f8a106de65`. It is no longer checked out on `beta`.
- Platform defaults retain their actual names (`cnb`, NFC `lineage-24.0`, libmeminfo `alioth-dmabuf-fallback`); do not rename them to aosp-17 merely because the ROM targets Android 17.
- libmeminfo moved from local `d3872e43f685` to organization head `f0f3040dbe74`. frameworks/av is aligned at `8fc27178f6fa`.
- Detached platform/HAL checkouts were attached to the matching default branch; all inspected working trees were clean.
- Replaced HEADs/local branch tips were preserved under local `refs/backup/pre-org-alignment/<timestamp>/head` or `/branch`. These are recovery references, not build branches.
- Obsolete remote branch references were pruned in device/vendor/kernel/Xiaomi hardware checkouts. Historical local kernel `aosp-16`, `candidate/alioth-cycle-count-fixes`, and vendor-camera `aosp-16` contain unique commits and were preserved. They are not current baselines.
- Alignment changed checkouts and tracking, not repo manifests. A later repo sync may detach HEAD or follow the manifest revision again; verify before further work.

## Alioth history cleanup

Removed `58d3a4249b4f03465e1d0d4b884e10244d4dbc12` (unused stock-derived Dolby leveler candidate) from branch history and replayed its 12 descendants. The only final file difference was deletion of `configs/dolby/dax-default.xml`. Current alioth head is `2bf9bcd13a086f85b97ec4ac507bb212b499ee7d`; old descendant SHAs are historical. Pushed with an explicit force-with-lease.

## Camera delivery and documentation

Both `device/xiaomi/camera` and `vendor/xiaomi/camera` are mandatory device-specific includes for the shipped MiuiCamera replacement, not optional add-ons.

- Device source head: `1335f9ada0a7` on GitHub `aosp-17`.
- Root README was simplified for ready-to-use prebuilt integration (`4fda21e`).
- `patches/README.md` documents all 24 patches, creation/implementation rationale, validation limitations and maintenance workflow (`1335f9a`). The `.patch` file filter means this README is not applied as a patch.
- GitLab vendor head remains `f13797ef3d93508756e06a4a185c9208dbc3ee88`, branch `aosp-17`.
- APK SHA256 remains `29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4` (223517496 bytes).
- September 23 validation still applies: main 4K30/60 and ultrawide 1080p recorded; ultrawide 4K is guarded, not enabled; ultrawide UI 1080p60 measured about 30 fps. No additional device validation occurred during this documentation/alignment session.

## Organization profile

`.github/main` now has one root commit `fa8c1d1bf33041f51b510d04f470db12949db68e`, containing the latest profile and WebP banner. Prior profile history was replaced at the user's request. Two unused SVG assets were removed. The directory lists the 18 public repositories, actual default branches, and separately hosted GitLab camera prebuilts. Both camera trees are grouped with required device sources. Published using explicit force-with-lease.

## Boundaries and next step

No ROM/APK rebuild, device flash or runtime test was performed. Use `user`, never `userdebug`/`eng`. Source alignment is not device validation. Refresh remote refs and installed-device state before new implementation work; no source fix is pending from this checkpoint.
