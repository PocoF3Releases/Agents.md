# Targeted audio and fingerprint regressions

2026-10-24 — source/build/host/device-tested; temporary deployment on Alioth.

## Fixes

- [Audio 68c704a](https://github.com/PocoF3Releases-Recovery/android_hardware_interfaces/commit/68c704a2ceed7973793fa0a015d6af472f821073): guard six modern output callback fields before inspecting a legacy C device layout. Actual stock primary API is `0x300` (3.0); the original dual-mono getter jumped through private state to address zero. Modern callback dispatch remains available for API3.2+. HIDL stays6.0.
- [Fingerprint c8efa74](https://github.com/PocoF3Releases/hardware_xiaomi/commit/c8efa74f359339c741e0ea6decf98b198c050532): complete an empty enrollment-removal list once without invoking a legacy remove-all operation. Nonempty dispatch remains unchanged in both backend variants.

The audio source is in the currently manifest-tracked shared interfaces fork; its commit changes only audio, separately from recovery patches. Both commits are published on `cnb`.

## Validation

Both audio wrapper ABIs and the fingerprint service built incrementally. Private host fixtures compile actual production method bodies: legacy guard-page audio access and empty fingerprint completion fail against original source and pass with the fixes. Fingerprint covers both IMPL variants; audio covers old layouts, modern null callbacks and implemented modern callbacks.

On the phone, exact built binaries were temporarily bind-mounted, leaving stock primary audio and vendor partitions unchanged. Audio checks exercise dual mono, audio-description mix and playback rate on advertised48kHz FAST, DEEP_BUFFER and MMAP primary profiles. Optional unsupported calls complete safely; this does not demonstrate those optional DSP features.

| Mode | Audio | Fingerprint |
| --- | --- | --- |
| Permissive diagnostic | 36/36 across both client ABIs, two repetitions | 20/20 session contract checks |
| Enforcing | 18/18 across both client ABIs | 20/20 session contract checks |

Both HAL process IDs stayed unchanged throughout the enforcing checks. Initial temporary fingerprint staging inherited userdata's `nosuid` flag and blocked init's domain transition; correcting only that bind mount's flag allowed normal enforcing startup. No SELinux rules were changed.

## Restoration and limits

All temporary mounts were removed; all three original binary hashes were rechecked. Both original HAL services are running, SELinux is enforcing, and `ro.debuggable`/`service.adb.root` are0. The fixes are built/published, not permanently installed or packaged in a newly flashed ROM.

These checks do not establish acoustic quality, physical fingerprint enrollment/authentication, endpoint-dependent Bluetooth/USB audio, or complete HAL conformance. Camera/USB findings remain separate unresolved investigations. Radio/call/SMS/SIM tests are excluded. Full Android17 VTS completion is not the release gate: select tests by actual interface, capabilities and end-to-end results.
