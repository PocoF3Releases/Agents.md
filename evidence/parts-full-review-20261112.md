# XiaomiParts full-topic review — November 12, 2026

Source-, host-, module- and temporarily device-tested. The audit covers shared UI,
MiSound, thermal/touch, display, refresh controls, Clear Speaker, integration and
localization. Existing icons, MiSound wordmark, saved-state contracts and legacy
QS aliases remain. No kernel, HAL, native library, policy or build dependency changed.

## Final source

ROM branch `aosp-17` contains six implementation topics and a separate translation
correction. Earlier approved implementations remain ancestors.

| Topic | Commit |
| --- | --- |
| Align shared controls with Settings | [333eaccc](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/333eaccc5d22f333d7c8d4b0cc027d0bc5425b1f) |
| Sample MiSound audio mode once | [8f61c586](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/8f61c5863ad27bff79fae6f2b3ea7ad3e522107f) |
| Keep refresh rules and tile state current | [323b02ab](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/323b02ab78d1b79925b18a89039cd0e5b2feecb2) |
| Recover foreground thermal assignments | [8dda1e53](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/8dda1e530a9f65353dafee7b4679cfb88d4f63ba) |
| Reconcile per-app touch tuning reliably | [1bc4bba8](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/1bc4bba8a6a3db7f84734e82bca2a1c3c07f90af) |
| Stop speaker cleaning on ducking focus | [07d95c74](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/07d95c7473132a2b9f2f52a96fb5c8c1c4ec78fb) |
| Correct device-control translations | [ff54c0c0](https://github.com/PocoF3Releases/device_xiaomi_sm8250-common/commit/ff54c0c06f9219ad1cf44fed1d349cf9a7e2c69f) |

Two authored recovery overlays remain local, outside the ROM ref. Their patch
bytes, author/committer metadata and messages were preserved when reparented.
Their unpushed object IDs are tracked privately, rather than linked as public objects.
The public and local Parts subtrees match the tested files exactly.

## Demonstrated defects and retained contracts

- Shared UI now follows current Settings 20 dp outer/4 dp inner group corners.
  Titles update the Activity and expose headings; populated search keeps its
  spoken purpose. RTL expansion arrows point down. Launcher icons reload for a
  new package/resume generation, without reloading on ordinary recomposition.
- MiSound samples audio mode once: two getters could falsely classify a
  RINGTONE-to-NORMAL transition as communication. Playback detection, effect
  recovery and persisted settings are retained.
- Refresh and thermal monitors handle gained task focus and bounded recovery
  after a failed focused-task query. The tile maps infinite limits to the highest
  supported rate and observes external changes only while listening; partial
  registration is cleaned up.
- Touch checks HAL success values, retries failed cleanup and restores owned
  tuning after process recreation. An Off profile skips its saved edge filter.
  Alioth reset group 0 restores modes 0–7, retaining orientation and gesture/power
  modes. Global sampling keeps ownership, including rotation races; presets
  still apply last. Legacy device dispatch is retained.
- Clear Speaker requests pause-on-duck so platform automatic ducking cannot
  suppress its existing stop callback. It retains call, route, visible-screen,
  timeout and error guards. See [AudioFocusRequest](https://developer.android.com/reference/android/media/AudioFocusRequest).
- Six Bosnian and seven Odia values were repaired. The displayed sensor weight
  sum is 939 in base and 88 translations; stock normalization 1000, compensation
  2169 and all policy values remain unchanged.

## Host and build evidence

The whole-controller tests reproduced old failures before checking candidates:
43 touch cases, 21 thermal-service groups, six thermal-formatting groups,
10 MiSound mode cases, 23 speaker cases and nine real Compose-runtime icon cases
pass. Refresh has combined focus/query/Infinity/listening/failure/teardown checks.
Boundary fakes are explicit; these do not certify physical firmware or acoustics.

Stock touch ELF mutators return 0 on success and negatives on failure. The selected
FocalTech source and six extracted native-driver assertions agree on reset/default,
preset and orientation semantics. All 26 thermal rows match decoded stock policy
fields; observed cooling-device ranges accommodate their targets. No speculative
DisplayFeature port or new display policy was justified.

Final `m -j4 XiaomiParts`, `lineage_alioth-cp2a-user`, passed. All 624 Parts input
files were unchanged during the build and match the published subtree. APK:
`e2c8c43712063d30b81b4528d45da45f7d9f7aa5da93107c68def067693f305e`,
7,451,692 bytes. Existing platform/HIDL deprecations remain warnings; no suppression
or dependency upgrade was added. No ROM/kernel build or firmware flash was run.

108 integration checks cover 17 components, five protected tiles, same-UID Settings
access, R8 entrypoints, resources and package/native dependencies. MiSound's 13
candidate native nodes and both 19-node Touch service/implementation closures have
no missing file/architecture dependency; this is distinct from runtime namespace,
DSP or physical-route proof. No unused resource or ProGuard deletion was warranted.

All 577 XML files/97 locale qualifiers pass structure, placeholder, escaping,
protected-brand/headset and duplicate checks. MiSound, Hi-Fi and all 24 headset
names remain non-translatable. Five numeric flags are valid language choices.

## Temporary phone acceptance

The exact signed APK was activated through supported staged installation and one
normal reboot: UID 1000, `devicesettings_app`, SELinux Enforcing. Ordinary persistent
app updates are rejected; no persistence/security flag was changed.

Twenty-five checks across six bounded flows passed:

| Flow | Observed result |
| --- | --- |
| Controlled profile | Conservative selector 11 and 60 Hz assignment applied; manual-zero after process recreation clears stale preset; Off leaves default edge; Home restores base policy/rates. |
| Global/rotation | Global sampling owns touch settings; per-app manual tuning replays after disabling it. Landscape rotation is applied and retained during cleanup; original rotation/global state restored. |
| Clear Speaker | With music volume 0/mute true, playback continues while paused but visible under a translucent idle app. A separate normal-UID MAY_DUCK requester stops/releases it while the producer stays visible; switch Off and focus cleanup confirmed. Original volume restored. |
| Refresh tile | Real SystemUI listening/binding confirms highest-rate Infinity state, live external updates and cycling to 60 Hz. Effective original tile order restored. |
| MiSound controls | Synthetic Rock preset, Music scene, EQ bypass and call-pause preference persist/recover across process recreation; UI agrees. Original MiSound preference state restored. |
| MiSound tiles | Both canonical and legacy protected tile bindings toggle the same master state while retaining preset/scene/EQ/pause. |

Seven main screens plus representative dialogs, Arabic RTL, font scale 1.3 and
landscape were captured fresh and reviewed. No reproducible clipping, overlap or
wrong arrow direction remained; scroll-view continuation is not truncation.
Default title/Info bounds also confirm separation. Existing artwork remains intact.

The original ROM APK, exact original preference bytes, locale/font/rotation/volume
and user controls were restored. Test helpers and owned remote files were removed;
no ready staged session remains. Kernel unchanged; stock thermal map/binary hashes
unchanged, mi_thermald running, selector 0 and global sampling Off. SELinux stayed
Enforcing; no thermal protection was disabled.

## Limits and reusable test setup

No physical headphones were available. New source capability opt-ins are absent
from the installed vendor property set, so optional USB/Bluetooth/3D/ear features
are not certified on this ROM. No SoundID calibration was invented. Optical panel,
firmware touch latency, native DSP/acoustic processing and dust-removal efficacy
remain outside this acceptance. Voice-mode interleavings and failure injection use
host boundaries; this milestone did not restart audioserver or test a complete ROM.
AI-assisted wording lacks native-speaker certification across all locales.

Use verified `cmd audio set-volume/get-stream-volume/is-stream-mute` for quiet tests;
a shell exit 0 is not a hardware acknowledgement. Use `cmd statusbar add-tile` /
`remove-tile` and actual QS listening/cache dumps: the current authoritative tile
flow reverts direct secure-setting edits. Private HIDL CLI clients must package
the generated base client classes; production R8 may rename private stubs.

Raw preferences, images, binaries and fixture logs remain private under
`~/evo/.repo/parts-full-review-20261112`; this record supplies sanitized scope and
public source links. [Device UX](../memory/xiaomiparts-device-ux.md) ·
[validation](../state/validation.md#v-parts).
