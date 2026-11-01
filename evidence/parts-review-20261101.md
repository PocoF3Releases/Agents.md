# XiaomiParts Kotlin review — 2026-11-01

## Scope

Full read of the Parts Kotlin sources on the Nov 1 ROM base: application/boot
receiver, preferences and file helpers, thermal service/profiles/details, touch
profile and sampling, refresh service/utils, display (HBM, DC dimming), tiles,
Clear Speaker, MiSound (lifecycle, presets, custom EQ, tile), app list and
haptics. Thermal profiles map 13 unique states to sconfig values whose conf
files all exist in the stock dump. The 120 Hz refresh choice is a per-app
maximum, matching its summary text.

## Correction

[Refresh screens once on resume](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/84bd69b3e80eca03ce7d0b26efa99b4382232070):
`OnResume` called the refresh explicitly when the owner was already resumed,
although `addObserver` replays ON_RESUME. Each screen therefore read its
sysfs/service state twice on first composition. No other defect was found.

## Verification and limits

The XiaomiParts module was rebuilt and the APK bind-mounted (root, test only)
over the ROM system_ext APK. MiSound, Thermal, Refresh, Touch sampling and
Display opened with focus and no FATAL log; Display showed its saved DC/HBM
states on first open. An external DC write for a resume-refresh check was
refused by sysfs permissions, so that path is not device-verified. The mount
was removed, the ROM APK identity restored and the test files deleted. No ROM
build or flash was performed; the fix ships in the next ROM build.

## Publication boundary

Cherry-picked alone onto public aosp-17 b53a218; patch-id matches local commit
c3e71a0, which sits on the recovery overlay. Public and local full-tree heads
differ intentionally; see the source ledger.
