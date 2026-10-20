# Initial-build changelog implementation audit

**2026-10-09 — source-checked.** Enumerated the current PocoF3Releases organization,
rechecked selected remote heads and inspected local final code/product wiring,
maintainer change families and recorded validation. All listed tracked trees clean.
No ROM build, flash or new app/device test was performed.

## Source coverage

The linked heads below were refreshed on October 11 after resync. Original
October 9 behavior/acceptance remains historical; this inventory is not a release manifest.

| Build source path | Verified local/remote head | Final behavior grouped in notes |
| --- | --- | --- |
| `device/xiaomi/sm8250-common` | [38b93bc3b49c](https://github.com/PocoF3Releases-Recovery/device_xiaomi_sm8250-common/commit/38b93bc3b49c3a56302eac6bfcc7c3b12730ee30) | Parts/touch/refresh/thermal, modem cache, power/memory/audio integration |
| `device/xiaomi/alioth` | [c1debf6b85f7](https://github.com/PocoF3Releases-Recovery/device_xiaomi_alioth/commit/c1debf6b85f71d640fa18beea6e9b3e13c79c8c2) | Product selection, brightness/HBM, proximity, stock haptics, camera input/recording gates |
| `vendor/xiaomi/alioth` | [8df5835cf12b](https://github.com/PocoF3Releases/vendor_xiaomi_alioth/commit/8df5835cf12b42262795de8a6bbc2e23b9ad3caf) | Stock audio/camera/sensor firmware, patched MIUS/CHI, waveform samples |
| `vendor/xiaomi/sm8250-common` | [1e11ce1c7634](https://github.com/PocoF3Releases/vendor_xiaomi_sm8250-common/commit/1e11ce1c76343da45338a9ee7c7b6601e6c31b49) | Stock HAL dependencies, tuning, media/graphics/thermal services and task profiles |
| `kernel/xiaomi/sm8250` | [a67e83add1fa](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/a67e83add1fa9398814db8451f91347c7c2d09ed) | 4.19.325, stock AW8697, display/audio/battery/touch guards, WireGuard |
| `hardware/xiaomi` | [7c226c2791d2](https://github.com/PocoF3Releases/hardware_xiaomi/commit/7c226c2791d24c00b53faf8b92d4e68a37bdbaf5) | Dolby/volume engine, sensor/fingerprint lifetime, stock HAL and LOW_TICK |
| `device/xiaomi/camera` | [a72242890b4a](https://github.com/PocoF3Releases/device_xiaomi_camera/commit/a72242890b4a762bd44df586277c479210d7f118) | Product/permissions/JNI/shim/cache/SAT/recording integration |
| `frameworks/av` | [81b959f7c519](https://github.com/PocoF3Releases/frameworks_av/commit/81b959f7c5197a52e5f3588e8c94f230fb9848a4) | AC-4/DAP opt-ins, camera tags, effect reply and MediaCodec safeguards |
| `frameworks/base` | [d88e1ba6da08](https://github.com/PocoF3Releases-Recovery/frameworks_base/commit/d88e1ba6da08dcd11127560a7eae81c5537ce0b5) | Xiaomi camera inputs, recording FPS/blur, HBM opt-in, controller restoration |
| `hardware/qcom-caf/sm8250/display` | [385a1c2fa09b](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_display/commit/385a1c2fa09b9f1ab1d566afa14727e54b6f57dc) | Legacy camera DisplayConfig endpoint and buffer allocation guards |
| `hardware/qcom-caf/sm8250/audio` | [147f4aae7eb3](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_audio/commit/147f4aae7eb3148baae6c992594a278630b09909) | AIDL Health battery listener with HIDL fallback |
| `hardware/qcom-caf/sm8250/media` | [4563de614468](https://github.com/PocoF3Releases/hardware_qcom-caf_sm8250_media/commit/4563de61446855e0b1dade548d9003e792cb143a) | C2D color/layout refresh and surface/GPU mapping lifetime |
| `hardware/nxp/nfc` | [53a125ca706a](https://github.com/PocoF3Releases/android_hardware_nxp_nfc/commit/53a125ca706afd1c6c09b0b3222fd6aeb25f1195) | Snapshot client queue during teardown; superseded timer fix excluded |
| `vendor/qcom/opensource/usb` | [34a2c8bb9b07](https://github.com/PocoF3Releases/vendor_qcom_opensource_usb/commit/34a2c8bb9b07b52b81921e9f4f4068009fb84050) | Platform configfs ownership/controller readiness |
| `vendor/xiaomi/camera` | [607c5b881ccf](https://gitlab.com/johnmart19/vendor_xiaomi_camera/-/commit/607c5b881ccfff475e0e56ec85ec55a9d3248ac4) | Final APK, ExtraPhoto/gson and matching native runtime |
| `external/tinycompress` | [eacefe332464](https://github.com/PocoF3Releases/external_tinycompress/commit/eacefe332464fbb2f55f12d70b2e60fb244e05ca) | Full capture-read semantics, poll state and EOF termination |

## Inclusion and finality

Alioth device.mk selects AW8697 and includes camera/miuicamera.mk; the common
product installs XiaomiParts/XiaomiDolby/DSPVolumeSynchronizer and opt-ins for
legacy DAP/AC-4. Alioth overlays enable high-refresh recording and independent
blur handling; normal cap is 60, selected maximum mode remains codec-limited.
Kernel Alioth config enables WireGuard. Audio HAL links libtinycompress; capture
loop/poll/EOF fixes are present in the complete final library source.

Camera APK is a real LFS payload, 223517496 bytes, SHA256
`29609d236d1e78e6839aa5e699f6479b963262b9d1a81d289c7d667068053de4`.
Both camera sources remain required. Current repo list includes tinycompress;
custom device/camera/hardware trees are manually supplied and absent from that
manifest inventory. Product inclusion was checked separately. No immutable full
included-commit manifest or matching release ZIP was available.

Finality means code is present on the selected branch and wired where applicable;
it does not certify every route/device or exact released artifact. Semantic
families are listed once: camera/display buffers, Dolby/framework lifecycle,
modem/cache, Parts/thermal and stock haptics each combine multiple repositories.

## Exclusions and wording limits

Reference-code/profile/workhub repositories are not ROM features. PBRP is a
separate recovery product. A16 and experimental refs are excluded. AAC renderer
is a development target, not full RichTap; no PWLE/Android spatializer claim.
No generic game/FPS/battery-life improvement or donor GPU port is established.

Tinycompress host/ARM/ARM64 tests are reported in commits; new library was not
installed into the ROM. Do not claim all messaging-app voice recording fixed.
C2D layout checks were host-tested; target build was blocked in the original
record, so describe implementation rather than proven screen/video symptom repair.
Dolby ACKs/profile transport are not listening proof for all effects/routes.
ExtraPhoto is packaged; full editor flows lack comprehensive acceptance.

The latest refresh APK, modem image, fuel-gauge change and thermal helper need
matching rebuilt acceptance. No replacement-battery boot cure, unlimited 120 FPS
recording, ultrawide true 60 FPS or complete biometric certification is claimed.
See [validation](validation.md) for historical scope and the final
[large](telegram-initial-full.md) / [small](telegram-initial-short.md) posts.

## Complete organization inventory and companion pass

All 19 current organization repositories were rechecked in a subsequent October 9
pass. The 15 organization ROM inputs above plus required GitLab camera make 16
custom ROM inputs. Their heads remained unchanged. Four remaining repositories:

| Repository | Head | Classification |
| --- | --- | --- |
| `.github` | [cb1815d9f2a9](https://github.com/PocoF3Releases/.github/commit/cb1815d9f2a9f592f268a531f564fb2f81a0bfab) | Organization profile/artwork; excluded from ROM features |
| `references_code` | [d301665e4c8d](https://github.com/PocoF3Releases/references_code/commit/d301665e4c8d442a98cdc636c9f12e260bd1de0b) | Reference code only; no production inclusion assumed |
| `Agents.md` | `enclosing commit` | This knowledge workhub; revision is the enclosing commit |
| `device_xiaomi_alioth-pbrp` | [1dcf2e2e1a26](https://github.com/pbrp-alioth/device_xiaomi_alioth-pbrp/commit/1dcf2e2e1a2600ce86291bd6324f90c494a74087) | Separate recovery build; unchanged source and excluded from ROM notes |

Companion Settings gesture/clipboard screens and controllers were inspected as
build integration evidence. Settings is an upstream dependency, excluded from
our maintained repository tracking. Current frameworks/base implements
independent wake/ambient double-tap arming, automatic-mode AOD clamp correction
and off-main-thread QS usage queries. Clipboard controller/resources and framework
setting coexist. Those are source-backed everyday controls, not new runtime tests.

Alioth vendor.prop overrides the common optional default to enable stock Dolby
speaker tuning; Android spatializer remains disabled. Final code gates tuning
by that property. Do not confuse this with audible certification of every profile.
GitLab camera head was reverified; camera/artifact validation from the first pass
remains valid because its source head and payload have not changed.

Upstream dependencies are excluded from the source ledger; this audit retains
only the integration findings needed to assess the changelog. Reverted NFC timer
work, optional AAC renderer, build-only changes and irrelevant other-device HAL
changes remain excluded. No attempt was made to certify every upstream project
in the 1257-project manifest or all historical commit effects; this audit covers
the requested organization sources and relevant companion integration.
