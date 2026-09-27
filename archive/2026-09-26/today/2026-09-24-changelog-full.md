# POCO F3 (alioth) — Evolution X
Android 17 | Evolution X v12.2

Draft: September 24 work only, after the published September 23 release. Final build metadata and package inclusion remain to be supplied.

## Dolby / Audio
- Fixed Dolby AC-4 decoder initialization and its required helper-library loading.
- Confirmed AC-4 stereo playback on the rebuilt device, including audible sound.

## XiaomiParts
- Fixed Thermal Profiles list content overlapping the dialog title and Cancel area.
- Corrected dialog spacing without the previous oversized footer gap.
- Confirmed working as intended by the maintainer.

## Maintainer-only scope

These are two final functional fixes, not a new Dolby or XiaomiParts overhaul. AC-4 validation covers the tested stereo/48 kHz sample, not every stream or offload route. Parts acceptance is user-confirmed with a System Profile screenshot.

Camera 4K60/ultrawide guards, startup cleanup, audio routes, charging ownership, kernel logging/WiGig/LHBM and USB/NFC fixes were already in the September 23 changelog and are excluded. Existing September 22 features are also excluded.

libmeminfo log suppression received validation/commit preparation today but was implemented earlier; it is tracked as an optional unannounced maintenance item, not a newly implemented today-only feature. Framework opt-in refactoring and documentation/history work are maintenance, not new Alioth functionality.

Do not invent a release date, ZIP/hash, upstream ROM changes or installation requirements. Confirm inclusion before publishing.
