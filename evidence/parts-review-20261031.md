# XiaomiParts review fixes — 2026-10-31

## Feature-separated corrections

- [HBM recovery](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/1fd464647f031e59e398316e81cda72a1780e86c): failed enable previously ignored disable-rollback failure and discarded the saved brightness. Reuse the disable transaction, retain the backup on either failed rollback step, and request disable for later recovery. A failed enable write may have partially reached sysfs, so it also triggers rollback.
- [Refresh retries](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/0115aef7a5e87c5e92880932751bba6e490ba386): cache a foreground package only after successful settings application. A nullable cache distinguishes failed/default work from a successfully applied empty foreground. Bound retries to three delayed attempts, cover screen-off/default restore, and cancel work during destruction.
- [Custom EQ draft recovery](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/fb71ef55883095a668a3b042802079c715e13da6): a rejected asynchronous edit now invalidates the slider draft even when its saved gain never changes. Preserve the existing failure toast, native EQ/preset contract and other settings callbacks.
- [Separate translations](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/381d2673a31a65b3a74fbc1c3a3762bf85de0212): add the four new custom-EQ text strings in 92 non-English locale folders. All 93 non-English folders now cover them; four English regional folders inherit English defaults. Russian is unchanged. The numeric dB format remains shared, with the existing Russian override retained. Translations are AI-assisted; native-speaker review is not claimed.

## Verification and limits

The review reproduced the HBM backup deletion and refresh failure-cache defect using unchanged production code and fault-injected boundaries. The final DisplayUtils passes eight scenarios: failed HBM disable rollback, failed brightness restoration, later restore, backlight failure, partial enable failure, pre-write failure, normal enable/disable and preservation of an existing backup/no-backup behavior. The full final RefreshService is compiled against private Android stubs; tests cover retry success, its attempt bound, successful package caching, teardown, empty foreground and screen-off restoration.

An extracted UI callback test verifies deferred failure revision, unchanged saved gain, successful editing and existing trailing-lambda call sites. The slider remember key includes the reset revision. This is not a rendered Compose or device test.

All Parts Kotlin sources compile in an isolated invocation using the checkout Kotlin/Compose compiler and existing module dependency classpath. Private R symbols supplement the older generated resource symbols for type checking; this does not verify resource linking, packaging, signing or installed inclusion. Existing deprecation/JDK tooling warnings are retained, not suppressed. AAPT2 separately compiles both res and Translations roots. XML, duplicate-key, new argument-placeholder and Git whitespace checks pass. No APK build, installclean, full ROM build, flash or device operation was performed; the prior APK build deferral remains in force.

Private fixtures/compiler output remain under ~/evo/.repo/parts-review-20261031, outside production repositories. No test code or temporary resources enter the four public commits.

## Publication boundary

The local tree includes the native recovery overlay. Only the four new Parts commits were cherry-picked onto public aosp-17, based on 2d5064c413a96343b40ca1501ab27b7978f2dbcd. The public and tested local Parts trees are identical; the public cumulative diff touches only Parts. Upstream/previous Claude authorship is unchanged. Public and local full-tree heads differ intentionally; see the source ledger.
