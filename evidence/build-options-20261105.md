# Mini GMS and snapshot rollback — November 5, 2026

History note: commit links may use verified same-tree aliases. Literal logs,
versions and recorded source IDs retain their original observed values; current
routing belongs in [the source ledger](../state/repositories.yaml).

The maintainer selected the ROM's existing mini preset, retaining full Google
Search and Pixel Launcher rather than pico's separate Google Go application.
No custom GMS bundle or new GMS fork was introduced.

## Product selection

Alioth sets TARGET_USES_MINI_GAPPS=true before inheriting common_full_phone.
Resolved configuration keeps WITH_GMS=true and the Google communications suite.
Full Velvet, NexusLauncherRelease, Play Store, Google Services Framework, the
GMS APEX and its modules, both setup wizards, restore, Chrome/WebView/Trichrome,
Gboard, contacts, dialer and Messages remain. Quick Tap remains enabled.

The completed graph selects all 21 checked required app/APEX paths. In mini,
GooglePackageInstaller is absent and the AOSP PackageInstaller remains selected;
normal package installation is not removed. Pico was not chosen because its
Search Lite package does not establish full Pixel search/feed integration.

Compared with full, 35 package requests disappear and the mini personalization
variant replaces the full Pixel 2026 variant. Exclusions include Photos, Gemini,
Pixel Weather, Pixel live wallpapers, ARCore, Pixel cross-device extras, Google
VPN and several optional accessibility/telemetry apps. Mini defaults stock
ARCore and live wallpapers off. This is the supported mini preset, not a strict
core-services-only bundle: Calendar, Files, Wellbeing and some wallpaper/Pixel
integrations remain by design.

The removed full-only and default-disabled groups account for about 767 MiB of
files in the previous installed manifests. Mini adds an approximately 79 MiB
source personalization APK. These are descriptive uncompressed inputs, not net
filesystem or OTA ZIP savings; compiled dependencies and compression differ.
Measure the new ZIP after rebuilding.

## LZ4 feature withdrawn

At the maintainer's request, removed the recent SM8250 LZ4 snapshot configuration
and full-OTA target-codec opt-in. The addition/removal commit pairs were dropped from published history. The rollback matched the pre-feature content at that verification point.
The [later audio cleanup](dolby-history-cleanup-20261105.md) changes only separate
packaging/fixup details; snapshot selection remains as described here. Virtual A/B, vendor-ramdisk support and independent COW v2 remain.
Compression/method and PRODUCT_OTA_FULL_USE_TARGET_VABC resolve unset; only the
existing ro.virtual_ab.enabled property remains from these snapshot selections.

The enhanced native recovery, kernel compression and upstream codec support are
unchanged. The four authored recovery patches reapply with zero pending entries.
Snapshot compression affects snapshot storage, not downloaded-payload compression;
this removal is a product choice, not a demonstrated bootloop fix.

## Current public commits

- [device/xiaomi/alioth: f7a82eadfef6](https://github.com/PocoF3Releases/device_xiaomi_alioth/commit/694d770254f8233d7c75752a228852dc702acfa9).
- [device/xiaomi/sm8250-common: 6fed13f4da77](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/2838130a6fa07154b16468ecc4bc06e7c77dd745).
- [build/make: 862350971ca3](https://github.com/PocoF3Releases-Recovery/android_build/commit/0acbb8a58c0514bb4c64e754037bd5936db7cd96).

## Verification and limits

All full/mini/pico product comparisons resolved successfully. Final actual
source selects mini without environment overrides. The complete
lineage_alioth-cp2a-user Soong/Make graph passes (m -j8 nothing). The generated
installation closure retains the 21 required targets and excludes the runtime
paths of all 35 removed modules. Source whitespace and restored Python syntax
checks pass; exact graph-tested active trees are preserved across publication.

Six focused existing OTA checks pass; one dynamic-partition partial-update check
requires unavailable external tools and is skipped. A broader host suite had an
unrelated existing Python 3.14 assertRaisesRegexp failure; no compatibility shim
or test suppression was introduced. No full ROM rebuild, new OTA size measurement,
installation or device test was performed for this configuration.

The [LZ4 experiment](source-refresh-20261105.md#lz4-snapshot-configuration)
is absent from current branch history. The [prebuilt cleanup](prebuilt-cleanup-20261105.md) remains intact.
Private selection, install-list and graph/test receipts remain under
`~/evo/.repo/gms-minimal-20261105/`.
